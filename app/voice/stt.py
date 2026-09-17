import gc

from faster_whisper import WhisperModel


class SpeechToText:
    """
    Speech-to-Text engine Sophie.

    Bertanggung jawab mengubah audio microphone
    menjadi teks.

    Engine ini tidak mengetahui SophieAgent.
    """

    def __init__(
        self,
        model_size: str = "base",
        sample_rate: int = 16000,
    ) -> None:
        self.sample_rate = sample_rate

        self.model: WhisperModel | None = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
        )

    def record(
        self,
        duration: float = 5.0,
    ):
        """
        Merekam audio dari microphone.

        Method ini dipertahankan untuk kompatibilitas
        dengan test STT lama.
        """

        if self.model is None:
            raise RuntimeError(
                "STT model sudah dilepas dari memory."
            )

        import sounddevice as sd

        frames = int(
            duration * self.sample_rate
        )

        audio = sd.rec(
            frames,
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
        )

        sd.wait()

        return audio.flatten()

    def transcribe(
        self,
        audio,
    ) -> str:
        """
        Mengubah audio menjadi teks.
        """

        if self.model is None:
            raise RuntimeError(
                "STT model sudah dilepas dari memory."
            )

        segments, _ = self.model.transcribe(
            audio,
            language="id",
            vad_filter=True,
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return text.strip()

    def listen(
        self,
        duration: float = 5.0,
    ) -> str:
        """
        Merekam lalu melakukan transkripsi.
        """

        audio = self.record(
            duration=duration
        )

        return self.transcribe(audio)

    def release(self) -> None:
        """
        Melepaskan model Whisper dari memory.
        """

        if self.model is None:
            return

        self.model = None

        gc.collect()

        print(
            "STT model dilepas dari memory."
        )