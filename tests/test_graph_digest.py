import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "current" / "graph.json"
EPOCH = ROOT / "current" / "epoch.json"
DIGEST = ROOT / "current" / "digest.txt"

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

class GraphDigestTest(unittest.TestCase):
    def test_epoch_graph_digest_matches_graph_file(self):
        graph_digest = sha256_file(GRAPH)
        epoch = json.loads(EPOCH.read_text(encoding="utf-8"))
        self.assertEqual(epoch["graph_digest"], graph_digest)

    def test_digest_manifest_matches_graph_file(self):
        expected = f"{sha256_file(GRAPH)}  current/graph.json"
        lines = DIGEST.read_text(encoding="utf-8").splitlines()
        self.assertIn(expected, lines)

    def test_digest_manifest_covers_proof_bundle(self):
        lines = DIGEST.read_text(encoding="utf-8").splitlines()
        self.assertTrue(any(line.endswith("  current/proof-bundle.json") for line in lines))

if __name__ == "__main__":
    unittest.main()
