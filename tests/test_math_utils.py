import pytest

from crc_reverse.polynomial_reversing_method_2 import poly_gcd, poly_mod
from crc_reverse.utils import unique


def test_poly_mod_reduces_degree() -> None:
    dividend = int("11010011101100000", 2)
    divisor = int("1011", 2)
    remainder = poly_mod(dividend, divisor)
    assert remainder == int("100", 2)


def test_poly_gcd_simple_case() -> None:
    a = int("1111", 2)
    b = int("101", 2)
    assert poly_gcd(a, b) == int("101", 2)


def test_unique_preserves_order_for_version_1() -> None:
    values = [3, 1, 3, 2, 2, 1, 4]
    assert unique(values, version=1) == [3, 1, 2, 4]


def test_unique_returns_counts_for_version_0() -> None:
    values = ["a", "b", "a", "c", "b", "a"]
    uniques, counts = unique(values, version=0)
    assert dict(zip(uniques, counts)) == {"a": 3, "b": 2, "c": 1}
