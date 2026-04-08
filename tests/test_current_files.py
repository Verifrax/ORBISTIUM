from pathlib import Path

def test_current_state_files_exist():
    required = [
        "current/graph.json",
        "current/epoch.json",
        "current/trust-summary.json",
        "current/contradictions.json",
        "current/repairs.json",
        "current/quarantine.json",
        "current/proof-bundle.json",
        "current/digest.txt",
    ]
    for rel in required:
        assert Path(rel).exists(), rel
