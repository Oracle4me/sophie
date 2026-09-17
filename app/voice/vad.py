import torch
from silero_vad import load_silero_vad


torch.set_num_threads(1)


class VoiceActivityDetector:
    """
    Voice Activity Detector Sophie.

    Bertanggung jawab mendeteksi apakah audio
    mengandung suara manusia.

    VAD tidak melakukan speech-to-text.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        threshold: float = 0.5,
    ) -> None:
        if sample_rate not in {8000, 16000}:
            raise ValueError(
                "sample_rate harus 8000 atau 16000."
            )

        if not 0.0 <= threshold <= 1.0:
            raise ValueError(
                "threshold harus berada di antara 0.0 dan 1.0."
            )

        self.sample_rate = sample_rate
        self.threshold = threshold
        self.model = load_silero_vad(
            sampling_rate=sample_rate
        )

    def is_speech(
        self,
        audio: torch.Tensor,
    ) -> bool:
        """
        Menentukan apakah audio mengandung suara manusia.
        """

        with torch.inference_mode():
            probability = self.model(
                audio,
                self.sample_rate,
            )

        return float(probability) >= self.threshold