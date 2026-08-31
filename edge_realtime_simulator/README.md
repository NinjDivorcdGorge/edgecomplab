# Edge-First Real-Time Processing Simulator

This project is a dedicated simulator for a realistic industrial edge-computing case study. It models a smart manufacturing environment where sensor telemetry is processed as close as possible to the source, with the cloud only handling non-critical workloads.

## Objective
The simulator demonstrates how edge nodes can be deployed to support real-time processing for industrial IoT devices while preserving responsiveness, reducing bandwidth, and improving system resilience.

## Scenario
A plant with machine sensors continuously sends vibration, temperature, and quality telemetry. A local edge layer performs filtering, anomaly detection, and emergency decisions. The cloud is used for long-term analytics and model updates.

## Files
- `run_simulation.py` – main simulator
- `problem.md` – problem statement and solution explanation
- `output/` – generated graphs and summary data

## Run it
```bash
cd /workspaces/edgecomplab/edge_realtime_simulator
python3 run_simulation.py
```

## Generated outputs
The script produces:
- `output/latency_comparison.png`
- `output/processing_share.png`
- `output/utilization.png`
- `output/queue_throughput.png`
- `output/edge_summary.json`

## Key idea
Maximum processing is done at the edge. Only a small fraction of tasks is routed to the cloud, which reflects a realistic edge-first deployment for real-time industrial monitoring.
