import inspect

import crc_reverse
from crc_reverse import api


def test_public_api_exports_are_stable() -> None:
    expected_exports = {
        "CrcReverseResult",
        "CrcReverseError",
        "InputValidationError",
        "PacketFormatError",
        "ReversalFailureError",
        "PacketSample",
        "ReverseConfig",
        "ReverseRequest",
        "crc_reversing",
        "reverse_crc_from_hex_packets",
        "reverse_crc_from_packets",
        "reverse_crc_interactive",
        "run_reversal_pipeline",
    }
    assert set(crc_reverse.__all__) == expected_exports


def test_public_function_signatures_are_stable() -> None:
    sig_packets = inspect.signature(api.reverse_crc_from_packets)
    assert list(sig_packets.parameters.keys()) == ["packets", "crc_width", "verbose"]

    sig_hex = inspect.signature(api.reverse_crc_from_hex_packets)
    assert list(sig_hex.parameters.keys()) == ["hex_packets", "crc_width", "verbose"]
