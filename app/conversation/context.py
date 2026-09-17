from pydantic import BaseModel

from app.core.models import Message


class ConversationContext(BaseModel):
    """
    Structured working context dari percakapan Sophie.

    Context ini merepresentasikan keadaan percakapan
    yang sedang aktif.

    Context belum termasuk memory jangka panjang.
    """

    messages: list[Message]
    recent_messages: list[Message]

    latest_user_message: str | None = None
    latest_assistant_message: str | None = None
    previous_topic: str | None = None

    message_count: int = 0
    user_turn_count: int = 0
    assistant_turn_count: int = 0

    conversation_active: bool = False


class ContextEngine:
    """
    Context Engine Sophie.

    Bertanggung jawab membangun working context
    dari conversation history.

    ConversationManager menyimpan seluruh history.
    ContextEngine menentukan bagian history yang
    relevan untuk siklus percakapan saat ini.
    """

    def __init__(
        self,
        max_recent_messages: int = 12,
    ) -> None:
        if max_recent_messages < 1:
            raise ValueError(
                "max_recent_messages harus lebih besar dari 0."
            )

        self.max_recent_messages = max_recent_messages

    def build(
        self,
        messages: list[Message],
        previous_topic: str | None = None,
    ) -> ConversationContext:
        latest_user_message = None
        latest_assistant_message = None

        for message in reversed(messages):
            if message.role == "user":
                latest_user_message = message.content
                break

        for message in reversed(messages):
            if message.role == "assistant":
                latest_assistant_message = message.content
                break

        recent_messages = list(
            messages[-self.max_recent_messages:]
        )

        user_turn_count = sum(
            1
            for message in messages
            if message.role == "user"
        )

        assistant_turn_count = sum(
            1
            for message in messages
            if message.role == "assistant"
        )

        return ConversationContext(
            messages=list(messages),
            recent_messages=recent_messages,
            latest_user_message=latest_user_message,
            latest_assistant_message=latest_assistant_message,
            previous_topic=previous_topic,
            message_count=len(messages),
            user_turn_count=user_turn_count,
            assistant_turn_count=assistant_turn_count,
            conversation_active=len(messages) > 0,
        )