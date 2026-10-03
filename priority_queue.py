"""Array-based max-heap priority queue for scheduling tasks.

A larger numeric priority means a task should be processed sooner.
The heap is stored in a normal Python list, which gives efficient parent/child
index calculations and O(log n) insertion/removal operations.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    """Represents one task that can be stored in the priority queue."""

    task_id: str
    priority: int
    arrival_time: int = 0
    deadline: Optional[int] = None
    description: str = ""

    # Internal sequence number used only to break ties consistently.
    # repr=False keeps it out of printed Task output.
    _sequence: int = field(default=0, repr=False, compare=False)


class MaxHeapPriorityQueue:
    """Max-heap where the task with the largest priority is served first."""

    def __init__(self):
        # 'heap' stores Task objects in max-heap order.
        self.heap = []

        # Map task_id -> current heap index.
        # This avoids an O(n) search when changing a task's priority.
        self.positions = {}

        # Used to preserve insertion order when priority and arrival time tie.
        self._sequence_counter = 0

    def __len__(self):
        """Return the number of tasks currently in the queue."""
        return len(self.heap)

    def is_empty(self):
        """Return True if the queue contains no tasks. Complexity: O(1)."""
        return len(self.heap) == 0

    def _higher_priority(self, a, b):
        """Return True when task a should come before task b.

        Tie-breaking rules:
        1. Larger priority value wins.
        2. Earlier arrival time wins if priorities are equal.
        3. Earlier insertion sequence wins if both are still tied.
        """
        if a.priority != b.priority:
            return a.priority > b.priority
        if a.arrival_time != b.arrival_time:
            return a.arrival_time < b.arrival_time
        return a._sequence < b._sequence

    def _swap(self, i, j):
        """Swap two heap entries and keep the positions dictionary accurate."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.positions[self.heap[i].task_id] = i
        self.positions[self.heap[j].task_id] = j

    def _sift_up(self, index):
        """Move a task upward until the max-heap property is restored."""
        while index > 0:
            # Parent of index i in a binary heap is (i - 1) // 2.
            parent = (index - 1) // 2

            if self._higher_priority(self.heap[index], self.heap[parent]):
                self._swap(index, parent)
                index = parent
            else:
                break

    def _sift_down(self, index):
        """Move a task downward until the max-heap property is restored."""
        n = len(self.heap)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index

            # Compare the current node with its left child.
            if left < n and self._higher_priority(self.heap[left], self.heap[largest]):
                largest = left

            # Compare the current best choice with the right child.
            if right < n and self._higher_priority(self.heap[right], self.heap[largest]):
                largest = right

            # If the current node already has the highest priority, stop.
            if largest == index:
                break

            self._swap(index, largest)
            index = largest

    def insert(self, task):
        """Insert a new task and restore heap order. Complexity: O(log n)."""

        # task_id values must be unique because positions uses them as keys.
        if task.task_id in self.positions:
            raise ValueError(f"Duplicate task_id: {task.task_id}")

        # Record insertion order for deterministic tie-breaking.
        task._sequence = self._sequence_counter
        self._sequence_counter += 1

        # Add the task to the end, then move it upward if necessary.
        self.heap.append(task)
        index = len(self.heap) - 1
        self.positions[task.task_id] = index
        self._sift_up(index)

    def peek_max(self):
        """Return the highest-priority task without removing it. O(1)."""
        if self.is_empty():
            raise IndexError("peek_max from empty priority queue")
        return self.heap[0]

    def extract_max(self):
        """Remove and return the highest-priority task. Complexity: O(log n)."""
        if self.is_empty():
            raise IndexError("extract_max from empty priority queue")

        # The root of a max heap is always the highest-priority task.
        maximum = self.heap[0]

        # Remove the final task so it can replace the root.
        last = self.heap.pop()
        del self.positions[maximum.task_id]

        # If tasks remain, move the final task to the root and sift it down.
        if self.heap:
            self.heap[0] = last
            self.positions[last.task_id] = 0
            self._sift_down(0)

        return maximum

    def _find_index(self, task_id):
        """Return a task's heap index or raise an error if it does not exist."""
        if task_id not in self.positions:
            raise KeyError(f"Task {task_id!r} not found")
        return self.positions[task_id]

    def increase_key(self, task_id, new_priority):
        """Increase a task's priority and move it upward. Complexity: O(log n)."""
        index = self._find_index(task_id)

        if new_priority < self.heap[index].priority:
            raise ValueError("new priority must be greater than or equal to current priority")

        self.heap[index].priority = new_priority
        self._sift_up(index)

    def decrease_key(self, task_id, new_priority):
        """Decrease a task's priority and move it downward. Complexity: O(log n)."""
        index = self._find_index(task_id)

        if new_priority > self.heap[index].priority:
            raise ValueError("new priority must be less than or equal to current priority")

        self.heap[index].priority = new_priority
        self._sift_down(index)


if __name__ == "__main__":
    # Demonstration of insertion, priority update, and extraction order.
    pq = MaxHeapPriorityQueue()

    pq.insert(Task("T1", 3, arrival_time=0, deadline=8))
    pq.insert(Task("T2", 5, arrival_time=1, deadline=4))
    pq.insert(Task("T3", 2, arrival_time=2, deadline=10))

    # Increase T3 so it becomes the highest-priority task.
    pq.increase_key("T3", 6)

    # Remove tasks from highest to lowest priority.
    while not pq.is_empty():
        print(pq.extract_max())
