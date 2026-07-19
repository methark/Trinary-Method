from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import threading
import xml.etree.ElementTree as ET

from .models import Evidence, EvidenceFactors


class XMLMemory:
    """Memória XML simples, auditável e com gravação atômica."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._lock = threading.RLock()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._initialize()

    def _initialize(self) -> None:
        root = ET.Element("trinary_memory", version="1")
        ET.SubElement(root, "identity")
        ET.SubElement(root, "facts")
        ET.SubElement(root, "interactions")
        ET.SubElement(root, "self_critiques")
        ET.SubElement(root, "system_events")
        self._write_tree(ET.ElementTree(root))

    def set_identity(self, name: str, creator: str, purpose: str) -> None:
        with self._lock:
            tree = ET.parse(self.path)
            identity = tree.getroot().find("identity")
            assert identity is not None
            identity.clear()
            identity.set("name", name)
            identity.set("creator", creator)
            identity.set("purpose", purpose)
            identity.set("updated_at", self._now())
            self._write_tree(tree)

    def get_identity(self) -> dict[str, str]:
        with self._lock:
            tree = ET.parse(self.path)
            identity = tree.getroot().find("identity")
            return dict(identity.attrib) if identity is not None else {}

    def add_evidence(self, evidence: Evidence) -> None:
        with self._lock:
            tree = ET.parse(self.path)
            facts = tree.getroot().find("facts")
            assert facts is not None
            node = ET.SubElement(facts, "evidence")
            node.set("proposition", evidence.proposition)
            node.set("value", str(evidence.value))
            node.set("source", evidence.source)
            node.set("context", evidence.context)
            node.set("observed_at", evidence.observed_at)
            factors = ET.SubElement(node, "factors")
            for key, value in asdict(evidence.factors).items():
                factors.set(key, str(value))
            metadata = ET.SubElement(node, "metadata")
            for key, value in evidence.metadata.items():
                item = ET.SubElement(metadata, "item", key=str(key))
                item.text = str(value)
            self._write_tree(tree)

    def find_evidence(self, proposition: str) -> list[Evidence]:
        with self._lock:
            tree = ET.parse(self.path)
            result: list[Evidence] = []
            for node in tree.findall("./facts/evidence"):
                if node.get("proposition") != proposition:
                    continue
                factors_node = node.find("factors")
                factor_data = factors_node.attrib if factors_node is not None else {}
                factors = EvidenceFactors(**{
                    key: float(value) for key, value in factor_data.items()
                })
                metadata = {
                    item.get("key", ""): item.text or ""
                    for item in node.findall("./metadata/item")
                }
                result.append(Evidence(
                    proposition=node.get("proposition", ""),
                    value=float(node.get("value", "0")),
                    source=node.get("source", "desconhecida"),
                    context=node.get("context", "geral"),
                    observed_at=node.get("observed_at", self._now()),
                    factors=factors,
                    metadata=metadata,
                ))
            return result

    def add_interaction(self, role: str, text: str) -> None:
        self._append_text("interactions", "message", text, role=role)

    def add_self_critique(self, text: str, score: float) -> None:
        self._append_text("self_critiques", "critique", text, score=str(score))

    def add_system_event(self, event_type: str, text: str) -> None:
        self._append_text("system_events", "event", text, type=event_type)

    def _append_text(self, parent_name: str, tag: str, text: str, **attrs: str) -> None:
        with self._lock:
            tree = ET.parse(self.path)
            parent = tree.getroot().find(parent_name)
            assert parent is not None
            node = ET.SubElement(parent, tag, timestamp=self._now(), **attrs)
            node.text = text
            self._write_tree(tree)

    def _write_tree(self, tree: ET.ElementTree) -> None:
        ET.indent(tree, space="  ")
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        tree.write(temporary, encoding="utf-8", xml_declaration=True)
        temporary.replace(self.path)

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()
