import unittest
from parametrize import parametrize


# from src.main import x


class Tests(unittest.TestCase):
    # tests must be a method that begins with test

    @parametrize("a", [1, 2, 3, 4])  # type: ignore[misc] # (ignores missing types for @parametrize)
    def test_one_arg(self, a: int) -> None:
        self.assertEqual(a, a)

    @parametrize("a,b", [(1, 1), (2, 2), (3, 3), (4, 4)])  # type: ignore[misc] # (ignores missing types for @parametrize)
    def test_two_args(self, a: int, b: int) -> None:
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
