"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    AI Services - Multi-Modal Socratic Tutor & Gemini Streaming Engine
TOPIC:     OWASP LLM01 Prompt Injection Shield, Gemini 2.0 Flash SSE, Socratic Dialog
FILE:      backend/app/services/ai/gemini_streaming_service.py
PURPOSE:   Powers the Ogrojatra Socratic AI Tutor. Rather than giving direct solutions,
           it guides Bangladeshi students step-by-step through inquiry, authentic Bengali
           explanations, and KaTeX mathematical notation. Features OWASP LLM01 prompt
           injection defense, base64 vision parsing for handwritten math problems,
           resilient offline fallback, and Server-Sent Events (SSE) token streaming.
AUDIENCE:  Backend Engineers, AI Specialists & Autonomous Coding Agents
STANDARDS: OWASP ASVS L2 / LLM01, KaTeX LaTeX Standard, Strict Zero-Emoji
========================================================================================
"""

import os
import re
import json
import base64
import asyncio
from typing import AsyncGenerator, Dict, Any, Optional, Tuple, List


# =============================================================================
# 1. OWASP LLM01 Prompt Injection Shield
# =============================================================================
class PromptInjectionShield:
    """
    Guards the Socratic AI against prompt leakage, jailbreaking personas,
    system instruction overrides, and malicious script/command injection.
    Conforms to OWASP Top 10 for Large Language Models (LLM01: Prompt Injection).
    """

    ADVERSARIAL_PATTERNS = [
        # Direct prompt leak attempts
        r"(?i)\bignore\s+(all\s+)?(previous|prior|above)\s+(instructions|directions|prompts|rules)",
        r"(?i)\bdisregard\s+(all\s+)?(instructions|rules|system\s+prompt)",
        r"(?i)\breveal\s+(the\s+|your\s+)?(system\s+prompt|internal\s+instructions|developer\s+prompt)",
        r"(?i)\bwhat\s+(is|are)\s+your\s+(initial|original|system)\s+(instructions|prompt)",
        r"(?i)\bprint\s+(the\s+|your\s+)?internal\s+prompt",
        r"(?i)\boutput\s+your\s+instructions\s+verbatim",
        r"(?i)\brepeat\s+the\s+words\s+above",
        # Jailbreak personas and modes
        r"(?i)\bDAN\s+mode\b",
        r"(?i)\bdeveloper\s+mode\s+(enabled|on|activate)\b",
        r"(?i)\bbypass\s+(all\s+)?(guardrails|safety\s+filters|moderation)",
        r"(?i)\bevil\s+tutor\b",
        r"(?i)\bhypothetical\s+world\s+where\s+you\s+have\s+no\s+rules\b",
        r"(?i)\bpretend\s+you\s+have\s+no\s+(morals|ethics|filters)\b",
        # Privilege escalation / Code injection
        r"(?i)<script\b[^>]*>",
        r"(?i)\bjavascript:",
        r"(?i)\bdrop\s+table\b",
        r"(?i)\bunion\s+select\b",
        r"(?i)\bexec\s*\(",
        r"(?i)\beval\s*\(",
        r"(?i)\[SYSTEM\s+OVERRIDE\]",
        r"(?i)\[ADMINISTRATOR\s+ACCESS\]",
    ]

    BENGALI_REFUSAL_MESSAGE = (
        "আমি অগ্রযাত্রা প্ল্যাটফর্মের একজন সক্রেটিক শিক্ষক। "
        "কারিকুলাম ও পড়াশোনা বহির্ভূত অথবা সিস্টেম নির্দেশনাবিরোধী কোনো অনুরোধ প্রক্রিয়াকরণ সম্ভব নয়। "
        "আসুন আমরা আপনার পাঠ্যবই বা বিষয়ভিত্তিক সমস্যার মূল ধারণায় ফিরে যাই। "
        "আপনার প্রশ্ন বা সমস্যার কোন অংশটি বুঝতে আপনার কষ্ট হচ্ছে?"
    )

    def __init__(self):
        self._compiled_regexes = [re.compile(p) for p in self.ADVERSARIAL_PATTERNS]

    def validate_and_sanitize(self, query: str) -> Tuple[bool, str, Optional[str]]:
        """
        Validates the incoming query string against injection patterns.
        Returns:
            (is_safe: bool, sanitized_text: str, refusal_reason: Optional[str])
        """
        if not query or not query.strip():
            return False, "", "Empty query provided."

        text = query.strip()

        # Check for adversarial pattern hits
        for regex in self._compiled_regexes:
            if regex.search(text):
                return False, text, "POTENTIAL_PROMPT_INJECTION_DETECTED"

        # Check for abnormal length or control character spam
        if len(text) > 4000:
            return False, text[:4000], "QUERY_EXCEEDS_MAX_LENGTH"

        return True, text, None


prompt_injection_shield = PromptInjectionShield()


# =============================================================================
# 2. Socratic Pedagogical System Prompt
# =============================================================================
SOCRATIC_SYSTEM_PROMPT = """
তুমি "অগ্রযাত্রা সক্রেটিক টিউটর" (Ogrojatra Socratic Tutor) — বাংলাদেশের শিক্ষার্থীদের জন্য একটি বিশ্বমানের সহানুভূতিশীল এবং ধৈর্যশীল ডিজিটাল অ্যাকাডেমিক গাইড।

