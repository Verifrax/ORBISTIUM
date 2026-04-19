from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def test_outsider_can_identify_current_accepted_epoch_from_objects():
    accepted = load("epochs/current/accepted-epoch-0001.json")
    index = load("epochs/current/index.json")

    assert accepted["object_type"] == "AcceptedEpoch"
    assert accepted["status"] == "ACTIVE_TRUTH"
    assert index["object_type"] == "AcceptedEpochIndex"
    assert index["status"] == "ACTIVE_TRUTH"
    assert index["current_accepted_epoch_ref"] == "epochs/current/accepted-epoch-0001.json"

    first = index["entries"][0]
    assert first["accepted_epoch_id"] == accepted["accepted_epoch_id"]
    assert first["epoch_ref"] == "current/epoch.json"
    assert first["graph_ref"] == "current/graph.json"
    assert accepted["trust_summary_ref"] == "current/trust-summary.json"
    assert accepted["digest_ref"] == "current/digest.txt"
    assert accepted["historical_archive_ref"] == "epochs/history/"
