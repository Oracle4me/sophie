import gc
import wave
from pathlib import Path

import numpy as np
import sounddevice as sd
from piper import PiperVoice


class PiperTextToSpeech:
    """
    Local Text-to-Speech engine Sophie menggunakan Piper.

    Model dimuat secara lazy dan dapat dilepas
    dari memory ketika Sophie idle.
    """

    def __init__(
        self,
        model_path: str | Path = (
            "data/voice/id_ID-news_tts-medium.onnx"
        ),
    ) -> None:
        self.model_path = Path(model_path)
        self._voice: PiperVoice | None = None

    def _get_voice(self) -> PiperVoice:
        """
        Memuat model Piper hanya ketika dibutuhkan.
        """

        if self._voice is None:
            if not self.model_path.exists():
                raise FileNotFoundError(
                    "Model Piper tidak ditemukan: "
                    f"{self.model_path}"
                )

            print(
                "Memuat voice model Piper..."
            )

            self._voice = PiperVoice.load(
                str(self.model_path)
            )

            print(
                "Voice model Piper siap."
            )

        return self._voice

    def synthesize(
        self,
        text: str,
        output_path: str | Path,
    ) -> Path:
        """
        Menghasilkan file WAV dari teks.
        """

        if not text.strip():
            raise ValueError(
                "Text TTS tidak boleh kosong."
            )

        voice = self._get_voice()
        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with wave.open(
            str(output_path),
            "wb",
        ) as wav_file:
            voice.synthesize_wav(
                text,
                wav_file,
            )

        return output_path

    def speak(
        self,
        text: str,
    ) -> None:
        """
        Menghasilkan audio lalu memutarnya.
        """

        output_path = Path(
            "data/voice/sophie_runtime.wav"
        )

        self.synthesize(
            text,
            output_path,
        )

        self._play_wav(
            output_path
        )

    def _play_wav(
        self,
        audio_path: Path,
    ) -> None:
        """
        Memutar WAV menggunakan sounddevice.
        """

        with wave.open(
            str(audio_path),
            "rb",
        ) as wav_file:
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            sample_rate = wav_file.getframerate()
            frame_count = wav_file.getnframes()

            audio_data = (
                wav_file.readframes(
                    frame_count
                )
            )

        if sample_width == 2:
            dtype = np.int16

        elif sample_width == 4:
            dtype = np.int32

        else:
            raise ValueError(
                "Sample width tidak didukung: "
                f"{sample_width}"
            )

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

    def release(self) -> None:
        """
        Melepaskan voice model Piper dari memory.
        """

        if self._voice is None:
            return

        self._voice = None

        gc.collect()

        print(
            "Piper voice model dilepas dari memory."
        )