#!/usr/bin/env python3
"""Plot supplied summary CSVs. This script does not run channel simulations."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
METHODS = [
    ("Algorithm1", "SNR-oriented AO", "#2C6CA2", "o", "-"),
    ("Predetermined", "Center", "#C78C27", "s", "--"),
    ("DistanceProduct", "Distance product", "#8B559E", "^", "-."),
    ("RandomPlacement", "Random", "#397B5A", "D", ":"),
    ("DetectionSelection", "Detection-aware selection", "#18334A", "^", "-"),
]


def load_rows(path: Path, method_key: str, mean_key: str):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        needed = {method_key, "rhoDb", mean_key, "ci95Lower", "ci95Upper"}
        if not needed.issubset(reader.fieldnames or []):
            raise ValueError(f"Missing columns in {path.name}: {needed - set(reader.fieldnames or [])}")
        rows = list(reader)
    groups = {}
    for row in rows:
        method = row[method_key]
        point = tuple(float(row[k]) for k in ("rhoDb", mean_key, "ci95Lower", "ci95Upper"))
        if not np.all(np.isfinite(point)):
            raise ValueError(f"Nonfinite summary value in {path.name}")
        snr, mean, lower, upper = point
        if not 0 <= mean <= 1 or lower > mean or mean > upper:
            raise ValueError(f"Invalid mean/interval ordering in {path.name}")
        groups.setdefault(method, []).append(point)
    for method, points in groups.items():
        points.sort(key=lambda p: p[0])
        if len({p[0] for p in points}) != len(points):
            raise ValueError(f"Duplicate SNR for {method} in {path.name}")
    return groups


def make_plot(groups, output: Path, stem: str, ymin: float):
    fig, ax = plt.subplots(figsize=(7.2, 4.8), constrained_layout=True)
    for key, label, color, marker, linestyle in METHODS:
        if key not in groups:
            continue
        a = np.asarray(groups[key], dtype=float)
        x, mean, lower, upper = a.T
        ax.plot(x, mean, label=label, color=color, marker=marker,
                linestyle=linestyle, linewidth=1.7, markersize=4.2,
                markerfacecolor="white", markeredgewidth=1.0)
        # The log axis cannot display nonpositive CI endpoints. Only the
        # displayed band is clipped to the visible probability range.
        # All original endpoints remain unchanged in the source CSVs.
        displayed_lower = np.clip(lower, ymin, 1.0)
        displayed_upper = np.clip(upper, ymin, 1.0)
        ax.fill_between(x, displayed_lower, displayed_upper,
                        color=color, alpha=0.12, linewidth=0)
    ax.set_yscale("log")
    ax.set_xlim(0, 50)
    ax.set_ylim(ymin, 1)
    ax.set_xticks(np.arange(0, 51, 10))
    ax.set_xlabel(r"Transmit SNR, $\rho_{\mathrm{tx}}$ (dB)")
    ax.set_ylabel(r"Mean index-error probability, $P_{\mathrm{I}}$")
    ax.grid(True, which="major", color="#DAE2E8", linewidth=0.65)
    ax.tick_params(direction="in", top=True, right=True)
    ax.legend(loc="lower left", fontsize=9, framealpha=0.95)
    for suffix in ("pdf", "png"):
        fig.savefig(output / f"{stem}.{suffix}", dpi=220)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "figures")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "pdf.fonttype": 42, "ps.fonttype": 42})
    independent = load_rows(ROOT / "data/detection_summary.csv", "scheme", "meanPe")
    selection = load_rows(ROOT / "data/detection_selection_summary.csv", "method", "meanError")
    make_plot(independent, args.output_dir, "independent_panel_detection", 1e-3)
    make_plot(selection, args.output_dir, "shared_ray_configuration_selection", 1e-7)
    print(f"Saved two PDF/PNG figure pairs to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
