
import csv
from pathlib import Path
from datetime import datetime

import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

source = Path.home() / "Projects" / "Radio-Telescope" / "instruments" / "data" / "observation_24h_2026-10-28_1337.csv"
output = Path.home() / "Projects" / "Radio-Telescope" / "graphs" / "solar_pointing_attempt_2_2026-10-29.png"

start = datetime(2026, 10, 29, 11, 0)
end = datetime(2026, 10, 29, 13, 0)
solar_noon = datetime(2026, 10, 29, 11, 28)

records = {}

with source.open(newline="") as file:
    reader = csv.reader(file)

    for row in reader:
        if len(row) < 7:
            continue

        try:
            timestamp = datetime.strptime(
                row[0].strip() + " " + row[1].strip(),
                "%Y-%m-%d %H:%M:%S"
            )

            if not start <= timestamp <= end:
                continue

            powers = [
                float(value)
                for value in row[6:]
                if value.strip()
            ]

            if not powers:
                continue

            records.setdefault(timestamp, []).extend(powers)

        except ValueError:
            continue

if not records:
    raise ValueError("No observations found in the selected interval.")

timestamps = sorted(records)
mean_powers = [
    sum(records[timestamp]) / len(records[timestamp])
    for timestamp in timestamps
]

series = pd.Series(
    mean_powers,
    index=pd.DatetimeIndex(timestamps)
)

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

fig, ax = plt.subplots(figsize=(15, 6))

ax.plot(
    series.index,
    series.values,
    color="steelblue",
    linewidth=0.5,
    alpha=0.25,
    label="Raw mean reported power"
)

ax.plot(
    median_60s.index,
    median_60s.values,
    color="royalblue",
    linewidth=1.1,
    label="60-second rolling median"
)

ax.plot(
    median_5min.index,
    median_5min.values,
    color="darkred",
    linewidth=2,
    label="5-minute rolling median"
)

ax.axvline(
    solar_noon,
    color="darkorange",
    linestyle="--",
    linewidth=1.5,
    label="Approximate solar noon (11:28)"
)

ax.set_title(
    "October 29, 2026 — Second Solar Pointing Attempt\n"
    "11:00 AM – 1:00 PM (PHT)",
    fontsize=14
)

ax.set_xlabel("Local Time (PHT)")
ax.set_ylabel("Mean Reported Power (dB)")
ax.set_xlim(start, end)

ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

ax.grid(True, alpha=0.25)
ax.legend()

fig.tight_layout()

output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output, dpi=250, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {output}")
print(f"Measurements: {len(series)}")
print(f"First timestamp: {series.index[0]}")
print(f"Last timestamp: {series.index[-1]}")
