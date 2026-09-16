from openai import OpenAI

from app.core.config import settings
from app.core.models import CognitiveState
from app.providers.llm import LLMProvider


class OpenAIProvider(LLMProvider):
    """
    LLM provider Sophie menggunakan OpenAI Responses API.

    Provider ini hanya bertanggung jawab sebagai adapter
    antara OpenAI dan kontrak internal Sophie.
    """

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY belum dikonfigurasi."
            )

        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

    def analyze(
        self,
        messages: list[dict[str, str]],
    ) -> CognitiveState:
        """
        Menganalisis pesan pengguna menjadi CognitiveState.
        """

        response = self.client.responses.parse(
            model=settings.llm_model,
            input=messages,
            text_format=CognitiveState,
        )

        if response.output_parsed is None:
            raise ValueError(
                "OpenAI tidak menghasilkan CognitiveState."
            )

        return response.output_parsed

    def generate(
        self,
        messages: list[dict[str, str]],
        cognitive_state: CognitiveState,
    ) -> str:
        """
        Menghasilkan respons berdasarkan cognitive state.

        Cognitive state diberikan secara eksplisit kepada
        model sehingga response generation mengetahui
        hasil analisis sebelumnya.
        """

        cognitive_context = (
            "Cognitive state Sophie:\n"
            f"- intent: {cognitive_state.intent.value}\n"
            f"- topic: {cognitive_state.topic}\n"
            f"- confidence: {cognitive_state.confidence}\n"
            f"- response_mode: {cognitive_state.response_mode.value}\n"
            f"- needs_context: {cognitive_state.needs_context}"
        )

        generation_messages = [
            *messages,
            {
                "role": "system",
                "content": cognitive_context,
            },
        ]

        response = self.client.responses.create(
            model=settings.llm_model,
            input=generation_messages,
        )

        if not response.output_text:
            raise ValueError(
                "OpenAI tidak menghasilkan teks respons."
            )

        return response.output_text