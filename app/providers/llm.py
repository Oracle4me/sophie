from abc import ABC, abstractmethod

from app.core.models import LLMResponse

class LLMProvider(ABC):
    """
    Interface dasar untuk semua LLM provider Sophie.

    Agent Sophie tidak boleh bergantung langsung
    pada provider tertentu.
    """

    @abstractmethod
    def generate(self, messages: list[dict[str, str]]) -> LLMResponse:
        """
        Menghasilkan respons dari kumpulan pesan percakapan.

        Args:
            messages: Daftar pesan dengan role dan content.

        Returns:
            Respons teks dari LLM.
        """
        raise NotImplementedError