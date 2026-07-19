from __future__ import annotations

from dataclasses import asdict

from .critic import SelfCritic
from .engine import TrinaryEngine
from .memory import XMLMemory
from .models import Evidence, EvidenceFactors
from .safety import SafeHardwareMonitor


class TrinaryAgent:
    def __init__(
        self,
        memory: XMLMemory,
        engine: TrinaryEngine | None = None,
        name: str = "Trian",
        creator: str = "Arthur Braga Padilha",
    ) -> None:
        self.memory = memory
        self.engine = engine or TrinaryEngine()
        self.critic = SelfCritic()
        self.hardware = SafeHardwareMonitor()
        if not self.memory.get_identity().get("name"):
            self.memory.set_identity(
                name=name,
                creator=creator,
                purpose="Aprender, avaliar evidências e cooperar com seu criador.",
            )

    def learn(
        self,
        proposition: str,
        value: float,
        source: str,
        factors: EvidenceFactors | None = None,
        context: str = "geral",
    ) -> str:
        if not -0.95 <= value <= 0.95:
            raise ValueError("O valor deve estar entre -0,95 e +0,95.")
        evidence = Evidence(
            proposition=proposition.strip(),
            value=value,
            source=source.strip() or "usuário",
            factors=factors or EvidenceFactors(),
            context=context,
        )
        self.memory.add_evidence(evidence)
        return f"Aprendido: {proposition!r} com valor {value:+.3f}."

    def evaluate(self, proposition: str) -> dict[str, object]:
        evidence = self.memory.find_evidence(proposition.strip())
        evaluation = self.engine.evaluate(proposition.strip(), evidence)
        critique = self.critic.review(evaluation)
        self.memory.add_self_critique(critique.text, critique.score)
        result = asdict(evaluation)
        result["state"] = evaluation.state.value
        result["diagnosis"] = evaluation.diagnosis.value if evaluation.diagnosis else None
        result["self_critique"] = asdict(critique)
        return result

    def status(self) -> dict[str, object]:
        status = self.hardware.inspect()
        self.memory.add_system_event("hardware_status", status.message)
        return asdict(status)

    def respond(self, text: str) -> str:
        self.memory.add_interaction("user", text)
        command = text.strip()
        lowered = command.lower()

        if lowered in {"ajuda", "/ajuda", "help"}:
            response = (
                "Comandos: aprender | avaliar | identidade | status | sair.\n"
                "Exemplo: aprender :: o céu está nublado :: 0.70 :: observação direta"
            )
        elif lowered in {"identidade", "/identidade"}:
            identity = self.memory.get_identity()
            response = (
                f"Eu sou {identity.get('name', 'sem nome')}, criada para "
                f"{identity.get('purpose', 'aprender e cooperar')}. "
                f"Criador registrado: {identity.get('creator', 'não informado')}."
            )
        elif lowered in {"status", "/status"}:
            status = self.status()
            response = (
                f"Sistema: {status['message']}; risco trinário {status['risk_value']:+.2f}; "
                f"disco livre {status['free_disk_bytes'] / (1024**3):.2f} GiB."
            )
        elif lowered.startswith("aprender ::"):
            response = self._parse_learn(command)
        elif lowered.startswith("avaliar ::"):
            proposition = command.split("::", 1)[1].strip()
            result = self.evaluate(proposition)
            response = (
                f"{result['state']} {result['value']:+.3f}"
                f"/{result['diagnosis'] or '-'} — {result['explanation']} "
                f"Autocrítica: {result['self_critique']['text']}"
            )
        else:
            response = (
                "Ainda não possuo um modelo de linguagem acoplado. Posso aprender e avaliar "
                "proposições pelo Método Trinário. Digite 'ajuda'."
            )

        self.memory.add_interaction("assistant", response)
        return response

    def _parse_learn(self, command: str) -> str:
        parts = [part.strip() for part in command.split("::")]
        if len(parts) < 4:
            return "Formato: aprender :: proposição :: valor :: fonte"
        _, proposition, raw_value, source, *rest = parts
        try:
            value = float(raw_value.replace(",", "."))
        except ValueError:
            return "Valor inválido. Use um número entre -0,95 e +0,95."
        context = rest[0] if rest else "geral"
        try:
            return self.learn(proposition, value, source, context=context)
        except ValueError as exc:
            return str(exc)
