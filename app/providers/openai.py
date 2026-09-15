from openai import OpenAI

from app.core.config import settings
from app.providers.llm import LLMProvider


class OpenAIProvider(LLMProvider):
    """
    LLM provider Sophie menggunakan OpenAI Responses API.
    """

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY belum dikonfigurasi."
            )

        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

    def generate(self, messages: list[dict[str, str]]) -> str:
        response = self.client.responses.create(
            model=settings.llm_model,
            input=messages,
        )

        return response.output_text