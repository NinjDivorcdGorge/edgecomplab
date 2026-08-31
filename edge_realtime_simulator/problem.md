# Problem Statement: Real-time Edge Processing for Smart Manufacturing

## Background
A modern manufacturing plant uses hundreds of industrial machines, each instrumented with vibration, temperature, pressure, and safety sensors. These devices produce telemetry continuously and require near-real-time analysis to detect anomalies, prevent failures, and maintain safe operating conditions.

The plant currently sends all raw telemetry to the cloud for analysis. This creates several issues:

- High network latency for time-critical decisions
- Excessive bandwidth consumption on the WAN link
- Delayed reaction to equipment faults
- Greater operational dependency on central cloud availability

Because machine faults can escalate in seconds, the plant needs a system that performs the first-stage detection and control decisions at the network edge, close to the machines.

## Real-world challenge
The plant must support the following conditions:

- Up to 260 industrial devices sending high-frequency telemetry
- Response time under 150 ms for anomaly detection and alerting
- Maximum processing at the edge to reduce bandwidth and latency
- Cloud connectivity reserved for historical analytics, backups, and long-term model retraining
- Stable operation under both normal and peak production loads

## Learning objective
This task aligns with the outcome:

- CO 2: Deploy and manage edge and fog nodes for real-time IoT data processing and communication
- Task 5: Develop and Deploy an Application on an Edge Device

## Proposed solution
Deploy a small cluster of edge nodes near the production line. Each edge node performs:

- local preprocessing of incoming machine telemetry
- filtering and anomaly detection
- event prioritization
- emergency alert generation
- local storage for short-term buffering

Only aggregated or non-critical data is forwarded to the cloud. The cloud remains responsible for:

- long-term trend analysis
- batch model updates
- centralized dashboards
- historical reporting

This design ensures that most computation happens at the edge, which reduces delay and keeps the system resilient when the cloud link is slow or temporarily unavailable.

## How the simulator models the solution
The simulator models four operating conditions:

1. Low load
2. Normal load
3. Peak load
4. Stress load

For each case, it estimates:

- edge and cloud task distribution
- end-to-end latency
- queue backlog
- device utilization
- processing share at the edge

The goal is to validate that an edge-first architecture keeps latency under the target threshold while processing the majority of work locally.

## Expected outcome
The edge-first design should demonstrate:

- more than 85% of workload processed at the edge
- low latency at normal and peak loads
- reduced dependence on the central cloud
- improved responsiveness and reliability for industrial monitoring

## Solution summary
The implementation uses an edge-first deployment pattern where the majority of tasks are executed on local edge gateways. Cloud processing is used only for secondary analysis, not for the real-time decision loop. This matches a realistic industrial IoT architecture and demonstrates how edge nodes can support time-sensitive operations.
