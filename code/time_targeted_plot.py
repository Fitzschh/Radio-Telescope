
import csv
from pathlib import Path
from datetime import datetime
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

source = Path.home() / "Projects" / "Radio-Telescope" / "instruments" / "data" / "day4_batch1_2026-10-25_0830.csv"
output = Path.home() / "Projects" / "Radio-Telescope" / "graphs" / "oct25_spike_spectra.png"

output.parent.mkdir(parents=True, exist_ok=True)

spectra = {}
current_time = None
frequencies = []
powers = []

with open(source, newline="") as file:
    reader = csv.reader(file)

    for row in reader:
        if len(row) < 39:
            continue

        time_str = row[0].strip() + " " + row[1].strip()

        if current_time is not None and time_str != current_time:
            if len(powers) == 128:
                spectra[current_time] = (
                    frequencies,
                    powers,
                    sum(powers) / len(powers)
                )

            frequencies = []
            powers = []

        current_time = time_str

        start_hz = float(row[2])
        step_hz = float(row[4])

        for i, value in enumerate(row[6:38]):
            frequency_mhz = (start_hz + (i + 0.5) * step_hz) / 1_000_000
            frequencies.append(frequency_mhz)
            powers.append(float(value))

if len(powers) == 128:
    spectra[current_time] = (
        frequencies,
        powers,
        sum(powers) / len(powers)
    )

if not spectra:
    raise ValueError("No complete spectra found")

sorted_spectra = sorted(
    spectra.items(),
    key=lambda item: item[1][2],
    reverse=True
)

spikes = []
for timestamp, spectrum in sorted_spectra:
    moment = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    if all(
        abs((moment - previous).total_seconds()) > 30
        for previous in spikes
    ):
        spikes.append(moment)

    if len(spikes) == 3:
        break

baseline_time = sorted(
    spectra.items(),
    key=lambda item: abs(item[1][2] - sorted(
        item[2] for item in spectra.values()
    )[len(spectra) // 2])
)[0][0]

plt.figure(figsize=(12, 6))

baseline = spectra[baseline_time]

plt.plot(
    baseline[0],
    baseline[1],
    label=f"Baseline: {baseline_time[-8:]}",
    linewidth=1.5
)

for moment in spikes:
    timestamp = moment.strftime("%Y-%m-%d %H:%M:%S")
    frequencies, powers, average = spectra[timestamp]

    plt.plot(
        frequencies,
        powers,
        label=f"Spike: {moment.strftime('%H:%M:%S')} ({average:.2f} dB)",
        linewidth=1.2
    )

plt.axvline(1205, linestyle="--", color="gray", alpha=0.7)

plt.xlabel("RTL-SDR Frequency (MHz)")
plt.ylabel("Reported Power (dB)")
plt.title("October 25, 2026 - Baseline vs Major Transient Spectra")

plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output, dpi=180)
plt.close()

print(f"Baseline: {baseline_time}")

for moment in spikes:
    timestamp = moment.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Spike: {timestamp} | {spectra[timestamp][2]:.2f} dB")

print(f"Saved graph to: {output}")
