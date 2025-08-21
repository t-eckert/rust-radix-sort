#!/usr/bin/env python3

import subprocess
import datetime

N_ITERATIONS = 10
MAX_ARRAY_LENGTH = 100_000_000


def main():
    times = []

    length = 1
    while length <= MAX_ARRAY_LENGTH:
        for _ in range(0, N_ITERATIONS):
            print(f"Running with length: {length}")
            output = run_app(length)
            print(output)
            radix_time, rust_time = output.splitlines()
            times.append(
                {"length": length, "radix_time": radix_time, "rust_time": rust_time}
            )
        length *= 10

    with open(f"./benchmark-data/{datetime.datetime.now()}.csv", "w+") as f:
        f.write("length,radix_time (ns),rust_time (ns)\n")
        for time in times:
            f.write(
                f"{time['length']},{time['radix_time'][:-2]},{time['rust_time'][:-2]}\n"
            )


def run_app(length):
    output = subprocess.run(
        ["./target/release/rust-radix-sort", str(length)],
        capture_output=True,
        text=True,
    )
    return output.stdout


if __name__ == "__main__":
    main()
