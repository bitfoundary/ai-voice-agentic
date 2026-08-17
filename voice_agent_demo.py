"""
voice_agent_demo.py

A minimal, illustrative example of a conversational turn-taking loop
for a voice agent. This is a simplified reference implementation for
research purposes only — it does not include real STT/TTS/LLM provider
integrations, credentials, or production error handling.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ConversationTurn:
    speaker: str  # "caller" or "agent"
    text: str


@dataclass
class ConversationState:
    history: List[ConversationTurn] = field(default_factory=list)

    def add_turn(self, speaker: str, text: str) -> None:
        self.history.append(ConversationTurn(speaker=speaker, text=text))

    def recent_context(self, n: int = 6) -> List[ConversationTurn]:
        return self.history[-n:]


def transcribe_audio_chunk(audio_chunk: bytes) -> str:
    """
    Placeholder for a streaming STT call.
    In a real system this would stream partial results as audio arrives.
    """
    raise NotImplementedError("Wire up a real STT provider here")


def generate_response(state: ConversationState, caller_text: str) -> str:
    """
    Placeholder for an LLM call using recent conversation context.
    """
    raise NotImplementedError("Wire up a real LLM provider here")


def synthesize_speech(text: str) -> bytes:
    """
    Placeholder for a streaming TTS call.
    In a real system this would stream audio back as it's generated,
    rather than waiting for the full response to synthesize.
    """
    raise NotImplementedError("Wire up a real TTS provider here")


def handle_call_turn(state: ConversationState, audio_chunk: bytes) -> bytes:
    """
    One full turn of the conversation loop:
    audio in -> transcript -> LLM response -> audio out
    """
    caller_text = transcribe_audio_chunk(audio_chunk)
    state.add_turn("caller", caller_text)

    agent_text = generate_response(state, caller_text)
    state.add_turn("agent", agent_text)

    return synthesize_speech(agent_text)


if __name__ == "__main__":
    # This is illustrative only — running it as-is will raise
    # NotImplementedError, since no real providers are wired up.
    state = ConversationState()
    print("Conversation state initialized. Wire up real providers to run this end to end.")
