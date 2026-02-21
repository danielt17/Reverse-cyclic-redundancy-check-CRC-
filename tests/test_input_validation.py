import pytest
from hypothesis import given
from hypothesis import strategies as st

from crc_reverse import InputValidationError, PacketFormatError, reverse_crc_from_hex_packets


def test_rejects_empty_packet_list() -> None:
    with pytest.raises(InputValidationError):
        reverse_crc_from_hex_packets([], crc_width=40)


def test_rejects_invalid_hex_packet() -> None:
    with pytest.raises(PacketFormatError):
        reverse_crc_from_hex_packets(["zz"], crc_width=40)


def test_rejects_odd_length_packet() -> None:
    with pytest.raises(PacketFormatError):
        reverse_crc_from_hex_packets(["abc"], crc_width=40)


@given(
    bad_text=st.text(
        alphabet=st.characters(min_codepoint=33, max_codepoint=126), min_size=1, max_size=64
    ).filter(lambda s: any(ch not in "0123456789abcdefABCDEF" for ch in s) or len(s) % 2 == 1)
)
def test_fuzz_invalid_hex_strings_raise(bad_text: str) -> None:
    with pytest.raises((PacketFormatError, InputValidationError)):
        reverse_crc_from_hex_packets([bad_text], crc_width=40)
