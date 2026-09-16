from app.core.models import (
    CognitiveIntent,
    CognitiveState,
    PersonalityState,
    ResponsePlan,
)


class ResponsePlanner:
    """
    Menentukan bagaimana Sophie sebaiknya merespons.

    ResponsePlanner menerjemahkan:
    - cognitive state
    - personality state

    menjadi ResponsePlan terstruktur.

    Planner tidak menghasilkan teks.
    """

    def plan(
        self,
        cognitive_state: CognitiveState,
        personality_state: PersonalityState,
    ) -> ResponsePlan:
        """
        Membuat rencana respons berdasarkan kondisi kognitif
        dan personality Sophie saat ini.
        """

        plan = ResponsePlan(
            tone="natural",
            verbosity="moderate",
            playful=False,
            supportive=True,
            focused=False,
        )

        intent = cognitive_state.intent

        if intent == CognitiveIntent.TECHNICAL_HELP:
            plan.tone = "focused"
            plan.verbosity = "detailed"
            plan.playful = personality_state.playfulness >= 0.7
            plan.supportive = True
            plan.focused = True

        elif intent == CognitiveIntent.PLANNING:
            plan.tone = "structured"
            plan.verbosity = "detailed"
            plan.playful = personality_state.playfulness >= 0.7
            plan.supportive = True
            plan.focused = True

        elif intent == CognitiveIntent.QUESTION:
            plan.tone = "curious"
            plan.verbosity = "moderate"
            plan.playful = personality_state.playfulness >= 0.75
            plan.supportive = True

        elif intent == CognitiveIntent.CONVERSATION:
            plan.tone = "warm"
            plan.verbosity = "moderate"
            plan.playful = personality_state.playfulness >= 0.6
            plan.supportive = True

        elif intent == CognitiveIntent.INSTRUCTION:
            plan.tone = "clear"
            plan.verbosity = "moderate"
            plan.playful = False
            plan.supportive = True
            plan.focused = True

        elif intent == CognitiveIntent.CLARIFICATION:
            plan.tone = "gentle"
            plan.verbosity = "concise"
            plan.playful = personality_state.playfulness >= 0.75
            plan.supportive = True

        return plan