from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str

class CognitiveState(BaseModel):
    """
    Structured state hasil pemahaman Sophie terhadap
    pesan dan konteks percakapan.

    Model ini sengaja hanya menyimpan state terstruktur,
    bukan reasoning atau chain-of-thought internal LLM.
    """

    intent: str = "unknown"
    topic: str | None = None
    confidence: float = 0.0
    response_mode: str = "normal"
    needs_context: bool = False

class CognitiveResult(BaseModel):
    """
    Hasil pemrosesan Cognitive Core.
    """

    response: str
    state: CognitiveState