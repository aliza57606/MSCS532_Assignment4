"""Simple non-preemptive priority scheduler using MaxHeapPriorityQueue.

The simulation represents a single worker. At each moment, it selects the
highest-priority task that has already arrived. Once a task starts, it finishes
before another task begins (non-preemptive scheduling).
"""

from dataclasses import dataclass
from typing import Optional

from priority_queue import Task, MaxHeapPriorityQueue


@dataclass
class ScheduledTask:
    """Stores the result of scheduling one task."""

    task_id: str
    priority: int
    arrival_time: int
    start_time: int
    completion_time: int
    deadline: Optional[int]
    met_deadline: Optional[bool]


def run_scheduler(tasks, service_time=1):
    """Run a single-worker, non-preemptive priority scheduling simulation.

    Rules:
    - A task becomes available when arrival_time <= current time.
    - The available task with the highest numeric priority runs next.
    - Every task takes 'service_time' time units to complete.
    - Once a task begins, it runs to completion before another task starts.
    """

    # Sort by arrival time so we can add tasks to the heap in time order.
    # task_id is used as a deterministic secondary key.
    tasks = sorted(tasks, key=lambda t: (t.arrival_time, t.task_id))

    # The max heap stores tasks that have arrived and are waiting to run.
    queue = MaxHeapPriorityQueue()

    # Store one ScheduledTask result for every completed task.
    results = []

    # 'time' is the simulation clock.
    time = 0

    # 'i' points to the next task in the sorted input list that has not yet
    # been inserted into the priority queue.
    i = 0

    # Continue while either unarrived tasks remain or the queue still has work.
    while i < len(tasks) or not queue.is_empty():

        # If nothing is waiting, jump the clock forward to the next arrival.
        # This avoids simulating idle time one unit at a time.
        if queue.is_empty() and i < len(tasks) and tasks[i].arrival_time > time:
            time = tasks[i].arrival_time

        # Add every task that has arrived by the current simulation time.
        while i < len(tasks) and tasks[i].arrival_time <= time:
            queue.insert(tasks[i])
            i += 1

        # Select the highest-priority available task.
        task = queue.extract_max()

        # Record when this task begins.
        start = time

        # Advance the clock by the amount of time needed to complete the task.
        time += service_time

        # If a deadline exists, determine whether completion occurred on time.
        if task.deadline is None:
            met_deadline = None
        else:
            met_deadline = time <= task.deadline

        # Save the scheduling result for later display or analysis.
        results.append(
            ScheduledTask(
                task_id=task.task_id,
                priority=task.priority,
                arrival_time=task.arrival_time,
                start_time=start,
                completion_time=time,
                deadline=task.deadline,
                met_deadline=met_deadline,
            )
        )

    return results


def demo():
    """Run the scheduler with five example tasks."""

    tasks = [
        Task("T1", priority=2, arrival_time=0, deadline=5, description="Routine report"),
        Task("T2", priority=5, arrival_time=0, deadline=3, description="Production incident"),
        Task("T3", priority=3, arrival_time=1, deadline=6, description="Data refresh"),
        Task("T4", priority=4, arrival_time=1, deadline=4, description="Customer escalation"),
        Task("T5", priority=1, arrival_time=2, deadline=8, description="Archive cleanup"),
    ]

    results = run_scheduler(tasks)

    # Print a small table showing the order and timing of scheduled tasks.
    print("Task  Pri  Arrive  Start  Complete  Deadline  Met")
    print("----  ---  ------  -----  --------  --------  ---")

    for r in results:
        print(
            f"{r.task_id:<4}  {r.priority:<3}  {r.arrival_time:<6}  {r.start_time:<5}  "
            f"{r.completion_time:<8}  {str(r.deadline):<8}  {r.met_deadline}"
        )


if __name__ == "__main__":
    demo()
