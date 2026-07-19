from __future__ import annotations

from dataclasses import dataclass

from .models import Diagnosis, Evidence, Evaluation, TrinaryState


@dataclass(slots=True)
class TrinaryEngine:
    cap: float = 0.95
    threshold: float = 1.0 / 3.0
    sufficiency: float = 1.0
    conflict_threshold: float = 0.5

    def clamp(self, value: float) -> float:
        return max(-self.cap, min(self.cap, value))

    @staticmethod
    def coverage(mass: float) -> float:
        if mass < 0:
            raise ValueError("A massa de evidência não pode ser negativa.")
        return mass / (mass + 1.0)

    def evaluate(
        self,
        proposition: str,
        evidence: list[Evidence],
        *,
        malformed: bool = False,
        pending_condition: bool = False,
    ) -> Evaluation:
        proposition = proposition.strip()
        if not proposition or malformed:
            return self._zero_result(
                proposition or "(proposição vazia)",
                Diagnosis.MALFORMED,
                "A proposição está vazia, ambígua ou malformada.",
                len(evidence),
            )
        if pending_condition:
            return self._zero_result(
                proposition,
                Diagnosis.PENDING_CONDITION,
                "A avaliação depende de uma condição ainda não resolvida.",
                len(evidence),
            )

        valid = [item for item in evidence if item.proposition == proposition]
        if not valid:
            return self._zero_result(
                proposition,
                Diagnosis.NO_DATA,
                "Não há evidências registradas para esta proposição.",
                0,
            )

        positive = [(item.factors.weight(), item.value) for item in valid if item.value > 0]
        negative = [(item.factors.weight(), -item.value) for item in valid if item.value < 0]

        positive_mass = sum(weight for weight, _ in positive)
        negative_mass = sum(weight for weight, _ in negative)

        positive_mean = self._weighted_mean(positive)
        negative_mean = self._weighted_mean(negative)
        positive_coverage = self.coverage(positive_mass)
        negative_coverage = self.coverage(negative_mass)
        positive_support = positive_mean * positive_coverage
        negative_support = negative_mean * negative_coverage

        support_sum = positive_support + negative_support
        conflict = (
            2.0 * min(positive_support, negative_support) / support_sum
            if support_sum > 0
            else 0.0
        )
        result = positive_support - negative_support
        value = self.clamp(result * self.sufficiency)

        if value >= self.threshold:
            state = TrinaryState.ACCEPTED
            diagnosis = None
        elif value <= -self.threshold:
            state = TrinaryState.REJECTED
            diagnosis = None
        else:
            state = TrinaryState.INDETERMINATE
            diagnosis = (
                Diagnosis.CONFLICT
                if conflict >= self.conflict_threshold
                else Diagnosis.INSUFFICIENT
            )

        explanation = self._explain(value, state, diagnosis, conflict, len(valid))
        return Evaluation(
            proposition=proposition,
            value=round(value, 6),
            state=state,
            diagnosis=diagnosis,
            positive_mean=round(positive_mean, 6),
            negative_mean=round(negative_mean, 6),
            positive_coverage=round(positive_coverage, 6),
            negative_coverage=round(negative_coverage, 6),
            positive_support=round(positive_support, 6),
            negative_support=round(negative_support, 6),
            conflict=round(conflict, 6),
            explanation=explanation,
            evidence_count=len(valid),
        )

    @staticmethod
    def protected_modus_ponens(premise: float, rule: float) -> float:
        return min(premise, rule) if premise > 0 and rule > 0 else 0.0

    @staticmethod
    def negation(value: float) -> float:
        return -value

    @staticmethod
    def conjunction(left: float, right: float) -> float:
        return min(left, right)

    @staticmethod
    def disjunction(left: float, right: float) -> float:
        return max(left, right)

    @staticmethod
    def biconditional_kleene(left: float, right: float) -> float:
        return min(max(-left, right), max(-right, left))

    @staticmethod
    def _weighted_mean(items: list[tuple[float, float]]) -> float:
        mass = sum(weight for weight, _ in items)
        if mass <= 0:
            return 0.0
        return sum(weight * value for weight, value in items) / mass

    def _zero_result(
        self,
        proposition: str,
        diagnosis: Diagnosis,
        explanation: str,
        count: int,
    ) -> Evaluation:
        return Evaluation(
            proposition=proposition,
            value=0.0,
            state=TrinaryState.INDETERMINATE,
            diagnosis=diagnosis,
            positive_mean=0.0,
            negative_mean=0.0,
            positive_coverage=0.0,
            negative_coverage=0.0,
            positive_support=0.0,
            negative_support=0.0,
            conflict=0.0,
            explanation=explanation,
            evidence_count=count,
        )

    @staticmethod
    def _explain(
        value: float,
        state: TrinaryState,
        diagnosis: Diagnosis | None,
        conflict: float,
        count: int,
    ) -> str:
        if state is TrinaryState.ACCEPTED:
            return f"Proposição sustentada por {count} evidência(s), com valor {value:.3f}."
        if state is TrinaryState.REJECTED:
            return f"Proposição refutada por {count} evidência(s), com valor {value:.3f}."
        if diagnosis is Diagnosis.CONFLICT:
            return f"Julgamento suspenso: conflito elevado ({conflict:.3f}) entre os canais."
        return "Julgamento suspenso: a força/cobertura disponível ainda é insuficiente."
