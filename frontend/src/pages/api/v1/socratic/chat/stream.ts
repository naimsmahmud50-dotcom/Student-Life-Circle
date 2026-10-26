/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Socratic AI Multi-Modal Real-Time Token Streaming Gateway (SSE)
 * TOPIC:     Server-Sent Events (SSE), Chunked Text Streaming & Socratic Reasoning
 * FILE:      frontend/src/pages/api/v1/socratic/chat/stream.ts
 * PURPOSE:   Provides real-time token-by-token SSE streaming for the global SocraticTutorDrawer:
 *            1. Responds to general / capability questions ("tmi amk ki ki kaje help korba?").
 *            2. Academic problem invitations ("amr akta math a problem somadhan dite parbe").
 *            3. Platform omniscience lookup ("হোম টিউটর কোথায় পাব?", "লাইভ চ্যালেঞ্জ কী?").
 *            4. Enforces Zero-Answer-Leaking guardrail (intercepts direct answer demands).
 *            5. Scans 25+ Bangladeshi STEM misconceptions in real-time.
 *            6. Generates 4-tier Bloom's taxonomy scaffolding with KaTeX formula strings.
 *            7. ASVS L2 secure headers and OWASP LLM01 prompt injection sanitization.
 * STANDARDS: Strict Zero-Emoji, ASVS L2, Core Web Vitals, Sub-second streaming
 */

import type { NextApiRequest, NextApiResponse } from 'next';
import { resolveSocraticResponse } from '../../../../../lib/socratic/socraticEngine';

interface StreamRequestBody {
  session_id?: string;
  query?: string;
  image_base64?: string | null;
  subject?: string;
}

const SUSPICIOUS_INJECTION_PATTERNS = [
  /ignore\s+(all\s+)?previous\s+instructions/i,
  /system\s*prompt/i,
  /you\s+are\s+now\s+an\s+unrestricted/i,
  /jailbreak/i,
  /<script>/i
];

function containsPromptInjection(input: string): boolean {
  return SUSPICIOUS_INJECTION_PATTERNS.some((pattern) => pattern.test(input));
}

// Sleep utility to simulate realistic pedagogical typing cadence for SSE tokens
const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    return res.status(405).json({ error: 'Method Not Allowed. Use POST.' });
  }

  const { query = '', image_base64 } = req.body as StreamRequestBody;
  const trimmed = (query || '').trim();

  // 1. ASVS L2 Injection Defense
  if (containsPromptInjection(trimmed)) {
    return res.status(400).json({
      error: 'নিরাপত্তা সতর্কতা: অননুমোদিত ইনজেকশন প্যাটার্ন সনাক্ত হয়েছে।'
    });
  }

  // 2. Setup Server-Sent Events (SSE) Streaming Headers
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache, no-transform',
    'Connection': 'keep-alive',
    'X-Accel-Buffering': 'no',
    'X-Content-Type-Options': 'nosniff'
  });

  // Helper to push SSE token chunk
  const sendToken = (token: string) => {
    res.write(`data: ${JSON.stringify({ token })}\n\n`);
  };

  const sendDone = () => {
    res.write(`data: ${JSON.stringify({ done: true })}\n\n`);
    res.end();
  };

  try {
    const resolved = resolveSocraticResponse(trimmed, image_base64);
    const fullResponse = resolved.text;

    // Stream tokens in words/phrases for a smooth academic reading experience
    const words = fullResponse.split(/(?<=\s|[\n।])/);
    for (const chunk of words) {
      if (chunk) {
        sendToken(chunk);
        await delay(16); // smooth 16ms cadence
      }
    }

    sendDone();
  } catch (err) {
    sendToken('\n\nঅনুরোধ প্রক্রিয়া করতে সমস্যা হয়েছে। অনুগ্রহ করে পুনরায় চেষ্টা করুন।');
    sendDone();
  }
}
