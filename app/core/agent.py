from app.conversation.manager import ConversationManager
from app.personality.sophie import SOPHIE_SYSTEM_PROMPT
from app.providers.llm import LLMProvider


class SophieAgent:
    """
    Core agent Sophie.

    Bertanggung jawab menggabungkan:
    - personality
    - conversation
    - LLM provider
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
    ) -> None:
        self.llm = llm_provider
        self.conversation = ConversationManager()

    def respond(self, user_message: str) -> str:
        """
        Memproses pesan pengguna dan menghasilkan respons Sophie.
        """

        self.conversation.add_user_message(user_message)

        messages = [
            {
                "role": "system",
                "content": SOPHIE_SYSTEM_PROMPT,
            },
            *self.conversation.get_messages(),
        ]

        response = self.llm.generate(messages)

        self.conversation.add_assistant_message(response)

        return response