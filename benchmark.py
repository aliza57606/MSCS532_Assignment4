"""Empirical comparison of Heapsort, Quicksort, and Merge Sort.

The assignment asks for measurements using different input sizes and input
orders. This script tests random, sorted, and reverse-sorted data at sizes
1,000, 5,000, and 10,000. Each timing is averaged across three runs.
"""

import csv
import random
import statistics
import time
from pathlib import Path

from heapsort import heapsort


def merge_sort(values):
    """Return a sorted copy of values using Merge Sort."""

    # A list of length 0 or 1 is already sorted.
    if len(values) <= 1:
        return list(values)

    # Split the list into two halves.
    mid = len(values) // 2
    left = merge_sort(values[:mid])
    right = merge_sort(values[mid:])

    # Merge the two already-sorted halves.
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # One side may still contain values after the other side is exhausted.
    result.extend(left[i:])
    result.extend(right[j:])

    return result


def quicksort(values):
    """Return a sorted copy using randomized three-way Quicksort."""

    if len(values) <= 1:
        return list(values)

    # Random pivot selection reduces dependence on the original input order.
    pivot = random.choice(values)

    # Three-way partitioning also handles duplicate values cleanly.
    less = [x for x in values if x < pivot]
    equal = [x for x in values if x == pivot]
    greater = [x for x in values if x > pivot]

    return quicksort(less) + equal + quicksort(greater)


def make_input(size, distribution, seed):
    """Create repeatable test data for one benchmark case."""

    # A local random generator with a fixed seed makes the random test data
    # reproducible from run to run.
    rng = random.Random(seed)

    if distribution == "random":
        return [rng.randint(0, size * 10) for _ in range(size)]

    if distribution == "sorted":
        return list(range(size))

    if distribution == "reverse":
        return list(range(size, 0, -1))

    raise ValueError(f"Unknown distribution: {distribution}")


def time_algorithm(func, data, repeats=3):
    """Measure average runtime and verify the algorithm sorts correctly."""

    times = []

    # Python's built-in sorted() gives a trusted expected answer that we use
    # only to verify correctness; it is not part of the measured time.
    expected = sorted(data)

    for _ in range(repeats):
        start = time.perf_counter()
        result = func(data)
        elapsed = time.perf_counter() - start

        # Stop immediately if an algorithm produces an incorrect result.
        assert result == expected

        times.append(elapsed)

    # Report the mean of the repeated timings to reduce random timing noise.
    return statistics.mean(times)


def main():
    """Run every algorithm on every requested size/distribution combination."""

    algorithms = {
        "Heapsort": heapsort,
        "Quicksort": quicksort,
        "Merge Sort": merge_sort,
    }

    sizes = [1000, 5000, 10000]
    distributions = ["random", "sorted", "reverse"]
    rows = []

    # Test each distribution and size with all three sorting algorithms.
    for distribution in distributions:
        for size in sizes:
            data = make_input(size, distribution, seed=2026 + size)

            for name, func in algorithms.items():
                seconds = time_algorithm(func, data, repeats=3)

                rows.append(
                    {
                        "distribution": distribution,
                        "size": size,
                        "algorithm": name,
                        "average_seconds": f"{seconds:.6f}",
                    }
                )

                print(f"{distribution:7} n={size:5} {name:10}: {seconds:.6f} s")

    # Save the measured values to a CSV file for use in the written report.
    output = Path(__file__).with_name("benchmark_results.csv")

    with output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved results to {output}")


if __name__ == "__main__":
    main()
