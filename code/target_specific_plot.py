
import csv
from pathlib import Path
from datetime import datetime, time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

source = Path.home() / "Projects" / "Radio-Telescope" / "instruments" / "data" / "observation_24h_2026-10-28_1337.csv"
output = Path.home() / "Projects" / "Radio-Telescope" / "graphs" / "afternoon_power_comparison_2026-10-28_29.png"

start_time = time(13, 37)
end_time = time(17, 30)

dates = ["2026-10-28", "2026-10-29"]
observations = {day: ([], []) for day in dates}

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

        day = timestamp.strftime("%Y-%m-%d")

        if day in observations and start_time <= timestamp.time() <= end_time:
            observations[day][0].append(timestamp)
            observations[day][1].append(average_power)

fig, axes = plt.subplots(2, 1, figsize=(14, 9), sharey=True)

for ax, day in zip(axes, dates):
    timestamps, powers = observations[day]

    ax.plot(timestamps, powers, linewidth=0.8)

    ax.set_title(f"Afternoon Power — {day}")
    ax.set_ylabel("Mean Reported Power (dB)")
    ax.grid(True, alpha=0.3)

    left = datetime.combine(datetime.strptime(day, "%Y-%m-%d").date(), start_time)
    right = datetime.combine(datetime.strptime(day, "%Y-%m-%d").date(), end_time)

    ax.set_xlim(left, right)
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_xlabel("Local Time (PHT)")

    if not timestamps:
        ax.text(
            0.5, 0.5,
            "No recorded data in this interval",
            ha="center",
            va="center",
            transform=ax.transAxes
        )

fig.suptitle("24-Hour Observation: Afternoon Power Comparison", fontsize=15)
fig.tight_layout()

output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output, dpi=200)
plt.close(fig)

print(f"Saved: {output}")

for day in dates:
    print(f"{day}: {len(observations[day][0])} measurements")
