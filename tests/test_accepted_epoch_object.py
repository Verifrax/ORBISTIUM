import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_accepted_epoch_object_minimum():
    path = ROOT / "epochs/current/accepted-epoch-0001.json"
    assert path.is_file()

    data = json.loads(path.read_text())
    assert data["object_type"] == "AcceptedEpoch"
    assert data["accepted_epoch_id"] == "accepted-epoch-0001"
    assert data["status"] == "ACTIVE_TRUTH"
    assert data["epoch_ref"] == "current/epoch.json"
    assert data["historical_archive_ref"] == "epochs/history/"
    assert data["graph_ref"] == "current/graph.json"
    assert data["trust_summary_ref"] == "current/trust-summary.json"
    assert data["digest_ref"] == "current/digest.txt"

    current_epoch = json.loads((ROOT / data["epoch_ref"]).read_text())
    assert current_epoch["status"] == "provisional"

    history_readme = ROOT / "epochs/history/README.md"
    assert history_readme.is_file()
    assert "historical snapshots" in history_readme.read_text().lower()
