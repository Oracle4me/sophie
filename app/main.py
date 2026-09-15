from app.core.agent import SophieAgent
from app.providers.openai import OpenAIProvider


def main() -> None:
    print("=" * 50)
    print("              SOPHIE CORE v0.1")
    print("=" * 50)
    print("Ketik 'exit' untuk keluar.")
    print()

    sophie = SophieAgent(
        llm_provider=OpenAIProvider()
    )

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                print("Sophie: Sampai nanti! 👋")
                break

            response = sophie.respond(user_input)

            print(f"Sophie: {response}")
            print()

        except KeyboardInterrupt:
            print("\nSophie: Sampai nanti! 👋")
            break

        except Exception as error:
            print(f"Sophie mengalami error: {error}")


if __name__ == "__main__":
    main()