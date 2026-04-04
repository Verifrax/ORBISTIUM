from __future__ import annotations
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CURRENT_FILES = [
    "current/graph.json",
    "current/epoch.json",
    "current/trust-summary.json",
    "current/contradictions.json",
    "current/repairs.json",
    "current/quarantine.json",
    "current/proof-bundle.json",
]

class CurrentStateTest(unittest.TestCase):
    def read_json(self, rel: str):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_current_files_are_valid_json(self) -> None:
        for rel in CURRENT_FILES:
            with self.subTest(rel=rel):
                self.assertIsInstance(self.read_json(rel), dict)

    def test_epoch_binds_graph_and_proof(self) -> None:
        graph = self.read_json("current/graph.json")
        epoch = self.read_json("current/epoch.json")
        proof = self.read_json("current/proof-bundle.json")

        graph_digest = hashlib.sha256(
            (json.dumps(graph, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        ).hexdigest()

        proof_digest = hashlib.sha256(
            (json.dumps(proof, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        ).hexdigest()

        self.assertEqual(epoch["graph_digest"], graph_digest)
        self.assertEqual(proof["graph_digest"], graph_digest)
        self.assertEqual(epoch["proof_bundle_digest"], proof_digest)
        self.assertEqual(epoch["law_version"], graph["law_version"])
        self.assertEqual(epoch["law_version"], proof["law_version"])
        self.assertEqual(epoch["runtime_version"], proof["runtime_version"])

    def test_digest_file_matches_current_files(self) -> None:
        digest_txt = (ROOT / "current/digest.txt").read_text(encoding="utf-8").strip().splitlines()
        digest_map = {}
        for line in digest_txt:
            digest, rel = line.split("  ", 1)
            digest_map[rel] = digest

        for rel in CURRENT_FILES:
            with self.subTest(rel=rel):
                data = (ROOT / rel).read_bytes()
                actual = hashlib.sha256(data).hexdigest()
                self.assertEqual(digest_map[rel], actual)

if __name__ == "__main__":
    unittest.main()
