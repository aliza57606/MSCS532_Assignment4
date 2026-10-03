"""Automated tests for Assignment 4.

These tests verify that the sorting algorithm, priority queue operations, and
scheduler produce the expected results before submission.
"""

import unittest

from heapsort import heapsort
from priority_queue import MaxHeapPriorityQueue, Task
from scheduler_simulation import run_scheduler


class TestHeapSort(unittest.TestCase):
    """Tests for the Heapsort implementation."""

    def test_random_values(self):
        # Includes an unsorted list and a duplicate value.
        data = [7, 2, 9, 1, 5, 5]
        self.assertEqual(heapsort(data), sorted(data))

    def test_empty(self):
        # Edge case: sorting an empty list should return an empty list.
        self.assertEqual(heapsort([]), [])


class TestPriorityQueue(unittest.TestCase):
    """Tests for max-heap priority queue behavior."""

    def test_extract_order(self):
        # Tasks should be removed from highest to lowest priority.
        pq = MaxHeapPriorityQueue()
        pq.insert(Task("A", 2))
        pq.insert(Task("B", 5))
        pq.insert(Task("C", 3))

        extracted = [pq.extract_max().task_id for _ in range(3)]
        self.assertEqual(extracted, ["B", "C", "A"])

    def test_key_updates(self):
        # Verify that increasing a priority can move a task upward.
        pq = MaxHeapPriorityQueue()
        pq.insert(Task("A", 2))
        pq.insert(Task("B", 5))

        pq.increase_key("A", 8)
        self.assertEqual(pq.extract_max().task_id, "A")

        # Verify that decreasing a priority is stored correctly.
        pq.decrease_key("B", 1)
        self.assertEqual(pq.extract_max().priority, 1)


class TestScheduler(unittest.TestCase):
    """Tests for non-preemptive priority scheduling."""

    def test_priority_scheduling(self):
        # B and A arrive at time 0, so B runs first because priority 5 > 1.
        # C arrives at time 1 and has priority 3, so it runs before A.
        tasks = [
            Task("A", 1, 0),
            Task("B", 5, 0),
            Task("C", 3, 1),
        ]

        result = run_scheduler(tasks)
        self.assertEqual([r.task_id for r in result], ["B", "C", "A"])


if __name__ == "__main__":
    unittest.main()
