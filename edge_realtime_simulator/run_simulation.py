#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

SCENARIOS = [
    {
        "name": "Low Load",
        "devices": 60,
        "edge_nodes": 3,
        "tasks_per_sec": 360,
        "edge_share": 0.97,
        "cloud_share": 0.03,
        "edge_latency": 42,
        "cloud_latency": 290,
        "utilization": 0.48,
        "queue_ms": 18,
        "packet_loss": 0.02,
    },
    {
        "name": "Normal Load",
        "devices": 120,
        "edge_nodes": 5,
        "tasks_per_sec": 760,
        "edge_share": 0.94,
        "cloud_share": 0.06,
        "edge_latency": 63,
        "cloud_latency": 330,
        "utilization": 0.69,
        "queue_ms": 34,
        "packet_loss": 0.08,
    },
    {
        "name": "Peak Load",
        "devices": 190,
        "edge_nodes": 7,
        "tasks_per_sec": 1220,
        "edge_share": 0.90,
        "cloud_share": 0.10,
        "edge_latency": 88,
        "cloud_latency": 420,
        "utilization": 0.82,
        "queue_ms": 59,
        "packet_loss": 0.12,
    },
    {
        "name": "Stress Load",
        "devices": 260,
        "edge_nodes": 8,
        "tasks_per_sec": 1610,
        "edge_share": 0.86,
        "cloud_share": 0.14,
        "edge_latency": 122,
        "cloud_latency": 510,
        "utilization": 0.94,
        "queue_ms": 91,
        "packet_loss": 0.18,
    },
]


def simulate_scenario(scenario):
    devices = scenario["devices"]
    edge_nodes = scenario["edge_nodes"]
    edge_share = scenario["edge_share"]
    cloud_share = scenario["cloud_share"]
    total_tasks = scenario["tasks_per_sec"]
    edge_tasks = total_tasks * edge_share
    cloud_tasks = total_tasks * cloud_share

    edge_latency = scenario["edge_latency"] + (devices / 240.0) * 14
    cloud_latency = scenario["cloud_latency"] + (devices / 220.0) * 20
    weighted_latency = (edge_share * edge_latency) + (cloud_share * cloud_latency)

    edge_util = min(0.98, scenario["utilization"] * 1.08)
    cloud_util = min(0.82, (cloud_tasks / 600.0) * 0.55)
    backlog = max(0.0, scenario["queue_ms"] + (devices - 120) * 0.18)
    throughput = total_tasks * (1.0 - scenario["packet_loss"])
    success_rate = 100 * (1.0 - scenario["packet_loss"])

    return {
        "name": scenario["name"],
        "devices": devices,
        "edge_nodes": edge_nodes,
        "total_tasks_per_sec": total_tasks,
        "edge_tasks_per_sec": edge_tasks,
        "cloud_tasks_per_sec": cloud_tasks,
        "edge_processing_share": edge_share,
        "cloud_processing_share": cloud_share,
        "edge_latency_ms": round(edge_latency, 2),
        "cloud_latency_ms": round(cloud_latency, 2),
        "weighted_latency_ms": round(weighted_latency, 2),
        "edge_utilization": round(edge_util, 3),
        "cloud_utilization": round(cloud_util, 3),
        "queue_backlog_ms": round(backlog, 2),
        "throughput_per_sec": round(throughput, 2),
        "success_rate_percent": round(success_rate, 2),
    }


def save_summary_json(results):
    path = OUTPUT_DIR / "edge_summary.json"
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return path


def plot_latency_comparison(results):
    labels = [r["name"] for r in results]
    edge_vals = [r["edge_latency_ms"] for r in results]
    cloud_vals = [r["cloud_latency_ms"] for r in results]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(labels))
    width = 0.35
    ax.bar(x - width / 2, edge_vals, width, label="Edge processing", color="#2ca02c")
    ax.bar(x + width / 2, cloud_vals, width, label="Cloud fallback", color="#ff7f0e")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Latency (ms)")
    ax.set_title("End-to-end latency under edge-first processing")
    ax.legend()
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    path = OUTPUT_DIR / "latency_comparison.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def plot_processing_share(results):
    labels = [r["name"] for r in results]
    edge_share = [r["edge_processing_share"] * 100 for r in results]
    cloud_share = [r["cloud_processing_share"] * 100 for r in results]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(labels))
    ax.bar(x, edge_share, label="Processed at Edge", color="#1f77b4")
    ax.bar(x, cloud_share, bottom=edge_share, label="Processed in Cloud", color="#d62728")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Processing share (%)")
    ax.set_title("Proportion of tasks executed at the edge")
    ax.legend()
    ax.grid(True, axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    path = OUTPUT_DIR / "processing_share.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def plot_utilization(results):
    labels = [r["name"] for r in results]
    edge_util = [r["edge_utilization"] * 100 for r in results]
    cloud_util = [r["cloud_utilization"] * 100 for r in results]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(labels, edge_util, marker="o", linewidth=2.5, label="Edge node utilization", color="#2ca02c")
    ax.plot(labels, cloud_util, marker="s", linewidth=2.5, label="Cloud utilization", color="#9467bd")
    ax.set_ylabel("Utilization (%)")
    ax.set_title("Edge and cloud utilization by workload")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()
    fig.tight_layout()
    path = OUTPUT_DIR / "utilization.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def plot_queue_and_throughput(results):
    labels = [r["name"] for r in results]
    backlog = [r["queue_backlog_ms"] for r in results]
    throughput = [r["throughput_per_sec"] for r in results]

    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    color = "#1f77b4"
    ax1.set_xlabel("Scenario")
    ax1.set_ylabel("Queue backlog (ms)", color=color)
    ax1.plot(labels, backlog, marker="o", color=color, linewidth=2.5, label="Queue backlog")
    ax1.tick_params(axis="y", labelcolor=color)
    ax1.grid(True, linestyle="--", alpha=0.3)

    ax2 = ax1.twinx()
    color2 = "#d62728"
    ax2.set_ylabel("Throughput (tasks/s)", color=color2)
    ax2.plot(labels, throughput, marker="s", color=color2, linewidth=2.5, label="Throughput")
    ax2.tick_params(axis="y", labelcolor=color2)

    fig.tight_layout()
    path = OUTPUT_DIR / "queue_throughput.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def main():
    results = [simulate_scenario(s) for s in SCENARIOS]
    save_summary_json(results)
    plot_latency_comparison(results)
    plot_processing_share(results)
    plot_utilization(results)
    plot_queue_and_throughput(results)

    print("Edge-first real-time simulation completed.")
    print(f"Summary JSON: {OUTPUT_DIR / 'edge_summary.json'}")
    print(f"Latency graph: {OUTPUT_DIR / 'latency_comparison.png'}")
    print(f"Processing share graph: {OUTPUT_DIR / 'processing_share.png'}")
    print(f"Utilization graph: {OUTPUT_DIR / 'utilization.png'}")
    print(f"Queue graph: {OUTPUT_DIR / 'queue_throughput.png'}")

    for r in results:
        print(
            f"{r['name']}: {r['devices']} devices, edge_share={r['edge_processing_share']*100:.0f}%, "
            f"weighted_latency={r['weighted_latency_ms']} ms, success_rate={r['success_rate_percent']}%"
        )


if __name__ == "__main__":
    main()
