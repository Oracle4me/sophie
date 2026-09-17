from app.core.agent import SophieAgent


class ConversationRuntime:
    """
    Runtime interaksi Sophie.

    Bertanggung jawab mengelola loop percakapan
    dan menjadi penghubung antara input/output
    dengan SophieAgent.

    SophieAgent tetap menjadi otak utama.
    """

    def __init__(self, agent: SophieAgent) -> None:
        self.agent = agent

    def process(self, user_input: str) -> str:
        """
        Memproses satu input pengguna.
        """

        return self.agent.respond(user_input)

    def run_text(self) -> None:
        """
        Menjalankan percakapan Sophie melalui terminal.
        """

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in {"exit", "quit"}:
                    print("Sophie: Sampai nanti! 👋")
                    break

                response = self.process(user_input)

                print(f"Sophie: {response}")
                print()

            except KeyboardInterrupt:
                print("\nSophie: Sampai nanti! 👋")
                break

            except Exception as error:
                print(f"Sophie mengalami error: {error}")