# ORBISTIUM World Doctrine

## Mission

ORBISTIUM stores accepted Verifrax world state.

## Required current surfaces

- current/graph.json
- current/epoch.json
- epochs/current/accepted-epoch-0001.json
- current/trust-summary.json
- current/contradictions.json
- current/repairs.json
- current/quarantine.json
- current/proof-bundle.json
- current/digest.txt

## Retention doctrine

Accepted epochs are immutable.
Current state is derived from the latest accepted epoch.
The current accepted-epoch object is `epochs/current/accepted-epoch-0001.json`.
Historical accepted-epoch objects must live under `epochs/history/` and remain subordinate to the current object.
Contradiction, repair, quarantine, and proof history must remain reconstructable.
