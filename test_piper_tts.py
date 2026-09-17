from app.voice.piper_tts import PiperTextToSpeech


def main() -> None:
    print()
    print("========================================")
    print("          SOPHIE PIPER TTS TEST")
    print("========================================")
    print()

    tts = PiperTextToSpeech()

    text = (
        "Halo. Aku Sophie. "
        "Sekarang suara Sophie sudah berjalan "
        "secara lokal di komputer ini."
    )

    print(f"Teks: {text}")
    print()

    tts.speak(text)

    print()
    print("Sophie selesai berbicara.")


if __name__ == "__main__":
    main()