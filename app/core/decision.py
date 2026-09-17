from app.core.models import AgentDecision, AttentionState, AutonomyState


class DecisionEngine:
    """
    Decision Engine Sophie.

    Bertanggung jawab menentukan keputusan akhir agent
    berdasarkan hasil attention dan autonomy.

    Decision Engine tidak menjalankan action apa pun.
    """

    def decide(
        self,
        attention: AttentionState,
        autonomy: AutonomyState,
        user_message: str,
    ) -> AgentDecision:
        """
        Menghasilkan keputusan akhir Sophie untuk
        satu siklus pemrosesan.
        """

        if not user_message.strip():
            return AgentDecision(
                decision="wait",
                reason="empty_user_message",
                confidence=1.0,
                requires_permission=False,
            )

        if autonomy.decision == "wait":
            return AgentDecision(
                decision="respond",
                reason="direct_user_request",
                confidence=max(
                    attention.attention_score,
                    0.8,
                ),
                requires_permission=False,
            )

        return AgentDecision(
            decision="wait",
            reason="autonomy_decision_not_actionable",
            confidence=autonomy.confidence,
            requires_permission=autonomy.requires_permission,
        )