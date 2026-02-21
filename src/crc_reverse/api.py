"""Public API helpers for programmatic CRC reverse engineering usage."""

from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO
from typing import Sequence

from .crc_reversing import crc_reversing, run_reversal_pipeline
from .errors import InputValidationError, ReversalFailureError
from .models import PacketSample, ReverseConfig, ReverseRequest


@dataclass(frozen=True)
class CrcReverseResult:
    """Single CRC parameter candidate returned by the reverse algorithm."""

    poly: int
    width: int
    seed: int
    ref_in: bool
    ref_out: bool
    xor_out: int


Combination = Sequence[int | bool]


def _convert_combinations(combinations: Sequence[Combination]) -> list[CrcReverseResult]:
    """Convert raw internal candidate tuples into typed public result objects."""
    results: list[CrcReverseResult] = []
    for combination in combinations:
        if len(combination) != 6:
            continue
        results.append(
            CrcReverseResult(
                poly=int(combination[0]),
                width=int(combination[1]),
                seed=int(combination[2]),
                ref_in=bool(combination[3]),
                ref_out=bool(combination[4]),
                xor_out=int(combination[5]),
            )
        )
    return results


def reverse_crc_from_packets(
    packets: Sequence[bytes | bytearray | memoryview], crc_width: int, verbose: bool = False
) -> list[CrcReverseResult]:
    """
    Reverse CRC parameters from packets where each packet is data+crc.
    """
    config = ReverseConfig(crc_width=crc_width, verbose=verbose)
    normalized_packets = [bytes(packet) for packet in packets]
    if not normalized_packets:
        raise InputValidationError("at least one packet is required")
    if verbose:
        combinations = run_reversal_pipeline(
            normalized_packets, config.crc_width, print_results=True
        )
    else:
        with redirect_stdout(StringIO()):
            combinations = run_reversal_pipeline(
                normalized_packets, config.crc_width, print_results=False
            )
    results = _convert_combinations(combinations)
    if not results:
        raise ReversalFailureError("CRC reversal produced no candidate combinations")
    return results


def reverse_crc_from_hex_packets(
    hex_packets: Sequence[str], crc_width: int, verbose: bool = False
) -> list[CrcReverseResult]:
    """Reverse CRC parameters from hexadecimal packet strings."""
    request = ReverseRequest.from_hex_packets(
        packets_hex=hex_packets,
        crc_width=crc_width,
        verbose=verbose,
    )
    packets = [sample.as_bytes for sample in request.packets]
    return reverse_crc_from_packets(
        packets, request.config.crc_width, verbose=request.config.verbose
    )


def reverse_crc_interactive() -> list[CrcReverseResult]:
    """Run the legacy interactive flow and return parsed candidate results."""
    combinations = crc_reversing()
    return _convert_combinations(combinations)


def main() -> None:
    """CLI entrypoint for the interactive mode."""
    crc_reversing()
