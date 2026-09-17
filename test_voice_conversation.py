from app.core.agent import SophieAgent
from app.providers.openai import OpenAIProvider
from app.voice.runtime import VoiceConversationRuntime


def main() -> None:
    print("Memulai Sophie...")

    agent = SophieAgent(
        llm_provider=OpenAIProvider()
    )

    runtime = VoiceConversationRuntime(
        agent=agent
    )

    runtime.run()


if __name__ == "__main__":
    main()