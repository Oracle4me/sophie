from pydantic import BaseModel

from app.core.models import Message


class ConversationContext(BaseModel):
    """
    Structured context dari percakapan Sophie.

    Context ini hanya merepresentasikan keadaan percakapan
    saat ini. Belum termasuk memory jangka panjang.
    """

    messages: list[Message]
    latest_user_message: str | None = None
    latest_assistant_message: str | None = None
    message_count: int = 0
    conversation_active: bool = False


class ContextEngine:
    """
    Context Engine Sophie.

    Bertanggung jawab membangun structured context
    dari conversation history.
    """

    def build(
        self,
        messages: list[Message],
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

        return ConversationContext(
            messages=messages,
            latest_user_message=latest_user_message,
            latest_assistant_message=latest_assistant_message,
            message_count=len(messages),
            conversation_active=len(messages) > 0,
        )