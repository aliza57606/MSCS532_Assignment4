# Assignment 4: Heap Data Structures - Implementation, Analysis, and Applications

This repository contains well-commented Python implementations for the Assignment 4 requirements: Heapsort, an array-based max-heap priority queue, a scheduler simulation, runtime benchmarking, and automated tests.

## Files

- `heapsort.py` - Heapsort implementation with detailed comments.
- `priority_queue.py` - `Task` class and `MaxHeapPriorityQueue` with commented heap operations.
- `scheduler_simulation.py` - Non-preemptive task scheduler using the priority queue.
- `benchmark.py` - Compares Heapsort, randomized Quicksort, and Merge Sort.
- `benchmark_results.csv` - Measured benchmark values.
- `test_assignment4.py` - Unit tests for sorting, queue behavior, and scheduling.
- `Assignment4_Report.docx` - Written analysis and report.
- `demo_output.txt` - Example output.
- `SUBMISSION_STEPS.txt` - GitHub submission steps.

## Requirements

- Python 3.8 or newer
- No third-party packages are required.

## Run the Programs

```bash
python heapsort.py
python priority_queue.py
python scheduler_simulation.py
python benchmark.py
python -m unittest test_assignment4.py
```

## Expected Demonstrations

### Heapsort

The sample list is sorted in ascending order.

### Priority Queue

Tasks are extracted from highest numeric priority to lowest numeric priority.

### Scheduler

The scheduler selects the highest-priority task among tasks that have already arrived and reports arrival, start, completion, deadline, and deadline status.

### Benchmark

The benchmark measures Heapsort, Quicksort, and Merge Sort on:

- Random data
- Sorted data
- Reverse-sorted data
- Input sizes 1,000, 5,000, and 10,000

Each timing is averaged across three runs and saved to `benchmark_results.csv`.

## Complexity Summary

| Operation / Algorithm | Complexity |
|---|---:|
| Heapsort best case | O(n log n) |
| Heapsort average case | O(n log n) |
| Heapsort worst case | O(n log n) |
| Priority queue insert | O(log n) |
| Priority queue extract_max | O(log n) |
| Priority increase/decrease | O(log n) |
| is_empty | O(1) |

The public `heapsort()` function copies the input list, so that function uses O(n) extra space for the copy. The heap manipulation itself is in-place, with recursive `heapify()` using up to O(log n) call-stack space.
