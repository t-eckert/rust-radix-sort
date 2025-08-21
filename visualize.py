#!/usr/bin/env python3

import csv
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

BENCHMARK_DIR = Path("benchmark-data")


def main(filename=None):
    if filename is None:
        latest_benchmark = latest_benchmark_filename()
        filename = latest_benchmark
    data = load_benchmark_data(filename)
    if data is None:
        return

    benchmark_date = filename.stem

    create_plot(data, benchmark_date)


def latest_benchmark_filename():
    csv_files = list(BENCHMARK_DIR.glob("*.csv"))

    # Get the most recent file
    return max(csv_files, key=os.path.getctime)


def load_benchmark_data(filename):
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(
                {
                    "length": int(row["length"]),
                    "radix_time": int(row["radix_time (ns)"]),
                    "rust_time": int(row["rust_time (ns)"]),
                }
            )

    return data


def create_plot(data, output_name="benchmark_graph"):
    lengths = [row["length"] for row in data]
    radix_times = [row["radix_time"] / 1_000_000 for row in data]  # Convert to ms
    rust_times = [row["rust_time"] / 1_000_000 for row in data]  # Convert to ms

    # Create single plot
    plt.figure(figsize=(10, 6))

    # Performance comparison
    plt.loglog(
        lengths,
        radix_times,
        "o-",
        label="Radix Sort",
        color="green",
        linewidth=2,
        markersize=6,
    )
    plt.loglog(
        lengths,
        rust_times,
        "s-",
        label="Rust Sort",
        color="orange",
        linewidth=2,
        markersize=6,
    )
    plt.xlabel("Array Length")
    plt.ylabel("Time (ms)")
    plt.title("Sorting Performance Comparison")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.gca().xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, p: f"{int(x):,}")
    )

    plt.tight_layout()

    # Save the graph in the benchmark data directory
    output_file = BENCHMARK_DIR / f"{output_name}.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Plot saved as: {output_file}")

    plt.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = Path(sys.argv[1])
    else:
        # If no filename is provided, this will use the latest benchmark file
        filename = None

    main(filename)
