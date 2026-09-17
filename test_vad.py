import torch

from app.voice.vad import VoiceActivityDetector


def main() -> None:
    print("Memuat VAD...")

    vad = VoiceActivityDetector()

    print("VAD siap.")

    silence = torch.zeros(512)

    result = vad.is_speech(silence)

    print(f"Silence terdeteksi sebagai speech: {result}")


if __name__ == "__main__":
    main()