import pytest
from parametrize import parametrize


@parametrize("a", [1, 2, 3, 4])  # type: ignore[misc]
def test_one_arg(a: int) -> None:
    assert a == a


@parametrize("a,b", [(1, 1), (2, 2), (3, 3), (4, 4)])  # type: ignore[misc]
def test_two_args(a: int, b: int) -> None:
    assert a == b
