import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPOCH = ROOT / "current" / "epoch.json"

class EpochSchemaTest(unittest.TestCase):
    def test_epoch_json_loads(self):
        payload = json.loads(EPOCH.read_text(encoding="utf-8"))
        self.assertIsInstance(payload, dict)

    def test_epoch_has_required_fields(self):
        payload = json.loads(EPOCH.read_text(encoding="utf-8"))
        required = {
            "epoch_id",
            "timestamp",
            "law_version",
            "runtime_version",
            "graph_digest",
            "status",
        }
        self.assertTrue(required.issubset(payload.keys()), payload.keys())

    def test_epoch_points_to_full_law_ref(self):
        payload = json.loads(EPOCH.read_text(encoding="utf-8"))
        self.assertTrue(payload["law_version"].startswith("SYNTAGMARIUM@"))
        self.assertGreaterEqual(len(payload["law_version"]), len("SYNTAGMARIUM@") + 40)

if __name__ == "__main__":
    unittest.main()
