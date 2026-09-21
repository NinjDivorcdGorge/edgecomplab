# Edge BioReef Guardian

A creative edge-computing simulation for a coral reef acoustic sensor swarm.

## Idea

Underwater hydrophones continuously hear reef soundscapes: fish choruses, spawning events, boat noise, and storm conditions. Sending raw audio to a distant cloud is expensive and too slow for a local warning system. This simulator places lightweight acoustic classifiers on submerged edge gateways.

Each gateway:

- classifies every sound frame locally;
- uses nearby hydrophones to fuse corroborating detections;
- raises a compact local alert for confirmed reef events;
- forwards only short evidence clips and event metadata to the cloud.

The cloud is still useful for long-term ecological analysis, but it is removed from the urgent alert loop.

## Why it is different

This is not generic task offloading, resource scaling, air-quality monitoring, surveillance, or anomaly/attack detection. Its central problem is **distributed acoustic evidence fusion under noisy environmental conditions**. The storm scenario deliberately tests the trade-off between noise, precision, uplink savings, and response time.

## Run

```bash
cd /workspaces/edgecomplab/edge_bioreef_guardian
python3 run_simulation.py
```

The script creates:

- `output/reef_guardian_summary.json`
- `output/bandwidth_reduction.png`
- `output/latency_and_quality.png`
- `output/load_and_energy.png`

## Main questions answered

- How much raw acoustic traffic can remain at the edge?
- Does local alerting stay below a 150 ms response target?
- How does noise affect alert precision?
- How much radio energy is avoided by reporting evidence instead of raw audio?
