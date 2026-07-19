from __future__ import annotations

from dataclasses import dataclass

from .models import Evaluation, TrinaryState


@dataclass(frozen=True, slots=True)
class Critique:
    score: float
    text: str


class SelfCritic:
    def review(self, evaluation: Evaluation) -> Critique:
        concerns: list[str] = []
        score = 0.85
        if evaluation.evidence_count == 0:
            concerns.append("não há evidências")
            score -= 0.55
        if evaluation.conflict >= 0.5:
            concerns.append("há conflito relevante")
            score -= 0.30
        if evaluation.state is TrinaryState.INDETERMINATE:
            concerns.append("a conclusão deve permanecer suspensa")
            score -= 0.15
        if not concerns:
            concerns.append("a resposta é coerente com as evidências registradas")
        score = max(-0.95, min(0.95, score))
        return Critique(score=score, text="; ".join(concerns).capitalize() + ".")
