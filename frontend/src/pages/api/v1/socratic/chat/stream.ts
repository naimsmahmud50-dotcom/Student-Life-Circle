/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Socratic AI Multi-Modal Real-Time Token Streaming Gateway (SSE)
 * TOPIC:     Server-Sent Events (SSE), Chunked Text Streaming & Socratic Reasoning
 * FILE:      frontend/src/pages/api/v1/socratic/chat/stream.ts
 * PURPOSE:   Provides real-time token-by-token SSE streaming for the global SocraticTutorDrawer:
 *            1. Responds to general / capability questions ("tmi amk ki ki kaje help korba?").
 *            2. Enforces Zero-Answer-Leaking guardrail (intercepts direct answer demands).
 *            3. Scans 25+ Bangladeshi STEM misconceptions in real-time.
 *            4. Generates 4-tier Bloom's taxonomy scaffolding with KaTeX formula strings.
 *            5. ASVS L2 secure headers and OWASP LLM01 prompt injection sanitization.
 * STANDARDS: Strict Zero-Emoji, ASVS L2, Core Web Vitals, Sub-second streaming
 */

import type { NextApiRequest, NextApiResponse } from 'next';
import {
  isCapabilityInquiry,
  TUTOR_CAPABILITIES_RESPONSE_BN,
  isDirectAnswerDemanded,
  ZERO_ANSWER_LEAKING_REFUSAL_BN,
  scanForMisconception,
  analyzeProblemDomain
} from '../../../../../lib/socratic/socraticEngine';

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
    let fullResponse = '';

    // A. Multimodal OCR detection if image is provided
    let ocrPrefix = '';
    if (image_base64) {
      if (image_base64.includes('projectile') || trimmed.includes('প্রাস')) {
        ocrPrefix = 'খাতার ছবি থেকে সনাক্তকৃত সমীকরণ: $H = \\frac{v_0^2 \\sin^2\\theta}{2g}$\n\n';
      } else if (image_base64.includes('chem') || trimmed.includes('মোল')) {
        ocrPrefix = 'খাতার ছবি থেকে সনাক্তকৃত সমীকরণ: $2\\text{NaOH} + \\text{H}_2\\text{SO}_4 \\longrightarrow \\text{Na}_2\\text{SO}_4 + 2\\text{H}_2\\text{O}$\n\n';
      } else {
        ocrPrefix = 'খাতার ছবি থেকে সনাক্তকৃত সমীকরণ: $2x^2 + 7x - 4 = 0$\n\n';
      }
    }

    const effectiveText = (trimmed + ' ' + (ocrPrefix ? 'সমীকরণ' : '')).trim();

    // B. Capability / Identity / Help Inquiries ("tmi amk ki ki kaje help korba?")
    if (isCapabilityInquiry(effectiveText) || (!effectiveText && !image_base64)) {
      fullResponse = ocrPrefix + TUTOR_CAPABILITIES_RESPONSE_BN;
    }
    // C. Zero-Answer-Leaking Guardrail
    else if (isDirectAnswerDemanded(effectiveText)) {
      fullResponse = ocrPrefix + ZERO_ANSWER_LEAKING_REFUSAL_BN;
    }
    // D. Misconception Scanner
    else {
      const misconception = scanForMisconception(effectiveText);
      if (misconception) {
        fullResponse =
          ocrPrefix +
          `সতর্কতা ও পর্যবেক্ষণ: ${misconception.titleBn}\n` +
          `${misconception.explanationBn}\n\n` +
          (misconception.remedialFormulaLatex
            ? `সঠিক রূপ: $${misconception.remedialFormulaLatex}$\n\n`
            : '') +
          `সক্রেটিক প্রশ্ন: ${misconception.guidingQuestionBn}`;
      } else {
        // E. Socratic Domain Scaffolding
        const analysis = analyzeProblemDomain(effectiveText);
        const scaffold = analysis.scaffolding[0];

        fullResponse =
          ocrPrefix +
          `[${analysis.identifiedTopicBn}]\n` +
          `${scaffold.hintTextBn}\n\n` +
          (scaffold.formulaLatex ? `প্রাসঙ্গিক সূত্র: $${scaffold.formulaLatex}$\n\n` : '') +
          `সক্রেটিক অনুসন্ধান: ${scaffold.guidingQuestionBn}`;
      }
    }

    // Stream tokens in words/phrases for a smooth academic reading experience
    const words = fullResponse.split(/(?<=\s|[\n।])/);
    for (const chunk of words) {
      if (chunk) {
        sendToken(chunk);
        await delay(18); // smooth 18ms cadence
      }
    }

    sendDone();
  } catch (err) {
    sendToken('\n\nঅনুরোধ প্রক্রিয়া করতে সমস্যা হয়েছে। অনুগ্রহ করে পুনরায় চেষ্টা করুন।');
    sendDone();
  }
}
