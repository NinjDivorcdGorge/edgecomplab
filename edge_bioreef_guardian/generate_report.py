#!/usr/bin/env python3
"""Create the Experiment 11 submission report for Edge BioReef Guardian."""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
REPORT = ROOT.parent / "5023146_SamuelR.pdf"
NAVY = "#153243"
CORAL = "#e07a5f"
GOLD = "#f2cc8f"
INK = "#24323d"
MUTED = "#5f6b72"


def load_results() -> list[dict]:
    return json.loads((OUTPUT / "reef_guardian_summary.json").read_text(encoding="utf-8"))


def new_page(title: str, subtitle: str | None = None):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
    fig.text(0.08, 0.955, "EDGE BIOREEF GUARDIAN  /  EXPERIMENT 11", color=CORAL,
             fontsize=8, weight="bold")
    fig.text(0.08, 0.915, title, color=NAVY, fontsize=21, weight="bold")
    if subtitle:
        fig.text(0.08, 0.885, subtitle, color=MUTED, fontsize=10)
    fig.lines.append(plt.Line2D([0.08, 0.92], [0.865, 0.865], color=CORAL, linewidth=1.2))
    return fig


def footer(fig, page: int):
    fig.text(0.08, 0.035, "5023146_SamuelR  |  Edge Computing Laboratory", fontsize=7, color=MUTED)
    fig.text(0.92, 0.035, str(page), fontsize=7, color=MUTED, ha="right")


def paragraph(fig, x: float, y: float, text: str, width: int = 88, size: float = 10):
    lines = textwrap.wrap(text, width=width)
    fig.text(x, y, "\n".join(lines), va="top", fontsize=size, color=INK, linespacing=1.35)
    return y - 0.021 * len(lines) - 0.014


def bullet_list(fig, x: float, y: float, items: list[str], width: int = 82):
    for item in items:
        lines = textwrap.wrap(item, width=width - 4)
        fig.text(x, y, "•", fontsize=10, color=CORAL, va="top")
        fig.text(x + 0.018, y, "\n".join(lines), fontsize=9.5, color=INK,
                 va="top", linespacing=1.35)
        y -= 0.027 * len(lines) + 0.012
    return y


def section(fig, x: float, y: float, heading: str, body: str):
    fig.text(x, y, heading, fontsize=12, weight="bold", color=CORAL, va="top")
    return paragraph(fig, x, y - 0.027, body, width=86, size=9.5)


