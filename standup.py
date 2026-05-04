from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Iterable

import matplotlib.pyplot as plt
import numpy as np


# =========================
# User configuration area
# =========================

CSV_PATH = Path(__file__).with_name("standup.csv")
OUTPUT_DIR = Path(__file__).with_name("plots")
OUTPUT_BASENAME = "standup_scientific"

# Data row index after the CSV header. For example, 0 means the first data row,
# 100 means plotting starts from the 101st data row.
START_ROW = 340
# Exclusive data row index after the CSV header. None means plotting to the end.
# For example, START_ROW = 340 and END_ROW = 1000 plots data rows [340, 1000).
END_ROW: int | None = 800

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
    # {
    #     "title": "Stand-up Position Signals",
    #     "ylabel": "angle [rad]",
    #     "columns": ["z"],
    #     "labels": [r"$\theta_b$"],
    #     "colors": ["#0066FF"],
    # },
    {
        "title": "Stand-up Balance",
        "ylabel": "vel [m/s]",
        "columns": ["ds"],
        "labels": [ r"$\dot{s}$"],
        "colors": [ "#FF3300"],
    },
    {
        "title": "Stand-up Balance",
        "ylabel": "angle [rad]",
        "columns": ["Channel 3", "Channel 4"],
        "labels": [r"$\theta_{ll}$", r"$\theta_{lr}$"],
        "colors": ["#00AA00", "#CC00FF"],
    },
    {
        "title": "Stand-up Balance",
        "ylabel": "torque [N.m]",
        "columns": ["Channel 5", "Channel 6"],
        "labels": [r"$T_{wl}$", r"$T_{wr}$"],
        "colors": ["#FF9900", "#00CCFF"],
    },
]


# =========================
# Plotting implementation
# =========================

DEFAULT_COLORS = [
    "#0066FF",
    "#FF3300",
    "#00AA00",
    "#CC00FF",
    "#FF9900",
    "#00CCFF",
    "#000000",
]


def load_numeric_csv(path: Path) -> tuple[list[str], np.ndarray]:
    """Load a header CSV whose remaining rows are numeric."""
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        try:
            headers = [cell.strip() for cell in next(reader)]
        except StopIteration as exc:
            raise ValueError(f"{path} is empty.") from exc

        rows: list[list[float]] = []
        for row_number, row in enumerate(reader, start=2):
            if not row or all(not cell.strip() for cell in row):
                continue
            if len(row) != len(headers):
                raise ValueError(
                    f"Row {row_number} has {len(row)} columns, expected {len(headers)}."
                )
            try:
                rows.append([float(cell) for cell in row])
            except ValueError as exc:
                raise ValueError(f"Row {row_number} contains non-numeric data.") from exc

    if not rows:
        raise ValueError(f"{path} has a header but no numeric data rows.")

    return headers, np.asarray(rows, dtype=float)


def resolve_column(column: str | int, headers: list[str]) -> int:
    """Resolve a CSV column by exact header name or zero-based index."""
    if isinstance(column, int):
        if 0 <= column < len(headers):
            return column
        raise IndexError(f"Column index {column} is out of range 0..{len(headers) - 1}.")

    if column in headers:
        return headers.index(column)

    available = ", ".join(headers)
    raise KeyError(f"Column '{column}' was not found. Available columns: {available}")


def configure_scientific_style() -> None:
    """Configure matplotlib to look close to journal-style stacked figures."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "mathtext.fontset": "dejavuserif",
            "axes.titlesize": 18,
            "axes.titleweight": "bold",
            "axes.labelsize": 16,
            "xtick.labelsize": 13,
            "ytick.labelsize": 13,
            "legend.fontsize": 10,
            "axes.linewidth": 0.8,
            "lines.linewidth": 1.2,
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
        }
    )


def build_x_axis(
    data: np.ndarray,
    headers: list[str],
    start_row: int,
    x_column: str | int | None,
    sample_period: float,
    x_offset: float,
) -> np.ndarray:
    if x_column is None:
        return np.arange(len(data), dtype=float) * sample_period + x_offset

    x_index = resolve_column(x_column, headers)
    x = data[:, x_index]
    return x - x[0] + x_offset


def plot_scientific_csv(
    csv_path: Path = CSV_PATH,
    subfigures: Iterable[dict[str, Any]] = SUBFIGURES,
    start_row: int = START_ROW,
    end_row: int | None = END_ROW,
    x_column: str | int | None = X_COLUMN,
    sample_period: float = SAMPLE_PERIOD,
    x_offset: float = X_OFFSET,
    x_label: str = X_LABEL,
    output_dir: Path = OUTPUT_DIR,
    output_basename: str = OUTPUT_BASENAME,
    show: bool = False,
) -> tuple[Path, Path]:
    headers, raw_data = load_numeric_csv(csv_path)

    if start_row < 0 or start_row >= len(raw_data):
        raise ValueError(f"START_ROW must be in 0..{len(raw_data) - 1}, got {start_row}.")
    if end_row is not None and (end_row <= start_row or end_row > len(raw_data)):
        raise ValueError(
            f"END_ROW must be None or in {start_row + 1}..{len(raw_data)}, got {end_row}."
        )

    data = raw_data[start_row:end_row, :]
    x = build_x_axis(data, headers, start_row, x_column, sample_period, x_offset)
    subfigure_list = list(subfigures)
    if not subfigure_list:
        raise ValueError("SUBFIGURES must contain at least one subfigure definition.")

    configure_scientific_style()

    fig_height = max(2.0 * len(subfigure_list), 2.8)
    fig, axes = plt.subplots(
        nrows=len(subfigure_list),
        ncols=1,
        figsize=(8.2, fig_height),
        sharex=True,
        constrained_layout=False,
    )
    axes_array = np.atleast_1d(axes)

    for ax, spec in zip(axes_array, subfigure_list):
        columns = spec.get("columns", [])
        if not columns:
            raise ValueError(f"Subfigure '{spec.get('title', '<untitled>')}' has no columns.")

        labels = spec.get("labels", columns)
        colors = spec.get("colors", DEFAULT_COLORS)
        linewidth = spec.get("linewidth", 1.2)

        for series_index, column in enumerate(columns):
            column_index = resolve_column(column, headers)
            label = labels[series_index] if series_index < len(labels) else headers[column_index]
            color = colors[series_index % len(colors)]
            ax.plot(x, data[:, column_index], color=color, linewidth=linewidth, label=label)

        ax.set_title(spec.get("title", ""))
        ax.set_ylabel(spec.get("ylabel", ""))
        ax.grid(True, color="0.86", linewidth=0.8)
        ax.tick_params(direction="in", top=True, right=True, length=6, width=0.8)

        if spec.get("ylim") is not None:
            ax.set_ylim(*spec["ylim"])
        if spec.get("legend", True):
            ax.legend(
                loc=spec.get("legend_loc", "upper right"),
                frameon=True,
                fancybox=False,
                framealpha=1.0,
                edgecolor="black",
            )

    axes_array[-1].set_xlabel(x_label)
    fig.align_ylabels(axes_array)
    fig.subplots_adjust(left=0.12, right=0.985, top=0.96, bottom=0.085, hspace=0.62)

    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / f"{output_basename}.png"
    pdf_path = output_dir / f"{output_basename}.pdf"
    fig.savefig(png_path)
    fig.savefig(pdf_path)

    if show:
        plt.show()
    else:
        plt.close(fig)

    return png_path, pdf_path


if __name__ == "__main__":
    png, pdf = plot_scientific_csv()
    print(f"Saved: {png}")
    print(f"Saved: {pdf}")
