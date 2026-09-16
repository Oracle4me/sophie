from enum import Enum

from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str

class CognitiveIntent(str, Enum):
    """
    Intent dasar yang dapat dikenali Cognitive Core Sophie.
    """

    CONVERSATION = "conversation"
    QUESTION = "question"
    TECHNICAL_HELP = "technical_help"
    PLANNING = "planning"
    INSTRUCTION = "instruction"
    CLARIFICATION = "clarification"
    UNKNOWN = "unknown"

class ResponseMode(str, Enum):
    """
    Mode respons yang digunakan Sophie berdasarkan
    hasil pemahaman cognitive layer.
    """

    NORMAL = "normal"
    TECHNICAL = "technical"
    DISCUSSION = "discussion"
    INSTRUCTIONAL = "instructional"
    CLARIFICATION = "clarification"

class CognitiveState(BaseModel):
    """
    Structured state hasil pemahaman Sophie terhadap
    pesan dan konteks percakapan.

    Model ini hanya menyimpan state terstruktur,
    bukan reasoning atau chain-of-thought internal LLM.
    """

    intent: CognitiveIntent = CognitiveIntent.UNKNOWN
    topic: str | None = None
    confidence: float = 0.0
    response_mode: ResponseMode = ResponseMode.NORMAL
    needs_context: bool = False

class PersonalityState(BaseModel):
    energy: float = 0.7
    curiosity: float = 0.8
    playfulness: float = 0.6
    warmth: float = 0.9
    seriousness: float = 0.3

class ResponsePlan(BaseModel):
    tone: str = "natural"
    verbosity: str = "moderate"
    playful: bool = False
    supportive: bool = True
    focused: bool = False

class LLMResponse(BaseModel):
    """
    Kontrak respons LLM yang digunakan oleh Sophie.

    Model ini sengaja tidak bergantung pada provider tertentu.
    Provider apa pun harus dapat menerjemahkan hasilnya
    ke dalam struktur ini.
    """

    text: str
    cognitive_state: CognitiveState

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
    user_message: str | None = None
    conversation_active: bool = False
    active_topic: str | None = None
    current_intent: str = "unknown"
    context_available: bool = False
    memory_available: bool = False
    response_mode: str = "normal"

    personality_state: PersonalityState | None = None
    response_plan: ResponsePlan | None = None

    should_respond: bool = True
    attention_score: float = 0.0
    attention_considered: bool = False
    autonomy_decision: str = "wait"
    autonomy_confidence: float = 0.0
    autonomy_reason: str = ""
    autonomy_requires_permission: bool = False
    decision: str = "wait"
    decision_confidence: float = 0.0
    decision_reason: str = ""
    decision_requires_permission: bool = False

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

class AgentDecision(BaseModel):
    """
    Keputusan akhir Agent Sophie untuk satu siklus.

    AgentDecision hanya merepresentasikan keputusan tingkat tinggi.
    Ia tidak menjalankan action secara langsung.
    """

    decision: str = "wait"
    reason: str = ""
    confidence: float = 0.0
    requires_permission: bool = False