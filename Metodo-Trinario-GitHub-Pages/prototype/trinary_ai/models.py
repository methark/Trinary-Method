from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class TrinaryState(str, Enum):
    REJECTED = "F"
    INDETERMINATE = "E"
    ACCEPTED = "V"


class Diagnosis(str, Enum):
    UNCLASSIFIED = "D0"
    NO_DATA = "D1"
    INSUFFICIENT = "D2"
    CONFLICT = "D3"
    MALFORMED = "D4"
    PENDING_CONDITION = "D5"


@dataclass(frozen=True, slots=True)
class EvidenceFactors:
    quality: float = 1.0
    reliability: float = 1.0
    independence: float = 1.0
    recency: float = 1.0
    relevance: float = 1.0
    consistency: float = 1.0

    def weight(self) -> float:
        values = (
            self.quality,
            self.reliability,
            self.independence,
            self.recency,
            self.relevance,
            self.consistency,
        )
        if any(not 0.0 <= value <= 1.0 for value in values):
            raise ValueError("Todos os fatores devem estar no intervalo [0, 1].")
        product = 1.0
        for value in values:
            product *= value
        return product ** (1.0 / len(values))


@dataclass(frozen=True, slots=True)
class Evidence:
    proposition: str
    value: float
    source: str
    factors: EvidenceFactors = field(default_factory=EvidenceFactors)
    context: str = "geral"
    observed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Evaluation:
    proposition: str
    value: float
    state: TrinaryState
    diagnosis: Diagnosis | None
    positive_mean: float
    negative_mean: float
    positive_coverage: float
    negative_coverage: float
    positive_support: float
    negative_support: float
    conflict: float
    explanation: str
    evidence_count: int
