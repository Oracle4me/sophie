from app.conversation.context import ContextEngine
from app.conversation.manager import ConversationManager
from app.core.cognitive import CognitiveCore
from app.personality.sophie import SOPHIE_SYSTEM_PROMPT
from app.providers.llm import LLMProvider


class SophieAgent:
    """
    Core agent Sophie.

    Bertanggung jawab mengoordinasikan:
    - personality
    - conversation
    - cognitive core
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
    ) -> None:
        self.conversation = ConversationManager()
        self.context = ContextEngine()
        self.cognitive = CognitiveCore(llm_provider)

    def respond(self, user_message: str) -> str:
        """
        Memproses pesan pengguna melalui Cognitive Core
        dan menghasilkan respons Sophie.
        """

        self.conversation.add_user_message(user_message)

        context = self.context.build(
            self.conversation.get_message_models()
        )

        messages = [
            {
                "role": "system",
                "content": SOPHIE_SYSTEM_PROMPT,
            },
            *[
                message.model_dump()
                for message in context.messages
            ],
        ]

        result = self.cognitive.process(messages)

        self.conversation.add_assistant_message(
            result.response
        )

        return result.response
