#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def need(cond, name):
    if cond:
        print(f"[VERIFY] {name}")
    else:
        print(f"[FAIL] {name}")
        errors.append(name)

accepted_path = ROOT / "epochs/current/accepted-epoch-0001.json"
index_path = ROOT / "epochs/current/index.json"
history_readme = ROOT / "epochs/history/README.md"

for rel in [
    "epochs/current/accepted-epoch-0001.json",
    "epochs/current/index.json",
    "epochs/history/README.md",
    "current/epoch.json",
    "current/graph.json",
    "current/trust-summary.json",
    "current/contradictions.json",
    "current/repairs.json",
    "current/quarantine.json",
    "current/digest.txt",
]:
    need((ROOT / rel).is_file(), f"file-present {rel}")

accepted = json.loads(accepted_path.read_text(encoding="utf-8"))
index = json.loads(index_path.read_text(encoding="utf-8"))

need(accepted.get("object_type") == "AcceptedEpoch", "accepted-epoch-type")
need(accepted.get("status") == "ACTIVE_TRUTH", "accepted-epoch-status")
need(accepted.get("historical_archive_ref") == "epochs/history/", "accepted-epoch-history-ref")
need(accepted.get("epoch_ref") == "current/epoch.json", "accepted-epoch-epoch-ref")
need(accepted.get("graph_ref") == "current/graph.json", "accepted-epoch-graph-ref")
need(accepted.get("trust_summary_ref") == "current/trust-summary.json", "accepted-epoch-trust-summary-ref")
need(accepted.get("contradictions_ref") == "current/contradictions.json", "accepted-epoch-contradictions-ref")
need(accepted.get("repairs_ref") == "current/repairs.json", "accepted-epoch-repairs-ref")
need(accepted.get("quarantine_ref") == "current/quarantine.json", "accepted-epoch-quarantine-ref")
need(accepted.get("digest_ref") == "current/digest.txt", "accepted-epoch-digest-ref")

need(index.get("object_type") == "AcceptedEpochIndex", "accepted-epoch-index-type")
need(index.get("status") == "ACTIVE_TRUTH", "accepted-epoch-index-status")
need(index.get("historical") is False, "accepted-epoch-index-historical-false")
need(index.get("current_accepted_epoch_ref") == "epochs/current/accepted-epoch-0001.json", "accepted-epoch-index-binding")

entries = index.get("entries", [])
need(len(entries) >= 1, "accepted-epoch-index-entry-present")
if entries:
    first = entries[0]
    need(first.get("accepted_epoch_id") == accepted.get("accepted_epoch_id"), "accepted-epoch-index-entry-id")
    need(first.get("path") == "epochs/current/accepted-epoch-0001.json", "accepted-epoch-index-entry-path")
    need(first.get("epoch_ref") == "current/epoch.json", "accepted-epoch-index-entry-epoch-ref")
    need(first.get("graph_ref") == "current/graph.json", "accepted-epoch-index-entry-graph-ref")

epoch = json.loads((ROOT / accepted["epoch_ref"]).read_text(encoding="utf-8"))
graph = json.loads((ROOT / accepted["graph_ref"]).read_text(encoding="utf-8"))
trust = json.loads((ROOT / accepted["trust_summary_ref"]).read_text(encoding="utf-8"))
contradictions = json.loads((ROOT / accepted["contradictions_ref"]).read_text(encoding="utf-8"))
repairs = json.loads((ROOT / accepted["repairs_ref"]).read_text(encoding="utf-8"))
quarantine = json.loads((ROOT / accepted["quarantine_ref"]).read_text(encoding="utf-8"))

need("epoch_id" in epoch, "epoch-object-readable")
need("law_version" in epoch, "epoch-law-version-present")
need("graph_digest" in epoch, "epoch-graph-digest-present")
need(isinstance(graph, dict) and len(graph) > 0, "graph-surface-readable")
need(isinstance(trust, dict) and len(trust) > 0, "trust-summary-readable")
need(isinstance(contradictions.get("items"), list), "contradictions-readable")
need(isinstance(repairs.get("items"), list), "repairs-readable")
need(isinstance(quarantine.get("items"), list), "quarantine-readable")
need("current/epoch.json" in (ROOT / "current/digest.txt").read_text(encoding="utf-8"), "digest-covers-current-epoch")
need("historical" in history_readme.read_text(encoding="utf-8").lower(), "history-archive-explicit")

if errors:
    print("[FAIL] PHASE 4 / STEP 51 accepted-epoch minimum verification failed")
    for e in errors:
        print(f" - {e}")
    sys.exit(1)

print("[PASS] PHASE 4 / STEP 51 accepted-epoch minimum verified")
