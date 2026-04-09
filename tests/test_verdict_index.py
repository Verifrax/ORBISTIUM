import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class VerdictIndexTest(unittest.TestCase):
    def test_current_verdict_index_loads(self):
        payload = json.loads((ROOT / "current" / "verdict-index.json").read_text(encoding="utf-8"))
        self.assertIn("epoch_id", payload)
        self.assertIn("law_version", payload)
        self.assertEqual(payload["verdict_count"], len(payload["verdicts"]))

    def test_indexes_verdicts_loads(self):
        payload = json.loads((ROOT / "indexes" / "verdicts.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(payload), 1)
        self.assertIn("verdict", payload[0])

if __name__ == "__main__":
    unittest.main()
