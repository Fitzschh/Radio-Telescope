
import csv
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

source = Path.home() / "Projects" / "Radio-Telescope" / "instruments" / "data" / "new_day_batch2_2026-10-26_1540.csv"

output = Path.home() / "Projects" / "Radio-Telescope" / "graphs" / "oct26_spike_spectra.png"

output.parent.mkdir(parents=True, exist_ok=True)

target_times = ["16:01:58", "16:21:14", "15:51:44"]

spectra = {}

for target_time in target_times:
    frequencies = []
    powers = []

    with open(source, newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) < 39:
                continue

            time = row[1].strip()

            if time != target_time:
                continue

            start_hz = float(row[2])
            step_hz = float(row[4])

            power_values = row[6:38]

            for i, value in enumerate(power_values):
                frequency_hz = start_hz + (i + 0.5) * step_hz
                frequency_mhz = frequency_hz / 1_000_000
                power_db = float(value)

                frequencies.append(frequency_mhz)
                powers.append(power_db)

    spectra[target_time] = (frequencies, powers)

plt.figure(figsize=(12, 6))

plt.plot(
    spectra["16:01:58"][0],
    spectra["16:01:58"][1],
    label="Typical baseline: 16:01:58"
)

plt.plot(
    spectra["16:21:14"][0],
    spectra["16:21:14"][1],
    label="Spike: 16:21:14"
)

plt.plot(
    spectra["15:51:44"][0],
    spectra["15:51:44"][1],
    label="Spike: 15:51:44"
)

plt.axvline(1205, linestyle="--", color="gray", alpha=0.7)

plt.xlabel("RTL-SDR Frequency (MHz)")
plt.ylabel("Reported Power (dB)")
plt.title("October 26, 2026 - Baseline vs Major Transient Spectra")

plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output, dpi=180)
plt.close()

print(f"Saved graph to: {output}")
