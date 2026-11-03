import csv
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

root = Path.home() / "Projects" / "Radio-Telescope"
source = root / "instruments" / "data" / "sps_exp_attempt_2026-10-30.csv"
output = root / "graphs" / "sps_exp_attempt_2026-10-30_heatmap.png"
title = "Candidate Solar Observation — October 30, 2026"

records = []

with source.open(newline="") as file:
    for row in csv.reader(file):
        if len(row) < 7:
            continue

        try:
            timestamp = datetime.strptime(
                row[0].strip() + " " + row[1].strip(),
                "%Y-%m-%d %H:%M:%S"
            )

            start_hz = float(row[2])
            step_hz = float(row[4])

            powers = [
                float(value)
                for value in row[6:]
                if value.strip()
            ]

            for i, power in enumerate(powers):
                frequency = start_hz + i * step_hz
                records.append((timestamp, frequency, power))

        except ValueError:
            continue

if not records:
    raise ValueError(f"No valid measurements found in {source}")

frame = pd.DataFrame(records, columns=["timestamp", "frequency", "power"])

matrix = frame.pivot_table(
    index="frequency",
    columns="timestamp",
    values="power",
    aggfunc="mean"
)

matrix = matrix.sort_index().sort_index(axis=1)

times = matrix.columns.to_pydatetime()
frequencies = matrix.index.to_numpy() / 1e6
values = matrix.to_numpy()

vmin, vmax = np.percentile(values[np.isfinite(values)], [2, 98])

fig, ax = plt.subplots(figsize=(16, 7))

image = ax.imshow(
    values,
    aspect="auto",
    origin="lower",
    interpolation="nearest",
    extent=[
        mdates.date2num(times[0]),
        mdates.date2num(times[-1]),
        frequencies[0],
        frequencies[-1]
    ],
    cmap="inferno",
    vmin=vmin,
    vmax=vmax
)

ax.set_title(title, fontsize=15)
ax.set_xlabel("Local Time (PHT)")
ax.set_ylabel("Frequency (MHz)")
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

cbar = fig.colorbar(image, ax=ax)
cbar.set_label("Reported Relative Power (dB)")

fig.tight_layout()
output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output, dpi=250, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {output}")
print(f"Frequency bins: {len(frequencies)}")
print(f"Time intervals: {len(times)}")