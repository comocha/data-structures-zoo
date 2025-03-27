# return value is j
# indices in [left .. j] <= pivot
# indices in [j+1 .. right] >= pivot
# the pivot can exist in both sides
def hoare_partition_var1(
    nums: list[int], left: int, right: int, pivot_index: int
) -> int:
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
