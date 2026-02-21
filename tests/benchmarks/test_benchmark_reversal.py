import pytest
from typing import Any, Callable, cast

from crc_reverse import reverse_crc_from_hex_packets


@pytest.mark.benchmark
def test_benchmark_crc_reversal(
    benchmark: Callable[..., Any], crc40_golden_fixture: dict[str, object]
) -> None:
    packets_hex = cast(list[str], crc40_golden_fixture["packets_hex"])
    crc_width = cast(int, crc40_golden_fixture["crc_width"])
    benchmark(reverse_crc_from_hex_packets, packets_hex, crc_width, False)
