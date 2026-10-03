"""Heapsort implementation using an array-based max heap.

This file demonstrates the two main phases of Heapsort:
1. Build a max heap so the largest value is at index 0.
2. Repeatedly move that largest value to the end of the list and repair the heap.
"""


def heapify(arr, heap_size, root_index):
    """Restore the max-heap property for the subtree rooted at root_index.

    Parameters:
        arr: The list being organized as a heap.
        heap_size: Number of elements that still belong to the active heap.
        root_index: Index of the subtree root that may violate the heap property.

    Time complexity: O(log n) in the worst case because a value may move
    from the root of the subtree down to a leaf.
    """

    # Assume the root is the largest value until a larger child is found.
    largest = root_index

    # In an array-based binary heap, the children of index i are located at:
    # left  = 2*i + 1
    # right = 2*i + 2
    left = 2 * root_index + 1
    right = 2 * root_index + 2

    # If the left child exists and is larger than the current largest value,
    # remember the left child's index.
    if left < heap_size and arr[left] > arr[largest]:
        largest = left

    # Do the same comparison for the right child.
    if right < heap_size and arr[right] > arr[largest]:
        largest = right

    # If one of the children is larger than the root, swap them.
    if largest != root_index:
        arr[root_index], arr[largest] = arr[largest], arr[root_index]

        # The old root value moved downward, so the subtree below it might now
        # violate the max-heap rule. Recursively repair that subtree.
        heapify(arr, heap_size, largest)


def build_max_heap(arr):
    """Convert arr into a valid max heap in place.

    Only parent nodes need to be heapified. Leaf nodes already satisfy the
    heap property because they have no children. The last parent is located at
    index len(arr)//2 - 1, so we start there and move toward the root.

    Time complexity: O(n).
    """

    # Move from the last parent node back to the root at index 0.
    for i in range(len(arr) // 2 - 1, -1, -1):
        heapify(arr, len(arr), i)


def heapsort(values):
    """Return a new list containing values in ascending order.

    The input is copied so the original list is not modified.

    Overall time complexity:
        Best case:    O(n log n)
        Average case: O(n log n)
        Worst case:   O(n log n)
    """

    # Copy the input so sorting does not change the caller's original list.
    arr = list(values)

    # Phase 1: Rearrange the array into a max heap.
    build_max_heap(arr)

    # Phase 2: Move the maximum value (at index 0) to the end of the unsorted
    # section. Then shrink the heap and restore the heap property.
    for end in range(len(arr) - 1, 0, -1):
        # Swap the maximum value with the last element in the active heap.
        arr[0], arr[end] = arr[end], arr[0]

        # 'end' is now the heap size, so elements at end and beyond are already
        # in their final sorted positions and must not be touched again.
        heapify(arr, end, 0)

    return arr


if __name__ == "__main__":
    # Small demonstration used to verify that the implementation works.
    sample = [12, 11, 13, 5, 6, 7]
    print("Original:", sample)
    print("Sorted:  ", heapsort(sample))
