
import csv
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path.home() / "Projects" / "Radio-Telescope"
data = root / "instruments" / "data"
graphs = root / "graphs"

solar_file = data / "solar_pointing_live_2026-10-30.csv"
rain_file = data / "new_baseline_rain_2026-10-30_1410.csv"
temperature_file = data / "temperature_log.csv"

graphs.mkdir(parents=True, exist_ok=True)

def load_recording(path):
    records = []
    spectra = {}

    with path.open(newline="") as file:
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

                powers = np.array(
                    [float(value) for value in row[6:] if value.strip()],
                    dtype=float
                )

                if not len(powers):
                    continue

                frequencies = start_hz + np.arange(len(powers)) * step_hz

                for frequency, power in zip(frequencies, powers):
                    records.append((timestamp, frequency, power))
                    spectra.setdefault(frequency, []).append(power)

            except ValueError:
                continue

    if not records:
        raise ValueError(f"No valid measurements found in {path}")

    frame = pd.DataFrame(
        records,
        columns=["timestamp", "frequency", "power"]
    )

    frame = frame.sort_values(["timestamp", "frequency"])

    power_series = frame.groupby("timestamp")["power"].mean()
    spectrum = frame.groupby("frequency")["power"].mean()

    return power_series, spectrum

solar_power, solar_spectrum = load_recording(solar_file)
rain_power, rain_spectrum = load_recording(rain_file)

def elapsed_minutes(series):
    return (
        series.index - series.index[0]
    ).total_seconds() / 60

def smooth(series):
    return series.rolling(
        "60s",
        center=True,
        min_periods=1
    ).median()

solar_smooth = smooth(solar_power)
rain_smooth = smooth(rain_power)

solar_relative = solar_smooth - solar_smooth.iloc[:30].median()
rain_relative = rain_smooth - rain_smooth.iloc[:30].median()

fig, axes = plt.subplots(3, 1, figsize=(15, 13))

axes[0].plot(
    elapsed_minutes(solar_power),
    solar_power.values,
    alpha=0.15,
    linewidth=0.5,
    color="royalblue"
)

axes[0].plot(
    elapsed_minutes(rain_power),
    rain_power.values,
    alpha=0.15,
    linewidth=0.5,
    color="darkorange"
)

axes[0].plot(
    elapsed_minutes(solar_smooth),
    solar_smooth.values,
    linewidth=2,
    color="royalblue",
    label="Candidate solar observation"
)

axes[0].plot(
    elapsed_minutes(rain_smooth),
    rain_smooth.values,
    linewidth=2,
    color="darkorange",
    label="Rain observation"
)

axes[0].set_title("Reported Power Comparison")
axes[0].set_xlabel("Elapsed Time (minutes)")
axes[0].set_ylabel("Mean Reported Power (dB)")
axes[0].legend()
axes[0].grid(alpha=0.25)

axes[1].plot(
    elapsed_minutes(solar_relative),
    solar_relative.values,
    linewidth=2,
    label="Candidate solar observation"
)

axes[1].plot(
    elapsed_minutes(rain_relative),
    rain_relative.values,
    linewidth=2,
    label="Rain observation"
)

axes[1].axhline(0, linestyle="--", color="gray")
axes[1].set_title("Baseline-Relative Power Comparison")
axes[1].set_xlabel("Elapsed Time (minutes)")
axes[1].set_ylabel("Relative Change (dB)")
axes[1].legend()
axes[1].grid(alpha=0.25)

axes[2].plot(
    solar_spectrum.index.to_numpy() / 1e6,
    solar_spectrum.values,
    linewidth=1.5,
    label="Candidate solar observation"
)

axes[2].plot(
    rain_spectrum.index.to_numpy() / 1e6,
    rain_spectrum.values,
    linewidth=1.5,
    label="Rain observation"
)

axes[2].set_title("Frequency Spectrum Comparison")
axes[2].set_xlabel("Frequency (MHz)")
axes[2].set_ylabel("Mean Reported Power (dB)")
axes[2].set_xlim(1200, 1210)
axes[2].legend()
axes[2].grid(alpha=0.25)

fig.tight_layout()

output = graphs / "solar_rain_power_comparison.png"
fig.savefig(output, dpi=250, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {output}")

if temperature_file.exists():
    temperatures = pd.read_csv(temperature_file)
    temperatures["timestamp"] = pd.to_datetime(
        temperatures["timestamp"]
    )

    temperatures = temperatures.sort_values("timestamp")

    combined = pd.concat(
        [solar_power.rename("power"), rain_power.rename("power")]
    ).sort_index()

    power_frame = combined.reset_index()
    power_frame.columns = ["timestamp", "power"]

    merged = pd.merge_asof(
        power_frame.sort_values("timestamp"),
        temperatures.sort_values("timestamp"),
        on="timestamp",
        direction="nearest",
        tolerance=pd.Timedelta("5min")
    )

    columns = [
        column
        for column in ["ambient_c", "lnb_c"]
        if column in merged.columns
    ]

    if columns:
        fig, axes = plt.subplots(
            len(columns),
            2,
            figsize=(14, 5 * len(columns)),
            squeeze=False
        )

        for i, column in enumerate(columns):
            valid = merged.dropna(subset=[column, "power"])

            axes[i, 0].plot(
                valid["timestamp"],
                valid[column],
                label=column
            )

            axes[i, 0].set_title(f"{column} vs Time")
            axes[i, 0].set_ylabel("Temperature (°C)")
            axes[i, 0].grid(alpha=0.25)

            axes[i, 1].scatter(
                valid[column],
                valid["power"],
                s=10,
                alpha=0.35
            )

            axes[i, 1].set_title(f"{column} vs Reported Power")
            axes[i, 1].set_xlabel("Temperature (°C)")
            axes[i, 1].set_ylabel("Reported Power (dB)")
            axes[i, 1].grid(alpha=0.25)

        fig.tight_layout()

        output_temperature = graphs / "temperature_power_comparison.png"
        fig.savefig(
            output_temperature,
            dpi=250,
            bbox_inches="tight"
        )

        plt.close(fig)
        print(f"Saved: {output_temperature}")

else:
    print("No temperature log found. Temperature comparison skipped.")
