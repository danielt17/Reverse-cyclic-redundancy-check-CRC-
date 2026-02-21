from hypothesis import given, settings
from hypothesis import strategies as st

from crc_reverse.polynomial_reversing_method_2 import poly_gcd, poly_mod


@settings(max_examples=200, deadline=None)
@given(
    dividend=st.integers(min_value=1, max_value=2**64 - 1),
    divisor=st.integers(min_value=1, max_value=2**32 - 1),
)
def test_poly_mod_degree_property(dividend: int, divisor: int) -> None:
    remainder = poly_mod(dividend, divisor)
    assert remainder == 0 or remainder.bit_length() < divisor.bit_length()


@settings(max_examples=150, deadline=None)
@given(
    a=st.integers(min_value=1, max_value=2**64 - 1),
    b=st.integers(min_value=1, max_value=2**64 - 1),
)
def test_poly_gcd_divides_inputs(a: int, b: int) -> None:
    g = poly_gcd(a, b)
    assert g > 0
    assert poly_mod(a, g) == 0
    assert poly_mod(b, g) == 0
