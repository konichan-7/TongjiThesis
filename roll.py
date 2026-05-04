from __future__ import annotations

from pathlib import Path
from typing import Any

from standup import plot_scientific_csv


# =========================
# User configuration area
# =========================

CSV_PATH = Path(__file__).with_name("roll.csv")
OUTPUT_DIR = Path(__file__).with_name("plots")
OUTPUT_BASENAME = "roll_scientific"

# Data row index after the CSV header. For example, 0 means the first data row,
# 100 means plotting starts from the 101st data row.
START_ROW = 2000
# Exclusive data row index after the CSV header. None means plotting to the end.
# For example, START_ROW = 340 and END_ROW = 1000 plots data rows [340, 1000).
END_ROW: int | None = None

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
        "title": "Roll Compensation",
        "ylabel": "angle [rad]",
        "columns": ["Channel 3"],
        "labels": [ r"$roll$"],
        "colors": [ "#FF3300"],
    },
    {
        "title": "Roll Compensation",
        "ylabel": "pos [m]",
        "columns": ["Channel 4"],
        "labels": [r"$\Delta hight$"],
        "colors": ["#00AA00"],
    },
    {
        "title": "Roll Compensation",
        "ylabel": "pos [m]",
        "columns": ["Channel 5", "Channel 7"],
        "labels": [r"$l_l \ set$", r"$l_l \ fdb$"],
        "colors": ["#FF9900", "#00CCFF"],
    },
    {
        "title": "Roll Compensation",
        "ylabel": "pos [m]",
        "columns": [ "Channel 6", "Channel 8"],
        "labels": [ r"$l_r \ set$", r"$l_r \ fdb$"],
        "colors": [ "#000000", "#FF00AA"],
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
