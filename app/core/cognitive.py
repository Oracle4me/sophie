from app.core.models import CognitiveResult, CognitiveState
from app.providers.llm import LLMProvider


class CognitiveCore:
    """
    Cognitive Core Sophie.

    Bertanggung jawab mengoordinasikan proses kognitif Sophie
    sebelum dan sesudah komunikasi dengan LLM.

    Untuk v0.2, Cognitive Core masih sederhana:
    - menerima pesan dan context
    - menggunakan LLM untuk menghasilkan respons
    - menghasilkan structured cognitive state
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
    ) -> None:
        self.llm = llm_provider

    def process(
        self,
        messages: list[dict[str, str]],
    ) -> CognitiveResult:
        """
        Memproses context percakapan dan menghasilkan
        respons serta cognitive state.
        """

        response = self.llm.generate(messages)

        state = CognitiveState(
            intent="conversation",
            topic=None,
            confidence=1.0,
            response_mode="normal",
            needs_context=False,
        )

        return CognitiveResult(
            response=response,
            state=state,
        )