import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPOCH_DIR = ROOT / "epochs"
CURRENT_EPOCH = ROOT / "current" / "epoch.json"

class EpochImmutabilityTest(unittest.TestCase):
    def test_historical_epochs_exist(self):
        files = sorted(EPOCH_DIR.rglob("*.json"))
        self.assertGreaterEqual(len(files), 1)

    def test_bootstrap_epoch_is_present(self):
        target = ROOT / "epochs" / "2026" / "epoch-0001-bootstrap.json"
        self.assertTrue(target.exists())

    def test_current_epoch_is_not_the_only_record(self):
        current = json.loads(CURRENT_EPOCH.read_text(encoding="utf-8"))
        historical = json.loads((ROOT / "epochs" / "2026" / "epoch-0001-bootstrap.json").read_text(encoding="utf-8"))
        self.assertIn("epoch_id", current)
        self.assertIn("epoch_id", historical)

if __name__ == "__main__":
    unittest.main()
