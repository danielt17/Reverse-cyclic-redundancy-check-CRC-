import pytest

pytest.importorskip("crcengine")

from crc_reverse import CrcReverseResult, reverse_crc_from_hex_packets


KNOWN_PACKETS_HEX = [
    "aaaa9a7d00011b6078e22800050a3dd91ac80b",
    "aaaa9a7d00011b6078e23c00050a7869ca436a",
    "aaaa9a7d00011b6078e23200050a9b97f38496",
    "aaaa9a7d00011b6078e24600050ac55da33901",
    "aaaa9a7d00011b6078e25000050aa07f7bf344",
    "aaaa9a7d00011b6078e25a00050a02a552b6f0",
    "aaaa9a7d00011b6078e29600050af73c635dc4",
    "aaaa9a7d00011b6078e27800050a2b1edae586",
    "aaaa9a7d00011b6078e26400050aece62b6a77",
    "aaaa9a7d00011b6078e26e6400050ad521480584",
    "aaaa9a7d00011b6078e26e64c800050a24a8659b05",
    "aaaa9a7d00011b6078e26e64c86400050a40db28c0be",
]


def test_reverse_crc_from_hex_packets_returns_expected_candidate() -> None:
    results = reverse_crc_from_hex_packets(KNOWN_PACKETS_HEX, crc_width=40, verbose=False)
    assert results
    assert all(isinstance(result, CrcReverseResult) for result in results)
    assert any(
        result.poly == 0x4820009
        and result.width == 40
        and result.seed == 0x0
        and result.ref_in is False
        and result.ref_out is False
        and result.xor_out == 0xFFFFFFFFFF
        for result in results
    )


def test_reverse_crc_from_packets_rejects_invalid_width() -> None:
    with pytest.raises(ValueError):
        reverse_crc_from_hex_packets(KNOWN_PACKETS_HEX, crc_width=0)
