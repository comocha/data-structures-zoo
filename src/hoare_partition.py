"""
hoare_partition.py

This module implements variations of the Hoare partitioning scheme, which is a key component
of the Quicksort algorithm. The Hoare partitioning scheme divides an array into two parts
based on a pivot element, ensuring that all elements in one part are less than or equal to
the pivot, while all elements in the other part are greater than or equal to the pivot.

Functions:
    - hoare_partition_var1: Implements a variation of the Hoare partitioning scheme where
      the pivot remains in its original position during the partitioning process.
    - hoare_partition_var2: Implements a variation of the Hoare partitioning scheme where
      the pivot is swapped to the start of the range before partitioning.

Notes:
    - Both variations perform the partitioning in-place, meaning no additional memory is allocated.
    - These implementations are efficient for arrays with many repeated elements and perform fewer
      swaps compared to the Lomuto partitioning scheme.
"""


def hoare_partition_var1(
    nums: list[int], left: int, right: int, pivot_index: int
) -> int:
    """
    Perform the Hoare partitioning scheme (Variation 1) on a list of integers.

    Variation 1 differs from Variation 2 in the following ways:
        - In Variation 1, the pivot element is not swapped to the start of the range.
        - The partitioning process begins with `i = left - 1` and `j = right + 1`.
        - The pivot remains in its original position during the partitioning process.
        - The returned partition index `j` need not correspond to the pivot's position.
        Instead, it ensures that all elements in `nums[left..j]` are less than or equal
        to the pivot, and all elements in `nums[j+1..right]` are greater than or equal
        to the pivot. The pivot itself may appear on either side of the partition.

    This function partitions the input list `nums` such that all elements in the range
    `nums[left..index]` are less than or equal to the pivot, and all elements in the range
    `nums[index + 1..right]` are greater than or equal to the pivot. The pivot itself may
    appear on either side of the partition.

    The partitioning is done in-place, meaning no additional memory is allocated.

    Args:
        nums (list[int]): The list of integers to partition. Must be non-empty.
        left (int): The starting index of the range to partition. Must satisfy `0 <= left <= right`.
        right (int): The ending index of the range to partition. Must satisfy `0 <= right < len(nums)`.
        pivot_index (int): The index of the pivot element in the list. Must satisfy `left <= pivot_index <= right`.

    Returns:
        int: The partition index `j`, such that all elements in `nums[left..j]` are
        less than or equal to the pivot, and all elements in `nums[j+1..right]` are
        greater than or equal to the pivot. Note that `j` does not necessarily correspond
        to the pivot's position in the list.

    Raises:
        IndexError: If `pivot_index` is out of the range `[left, right]`.
        ValueError: If `left` or `right` are out of bounds or if `left > right`.

    Notes:
        - This variation of the Hoare partitioning scheme is more efficient than the
        Lomuto partitioning scheme, as it performs fewer swaps on average.
        - It is particularly efficient for arrays with many repeated elements. Lomuto
        ends up with the left segment of the partition index being empty and the right
        being the entire array, whereas this method ensures a more balanced partition.

    Examples:
        >>> nums = [4, 5, 3, 7, 2]
        >>> hoare_partition_var1(nums, 0, 4, 2)
        2  # The pivot is 3 (nums[2]). After partitioning, nums becomes [3, 2, 4, 7, 5], and the pivot index is 2.
        >>> nums
        [3, 2, 4, 7, 5]
    """
    if not (0 <= left <= right):
        raise ValueError(
            f"The 'left' argument must satisfy 0 <= left <= right, but got left={left} and right={right}."
        )
    if not (0 <= right < len(nums)):
        raise ValueError(
            f"'right' must satisfy 0 <= right < len(nums), but got right={right} and len(nums)={len(nums)}"
        )
    if not (left <= pivot_index <= right):
        raise IndexError(
            f"'pivot_index' must satisfy left <= pivot_index <= right, but got pivot_index={pivot_index}, left={left}, and right={right}."
        )
    pivot = nums[pivot_index]
    i = left - 1
    j = right + 1
    while True:
        i += 1
        while nums[i] < pivot:
            i += 1
        j -= 1
        while nums[j] > pivot:
            j -= 1
        if i >= j:
            return j  # Return the partition index
        nums[i], nums[j] = nums[j], nums[i]


def hoare_partition_var2(nums: list[int], left: int, right: int, pivot_index: int):
    """
    Perform the Hoare partitioning scheme on a list of integers.

    This function partitions the input list `nums` into two segments based on a pivot element:
    - All elements in the range `nums[left..j]` are less than or equal to the pivot.
    - All elements in the range `nums[j+1..right]` are greater than or equal to the pivot.

    The pivot element is moved to its correct position during the partitioning process, ensuring
    that the array is partially sorted around the pivot.

    Use this variation when you want the pivot element to be explicitly moved to its correct
    position in the array after partitioning.

    The partitioning is done in-place, meaning no additional memory is allocated.

    Args:
        nums (list[int]): The list of integers to partition. Must be non-empty.
        left (int): The starting index of the range to partition. Must satisfy `0 <= left <= right`.
        right (int): The ending index of the range to partition. Must satisfy `0 <= right < len(nums)`.
        pivot_index (int): The index of the pivot element in the list. Must satisfy `left <= pivot_index <= right`.

    Returns:
        int: The partition index `j`, such that all elements in `nums[left..j]` are
        less than or equal to the pivot, and all elements in `nums[j+1..right]` are
        greater than or equal to the pivot. The pivot element will be at `nums[j]`.

    Raises:
        IndexError: If `pivot_index` is out of the range `[left, right]`.
        ValueError: If `left` or `right` are out of bounds or if `left > right`.

    Notes:
        - This variation is efficient for arrays with many repeated elements.
        - It performs fewer swaps compared to the Lomuto partitioning scheme.
        - The pivot element is guaranteed to be in its correct position after partitioning.

    Examples:
        >>> nums = [4, 5, 3, 7, 2]
        >>> hoare_partition_var2(nums, 0, 4, 2)
        1  # The pivot is 3 (nums[2]). After partitioning, nums becomes [2, 3, 4, 7, 5], and the pivot index is 1.
        >>> nums
        [2, 3, 4, 7, 5]
    """
    pivot = nums[pivot_index]
    nums[left], nums[pivot_index] = nums[pivot_index], nums[left]
    i = left
    j = right + 1
    while True:
        i += 1
        while i <= right and nums[i] < pivot:
            i += 1
        j -= 1
        while nums[j] > pivot:
            j -= 1
        if i >= j:
            nums[j], nums[left] = nums[left], nums[j]
            return j  # Return the partition index
        nums[i], nums[j] = nums[j], nums[i]
