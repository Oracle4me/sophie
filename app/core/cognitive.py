from app.core.models import CognitiveResult
from app.providers.llm import LLMProvider


class CognitiveCore:
    """
    Cognitive Core Sophie.

    Bertanggung jawab mengoordinasikan proses kognitif Sophie:
    analisis pesan terlebih dahulu, kemudian menghasilkan respons.

    Cognitive Core tidak bergantung pada provider tertentu.
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
        Memproses pesan melalui dua tahap:

        1. Cognitive analysis
        2. Response generation
        """

        cognitive_state = self.llm.analyze(messages)

        response = self.llm.generate(
            messages,
            cognitive_state,
        )

        return CognitiveResult(
            response=response,
            state=cognitive_state,
        )