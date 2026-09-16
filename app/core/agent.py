from app.conversation.context import ContextEngine
from app.conversation.manager import ConversationManager
from app.core.attention import AttentionEngine
from app.core.autonomy import AutonomyEngine
from app.core.cognitive import CognitiveCore
from app.core.decision import DecisionEngine
from app.core.runtime import AgentRuntime
from app.personality.sophie import (
    COGNITIVE_SYSTEM_PROMPT,
    SOPHIE_SYSTEM_PROMPT,
)
from app.providers.llm import LLMProvider


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
        self.autonomy = AutonomyEngine()
        self.decision = DecisionEngine()

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
            {
                "role": "system",
                "content": COGNITIVE_SYSTEM_PROMPT,
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

        autonomy = self.autonomy.decide(
            attention=attention,
            user_focus=0.0,
        )

        decision = self.decision.decide(
            attention=attention,
            autonomy=autonomy,
            user_message=user_message,
        )

        self.runtime.update(
            current_intent=result.state.intent,
            active_topic=result.state.topic,
            response_mode=result.state.response_mode,
            should_respond=decision.decision != "wait",

            attention_score=attention.attention_score,
            attention_considered=attention.should_consider,

            autonomy_decision=autonomy.decision,
            autonomy_confidence=autonomy.confidence,
            autonomy_reason=autonomy.reason,
            autonomy_requires_permission=autonomy.requires_permission,

            decision=decision.decision,
            decision_confidence=decision.confidence,
            decision_reason=decision.reason,
            decision_requires_permission=decision.requires_permission,
        )

        self.conversation.add_assistant_message(
            result.response
        )

        return result.response