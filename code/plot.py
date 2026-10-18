
import csv
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

source = Path.home() / "Projects" / "Radio-Telescope" / "instruments" / "data" / "observation_2026_10_18_0900.csv"

output = Path.home() / "Projects" / "Radio-Telescope" / "graphs" / "observation_2026_10_18_0900_spectrum.png"

output.parent.mkdir(parents=True, exist_ok=True)

frequencies = []
powers = []
first_time = None

with open(source, newline="") as file:
    reader = csv.reader(file)

    for row in reader:
        time = row[1].strip()

        if first_time is None:
            first_time = time

        if time != first_time:
            break

        start_hz = float(row[2])
        step_hz = float(row[4])

        power_values = row[6:-1]

        for i, value in enumerate(power_values):
            frequency_hz = start_hz + (i + 0.5) * step_hz
            frequency_mhz = frequency_hz / 1_000_000
            power_db = float(value)

            frequencies.append(frequency_mhz)
            powers.append(power_db)

plt.figure(figsize=(10, 6))

plt.plot(frequencies, powers)

plt.xlabel("Frequency (MHz)")
plt.ylabel("Reported Relative Power (dB)")
plt.title(f"Morning RF Spectrum - {first_time}")
plt.grid(True)

plt.tight_layout()
plt.savefig(output, dpi=180)
plt.close()

print(f"Plotted {len(frequencies)} frequency bins")
print(f"Saved graph to: {output}")
