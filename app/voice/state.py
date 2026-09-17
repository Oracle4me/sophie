from enum import Enum


class VoiceState(str, Enum):
    """
    State machine percakapan suara Sophie.
    """

    PASSIVE = "passive"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"