
import csv
from pathlib import Path
from datetime import datetime
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

source = Path.home() / "Projects" / "Radio-Telescope" / "instruments" / "data" / "day2_batch1_2026-10-22_1100.csv"
output = Path.home() / "Projects" / "Radio-Telescope" / "graphs" / "day2_batch1_2026-10-22_1100_pvt.png"

output.parent.mkdir(parents=True, exist_ok=True)

times = []
powers = []

current_time = None
current_all_powers = []

with open(source, newline="") as file:
    reader = csv.reader(file)

    for row in reader:
        if len(row) < 39:
            continue

        time_str = row[0].strip() + " " + row[1].strip()

        row_powers = [float(value) for value in row[6:38]]

        if current_time is None:
            current_time = time_str

        if time_str != current_time:
            average_power = sum(current_all_powers) / len(current_all_powers)
            time_obj = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
            times.append(time_obj)
            powers.append(average_power)

            current_time = time_str
            current_all_powers = []

        current_all_powers.extend(row_powers)

if current_all_powers:
    average_power = sum(current_all_powers) / len(current_all_powers)
    time_obj = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
    times.append(time_obj)
    powers.append(average_power)

plt.figure(figsize=(12, 6))
plt.plot(times, powers, linewidth=1)

plt.xlabel("Time")
plt.ylabel("Average Reported Power (dB)")
plt.title("October 22, 2026 - 11:00 AM Day Observation")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))

plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output, dpi=180)
plt.close()

print(f"Saved graph to: {output}")
