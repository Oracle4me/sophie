from app.core.agent import SophieAgent
from app.voice.input import RealtimeVoiceInput
from app.voice.piper_tts import PiperTextToSpeech
from app.voice.state import VoiceState
from app.voice.stt import SpeechToText


class VoiceConversationRuntime:
    """
    Runtime percakapan suara Sophie.

    Pipeline:

        microphone
        -> VAD
        -> STT
        -> SophieAgent
        -> Piper TTS
        -> speaker

    Runtime juga mengatur lifecycle resource
    untuk model-model voice yang berat.
    """

    def __init__(
        self,
        agent: SophieAgent,
        voice_input: RealtimeVoiceInput | None = None,
        tts: PiperTextToSpeech | None = None,
        idle_timeout: float = 60.0,
    ) -> None:
        self.agent = agent

        self.voice_input = (
            voice_input
            or RealtimeVoiceInput()
        )

        self.tts = (
            tts
            or PiperTextToSpeech()
        )

        self.stt: SpeechToText | None = None

        self.idle_timeout = idle_timeout

        self.state = VoiceState.PASSIVE

    def _set_state(
        self,
        state: VoiceState,
    ) -> None:
        """
        Mengubah state voice Sophie.
        """

        self.state = state

    def _get_stt(self) -> SpeechToText:
        """
        Lazy-load Whisper.

        Whisper baru dimuat ketika Sophie
        benar-benar menerima speech.
        """

        if self.stt is None:
            print("Memuat STT...")

            self.stt = SpeechToText()

            print("STT siap.")

        return self.stt

    def release_resources(self) -> None:
        """
        Melepaskan resource voice yang berat.
        """

        if self.stt is not None:
            self.stt.release()
            self.stt = None

        self.tts.release()

    def process_once(self) -> str:
        """
        Memproses satu siklus percakapan suara.
        """

        self._set_state(
            VoiceState.LISTENING
        )

        audio = self.voice_input.listen(
            idle_timeout=self.idle_timeout
        )

        if len(audio) == 0:
            self.release_resources()

            self._set_state(
                VoiceState.PASSIVE
            )

            print(
                "Sophie idle terlalu lama. "
                "Resource voice dilepas."
            )

            return ""

        self._set_state(
            VoiceState.THINKING
        )

        print(
            "Suara selesai direkam."
        )

        stt = self._get_stt()

        print(
            "Mentranskripsikan..."
        )

        text = stt.transcribe(
            audio
        )

        if not text:
            print(
                "Sophie tidak menangkap teks."
            )

            self._set_state(
                VoiceState.PASSIVE
            )

            return ""

        print(
            f"You: {text}"
        )

        response = self.agent.respond(
            text
        )

        print(
            f"Sophie: {response}"
        )

        self._set_state(
            VoiceState.SPEAKING
        )

        self.tts.speak(
            response
        )

        self._set_state(
            VoiceState.PASSIVE
        )

        return response

    def run(self) -> None:
        """
        Menjalankan percakapan suara terus-menerus.
        """

        print()
        print(
            "========================================"
        )
        print(
            "       SOPHIE FULL VOICE MODE"
        )
        print(
            "========================================"
        )
        print(
            "Tekan Ctrl+C untuk keluar."
        )
        print()

        try:
            while True:
                self.process_once()

        except KeyboardInterrupt:
            self.release_resources()

            self._set_state(
                VoiceState.PASSIVE
            )

            print()
            print(
                "Sophie: Sampai nanti! 👋"
            )

        except Exception:
            self.release_resources()

            self._set_state(
                VoiceState.PASSIVE
            )

            raise