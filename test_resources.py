import gc

from app.core.resources import ResourceMonitor
from app.voice.piper_tts import PiperTextToSpeech
from app.voice.stt import SpeechToText
from app.voice.vad import VoiceActivityDetector


def main() -> None:
    monitor = ResourceMonitor()

    print()
    print("========================================")
    print("       SOPHIE RESOURCE PROFILING")
    print("========================================")
    print()

    # --------------------------------------------------
    # BASELINE
    # --------------------------------------------------

    baseline = monitor.print_snapshot(
        "Python baseline"
    )

    baseline_mb = baseline.memory_mb

    # --------------------------------------------------
    # VAD
    # --------------------------------------------------

    print()
    print("Memuat VAD...")

    vad = VoiceActivityDetector()

    monitor.print_snapshot(
        "VAD loaded",
        baseline_mb,
    )

    # --------------------------------------------------
    # STT
    # --------------------------------------------------

    print()
    print("Memuat STT...")

    stt = SpeechToText()

    monitor.print_snapshot(
        "STT loaded",
        baseline_mb,
    )

    # --------------------------------------------------
    # PIPER TTS
    # --------------------------------------------------

    print()
    print("Memuat Piper...")

    tts = PiperTextToSpeech()

    tts._get_voice()

    monitor.print_snapshot(
        "Piper loaded",
        baseline_mb,
    )

    # --------------------------------------------------
    # RELEASE STT
    # --------------------------------------------------

    print()
    print("Release STT...")

    stt.release()

    monitor.print_snapshot(
        "After STT release",
        baseline_mb,
    )

    # --------------------------------------------------
    # RELEASE PIPER
    # --------------------------------------------------

    print()
    print("Release Piper...")

    tts.release()

    monitor.print_snapshot(
        "After Piper release",
        baseline_mb,
    )

    # --------------------------------------------------
    # CLEANUP
    # --------------------------------------------------

    del stt
    del tts

    gc.collect()

    monitor.print_snapshot(
        "Final cleanup",
        baseline_mb,
    )

    # VAD sengaja tetap resident karena saat ini
    # VAD adalah sensor voice utama Sophie.
    del vad

    gc.collect()

    print()
    print("Resource profiling selesai.")


if __name__ == "__main__":
    main()