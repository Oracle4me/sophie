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


class MemoryCandidate(BaseModel):
    """
    Kandidat memory yang dihasilkan dari percakapan.

    Candidate belum otomatis disimpan ke MemoryStore.
    """

    content: str
    memory_type: str = "semantic"
    importance: float = 0.5
    should_store: bool = False

class AgentState(BaseModel):
    """
    State runtime Sophie pada satu siklus pemrosesan.

    AgentState merupakan representasi keadaan Sophie saat ini,
    bukan memory permanen dan bukan chain-of-thought.
    """

    user_message: str | None = None
    conversation_active: bool = False

    active_topic: str | None = None
    current_intent: str = "unknown"

    context_available: bool = False
    memory_available: bool = False

    response_mode: str = "normal"
    should_respond: bool = True

    attention_score: float = 0.0
    attention_considered: bool = False

class AttentionState(BaseModel):
    """
    State perhatian Sophie terhadap keadaan saat ini.

    AttentionState bukan keputusan untuk melakukan aksi.
    State ini hanya menggambarkan seberapa relevan sesuatu
    untuk diperhatikan oleh Sophie.
    """

    relevance: float = 0.0
    importance: float = 0.0
    urgency: float = 0.0
    interruption_cost: float = 0.0

    attention_score: float = 0.0

    should_consider: bool = False

class AutonomyState(BaseModel):
    """
    Keputusan autonomy Sophie.

    State ini merepresentasikan keputusan tingkat tinggi
    yang dapat diambil agent terhadap keadaan saat ini.

    AutonomyState tidak menjalankan tindakan secara langsung.
    """

    decision: str = "wait"
    confidence: float = 0.0
    reason: str = ""
    requires_permission: bool = False