import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "current"

class CurrentFilesTest(unittest.TestCase):
    def test_expected_current_files_exist(self):
        expected = {
            "contradictions.json",
            "digest.txt",
            "epoch.json",
            "graph.json",
            "proof-bundle.json",
            "quarantine.json",
            "repairs.json",
            "trust-summary.json",
        }
        actual = {p.name for p in CURRENT.iterdir() if p.is_file()}
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
