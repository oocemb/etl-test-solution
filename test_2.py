# from is_broken import isBrokenVersion
import pytest
from unittest.mock import MagicMock


def side_effect_func(n: int):
    if n == 1:
        return False
    elif n == 2:
        return False
    elif n == 3:
        return True
    elif n == 4:
        return True
    elif n == 5:
        return True
    else:
        raise ValueError


test_params = [(5, 3)]
isBrokenVersion = MagicMock(side_effect=side_effect_func)


def solve(n: int) -> int:
    """
    Предположим, у вас есть n версий [1, 2, ..., n] и вы хотите найти первую сломанную версию,
    из-за которой все последующие будут сломаны.
    Вам предоставляется bool API isBrokenVersion (версия), который возвращает, является ли версия сломанной.
    1 <= bad <= n <= 230
    Сложность по памяти O(1)
    Сложность по времени O(LogN)
    """
    left = 1
    right = n
    while right > left:
        middle = (right + left) // 2
        if isBrokenVersion(middle):
            right = middle
        else:
            left = middle + 1
    return right


@pytest.mark.parametrize("n, result", test_params)
def test_solve(n, result):
    assert solve(n) == result
