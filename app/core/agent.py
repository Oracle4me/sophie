from app.conversation.context import ContextEngine
from app.conversation.manager import ConversationManager
from app.core.cognitive import CognitiveCore
from app.core.runtime import AgentRuntime
from app.personality.sophie import SOPHIE_SYSTEM_PROMPT
from app.providers.llm import LLMProvider
from app.core.attention import AttentionEngine


class SophieAgent:
    """
    Core agent Sophie.

    Bertanggung jawab mengoordinasikan:
    - personality
    - conversation
    - context
    - cognitive core
    - runtime state
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
    ) -> None:
        self.conversation = ConversationManager()
        self.context = ContextEngine()
        self.cognitive = CognitiveCore(llm_provider)
        self.runtime = AgentRuntime()
        self.attention = AttentionEngine()

    def respond(self, user_message: str) -> str:
        """
        Memproses satu siklus interaksi Sophie.
        """

        self.runtime.update(
            user_message=user_message,
            conversation_active=True,
        )

        self.conversation.add_user_message(user_message)

        context = self.context.build(
            self.conversation.get_message_models()
        )

        self.runtime.update(
            context_available=context.message_count > 0,
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

        attention = self.attention.evaluate(
            relevance=1.0,
            importance=0.5,
            urgency=0.2,
            interruption_cost=0.0,
        )

        self.runtime.update(
            current_intent=result.state.intent,
            active_topic=result.state.topic,
            response_mode=result.state.response_mode,
            should_respond=True,
            attention_score=attention.attention_score,
            attention_considered=attention.should_consider,
        )

        self.conversation.add_assistant_message(
            result.response
        )

        return result.response