from app.core.models import AgentState


class AgentRuntime:
    """
    Runtime state Sophie.

    Menyimpan keadaan agent selama siklus hidup aplikasi.
    """

    def __init__(self) -> None:
        self.state = AgentState()

    def update(
        self,
        **changes,
    ) -> AgentState:
        """
        Menghasilkan state baru berdasarkan perubahan
        yang diberikan oleh subsystem Sophie.
        """

        self.state = self.state.model_copy(
            update=changes
        )

        return self.state

    def reset(self) -> None:
        """
        Mengembalikan runtime ke keadaan awal.
        """

        self.state = AgentState()