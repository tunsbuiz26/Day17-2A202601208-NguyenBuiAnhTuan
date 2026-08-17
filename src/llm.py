"""Thin OpenAI wrapper for the demo UI chat reply.

This is the ONLY place the lab calls a generative LLM. Benchmark scoring never
uses an LLM (see LAB.md): retrieval evidence is graded deterministically. Here
OpenAI only turns retrieved memory context into a grounded assistant reply so
the mini-product feels real.

Default model: gpt-4o-mini (override with OPENAI_MODEL).
"""

from __future__ import annotations

from .config import settings

SYSTEM_INSTRUCTION = (
    "You are the assistant of a personal memory agent for VinUni Lab 17. "
    "Answer the user grounded ONLY in the retrieved memory context provided. "
    "If the context does not contain the answer, say so plainly instead of "
    "inventing facts. Be concise and cite the concrete markers/ids you used. "
    "You may reply in the user's language (Vietnamese or English)."
)


def openai_available() -> bool:
    """True when an OpenAI project key is configured."""
    return bool(settings.openai_api_key)


def _to_input(history: list[dict[str, str]]) -> list[dict[str, str]]:
    """Map local chat history to Responses API input messages."""
    messages: list[dict[str, str]] = []
    for msg in history:
        role = "user" if msg.get("role") == "user" else "assistant"
        text = msg.get("content", "")
        if text:
            messages.append({"role": role, "content": text})
    return messages


def generate_reply(
    memory_context: str,
    history: list[dict[str, str]],
    user_message: str,
    *,
    model: str | None = None,
) -> str:
    """Generate a grounded assistant reply with the OpenAI Responses API.

    `history` excludes the latest user turn; `user_message` is appended as the
    final grounded input. SDK and network errors intentionally bubble up so the
    UI can display them.
    """
    if not settings.openai_api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add an "
            "OpenAI project API key to enable chat replies."
        )

    # Lazy import: benchmark scoring and memory retrieval never require an LLM.
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    model_name = model or settings.openai_model
    grounding = (
        "Retrieved memory context for this turn:\n"
        "-------------------------------------\n"
        f"{memory_context.strip() or '(no memory retrieved)'}\n"
        "-------------------------------------\n\n"
        f"User message: {user_message}"
    )

    messages = _to_input(history)
    messages.append({"role": "user", "content": grounding})
    response = client.responses.create(
        model=model_name,
        instructions=SYSTEM_INSTRUCTION,
        input=messages,
        temperature=0.3,
        max_output_tokens=800,
    )
    return (getattr(response, "output_text", "") or "").strip()
