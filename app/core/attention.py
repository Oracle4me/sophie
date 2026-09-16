from app.core.models import AttentionState


class AttentionEngine:
    """
    Attention Engine Sophie.

    Bertanggung jawab menilai apakah suatu keadaan
    layak mendapatkan perhatian Sophie.

    Engine ini belum menentukan tindakan.
    """

    def evaluate(
        self,
        relevance: float = 0.0,
        importance: float = 0.0,
        urgency: float = 0.0,
        interruption_cost: float = 0.0,
    ) -> AttentionState:
        """
        Menghitung attention score dari beberapa faktor.

        Semua nilai harus berada pada rentang 0.0 - 1.0.
        """

        values = [
            relevance,
            importance,
            urgency,
            interruption_cost,
        ]

        if not all(0.0 <= value <= 1.0 for value in values):
            raise ValueError(
                "Semua nilai attention harus berada "
                "di antara 0.0 dan 1.0."
            )

        attention_score = (
            (relevance * 0.35)
            + (importance * 0.30)
            + (urgency * 0.25)
            - (interruption_cost * 0.20)
        )

        attention_score = max(
            0.0,
            min(1.0, attention_score),
        )

        should_consider = attention_score >= 0.50

        return AttentionState(
            relevance=relevance,
            importance=importance,
            urgency=urgency,
            interruption_cost=interruption_cost,
            attention_score=attention_score,
            should_consider=should_consider,
        )