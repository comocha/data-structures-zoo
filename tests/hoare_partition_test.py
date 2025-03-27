from hoare_partition import hoare_partition_var1, hoare_partition_var2


def test_hoare_partition_var1():
    nums = [1]
    left = 0
    right = 0
    pivot_index = 0
    assert hoare_partition_var1(nums, left, right, pivot_index) == 0
    assert nums == [1]


def test_hoare_partition_var1_ascending_last():
    nums = [1, 2, 3]
    left = 0
    right = 2
    pivot_index = 2
    assert hoare_partition_var1(nums, left, right, pivot_index) == 2
    assert nums == [1, 2, 3]


def test_hoare_partition_var1_ascending_first():
    nums = [1, 2, 3]
    left = 0
    right = 2
    pivot_index = 0
    assert hoare_partition_var1(nums, left, right, pivot_index) == 0
    assert nums == [1, 2, 3]


def test_hoare_partition_var1_descending_first():
    nums = [3, 2, 1]
    left = 0
    right = 2
    pivot_index = 0
    assert hoare_partition_var1(nums, left, right, pivot_index) == 1
    assert nums == [1, 2, 3]


def test_hoare_partition_var1_descending_last():
    nums = [3, 2, 1]
    left = 0
    right = 2
    pivot_index = 2
    assert hoare_partition_var1(nums, left, right, pivot_index) == 0
    assert nums == [1, 2, 3]


def test_hoare_partition_var1_dups():
    # array with all duplicates. Index is midway point. This makes it better than lomuto partition
    nums = [1] * 50
    left = 0
    right = 49
    pivot_index = 0
    assert hoare_partition_var1(nums, left, right, pivot_index) == 24
    pivot_index = 49
    assert hoare_partition_var1(nums, left, right, pivot_index) == 24
    pivot_index = 5
    assert hoare_partition_var1(nums, left, right, pivot_index) == 24


def test_hoare_partition_var1_pivot_not_ret():
    # This is a test to see why the index returned is not the index of the final position of the
    # pivot value
    nums = [3, 2, 5, 2, 4, 9, 1, 3, -1]
    left = 0
    right = 8
    pivot_index = 0
    assert hoare_partition_var1(nums, left, right, pivot_index) == 4
    assert nums[4] != 3  # pivot value was 3. But we are returning value 2 at index 2
    assert nums[:5] == [-1, 2, 3, 2, 1]  # All values in [0..j] <= 3
    assert nums[5:] == [9, 4, 5, 3]  # All values in [j..right] >= 3


## Tests for hoare_partition_var2
def test_hoare_partition_var2():
    nums = [1]
    left = 0
    right = 0
    pivot_index = 0
    assert hoare_partition_var2(nums, left, right, pivot_index) == 0
    assert nums == [1]


def test_hoare_partition_var2_ascending_last():
    nums = [1, 2, 3]
    left = 0
    right = 2
    pivot_index = 2
    assert hoare_partition_var2(nums, left, right, pivot_index) == 2
    assert nums == [1, 2, 3]


def test_hoare_partition_var2_ascending_first():
    nums = [1, 2, 3]
    left = 0
    right = 2
    pivot_index = 0
    assert hoare_partition_var2(nums, left, right, pivot_index) == 0
    assert nums == [1, 2, 3]


def test_hoare_partition_var2_descending_first():
    nums = [3, 2, 1]
    left = 0
    right = 2
    pivot_index = 0
    assert hoare_partition_var2(nums, left, right, pivot_index) == 2
    assert nums == [1, 2, 3]


def test_hoare_partition_var2_descending_last():
    nums = [3, 2, 1]
    left = 0
    right = 2
    pivot_index = 2
    assert hoare_partition_var2(nums, left, right, pivot_index) == 0
    assert nums == [1, 2, 3]


def test_hoare_partition_var2_dups():
    # array with all duplicates. Index is midway point. This makes it better than lomuto partition
    nums = [1] * 50
    left = 0
    right = 49
    pivot_index = 0
    assert hoare_partition_var2(nums, left, right, pivot_index) == 25
    pivot_index = 49
    assert hoare_partition_var2(nums, left, right, pivot_index) == 25
    pivot_index = 5
    assert hoare_partition_var2(nums, left, right, pivot_index) == 25


def test_hoare_partition_var2_pivot_complex():
    # This is a test to see why the index returned is not the index of the final position of the
    # pivot value
    nums = [3, 2, 5, 2, 4, 9, 1, 3, -1]
    left = 0
    right = 8
    pivot_index = 0
    assert hoare_partition_var2(nums, left, right, pivot_index) == 5
    assert nums[5] == 3  # pivot value was 3. But we are returning value 2 at index 2
    assert nums[:5] == [1, 2, -1, 2, 3]  # All values in [0..j] <= 3
    assert nums[6:] == [9, 4, 5]  # All values in [j..right] >= 3
