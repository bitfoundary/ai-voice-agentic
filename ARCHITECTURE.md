# Agentic Voice Pipeline — Architecture Notes

A general reference architecture for a real-time conversational voice agent.

## Pipeline stages

1. **Audio ingestion** — audio arrives from a telephony leg (SIP/PSTN) or a WebRTC client and is normalized to a consistent sample rate/codec before processing.
2. **Speech-to-text (STT)** — streaming transcription converts audio to text incrementally, ideally with partial/interim results to minimize perceived latency.
3. **Turn detection / endpointing** — the system decides when the caller has finished speaking, using a combination of silence duration, semantic completion cues, and prosody, rather than silence timing alone.
4. **LLM reasoning** — the transcribed utterance, along with conversation history and any relevant retrieved context, is sent to a language model to generate the next response.
5. **Text-to-speech (TTS)** — the response is synthesized back into audio, streamed to the caller as it's generated rather than waiting for the full response.
6. **Barge-in handling** — if the caller starts speaking while the agent is talking, the agent should detect this and yield the floor gracefully rather than talking over the caller.

## Key design considerations

- **Latency budget.** Each stage above adds real, perceptible delay. A natural-feeling conversation typically needs end-to-end response latency in the low hundreds of milliseconds, which means streaming at every stage rather than batching.
- **Endpointing accuracy.** Cutting a caller off too early (false endpoint) or leaving too much silence (slow to respond) both degrade the experience noticeably. Semantic endpointing (does this sound like a complete thought?) tends to outperform pure silence-duration heuristics.
- **Context management.** Long conversations need summarization or windowing strategies to stay within LLM context limits without losing important earlier details.
- **Telephony transport.** SIP trunking for PSTN reach, WebRTC for browser/app-based calling — both need to terminate into the same real-time media pipeline, ideally without duplicating agent logic per transport.

## Open problems

- Reliable interruption handling under real network jitter
- Balancing response latency against response quality/depth
- Multi-language and code-switching support within a single call
