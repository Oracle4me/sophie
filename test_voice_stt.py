from app.voice.input import RealtimeVoiceInput
from app.voice.stt import SpeechToText


def main() -> None:
    print()
    print("========================================")
    print("        SOPHIE VOICE STT TEST")
    print("========================================")
    print()

    voice_input = RealtimeVoiceInput()

    print("Sophie siap mendengar.")
    print("Silakan bicara...")

    audio = voice_input.listen()

    if len(audio) == 0:
        print("Tidak ada suara yang terdeteksi.")
        return

    print()
    print("Suara selesai direkam.")
    print("Memuat STT...")

    # STT baru dimuat setelah ada speech.
    # Ini menghemat resource saat Sophie idle.
    stt = SpeechToText()

    print("STT siap.")
    print("Mentranskripsikan...")

    text = stt.transcribe(audio)

    print()
    print(f"Hasil STT: {text}")


if __name__ == "__main__":
    main()