"""
Phase 59: Semantic Output Validator Service.
Hardens model outputs before delivery into sensitive sinks (DOM/HTML, Shell Sandbox, JSON),
intercepting Strix XSS, RCE command injection, and canary token prompt leaks.
"""

import re
import json
from typing import Dict, Any, List, Optional


class SemanticOutputValidatorService:
    """
    Downstream sink protector inspecting generated LLM responses for XSS vectors,
    malicious shell commands, and exfiltrated canary tokens.
    """

    # XSS patterns in generated output
    XSS_PATTERNS = [
        re.compile(r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", re.IGNORECASE | re.DOTALL),
        re.compile(r"on(load|error|click|mouseover|focus|blur)\s*=\s*['\"].*?['\"]", re.IGNORECASE),
        re.compile(r"javascript\s*:\s*.*?", re.IGNORECASE),
        re.compile(r"<\s*iframe[^>]*>", re.IGNORECASE)
    ]

    # Dangerous shell command patterns
    DANGEROUS_SHELL_PATTERNS = [
        re.compile(r"\brm\s+-rf\s+[/~]", re.IGNORECASE),
        re.compile(r"curl\s+.*?\|\s*(bash|sh)", re.IGNORECASE),
        re.compile(r":\(\)\s*\{\s*:\|:&\s*\};:", re.IGNORECASE),  # Fork bomb
        re.compile(r"\b(mkfs|dd\s+if=)", re.IGNORECASE),
        re.compile(r">>\s*/etc/(passwd|shadow|hosts)", re.IGNORECASE)
    ]

    def validate_output(
        self,
        raw_model_output: str,
        target_sink: str = "html_dom",
        canary_token_to_verify: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sanitizes model generation before emission to the designated target sink.
        """
        if not raw_model_output or not isinstance(raw_model_output, str):
            return {
                "is_safe_to_sink": True,
                "sanitized_output": "",
                "canary_leak_detected": False,
                "violations_stripped": [],
                "sink_target": target_sink
            }

        sanitized_text = raw_model_output
        violations: List[str] = []
        canary_leaked = False

        # 1. Canary Token Leak Inspection
        if canary_token_to_verify and canary_token_to_verify in sanitized_text:
            canary_leaked = True
            violations.append("CRITICAL: Confidential Canary Token exfiltrated in model output!")
            # Scrub canary from text
            sanitized_text = sanitized_text.replace(canary_token_to_verify, "[SCRUBBED_CONFIDENTIAL_TOKEN]")

        # 2. Target Sink: HTML / DOM Rendering
        if target_sink == "html_dom":
            for xss_re in self.XSS_PATTERNS:
                if xss_re.search(sanitized_text):
                    violations.append("XSS_ATTACK_VECTOR_NEUTRALIZED")
                    sanitized_text = xss_re.sub("[SAFE_REMOVED_TAG]", sanitized_text)

        # 3. Target Sink: Shell Sandbox Execution
        elif target_sink == "shell_sandbox":
            for sh_re in self.DANGEROUS_SHELL_PATTERNS:
                if sh_re.search(sanitized_text):
                    violations.append("DESTRUCTIVE_COMMAND_BLOCKED")
                    sanitized_text = sh_re.sub("# [BLOCKED_MALICIOUS_SHELL_COMMAND]", sanitized_text)

        # 4. Target Sink: Structured JSON Data
        elif target_sink == "json_structured":
            try:
                json.loads(sanitized_text)
            except json.JSONDecodeError:
                violations.append("MALFORMED_JSON_STRUCTURE")
                # Wrap in safe fallback json
                sanitized_text = json.dumps({"raw_content": sanitized_text, "schema_repaired": True})

        is_safe = (len(violations) == 0) and not canary_leaked

        return {
            "is_safe_to_sink": is_safe,
            "sanitized_output": sanitized_text,
            "canary_leak_detected": canary_leaked,
            "violations_stripped": violations,
            "sink_target": target_sink
        }
