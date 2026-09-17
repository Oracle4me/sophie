from app.voice.stt import SpeechToText


def main() -> None:
    print("Memuat model STT...")

    stt = SpeechToText()

    print("Model siap.")
    print("Silakan bicara selama 5 detik...")

    text = stt.listen(duration=5.0)

    print()
    print(f"Hasil: {text}")


if __name__ == "__main__":
    main()