from app.voice.tts import TextToSpeech


def main() -> None:
    print()
    print("========================================")
    print("           SOPHIE TTS TEST")
    print("========================================")
    print()

    tts = TextToSpeech()

    text = (
        "Halo. Aku Sophie. "
        "Sekarang aku sudah bisa berbicara."
    )

    print(f"Teks: {text}")
    print("Menghasilkan suara...")

    tts.speak(text)

    print("Sophie selesai berbicara.")


if __name__ == "__main__":
    main()