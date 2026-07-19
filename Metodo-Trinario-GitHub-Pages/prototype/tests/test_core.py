from pathlib import Path
import tempfile
import unittest

from trinary_ai.agent import TrinaryAgent
from trinary_ai.engine import TrinaryEngine
from trinary_ai.memory import XMLMemory
from trinary_ai.models import Diagnosis, Evidence, TrinaryState


class EngineTests(unittest.TestCase):
    def test_no_data(self) -> None:
        result = TrinaryEngine().evaluate("p", [])
        self.assertEqual(result.state, TrinaryState.INDETERMINATE)
        self.assertEqual(result.diagnosis, Diagnosis.NO_DATA)

    def test_conflict(self) -> None:
        evidence = [
            Evidence("p", 0.9, "a"),
            Evidence("p", -0.9, "b"),
        ]
        result = TrinaryEngine().evaluate("p", evidence)
        self.assertEqual(result.value, 0.0)
        self.assertEqual(result.diagnosis, Diagnosis.CONFLICT)
        self.assertEqual(result.conflict, 1.0)

    def test_positive_support(self) -> None:
        evidence = [Evidence("p", 0.9, "a") for _ in range(3)]
        result = TrinaryEngine().evaluate("p", evidence)
        self.assertEqual(result.state, TrinaryState.ACCEPTED)

    def test_protected_modus_ponens(self) -> None:
        self.assertEqual(TrinaryEngine.protected_modus_ponens(-0.7, 0.9), 0.0)
        self.assertEqual(TrinaryEngine.protected_modus_ponens(0.8, 0.9), 0.8)


class MemoryTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            memory = XMLMemory(Path(folder) / "memory.xml")
            agent = TrinaryAgent(memory)
            agent.learn("teste", 0.8, "unittest")
            found = memory.find_evidence("teste")
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].value, 0.8)


if __name__ == "__main__":
    unittest.main()
