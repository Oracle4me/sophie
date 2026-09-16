from app.core.models import AttentionState, AutonomyState


class AutonomyEngine:
    """
    Autonomy Engine Sophie.

    Mengubah hasil attention menjadi keputusan tingkat tinggi.

    Engine ini belum menjalankan action apa pun.
    """

    def decide(
        self,
        attention: AttentionState,
        user_focus: float = 0.0,
    ) -> AutonomyState:
        """
        Menentukan keputusan autonomy berdasarkan attention
        dan kondisi fokus pengguna.

        user_focus:
            0.0 = user tidak sedang fokus
            1.0 = user sangat fokus
        """

        if not 0.0 <= user_focus <= 1.0:
            raise ValueError(
                "user_focus harus berada di antara 0.0 dan 1.0."
            )

        if not attention.should_consider:
            return AutonomyState(
                decision="wait",
                confidence=1.0 - attention.attention_score,
                reason="attention_below_threshold",
                requires_permission=False,
            )

        if user_focus >= 0.8:
            return AutonomyState(
                decision="wait",
                confidence=user_focus,
                reason="user_focus_high",
                requires_permission=False,
            )

        if attention.attention_score >= 0.7:
            return AutonomyState(
                decision="offer_help",
                confidence=attention.attention_score,
                reason="relevant_and_attention_high",
                requires_permission=False,
            )

        return AutonomyState(
            decision="wait",
            confidence=attention.attention_score,
            reason="attention_not_sufficient_for_action",
            requires_permission=False,
        )