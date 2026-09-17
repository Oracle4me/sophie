from app.core.models import (
    CognitiveResult,
    CognitiveState,
    ResponsePlan,
)
from app.providers.llm import LLMProvider
from app.personality.sophie import GENERATION_SYSTEM_PROMPT


class CognitiveCore:
    """
    Cognitive Core Sophie.

    Bertanggung jawab mengoordinasikan proses kognitif Sophie:
    analisis pesan dan response generation.

    Cognitive Core tidak bergantung pada provider tertentu.
    """

    def __init__(self, llm_provider: LLMProvider) -> None:
        self.llm = llm_provider

    def analyze(
        self,
        messages: list[dict[str, str]],
    ) -> CognitiveState:
        """
        Melakukan cognitive analysis tanpa menghasilkan respons.
        """

        return self.llm.analyze(messages)

    def generate(
        self,
        messages: list[dict[str, str]],
        cognitive_state: CognitiveState,
        response_plan: ResponsePlan | None = None,
    ) -> str:
        """
        Menghasilkan respons berdasarkan cognitive state
        dan optional response plan.
        """
        generation_messages = list(messages)

        generation_messages.append(
            {
                "role": "system",
                "content" : GENERATION_SYSTEM_PROMPT,
            }
        )

        if response_plan is not None:
            generation_messages.append(
                {
                    "role": "system",
                    "content": (
                        "Response plan Sophie:\n"
                        f"- tone: {response_plan.tone}\n"
                        f"- verbosity: {response_plan.verbosity}\n"
                        f"- playful: {response_plan.playful}\n"
                        f"- supportive: {response_plan.supportive}\n"
                        f"- focused: {response_plan.focused}"
                    ),
                }
            )

        return self.llm.generate(
            generation_messages,
            cognitive_state,
        )

    def process(
        self,
        messages: list[dict[str, str]],
        response_plan: ResponsePlan | None = None,
    ) -> CognitiveResult:
        """
        Compatibility method.

        Menjalankan analyze lalu generate.
        """

        cognitive_state = self.analyze(messages)

        response = self.generate(
            messages,
            cognitive_state,
            response_plan,
        )

        return CognitiveResult(
            response=response,
            state=cognitive_state,
        )