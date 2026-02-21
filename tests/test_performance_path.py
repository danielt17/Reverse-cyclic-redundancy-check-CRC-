from crc_reverse.performance import NUMBA_ENABLED, poly_gcd_fast, poly_mod_fast


def test_performance_helpers_match_expected_math() -> None:
    assert poly_mod_fast(int("11010011101100000", 2), int("1011", 2)) == int("100", 2)
    assert poly_gcd_fast(int("1111", 2), int("101", 2)) == int("101", 2)
    assert isinstance(NUMBA_ENABLED, bool)
