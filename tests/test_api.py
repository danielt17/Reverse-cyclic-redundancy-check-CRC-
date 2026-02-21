import pytest
from typing import Any, cast

pytest.importorskip("crcengine")

from crc_reverse import CrcReverseResult, InputValidationError, reverse_crc_from_hex_packets


def test_reverse_crc_from_hex_packets_returns_expected_candidate(
    crc40_golden_fixture: dict[str, object]
) -> None:
    packets_hex = cast(list[str], crc40_golden_fixture["packets_hex"])
    crc_width = cast(int, crc40_golden_fixture["crc_width"])
    expected_candidates = cast(list[dict[str, Any]], crc40_golden_fixture["expected_candidates"])
    expected = expected_candidates[0]
    results = reverse_crc_from_hex_packets(packets_hex, crc_width=crc_width, verbose=False)
    assert results
    assert all(isinstance(result, CrcReverseResult) for result in results)
    expected_poly = cast(int, expected["poly"])
    expected_width = cast(int, expected["width"])
    expected_seed = cast(int, expected["seed"])
    expected_ref_in = cast(bool, expected["ref_in"])
    expected_ref_out = cast(bool, expected["ref_out"])
    expected_xor_out = cast(int, expected["xor_out"])
    assert any(
        result.poly == expected_poly
        and result.width == expected_width
        and result.seed == expected_seed
        and result.ref_in is expected_ref_in
        and result.ref_out is expected_ref_out
        and result.xor_out == expected_xor_out
        for result in results
    )


def test_reverse_crc_from_packets_rejects_invalid_width() -> None:
    with pytest.raises(InputValidationError):
        reverse_crc_from_hex_packets(["00aa"], crc_width=0)
