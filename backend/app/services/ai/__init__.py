"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    AI Services Package Initialization
TOPIC:     Multi-Modal AI Socratic Tutor & Gemini Streaming Services
FILE:      backend/app/services/ai/__init__.py
PURPOSE:   Initializes the AI services package, exposing the Gemini streaming service,
           OWASP LLM01 injection shield, and Socratic pedagogical response generator.
AUDIENCE:  Backend Engineers, AI Integration Specialists & Autonomous Agents
STANDARDS: Clean Architecture, PEP 8, Strict Zero-Emoji
========================================================================================
"""

from backend.app.services.ai.gemini_streaming_service import (
    GeminiStreamingService,
    gemini_streaming_service,
    PromptInjectionShield,
    prompt_injection_shield,
    SOCRATIC_SYSTEM_PROMPT,
    SocraticChatSession
)

__all__ = [
    "GeminiStreamingService",
    "gemini_streaming_service",
    "PromptInjectionShield",
    "prompt_injection_shield",
    "SOCRATIC_SYSTEM_PROMPT",
    "SocraticChatSession"
]
