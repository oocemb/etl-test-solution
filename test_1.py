from typing import List
import pytest

test_params = [([2, 7, 11, 15], 9, [0, 1]), ([3, 2, 4], 6, [1, 2]), ([3, 3], 6, [0, 1])]


def solve(nums: List[int], target: int) -> List[int]:
    """
    Дан массив целых чисел nums и целое число target.
    Необходимо вернуть индексы двух чисел таких, чтобы их сумма равна target.
    Сложность по памяти O(N)
    Сложность по времени O(N)
    """
    previous_dict = {}
    for i, num in enumerate(nums):
        if target - num in previous_dict:
            return [previous_dict[target-num], i]
        previous_dict[num] = i
    return []


@pytest.mark.parametrize("nums, target, result", test_params)
def test_solve(nums, target, result):
    assert solve(nums, target) == result
