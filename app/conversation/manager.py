from app.core.models import Message


class ConversationManager:
    """
    Mengelola riwayat percakapan Sophie.
    """

    def __init__(self) -> None:
        self.messages: list[Message] = []

    def add_user_message(self, content: str) -> None:
        self.messages.append(
            Message(
                role="user",
                content=content,
            )
        )

    def add_assistant_message(self, content: str) -> None:
        self.messages.append(
            Message(
                role="assistant",
                content=content,
            )
        )

    def get_messages(self) -> list[dict[str, str]]:
        return [
            message.model_dump()
            for message in self.messages
        ]

    # get message models
    def get_message_models(self) -> list[Message]:
        return list(self.messages)

    def clear(self) -> None:
        self.messages.clear()