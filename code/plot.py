import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

source = Path.home() / "Projects" / "Radio-Telescope" / "instruments" / "data" / "first_lnb_scan.csv"
output = Path.home() / "Projects" / "Radio-Telescope" / "graphs" / "first_lnb_scan.png"

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
        end_hz = float(row[3])
        power_db = float(row[6])

        frequency_mhz = ((start_hz + end_hz) / 2) / 1000000 #Converting to MHz

        frequencies.append(frequency_mhz)
        powers.append(power_db)

plt.figure(figsize=(10, 6))

plt.plot(frequencies, powers)

plt.xlabel("Frequency (MHz)")
plt.ylabel("Power (dB)")
plt.title("First LNB Scan")
plt.grid(True)

plt.tight_layout()
plt.savefig(output)
plt.close()

print(f"Plotted {len(frequencies)} measurements")
print(f"Saved graph to {output}")







