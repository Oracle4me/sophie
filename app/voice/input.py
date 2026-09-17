import queue
import time

import numpy as np
import sounddevice as sd
import torch

from app.voice.vad import VoiceActivityDetector


class RealtimeVoiceInput:
    """
    Realtime microphone input Sophie.

    Pipeline:
        microphone
        -> audio chunks
        -> VAD
        -> speech segment

    Kelas ini belum melakukan STT.
    """

    def __init__(
        self,
        vad: VoiceActivityDetector | None = None,
        sample_rate: int = 16000,
        block_size: int = 512,
        speech_threshold: int = 2,
        silence_threshold: int = 16,
        max_duration: float = 15.0,
    ) -> None:
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.speech_threshold = speech_threshold
        self.silence_threshold = silence_threshold
        self.max_duration = max_duration

        self.vad = vad or VoiceActivityDetector(
            sample_rate=sample_rate
        )

        self.audio_queue: queue.Queue[np.ndarray] = queue.Queue()

    def _callback(
        self,
        indata: np.ndarray,
        frames: int,
        time_info,
        status,
    ) -> None:
        """
        Callback microphone.

        Callback hanya memasukkan audio ke queue.
        VAD tidak dijalankan di thread audio.
        """

        if status:
            print(f"Microphone: {status}")

        self.audio_queue.put(
            indata[:, 0].copy()
        )

    def listen(self) -> np.ndarray:
        """
        Menunggu suara, lalu mengumpulkan satu
        segment percakapan sampai silence.
        """

        self.vad.model.reset_states()

        speech_count = 0
        silence_count = 0
        started = False

        audio_chunks: list[np.ndarray] = []

        start_time: float | None = None

        print("Sophie siap mendengar...")

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            blocksize=self.block_size,
            callback=self._callback,
        ):
            while True:
                try:
                    chunk = self.audio_queue.get(
                        timeout=1.0
                    )
                except queue.Empty:
                    continue

                audio_tensor = torch.from_numpy(
                    chunk
                )

                with torch.inference_mode():
                    probability = self.vad.model(
                        audio_tensor,
                        self.sample_rate,
                    )

                is_speech = (
                    float(probability)
                    >= self.vad.threshold
                )

                if not started:
                    if is_speech:
                        speech_count += 1
                    else:
                        speech_count = 0

                    if speech_count >= self.speech_threshold:
                        started = True
                        start_time = time.monotonic()

                        audio_chunks.append(chunk)

                        print("Suara terdeteksi...")
                else:
                    audio_chunks.append(chunk)

                    if is_speech:
                        silence_count = 0
                    else:
                        silence_count += 1

                    if (
                        silence_count
                        >= self.silence_threshold
                    ):
                        break

                    if (
                        start_time is not None
                        and time.monotonic() - start_time
                        >= self.max_duration
                    ):
                        break

        if not audio_chunks:
            return np.array(
                [],
                dtype=np.float32,
            )

        self.vad.model.reset_states()

        return np.concatenate(
            audio_chunks
        )