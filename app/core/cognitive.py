from app.core.models import CognitiveResult
from app.providers.llm import LLMProvider


class CognitiveCore:
    """
    Cognitive Core Sophie.

    Bertanggung jawab mengoordinasikan proses kognitif Sophie
    sebelum dan sesudah komunikasi dengan LLM.

    Cognitive Core tidak bergantung pada provider tertentu.
    Provider bertanggung jawab mengubah respons backend
    menjadi LLMResponse.
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

        Cognitive state berasal dari LLMProvider,
        bukan dibuat secara hard-code oleh Cognitive Core.
        """

        llm_response = self.llm.generate(messages)

        return CognitiveResult(
            response=llm_response.text,
            state=llm_response.cognitive_state,
        )