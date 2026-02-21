"""Command-line interface for CRC reverse engineering."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .api import CrcReverseResult, reverse_crc_from_hex_packets, reverse_crc_interactive
from .errors import InputValidationError, PacketFormatError, ReversalFailureError


def _load_hex_packets_from_file(path: Path) -> list[str]:
    """Load packet hex strings from a text or JSON file path."""
    if not path.exists():
        raise InputValidationError(f"packets file not found: {path}")
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        raise InputValidationError("packets file is empty")
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
        if isinstance(data, list):
            packets = [str(item).strip() for item in data if str(item).strip()]
        elif isinstance(data, dict) and "packets_hex" in data:
            packets = [str(item).strip() for item in data["packets_hex"] if str(item).strip()]
        else:
            raise InputValidationError(
                "JSON file must be a list of hex strings or an object with 'packets_hex'"
            )
        return packets
    return [line.strip() for line in raw.splitlines() if line.strip() and not line.startswith("#")]


def _result_to_dict(result: CrcReverseResult) -> dict[str, int | bool | str]:
    """Serialize one candidate result into a JSON-friendly dictionary."""
    return {
        "poly_int": result.poly,
        "poly_hex": hex(result.poly),
        "width": result.width,
        "seed_int": result.seed,
        "seed_hex": hex(result.seed),
        "ref_in": result.ref_in,
        "ref_out": result.ref_out,
        "xor_out_int": result.xor_out,
        "xor_out_hex": hex(result.xor_out),
    }


def _print_human_results(results: Sequence[CrcReverseResult]) -> None:
    """Render candidate results in a concise human-readable format."""
    if not results:
        print("No candidates were found.")
        return
    print(f"Found {len(results)} candidate(s):")
    for idx, item in enumerate(results, start=1):
        print(
            f"[{idx}] poly={hex(item.poly)} width={item.width} seed={hex(item.seed)} "
            f"ref_in={item.ref_in} ref_out={item.ref_out} xor_out={hex(item.xor_out)}"
        )


def build_parser() -> argparse.ArgumentParser:
    """Create and configure the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="crc-reverse",
        description="Reverse engineer CRC parameters from packet samples.",
    )
    parser.add_argument(
        "--crc-width",
        type=int,
        help="Known CRC width in bits (required for non-interactive mode).",
    )
    parser.add_argument(
        "--packets-file",
        type=Path,
        help="Path to packet file (.txt lines or .json list/object with packets_hex).",
    )
    parser.add_argument(
        "--packet-hex",
        action="append",
        default=[],
        help="Packet sample as concatenated hex data+crc (repeatable).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show algorithm internal logs during reversal.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Print results as JSON.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Force legacy interactive mode.",
    )
    return parser


def run_cli(args: argparse.Namespace) -> int:
    """Execute CLI logic from parsed argparse namespace values."""
    if args.interactive or (args.crc_width is None and not args.packet_hex and args.packets_file is None):
        results = reverse_crc_interactive()
    else:
        if args.crc_width is None:
            raise InputValidationError("--crc-width is required in non-interactive mode")
        packet_values: list[str] = list(args.packet_hex)
        if args.packets_file is not None:
            packet_values.extend(_load_hex_packets_from_file(args.packets_file))
        if not packet_values:
            raise InputValidationError("no packets supplied; use --packet-hex or --packets-file")
        results = reverse_crc_from_hex_packets(
            packet_values,
            crc_width=args.crc_width,
            verbose=bool(args.verbose),
        )
    if args.json_output:
        payload = {
            "status": "ok",
            "candidate_count": len(results),
            "candidates": [_result_to_dict(item) for item in results],
        }
        print(json.dumps(payload, indent=2))
    else:
        _print_human_results(results)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint returning process-style exit codes."""
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        return run_cli(args)
    except (InputValidationError, PacketFormatError, ReversalFailureError) as exc:
        parser.error(str(exc))
    return 2