def cover(pdf: PdfPages, results: list[dict]):
    fig = plt.figure(figsize=(8.27, 11.69), facecolor=NAVY)
    fig.text(0.08, 0.84, "EXPERIMENT 11", color=GOLD, fontsize=12, weight="bold")
    fig.text(0.08, 0.75, "Edge BioReef\nGuardian", color="white", fontsize=35,
             weight="bold", linespacing=1.05)
    fig.text(0.08, 0.60, "Latency-aware acoustic evidence fusion for\ncoral reef monitoring",
             color="#dce8eb", fontsize=15, linespacing=1.45)
    fig.add_artist(plt.Rectangle((0.08, 0.49), 0.84, 0.004, transform=fig.transFigure, color=CORAL))
    fig.text(0.08, 0.42, "Submitted by", color="#a9c0c7", fontsize=9)
    fig.text(0.08, 0.385, "5023146 / Samuel R", color="white", fontsize=18, weight="bold")
    fig.text(0.08, 0.29, "A Python simulation of submerged hydrophones,\nedge gateways, evidence reporting, and cloud analysis.",
             color="#dce8eb", fontsize=11, linespacing=1.5)
    total_raw = sum(r["raw_uplink_mb_per_min"] for r in results)
    total_reported = sum(r["reported_uplink_mb_per_min"] for r in results)
    fig.text(0.08, 0.12, f"{len(results)} operating scenarios   |   {total_raw:.2f} MB/min raw stream\n"
                          f"{total_reported:.4f} MB/min reported evidence   |   50–55 ms local alerting",
             color=GOLD, fontsize=10, linespacing=1.6)
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def overview(pdf: PdfPages):
    fig = new_page("Aim, objectives, and requirements", "A focused edge-computing experiment for reef acoustics")
    y = 0.82
    y = section(fig, 0.08, y, "Aim", "To implement and evaluate an edge-first acoustic monitoring system that classifies hydrophone frames locally, fuses corroborating detections at nearby gateways, raises rapid reef alerts, and forwards only compact evidence to the cloud.")
    y -= 0.015
    fig.text(0.08, y, "Objectives", fontsize=12, weight="bold", color=CORAL, va="top")
    y -= 0.03
    y = bullet_list(fig, 0.08, y, [
        "Simulate four reef soundscape conditions: Dawn Chorus, Tourist Boats, Spawning Pulse, and Storm Front.",
        "Model hydrophone frame rates, gateway capacity, environmental noise, event rates, and cloud round-trip delay.",
        "Classify every frame at the edge and fuse candidate clips into confirmed alerts with recall and precision metrics.",
        "Compare local alert latency with a cloud-only path and measure the reduction in upstream bandwidth.",
        "Quantify gateway utilization and radio energy used to report evidence instead of raw audio.",
        "Visualize traffic reduction, alert response, fusion quality, local load, and reporting energy.",
    ])
    fig.text(0.08, y - 0.01, "Requirements", fontsize=12, weight="bold", color=CORAL, va="top")
    y -= 0.045
    req = [["Hardware", "Computer or laptop; minimum 4 GB RAM; no additional edge hardware required."],
           ["Software", "Python 3.x; VS Code, Notepad, or another Python editor; terminal or command prompt."],
           ["Libraries", "matplotlib >= 3.8 and numpy >= 1.26. Python built-ins: json and pathlib."],
           ["Execution", "python3 run_simulation.py from the edge_bioreef_guardian directory."]]
    table = fig.add_axes([0.08, y - 0.18, 0.84, 0.18])
    table.axis("off")
    cells = table.table(cellText=req, colLabels=["Category", "Specification"], loc="center",
                        cellLoc="left", colWidths=[0.18, 0.82])
    cells.auto_set_font_size(False)
    cells.set_fontsize(8.5)
    cells.scale(1, 1.65)
    for (row, col), cell in cells.get_celld().items():
        cell.set_edgecolor("#d6dfe2")
        cell.set_facecolor(NAVY if row == 0 else "#f5f8f8")
        cell.get_text().set_color("white" if row == 0 else INK)
        if row == 0:
            cell.get_text().set_weight("bold")
    footer(fig, 2)
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def theory_method(pdf: PdfPages):
    fig = new_page("Theory and implementation", "Why local acoustic triage is useful")
    y = 0.82
    y = section(fig, 0.08, y, "Theory", "Edge computing places computation close to the data source. In this experiment, submerged hydrophones continuously observe reef soundscapes. Local gateways classify frames and combine nearby detections, so urgent alerts do not wait for a distant cloud round trip. The cloud remains useful for long-term ecological analysis, but only short evidence clips and event metadata cross the uplink.")
    y -= 0.01
    y = section(fig, 0.08, y, "Simulation method", "For each one-minute scenario, the program calculates the raw audio volume, gateway utilization, candidate clips caused by noise, confirmed events after fusion, false alerts, local alert latency, cloud-only latency, bandwidth reduction, detection recall, alert precision, and radio energy. The same formula is applied consistently across all four environments.")
    y -= 0.01
    fig.text(0.08, y, "Important code snippets", fontsize=12, weight="bold", color=CORAL, va="top")
    snippets = [
        ("A. Local classification and fusion", "frames = sound_frames_per_sec * 60\ncandidate_clips = frames * 0.000012 * noise_factor\nconfirmed_events = true_events * (0.985 - 0.025 * noise_factor)"),
        ("B. Edge versus cloud latency", "edge_latency = 24 + 36 * edge_utilization + 3 * noise_factor\ncloud_only_latency = cloud_rtt_ms + 42 + (candidate_clips / frames) * 1000\nalert_latency = edge_latency + 18"),
        ("C. Evidence-only reporting", "cloud_frames = candidate_clips * 0.16 + fused_alerts\ncloud_bytes = cloud_frames * EVENT_PACKET_BYTES\nbandwidth_reduction = 100 * (1 - cloud_bytes / raw_bytes)"),
    ]
    y -= 0.04
    for heading, code in snippets:
        fig.text(0.08, y, heading, fontsize=9, weight="bold", color=NAVY, va="top")
        fig.text(0.08, y - 0.023, code, fontsize=8, family="monospace", color=INK,
                 va="top", linespacing=1.35,
                 bbox={"boxstyle": "round,pad=0.45", "facecolor": "#f2f6f6", "edgecolor": "#d6dfe2"})
        y -= 0.105
    footer(fig, 3)
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def results_page(pdf: PdfPages, results: list[dict]):
    fig = new_page("Results", "One minute of simulated operation per reef scenario")
    headers = ["Scenario", "Hydrophones", "Raw MB/min", "Evidence MB/min", "Saved", "Edge alert", "Cloud-only", "Recall", "Precision"]
    rows = [[r["name"], r["hydrophones"], f'{r["raw_uplink_mb_per_min"]:.2f}',
             f'{r["reported_uplink_mb_per_min"]:.4f}', f'{r["bandwidth_reduction_percent"]:.3f}%',
             f'{r["edge_alert_latency_ms"]:.2f} ms', f'{r["cloud_only_latency_ms"]:.2f} ms',
             f'{r["detection_recall_percent"]:.2f}%', f'{r["alert_precision_percent"]:.2f}%'] for r in results]
    table = fig.add_axes([0.055, 0.60, 0.89, 0.22])
    table.axis("off")
    cells = table.table(cellText=rows, colLabels=headers, loc="center", cellLoc="center",
                        colWidths=[0.16, 0.10, 0.11, 0.13, 0.11, 0.11, 0.12, 0.08, 0.08])
    cells.auto_set_font_size(False)
    cells.set_fontsize(7.2)
    cells.scale(1, 2.0)
    for (row, col), cell in cells.get_celld().items():
        cell.set_edgecolor("#d6dfe2")
        cell.set_facecolor(NAVY if row == 0 else ("#f5f8f8" if row % 2 else "#ffffff"))
        cell.get_text().set_color("white" if row == 0 else INK)
        if row == 0:
            cell.get_text().set_weight("bold")
    fig.text(0.08, 0.54, "Key findings", fontsize=12, weight="bold", color=CORAL)
    bullet_list(fig, 0.08, 0.505, [
        "The system classifies 100% of incoming frames at the edge in every scenario; only compact evidence is reported upstream.",
        "Bandwidth reduction is effectively 99.997–99.998%, from 6.91–64.51 MB/min of raw audio to 0.0002–0.0013 MB/min of evidence.",
        "Local alerts remain between 50.00 and 54.90 ms, well below the 150 ms response target.",
        "Cloud-only alert latency grows from 227.01 ms at dawn to 472.03 ms during the storm, showing why urgent decisions stay local.",
        "Storm noise lowers precision to 78.13% and recall to 93.00%, exposing the principal quality trade-off in the model.",
    ], width=84)
    footer(fig, 4)
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def graph_page(pdf: PdfPages, filename: str, title: str, interpretation: str, page: int):
    fig = new_page(title, "Generated directly from run_simulation.py")
    image = mpimg.imread(OUTPUT / filename)
    ax = fig.add_axes([0.08, 0.34, 0.84, 0.49])
    ax.imshow(image)
    ax.axis("off")
    fig.text(0.08, 0.26, "Interpretation", fontsize=12, weight="bold", color=CORAL)
    paragraph(fig, 0.08, 0.225, interpretation, width=88, size=10)
    footer(fig, page)
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def conclusion(pdf: PdfPages):
    fig = new_page("Result and conclusion", "Assessment of the Edge BioReef Guardian design")
    y = 0.82
    y = section(fig, 0.08, y, "Result", "The Edge BioReef Guardian successfully keeps the urgent acoustic monitoring loop local. Across Dawn Chorus, Tourist Boats, Spawning Pulse, and Storm Front, all hydrophone frames are classified at the edge while only tiny evidence reports reach the cloud. The design reduces upstream traffic by approximately 99.997–99.998% and delivers alerts in about 50–55 ms. Cloud-only response is substantially slower, reaching 472.03 ms in the storm scenario.")
    y -= 0.01
    y = section(fig, 0.08, y, "Conclusion", "The experiment demonstrates that distributed acoustic evidence fusion is a strong edge-computing use case. Local processing protects response time and dramatically reduces communication cost. Fusion maintains high recall and precision in ordinary conditions, while the storm case shows that environmental noise remains a meaningful limitation. A practical next step would be adaptive thresholds or a noise-aware fusion model for severe weather.")
    y -= 0.02
    fig.text(0.08, y, "Final assessment", fontsize=12, weight="bold", color=CORAL)
    y -= 0.04
    metrics = [("Raw traffic retained locally", "99.997–99.998%"), ("Fastest local alert", "50.00 ms"),
               ("Slowest local alert", "54.90 ms"), ("Worst precision under noise", "78.13%"),
               ("Worst recall under noise", "93.00%")]
    for label, value in metrics:
        fig.text(0.10, y, label, fontsize=10, color=INK)
        fig.text(0.87, y, value, fontsize=10, color=NAVY, weight="bold", ha="right")
        fig.lines.append(plt.Line2D([0.10, 0.87], [y - 0.012, y - 0.012], color="#d6dfe2", linewidth=0.7))
        y -= 0.045
    fig.text(0.08, 0.12, "Source files: edge_bioreef_guardian/run_simulation.py, output/reef_guardian_summary.json, and generated PNG figures.", fontsize=8, color=MUTED)
    footer(fig, 8)
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    results = load_results()
    with PdfPages(REPORT) as pdf:
        cover(pdf, results)
        overview(pdf)
        theory_method(pdf)
        results_page(pdf, results)
        graph_page(pdf, "bandwidth_reduction.png", "Graph 1: bandwidth reduction", "The raw hydrophone stream increases with the number of sensors and sound frames, reaching 64.51 MB/min during the storm. The evidence stream remains almost invisible by comparison because local gateways forward only candidate clips and fused alert metadata.", 5)
        graph_page(pdf, "latency_and_quality.png", "Graph 2: alert latency and fusion quality", "Local alerting remains below the 150 ms target in all four scenarios. The cloud-only path is slower because it includes the scenario-specific round trip. Recall stays above 93%, while storm noise causes the largest precision decline.", 6)
        graph_page(pdf, "load_and_energy.png", "Graph 3: local load and reporting energy", "Gateway utilization is highest at Dawn Chorus because its scenario capacity is relatively smaller, while radio energy stays extremely low because the gateway reports evidence rather than raw audio. The storm has the largest local processing energy due to its frame volume.", 7)
        conclusion(pdf)
    print(f"Created {REPORT}")


if __name__ == "__main__":
    main()