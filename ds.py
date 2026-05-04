from __future__ import annotations

from pathlib import Path
from typing import Any

from standup import plot_scientific_csv


# =========================
# User configuration area
# =========================

CSV_PATH = Path(__file__).with_name("ds.csv")
OUTPUT_DIR = Path(__file__).with_name("plots")
OUTPUT_BASENAME = "ds_scientific"

# Data row index after the CSV header. For example, 0 means the first data row,
# 100 means plotting starts from the 101st data row.
START_ROW = 3800
# Exclusive data row index after the CSV header. None means plotting to the end.
# For example, START_ROW = 340 and END_ROW = 1000 plots data rows [340, 1000).
END_ROW: int | None = 4300

# X axis setup:
# - X_COLUMN = None: build time from row index and SAMPLE_PERIOD, starting at 0.
# - X_COLUMN = "time" or X_COLUMN = 0: use a CSV column and shift it to start at 0.
X_COLUMN: str | int | None = None
SAMPLE_PERIOD = 0.01
X_OFFSET = 0.0
X_LABEL = "time [s]"

# Define subfigures here. Columns can be names from the CSV header or zero-based
# integer column indices. Labels can use matplotlib math text, such as r"$\theta_b$".
SUBFIGURES: list[dict[str, Any]] = [
    {
        "title": "Velocity Tracking",
        "ylabel": "vel [m/s]",
        "columns": ["Channel 3", "Channel 4"],
        "labels": [r"$\dot s_{set}$", r"$\dot s_{fdb}$"],
        "colors": ["#00AA00", "#CC00FF"],
    },
    {
        "title": "Velocity Tracking",
        "ylabel": "angle [rad]",
        "columns": ["z", "ds"],
        "labels": [r"$\theta_{ll}$", r"$\theta_{lr}$"],
        "colors": ["#0066FF", "#FF3300"],
    },
    {
        "title": "Velocity Tracking",
        "ylabel": "torque [N.m]",
        "columns": [ "Channel 6", "Channel 7"],
        "labels": [r"$T_{wl}$", r"$T_{wr}$"],
        "colors": [ "#00CCFF", "#000000"],
    },
]


if __name__ == "__main__":
    png, pdf = plot_scientific_csv(
        csv_path=CSV_PATH,
        subfigures=SUBFIGURES,
        start_row=START_ROW,
        end_row=END_ROW,
        x_column=X_COLUMN,
        sample_period=SAMPLE_PERIOD,
        x_offset=X_OFFSET,
        x_label=X_LABEL,
        output_dir=OUTPUT_DIR,
        output_basename=OUTPUT_BASENAME,
    )
    print(f"Saved: {png}")
    print(f"Saved: {pdf}")
