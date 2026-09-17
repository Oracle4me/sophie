from app.core.agent import SophieAgent
from app.voice.input import RealtimeVoiceInput
from app.voice.stt import SpeechToText


class VoiceConversationRuntime:
    """
    Runtime percakapan suara Sophie.

    Pipeline:

        microphone
        -> VAD
        -> speech segment
        -> STT
        -> SophieAgent
        -> response text

    TTS belum ditangani oleh runtime ini.
    """

    def __init__(
        self,
        agent: SophieAgent,
        voice_input: RealtimeVoiceInput | None = None,
    ) -> None:
        self.agent = agent

        self.voice_input = (
            voice_input
            or RealtimeVoiceInput()
        )

        self.stt: SpeechToText | None = None

    def _get_stt(self) -> SpeechToText:
        """
        Lazy-load STT.

        Whisper tidak dimuat selama Sophie
        belum menerima speech.
        """

        if self.stt is None:
            print("Memuat STT...")
            self.stt = SpeechToText()
            print("STT siap.")

        return self.stt

    def process_once(self) -> str:
        """
        Menjalankan satu siklus percakapan suara.
        """

        print()
        print("Sophie siap mendengar...")

        audio = self.voice_input.listen()

        if len(audio) == 0:
            return ""

        print("Suara selesai direkam.")

        stt = self._get_stt()

        print("Mentranskripsikan...")

        text = stt.transcribe(audio)

        if not text:
            print("Sophie tidak menangkap teks.")
            return ""

        print(f"You: {text}")

        response = self.agent.respond(text)

        print(f"Sophie: {response}")

        return response

    def run(self) -> None:
        """
        Menjalankan percakapan suara secara terus-menerus.
        """

        print()
        print("========================================")
        print("       SOPHIE VOICE CONVERSATION")
        print("========================================")
        print("Tekan Ctrl+C untuk keluar.")
        print()

        try:
            while True:
                self.process_once()

        except KeyboardInterrupt:
            print()
            print("Sophie: Sampai nanti! 👋")