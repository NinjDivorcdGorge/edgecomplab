#!/usr/bin/env python3
"""Simulate an edge bioacoustic guardian for a coral reef sensor swarm."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SCENARIOS = [
    {
        "name": "Dawn Chorus",
        "hydrophones": 24,
        "gateways": 3,
        "sound_frames_per_sec": 720,
        "real_events_per_hour": 18,
        "noise_factor": 0.85,
        "edge_capacity": 900,
        "cloud_rtt_ms": 185,
    },
    {
        "name": "Tourist Boats",
        "hydrophones": 48,
        "gateways": 5,
        "sound_frames_per_sec": 1_920,
        "real_events_per_hour": 34,
        "noise_factor": 1.35,
        "edge_capacity": 2_400,
        "cloud_rtt_ms": 245,
    },
    {
        "name": "Spawning Pulse",
        "hydrophones": 72,
        "gateways": 7,
        "sound_frames_per_sec": 3_960,
        "real_events_per_hour": 160,
        "noise_factor": 1.05,
        "edge_capacity": 4_200,
        "cloud_rtt_ms": 310,
    },
    {
        "name": "Storm Front",
        "hydrophones": 96,
        "gateways": 8,
        "sound_frames_per_sec": 6_720,
        "real_events_per_hour": 52,
        "noise_factor": 2.2,
        "edge_capacity": 4_800,
        "cloud_rtt_ms": 430,
    },
]

WINDOW_SECONDS = 60
BYTES_PER_AUDIO_FRAME = 160
EVENT_PACKET_BYTES = 420


def simulate_scenario(scenario: dict) -> dict:
    """Run one minute of local classification and evidence reporting."""
    frames = scenario["sound_frames_per_sec"] * WINDOW_SECONDS
    raw_bytes = frames * BYTES_PER_AUDIO_FRAME
    capacity = scenario["edge_capacity"] * scenario["gateways"] * WINDOW_SECONDS
    edge_utilization = min(0.99, frames / capacity)

    # Noise creates more candidate clips, while fusion rejects isolated false alarms.
    candidate_rate = 0.000012 * scenario["noise_factor"]
    candidate_clips = frames * candidate_rate
    true_events = scenario["real_events_per_hour"] / 60
    confirmed_events = min(true_events, true_events * (0.985 - 0.025 * scenario["noise_factor"]))
    false_events = candidate_clips * (0.008 + 0.006 * scenario["noise_factor"])
    fused_alerts = confirmed_events + false_events
    edge_classified = frames
    cloud_frames = candidate_clips * 0.16 + fused_alerts
    cloud_bytes = cloud_frames * EVENT_PACKET_BYTES

    edge_latency = 24 + (edge_utilization * 36) + (scenario["noise_factor"] * 3)
    cloud_only_latency = scenario["cloud_rtt_ms"] + 42 + (candidate_clips / max(frames, 1)) * 1_000
    alert_latency = edge_latency + 18
    edge_energy_wh = (frames / 100_000) * (0.82 + edge_utilization * 0.36)
    radio_energy_wh = (cloud_bytes / 1_000_000) * 1.8
    bandwidth_reduction = 100 * (1 - cloud_bytes / raw_bytes)
    edge_processing_share = 1 - (cloud_frames / frames)
    detection_recall = 100 * confirmed_events / max(true_events, 1e-9)
    precision = 100 * confirmed_events / max(fused_alerts, 1e-9)

    return {
        "name": scenario["name"],
        "hydrophones": scenario["hydrophones"],
        "gateways": scenario["gateways"],
        "raw_frames_per_sec": scenario["sound_frames_per_sec"],
        "edge_classified_frames": round(edge_classified, 2),
        "cloud_forwarded_frames": round(cloud_frames / WINDOW_SECONDS, 2),
        "edge_processing_share": round(edge_processing_share, 4),
        "edge_utilization": round(edge_utilization, 4),
        "raw_uplink_mb_per_min": round(raw_bytes / 1_000_000, 2),
        "reported_uplink_mb_per_min": round(cloud_bytes / 1_000_000, 4),
        "bandwidth_reduction_percent": round(bandwidth_reduction, 3),
        "real_events_per_min": round(true_events, 2),
        "confirmed_alerts_per_min": round(confirmed_events, 2),
        "false_alerts_per_min": round(false_events, 2),
        "detection_recall_percent": round(detection_recall, 2),
        "alert_precision_percent": round(precision, 2),
        "edge_alert_latency_ms": round(alert_latency, 2),
        "cloud_only_latency_ms": round(cloud_only_latency, 2),
        "edge_energy_wh_per_min": round(edge_energy_wh, 4),
        "radio_energy_wh_per_min": round(radio_energy_wh, 4),
    }


def save_summary(results: list[dict]) -> Path:
    path = OUTPUT_DIR / "reef_guardian_summary.json"
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return path


def plot_bandwidth(results: list[dict]) -> Path:
    labels = [result["name"] for result in results]
    raw = [result["raw_uplink_mb_per_min"] for result in results]
    reported = [result["reported_uplink_mb_per_min"] for result in results]
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.bar(x - 0.19, raw, 0.38, label="Raw hydrophone stream", color="#153243")
    ax.bar(x + 0.19, reported, 0.38, label="Evidence sent upstream", color="#e07a5f")
    ax.set_xticks(x, labels)
    ax.set_ylabel("Megabytes per minute")
    ax.set_title("Edge acoustic triage keeps reef data local")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    path = OUTPUT_DIR / "bandwidth_reduction.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def plot_latency_and_quality(results: list[dict]) -> Path:
    labels = [result["name"] for result in results]
    x = np.arange(len(labels))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    ax1.plot(labels, [r["edge_alert_latency_ms"] for r in results], marker="o", linewidth=2.5, label="Edge alert")
    ax1.plot(labels, [r["cloud_only_latency_ms"] for r in results], marker="s", linewidth=2.5, label="Cloud-only alert")
    ax1.axhline(150, color="#e07a5f", linestyle="--", label="150 ms target")
    ax1.set_ylabel("Milliseconds")
    ax1.set_title("Alert response")
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    ax1.legend(fontsize=8)
    ax2.bar(x - 0.18, [r["detection_recall_percent"] for r in results], 0.36, label="Recall", color="#3d9970")
    ax2.bar(x + 0.18, [r["alert_precision_percent"] for r in results], 0.36, label="Precision", color="#f2cc8f")
    ax2.set_xticks(x, labels, rotation=18, ha="right")
    ax2.set_ylim(0, 105)
    ax2.set_ylabel("Percent")
    ax2.set_title("Fusion quality")
    ax2.grid(axis="y", linestyle="--", alpha=0.3)
    ax2.legend(fontsize=8)
    fig.tight_layout()
    path = OUTPUT_DIR / "latency_and_quality.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def plot_load_and_energy(results: list[dict]) -> Path:
    labels = [result["name"] for result in results]
    x = np.arange(len(labels))
    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    ax1.plot(labels, [r["edge_utilization"] * 100 for r in results], marker="o", linewidth=2.5, color="#153243", label="Gateway utilization")
    ax1.set_ylabel("Gateway utilization (%)", color="#153243")
    ax1.set_ylim(0, 105)
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    ax2 = ax1.twinx()
    ax2.bar(x, [r["radio_energy_wh_per_min"] for r in results], alpha=0.55, color="#e07a5f", label="Radio energy")
    ax2.set_ylabel("Radio energy (Wh/min)", color="#e07a5f")
    ax1.set_xticks(x, labels)
    ax1.set_title("Local load and reporting energy")
    fig.tight_layout()
    path = OUTPUT_DIR / "load_and_energy.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def main() -> None:
    results = [simulate_scenario(scenario) for scenario in SCENARIOS]
    save_summary(results)
    plot_bandwidth(results)
    plot_latency_and_quality(results)
    plot_load_and_energy(results)

    print("Edge BioReef Guardian simulation completed.")
    for result in results:
        print(
            f"{result['name']}: {result['hydrophones']} hydrophones, "
            f"{result['bandwidth_reduction_percent']}% bandwidth saved, "
            f"edge alert={result['edge_alert_latency_ms']} ms, "
            f"precision={result['alert_precision_percent']}%"
        )
    print(f"Outputs: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