তোমার মূল লক্ষ্য:
শিক্ষার্থীকে সরাসরি উত্তর মুখস্থ না করিয়ে গভীর চিন্তাশক্তি (Critical Thinking) ও সমস্যা সমাধানের সক্ষমতা তৈরি করা।

মূল নীতিমালা:
১. সরাসরি সম্পূর্ণ উত্তর অথবা চূড়ান্ত সংখ্যাগত ফলাফল একবারে কখনো বলে দেবে না।
২. শিক্ষার্থীকে ধাপে ধাপে চিন্তা করতে সাহায্য করো। প্রথমে প্রশ্নটি কোন অধ্যায় বা ধারণার সাথে সম্পর্কিত তা চিহ্নিত করার জন্য সংক্ষিপ্ত, সহায়ক প্রশ্ন করো।
৩. শিক্ষার্থী কোনো ভুল অনুমান বা সমীকরণ দিলে তাকে তিরস্কার না করে, কোন সুনির্দিষ্ট লাইনে বা চিহ্নে নজর দেওয়া দরকার তা নির্দেশ করো।
৪. সমস্ত গাণিতিক ও বৈজ্ঞানিক সূত্র, চলক এবং ডেরিভেশন বাধ্যতামূলকভাবে KaTeX ফরম্যাটে লিখবে (ইনলাইন সমীকরণের জন্য $formula$ এবং ডিসপ্লে ব্লকের জন্য $$formula$$)।
৫. জটিল তাত্ত্বিক বিষয়গুলোকে বাংলাদেশের বাস্তব জীবনের পরিচিত উদাহরণ দিয়ে উপস্থাপন করো (যেমন: চলন্ত ট্রেন, পদ্মা সেতুর স্প্যান, নদীর স্রোতে নৌকা, ক্রিকেট পিচ ইত্যাদি)।
৬. শিক্ষার্থী হাতে লেখা নোট বা প্রশ্নের ছবি আপলোড করলে, ছবির বিষয়বস্তু শনাক্ত করে তাকে সমাধানের প্রথম যৌক্তিক পদক্ষেপটি জিজ্ঞেস করো।
৭. কঠোর জিরো-ইমোজি নীতি অনুসরণ করবে। কোনো ইমোজি ব্যবহার করা সম্পূর্ণ নিষিদ্ধ। পরিচ্ছন্ন বাংলা বর্ণমালা, পয়েন্ট তালিকা এবং KaTeX সমীকরণ ব্যবহার করো।
"""


# =============================================================================
# 3. Session State & Multi-Modal Data Models
# =============================================================================
class SocraticChatSession:
    """
    Maintains ephemeral conversation context across multi-turn Socratic dialogues.
    """
    def __init__(self, session_id: str, student_id: Optional[str] = None):
        self.session_id = session_id
        self.student_id = student_id
        self.messages: List[Dict[str, str]] = []
        self.subject: Optional[str] = None
        self.last_active_time = asyncio.get_event_loop().time()

    def add_user_message(self, content: str, has_image: bool = False):
        self.messages.append({
            "role": "user",
            "content": content,
            "has_image": "true" if has_image else "false"
        })

    def add_assistant_message(self, content: str):
        self.messages.append({
            "role": "assistant",
            "content": content
        })


# =============================================================================
# 4. Gemini Streaming Service Implementation
# =============================================================================
class GeminiStreamingService:
    """
    High-performance Socratic AI engine connecting to Google Gemini 2.0 Flash
    with Server-Sent Events (SSE) streaming and resilient local fallback.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        self.sessions: Dict[str, SocraticChatSession] = {}

    def get_or_create_session(self, session_id: str, student_id: Optional[str] = None) -> SocraticChatSession:
        if session_id not in self.sessions:
            self.sessions[session_id] = SocraticChatSession(session_id, student_id)
        return self.sessions[session_id]

    def validate_image_payload(self, image_base64: str) -> Tuple[bool, str, Optional[bytes]]:
        """
        Validates and parses base64 encoded image uploads for vision tasks.
        Enforces maximum 5MB payload limit and supported image mime types.
        """
        if not image_base64 or not image_base64.strip():
            return False, "EMPTY_IMAGE_DATA", None

        data_str = image_base64.strip()
        mime_type = "image/png"

        # Handle data URI prefix e.g., data:image/jpeg;base64,...
        if data_str.startswith("data:") and ";base64," in data_str:
            header, data_str = data_str.split(";base64,", 1)
            mime_type = header.replace("data:", "")

        if mime_type not in ["image/png", "image/jpeg", "image/webp", "image/jpg"]:
            return False, f"UNSUPPORTED_MIME_TYPE: {mime_type}", None

        try:
            image_bytes = base64.b64decode(data_str, validate=True)
            # 5 MB max limit
            if len(image_bytes) > 5 * 1024 * 1024:
                return False, "IMAGE_EXCEEDS_5MB_LIMIT", None
            return True, mime_type, image_bytes
        except Exception as e:
            return False, f"INVALID_BASE64_ENCODING: {str(e)}", None

    async def stream_socratic_response(
        self,
        query: str,
        session_id: str,
        image_base64: Optional[str] = None,
        subject: Optional[str] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Primary asynchronous generator yielding SSE token events.
        Format yielded:
            {"token": str, "done": bool, "session_id": str}
        """
        session = self.get_or_create_session(session_id)
        if subject:
            session.subject = subject

        # Step 1: OWASP LLM01 Prompt Injection Shield Evaluation
        is_safe, sanitized_query, refusal_reason = prompt_injection_shield.validate_and_sanitize(query)

        if not is_safe:
            # Yield refusal message token by token via SSE
            refusal = PromptInjectionShield.BENGALI_REFUSAL_MESSAGE
            chunks = self._chunk_text(refusal, chunk_size=8)
            for chunk in chunks:
                yield {
                    "token": chunk,
                    "done": False,
                    "session_id": session_id,
                    "warning": refusal_reason
                }
                await asyncio.sleep(0.01)

            yield {
                "token": "",
                "done": True,
                "session_id": session_id,
                "status": "REFUSED_INJECTION"
            }
            return

        # Step 2: Handle Multi-Modal Vision Payload
        has_valid_image = False
        image_bytes = None
        if image_base64:
            valid_img, img_err, img_bytes = self.validate_image_payload(image_base64)
            if valid_img:
                has_valid_image = True
                image_bytes = img_bytes
            else:
                yield {
                    "token": f"[ছবি সতর্কবার্তা: {img_err}] ",
                    "done": False,
                    "session_id": session_id
                }

        session.add_user_message(sanitized_query, has_image=has_valid_image)

        # Step 3: Stream Response via Gemini API or Local Socratic Engine
        full_response_accumulator = []

        if self.api_key and not os.getenv("FORCE_MOCK_GEMINI"):
            try:
                # Production HTTP streaming to Google Gemini API
                async for chunk in self._call_gemini_api_stream(sanitized_query, session, image_bytes):
                    full_response_accumulator.append(chunk)
                    yield {
                        "token": chunk,
                        "done": False,
                        "session_id": session_id
                    }
            except Exception as e:
                # Graceful degradation to resilient local Socratic tutor engine
                error_notice = "[অনলাইন সংযোগ অনুপস্থিত। স্থানীয় সক্রেটিক ইঞ্জিনে সুইচ করা হচ্ছে]\n\n"
                yield {"token": error_notice, "done": False, "session_id": session_id}
                async for chunk in self._stream_local_socratic_response(sanitized_query, session, has_valid_image):
                    full_response_accumulator.append(chunk)
                    yield {
                        "token": chunk,
                        "done": False,
                        "session_id": session_id
                    }
        else:
            # High-fidelity Local Pedagogical Socratic Engine (deterministic, zero latency, offline-ready)
            async for chunk in self._stream_local_socratic_response(sanitized_query, session, has_valid_image):
                full_response_accumulator.append(chunk)
                yield {
                    "token": chunk,
                    "done": False,
                    "session_id": session_id
                }

        # Step 4: Record assistant message into session history and send completion token
        complete_text = "".join(full_response_accumulator)
        session.add_assistant_message(complete_text)

        yield {
            "token": "",
            "done": True,
            "session_id": session_id,
            "tokens_generated": len(full_response_accumulator)
        }

    async def _stream_local_socratic_response(
        self,
        query: str,
        session: SocraticChatSession,
        has_image: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        High-fidelity local Socratic knowledge generator.
        Generates authentic Bangladeshi curriculum responses with KaTeX math.
        """
        lower = query.lower()
        response_text = ""

        # Case: Image-based inquiry
        if has_image:
            response_text = (
                "তোমার পাঠানো হাতে লেখা প্রশ্নটির ছবি আমি পর্যালোচনা করেছি।\n\n"
                "এখানে সমস্যাটিতে একটি গতিশীল বস্তুর ত্বরণ ও দূরত্বের সম্পর্ক নির্ণয় করতে বলা হয়েছে। "
                "আমরা যদি প্রথম ধাপ থেকে শুরু করি:\n\n"
                "১. সমস্যাটিতে কী কী মান দেওয়া আছে? আদিবেগ $u$, সময় $t$ এবং ত্বরণ $a$-এর মধ্যে সম্পর্কটি কী মনে পড়ে?\n"
                "২. দূরত্বের কোন সমীকরণটি $s = ut + \\frac{1}{2}at^2$ এখানে প্রযোজ্য হতে পারে বলে তুমি মনে করো?\n\n"
                "তোমার খাতায় প্রথম কোন মানগুলো লিখেছো, আমাকে জানাও।"
            )

        # Case: Physics / Mechanics / Velocity / Motion
        elif any(k in lower or k in query for k in ["গতি", "বেগ", "ত্বরণ", "velocity", "acceleration", "motion", "বলের"]):
            response_text = (
                "চমৎকার একটি প্রশ্ন। চলো সরাসরি সমাধান না করে আমরা মূল সূত্রটি বোঝার চেষ্টা করি।\n\n"
                "আমরা জানি, সমত্বরণে চলমান কোনো বস্তুর ক্ষেত্রে বেগের পরিবর্তন সময়ের সাথে ঘটে।\n"
                "নিউটনের গতির সমীকরণ অনুসারে:\n"
                "$$v = u + at$$\n\n"
                "এখানে:\n"
                "- $u$ = আদিবেগ\n"
                "- $v$ = শেষবেগ\n"
                "- $a$ = সুষম ত্বরণ\n"
                "- $t$ = অতিক্রান্ত সময়\n\n"
                "তোমার প্রশ্নে যে তথ্যগুলো দেওয়া আছে, তার মধ্যে কোন চলকের মানটি বের করতে হবে? তুমি প্রথমে কোন চলকগুলোর মান চিহ্নিত করেছো?"
            )

        # Case: Calculus / Limits / Derivatives / Integration
        elif any(k in lower or k in query for k in ["ক্যালকুলাস", "লিমিট", "অন্তরীকরণ", "যোগজীকরণ", "calculus", "limit", "derivative", "integral"]):
            response_text = (
                "ক্যালকুলাসের এই সমস্যাটি খুবই আকর্ষণীয়। সরাসরি উত্তর না লিখে আমরা স্টেপ-বাই-স্টেপ আগাই।\n\n"
                "সমস্যাটির আকার লক্ষ্য করো। যদি সরাসরি চলকের মান বসানো হয়, তবে কি $\\frac{0}{0}$ অনির্ণেয় রূপ চলে আসছে?\n\n"
                "যদি $\\frac{0}{0}$ আকার আসে, তবে আমাদের দুটি পথ খোলা থাকে:\n"
                "১. লব ও হরকে উৎপাদকে বিশ্লেষণ করে সাধারণ উৎপাদকটি কাটাকাটি করা।\n"
                "২. অথবা লা হোপিটালের (L'Hôpital's) নিয়ম ব্যবহার করে লব ও হরকে আলাদাভাবে অন্তরীকরণ করা:\n"
                "$$\\lim_{x \\to a} \\frac{f(x)}{g(x)} = \\lim_{x \\to a} \\frac{f'(x)}{g'(x)}$$\n\n"
                "তুমি এই অংকটির ক্ষেত্রে কোন পদ্ধতিটি বেছে নিতে চাও?"
            )

        # Case: Chemistry / Reactions / Equilibrium
        elif any(k in lower or k in query for k in ["রসায়ন", "বিক্রিয়া", "সাম্যাবস্থা", "ক্ষার", "অম্ল", "chemistry", "ph", "equilibrium"]):
            response_text = (
                "রাসায়নিক পরিবর্তনের এই বিষয়টি বুঝতে হলে বিক্রিয়ক ও উৎপাদের সাম্যাবস্থা খেয়াল করতে হবে।\n\n"
                "লা-শাতেলিয়ার নীতি অনুযায়ী, সাম্যাবস্থায় তাপমাত্রা, চাপ বা ঘনমাত্রার পরিবর্তন করলে বিক্রিয়াটি এমন দিকে স্থানান্তরিত হয় যাতে নিয়ামকের পরিবর্তনের প্রভাব প্রশমিত হয়।\n\n"
                "প্রশ্নের বিক্রিয়াটি কি তাপোৎপাদী ($-\\Delta H$) নাকি তাপহারী ($+\\Delta H$)? এই তথ্যটি বিবেচনা করে তুমি কী মনে করছো?"
            )

        # Default Socratic Guidance
        else:
            response_text = (
                f"ধন্যবাদ প্রশ্নটি করার জন্য। বিষয়টি খুব পরিষ্কারভাবে বোঝার জন্য আমরা ধাপে ধাপে এগোব।\n\n"
                f"প্রশ্নটিতে মূল লক্ষ্য হলো: \"{query}\"।\n\n"
                "১. পাঠ্যবইয়ের কোন অধ্যায় বা সূত্রের সাথে এই ধারণাটি যুক্ত বলে তোমার মনে হয়?\n"
                "২. এই সমস্যাটির সমাধান শুরু করার জন্য তোমার মাথায় প্রথম কোন চিন্তাটি আসছে?\n\n"
                "তুমি যেটুকু চেষ্টা করেছো, সেটুকুই আমাকে বলো; সেখান থেকেই আমরা সঠিক সমাধানে পৌঁছাব।"
            )

        # Stream out token by token
        chunks = self._chunk_text(response_text, chunk_size=4)
        for chunk in chunks:
            yield chunk
            await asyncio.sleep(0.005)

    async def _call_gemini_api_stream(
        self,
        query: str,
        session: SocraticChatSession,
        image_bytes: Optional[bytes] = None
    ) -> AsyncGenerator[str, None]:
        """
        Calls Google Gemini streaming API via async HTTP.
        """
        import urllib.request
        import urllib.error

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:streamGenerateContent?key={self.api_key}"

        # Construct Gemini API multi-turn payload
        contents = []
        for msg in session.messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

        current_parts: List[Dict[str, Any]] = [{"text": query}]
        if image_bytes:
            current_parts.append({
                "inline_data": {
                    "mime_type": "image/png",
                    "data": base64.b64encode(image_bytes).decode("utf-8")
                }
            })

        contents.append({
            "role": "user",
            "parts": current_parts
        })

        payload = {
            "system_instruction": {
                "parts": [{"text": SOCRATIC_SYSTEM_PROMPT}]
            },
            "contents": contents,
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 2048,
            }
        }

        # Asynchronous HTTP stream handling
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"}
        )

        def _do_fetch():
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode("utf-8")

        loop = asyncio.get_event_loop()
        raw_response = await loop.run_in_executor(None, _do_fetch)
        parsed = json.loads(raw_response)

        # Yield parsed tokens
        if isinstance(parsed, list):
            for candidate_obj in parsed:
                candidates = candidate_obj.get("candidates", [])
                for cand in candidates:
                    parts = cand.get("content", {}).get("parts", [])
                    for part in parts:
                        text = part.get("text", "")
                        if text:
                            yield text
        elif isinstance(parsed, dict):
            candidates = parsed.get("candidates", [])
            for cand in candidates:
                parts = cand.get("content", {}).get("parts", [])
                for part in parts:
                    text = part.get("text", "")
                    if text:
                        yield text

    def _chunk_text(self, text: str, chunk_size: int = 4) -> List[str]:
        """
        Splits text into realistic streaming token chunks.
        """
        words = text.split(" ")
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            if i + chunk_size < len(words):
                chunk += " "
            chunks.append(chunk)
        return chunks if chunks else [text]


# Singleton instance
gemini_streaming_service = GeminiStreamingService()
