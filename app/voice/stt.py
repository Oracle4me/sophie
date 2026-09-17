import sounddevice as sd
from faster_whisper import WhisperModel


class SpeechToText:
    """
    Speech-to-Text engine Sophie.

    Bertanggung jawab mengubah suara microphone
    menjadi teks.

    Engine ini tidak mengetahui SophieAgent.
    """

    def __init__(
        self,
        model_size: str = "base",
        sample_rate: int = 16000,
    ) -> None:
        self.sample_rate = sample_rate

        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
        )

    def record(
        self,
        duration: float = 5.0,
    ):
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

    def transcribe(self, audio) -> str:
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
        audio = self.record(duration)
        return self.transcribe(audio)