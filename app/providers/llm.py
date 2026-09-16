from abc import ABC, abstractmethod

from app.core.models import CognitiveState


class LLMProvider(ABC):
    """
    Interface dasar untuk semua LLM provider Sophie.

    Sophie tidak bergantung pada provider tertentu.
    Setiap provider bertanggung jawab menerjemahkan
    backend masing-masing ke kontrak internal Sophie.
    """

    @abstractmethod
    def analyze(
        self,
        messages: list[dict[str, str]],
    ) -> CognitiveState:
        """
        Menganalisis pesan dan menghasilkan cognitive state.
        """
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        messages: list[dict[str, str]],
        cognitive_state: CognitiveState,
    ) -> str:
        """
        Menghasilkan teks respons berdasarkan cognitive state.
        """
        raise NotImplementedError