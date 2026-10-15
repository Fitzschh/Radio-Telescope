import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

source = Path.home() / "Projects" / "Radio-Telescope" / "data" / "first_lnb_scan.csv"
output = Path.home() / "Projects" / "Radio-Telescope" / "graphs" / "first_lnb_scan.png"

frequencies = []
powers = []
