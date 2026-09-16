from openai import OpenAI

from app.core.config import settings
from app.core.models import LLMResponse
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

    def generate(self, messages: list[dict[str, str]]) -> LLMResponse:

        response = self.client.responses.parse(
            model=settings.llm_model,
            input=messages,
            text_format=LLMResponse,
        )

        if response.output_parsed is None:
            raise ValueError(
                "OpenAI tidak menghasilkan LLMResponse "
                "yang dapat diparse."
            )

        return response.output_parsed