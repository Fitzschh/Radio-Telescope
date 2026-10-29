import csv
from pathlib import Path
from datetime import datetime

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

source = Path.home() / "Projects" / "Radio-Telescope" / "instruments" / "data" / "observation_24h_2026-10-28_1337.csv"
output = Path.home() / "Projects" / "Radio-Telescope" / "graphs" / "transition_spectra_comparison.png"

windows = [
    {
        "title": "October 28, 2026 — Upward Transition",
        "before_label": "Before transition (14:45–15:05)",
        "after_label": "After transition (15:40–16:00)",
        "before_start": datetime(2026, 10, 28, 14, 45),
        "before_end": datetime(2026, 10, 28, 15, 5),
        "after_start": datetime(2026, 10, 28, 15, 40),
        "after_end": datetime(2026, 10, 28, 16, 0),
    },
    {
        "title": "October 29, 2026 — Downward Transition",
        "before_label": "Before transition (10:05–10:25)",
        "after_label": "After transition (13:05–13:25)",
        "before_start": datetime(2026, 10, 29, 10, 5),
        "before_end": datetime(2026, 10, 29, 10, 25),
        "after_start": datetime(2026, 10, 29, 13, 5),
        "after_end": datetime(2026, 10, 29, 13, 25),
    }
]

def parse_row(row):
    timestamp = datetime.strptime(row[0] + " " + row[1], "%Y-%m-%d %H:%M:%S")
    start_hz = float(row[2])
    stop_hz = float(row[3])
    step_hz = float(row[4])
    power_values = [float(x) for x in row[6:] if x.strip()]
    if not power_values:
        return None
    n = len(power_values)
    freqs_hz = start_hz + np.arange(n) * step_hz
    freqs_mhz = freqs_hz / 1e6
    powers = np.array(power_values, dtype=float)
    return timestamp, freqs_mhz, powers

def average_spectrum(rows):
    if not rows:
        return None, None
    reference_freqs = rows[0][0]
    stacked = np.vstack([item[1] for item in rows])
    mean_spectrum = stacked.mean(axis=0)
    return reference_freqs, mean_spectrum

collected = []
with source.open(newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) < 7:
            continue
        try:
            parsed = parse_row(row)
        except ValueError:
            continue
        if parsed is None:
            continue
        collected.append(parsed)

results = []

for window in windows:
    before_rows = []
    after_rows = []

    for timestamp, freqs_mhz, powers in collected:
        if window["before_start"] <= timestamp <= window["before_end"]:
            before_rows.append((freqs_mhz, powers))
        if window["after_start"] <= timestamp <= window["after_end"]:
            after_rows.append((freqs_mhz, powers))

    before_freqs, before_mean = average_spectrum(before_rows)
    after_freqs, after_mean = average_spectrum(after_rows)

    results.append({
        "title": window["title"],
        "before_label": window["before_label"],
        "after_label": window["after_label"],
        "before_freqs": before_freqs,
        "before_mean": before_mean,
        "after_freqs": after_freqs,
        "after_mean": after_mean,
        "before_count": len(before_rows),
        "after_count": len(after_rows)
    })

fig, axes = plt.subplots(4, 1, figsize=(15, 16), height_ratios=[3, 1.5, 3, 1.5])

for i, result in enumerate(results):
    ax_spec = axes[i * 2]
    ax_diff = axes[i * 2 + 1]

    before_freqs = result["before_freqs"]
    before_mean = result["before_mean"]
    after_freqs = result["after_freqs"]
    after_mean = result["after_mean"]

    if before_freqs is None or after_freqs is None:
        ax_spec.text(0.5, 0.5, "No data for selected window", ha="center", va="center", transform=ax_spec.transAxes)
        ax_diff.text(0.5, 0.5, "No data for selected window", ha="center", va="center", transform=ax_diff.transAxes)
        continue

    difference = after_mean - before_mean

    ax_spec.plot(before_freqs, before_mean, linewidth=2, label=f'{result["before_label"]} (n={result["before_count"]})')
    ax_spec.plot(after_freqs, after_mean, linewidth=2, label=f'{result["after_label"]} (n={result["after_count"]})')
    ax_spec.set_title(result["title"], fontsize=14)
    ax_spec.set_ylabel("Reported Power (dB)")
    ax_spec.grid(True, alpha=0.3)
    ax_spec.legend()

    ax_diff.plot(before_freqs, difference, linewidth=1.8)
    ax_diff.axhline(0, linestyle="--", linewidth=1)
    ax_diff.set_ylabel("After - Before (dB)")
    ax_diff.set_xlabel("RTL-SDR Frequency (MHz)")
    ax_diff.grid(True, alpha=0.3)

fig.suptitle("Baseline Transition Spectra Comparison", fontsize=18, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.97])

output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output, dpi=250, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {output}")
for result in results:
    print(result["title"])
    print(f'  {result["before_label"]}: {result["before_count"]} spectra')
    print(f'  {result["after_label"]}: {result["after_count"]} spectra')