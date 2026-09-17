import wave

import numpy as np

from app.voice.input import RealtimeVoiceInput


def save_wav(
    filename: str,
    audio: np.ndarray,
    sample_rate: int,
) -> None:
    """
    Menyimpan audio float32 [-1.0, 1.0]
    sebagai PCM 16-bit WAV.
    """

    audio = np.clip(audio, -1.0, 1.0)

    pcm_audio = (
        audio * 32767
    ).astype(np.int16)

    with wave.open(filename, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(
            pcm_audio.tobytes()
        )


def main() -> None:
    voice_input = RealtimeVoiceInput()

    print()
    print("========================================")
    print("       SOPHIE REALTIME VOICE TEST")
    print("========================================")
    print("Bicaralah setelah Sophie siap.")
    print("Berhenti bicara sekitar 0.5 detik untuk selesai.")
    print()

    audio = voice_input.listen()

    print()
    print(
        f"Audio berhasil direkam: "
        f"{len(audio)} samples"
    )

    if len(audio) == 0:
        print("Tidak ada suara terdeteksi.")
        return

    filename = "test_voice_input.wav"

    save_wav(
        filename,
        audio,
        voice_input.sample_rate,
    )

    print(
        f"Audio disimpan ke {filename}"
    )


if __name__ == "__main__":
    main()