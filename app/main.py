from app.core.agent import SophieAgent
from app.core.conversation_runtime import ConversationRuntime
from app.providers.openai import OpenAIProvider


def main() -> None:
    print("=" * 50)
    print("              SOPHIE CORE v0.13")
    print("=" * 50)
    print("Ketik 'exit' untuk keluar.")
    print()

    sophie = SophieAgent(
        llm_provider=OpenAIProvider()
    )

    runtime = ConversationRuntime(
        agent=sophie
    )

    runtime.run_text()


if __name__ == "__main__":
    main()