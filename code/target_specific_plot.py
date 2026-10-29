
import csv
from pathlib import Path
from datetime import datetime

import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

source = Path.home() / "Projects" / "Radio-Telescope" / "instruments" / "data" / "observation_24h_2026-10-28_1337.csv"
output = Path.home() / "Projects" / "Radio-Telescope" / "graphs" / "afternoon_power_transitions_clean.png"

periods = [
    (
        "October 28 — Increasing Power",
        datetime(2026, 10, 28, 13, 37),
        datetime(2026, 10, 28, 16, 0)
    ),
    (
        "October 29 — Decreasing Power",
        datetime(2026, 10, 29, 10, 0),
        datetime(2026, 10, 29, 13, 37)
    )
]

observations = [([], []) for _ in periods]

with source.open(newline="") as file:
    reader = csv.reader(file)

    for row in reader:
        if len(row) < 7:
            continue

        try:
            timestamp = datetime.strptime(
                row[0] + " " + row[1],
                "%Y-%m-%d %H:%M:%S"
            )

            power_bins = [
                float(value)
                for value in row[6:]
                if value.strip()
            ]

            if not power_bins:
                continue

            average_power = sum(power_bins) / len(power_bins)

        except ValueError:
            continue

        for i, (_, start, end) in enumerate(periods):
            if start <= timestamp <= end:
                observations[i][0].append(timestamp)
                observations[i][1].append(average_power)

fig, axes = plt.subplots(2, 1, figsize=(15, 9), sharey=True)

for ax, (title, start, end), (timestamps, powers) in zip(
    axes, periods, observations
):
    if timestamps:
        series = pd.Series(
            powers,
            index=pd.DatetimeIndex(timestamps)
        ).sort_index()

        series = series.groupby(level=0).mean()

        median_60s = series.rolling(
            "60s",
            center=True,
            min_periods=1
        ).median()

        median_5min = series.rolling(
            "5min",
            center=True,
            min_periods=1
        ).median()

        ax.plot(
            series.index,
            series.values,
            color="steelblue",
            linewidth=0.4,
            alpha=0.18,
            label="Raw reported power"
        )

        ax.plot(
            median_60s.index,
            median_60s.values,
            color="royalblue",
            linewidth=1.1,
            alpha=0.75,
            label="60-second rolling median"
        )

        ax.plot(
            median_5min.index,
            median_5min.values,
            color="darkred",
            linewidth=2.2,
            label="5-minute rolling median"
        )

    else:
        ax.text(
            0.5,
            0.5,
            "No recorded data",
            ha="center",
            va="center",
            transform=ax.transAxes
        )

    ax.set_title(title, fontsize=13)
    ax.set_ylabel("Mean Reported Power (dB)")
    ax.set_xlabel("Local Time (PHT)")
    ax.set_xlim(start, end)

    ax.xaxis.set_major_locator(
        mdates.MinuteLocator(interval=15)
    )
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%H:%M")
    )

    ax.grid(True, alpha=0.2)
    ax.legend(loc="upper right", fontsize=9)

fig.suptitle(
    "24-Hour Observation — Afternoon Power Transitions",
    fontsize=16,
    fontweight="bold"
)

fig.tight_layout(rect=[0, 0, 1, 0.96])

output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output, dpi=250, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {output}")

for (title, _, _), (timestamps, powers) in zip(periods, observations):
    print(f"{title}: {len(timestamps)} measurements")
