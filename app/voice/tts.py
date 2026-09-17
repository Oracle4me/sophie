import tempfile
import wave
from pathlib import Path

import sounddevice as sd
from openai import OpenAI

from app.core.config import settings


class TextToSpeech:
    """
    Text-to-Speech Sophie.

    Adapter TTS ini menggunakan OpenAI Audio Speech API.

    TTS tidak bergantung pada SophieAgent.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini-tts",
        voice: str = "marin",
        speed: float = 1.0,
    ) -> None:
        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY belum dikonfigurasi."
            )

        if not 0.25 <= speed <= 4.0:
            raise ValueError(
                "speed harus berada di antara 0.25 dan 4.0."
            )

        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

        self.model = model
        self.voice = voice
        self.speed = speed

    def synthesize(
        self,
        text: str,
        output_path: str | Path,
    ) -> Path:
        """
        Mengubah teks menjadi file WAV.
        """

        if not text.strip():
            raise ValueError(
                "Text TTS tidak boleh kosong."
            )

        output_path = Path(output_path)

        with self.client.audio.speech.with_streaming_response.create(
            model=self.model,
            voice=self.voice,
            input=text,
            response_format="wav",
            speed=self.speed,
        ) as response:
            response.stream_to_file(output_path)

        return output_path

    def speak(self, text: str) -> None:
        """
        Mengubah teks menjadi audio lalu memutarnya.

        File audio bersifat sementara dan dihapus
        setelah playback selesai.
        """

        with tempfile.TemporaryDirectory(
            prefix="sophie_tts_"
        ) as temp_dir:
            output_path = (
                Path(temp_dir) / "speech.wav"
            )

            self.synthesize(
                text,
                output_path,
            )

            self._play_wav(output_path)

    def _play_wav(
        self,
        audio_path: Path,
    ) -> None:
        """
        Memutar file WAV menggunakan sounddevice.
        """

        with wave.open(
            str(audio_path),
            "rb",
        ) as wav_file:
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            sample_rate = wav_file.getframerate()
            frame_count = wav_file.getnframes()
            audio_data = wav_file.readframes(
                frame_count
            )

        if sample_width == 2:
            dtype = "int16"
        elif sample_width == 4:
            dtype = "int32"
        else:
            raise ValueError(
                f"Format sample WAV tidak didukung: "
                f"{sample_width} bytes."
            )

        import numpy as np

        audio = np.frombuffer(
            audio_data,
            dtype=dtype,
        )

        if channels > 1:
            audio = audio.reshape(
                -1,
                channels,
            )

        sd.play(
            audio,
            samplerate=sample_rate,
        )

        sd.wait()