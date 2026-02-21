"""Typed request models used by API/CLI layers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from .errors import InputValidationError, PacketFormatError

MIN_CRC_WIDTH = 8
MAX_CRC_WIDTH = 128
MIN_PACKETS = 2
MAX_PACKETS = 1000


@dataclass(frozen=True)
class PacketSample:
    """Single packet sample represented as a normalized hexadecimal string."""

    hex_value: str

    def __post_init__(self) -> None:
        """Normalize and validate packet hex content after dataclass construction."""
        normalized = self.hex_value.strip().lower()
        if not normalized:
            raise PacketFormatError("packet hex string cannot be empty")
        if len(normalized) % 2 != 0:
            raise PacketFormatError("hex packet length must be an even number of characters")
        try:
            bytes.fromhex(normalized)
        except ValueError as exc:
            raise PacketFormatError(f"invalid hex packet: {self.hex_value!r}") from exc
        object.__setattr__(self, "hex_value", normalized)

    @property
    def as_bytes(self) -> bytes:
        """Binary representation of this packet sample."""
        return bytes.fromhex(self.hex_value)


@dataclass(frozen=True)
class ReverseConfig:
    """Execution configuration for CRC reversing."""

    crc_width: int
    verbose: bool = False

    def __post_init__(self) -> None:
        """Validate reverse configuration boundaries and value types."""
        if not isinstance(self.crc_width, int):
            raise InputValidationError("crc_width must be an integer")
        if not (MIN_CRC_WIDTH <= self.crc_width <= MAX_CRC_WIDTH):
            raise InputValidationError(
                f"crc_width must be between {MIN_CRC_WIDTH} and {MAX_CRC_WIDTH}"
            )


@dataclass(frozen=True)
class ReverseRequest:
    """Validated request model for packet-based reverse operations."""

    packets: tuple[PacketSample, ...] = field(default_factory=tuple)
    config: ReverseConfig = field(default_factory=lambda: ReverseConfig(crc_width=32))

    def __post_init__(self) -> None:
        """Enforce request-level packet count constraints."""
        if not self.packets:
            raise InputValidationError("at least one packet is required")
        if not (MIN_PACKETS <= len(self.packets) <= MAX_PACKETS):
            raise InputValidationError(
                f"packet count must be between {MIN_PACKETS} and {MAX_PACKETS}"
            )

    @classmethod
    def from_hex_packets(
        cls, packets_hex: Sequence[str], crc_width: int, verbose: bool = False
    ) -> "ReverseRequest":
        """Build a fully validated request model from raw hex packet inputs."""
        samples = tuple(PacketSample(packet) for packet in packets_hex)
        return cls(packets=samples, config=ReverseConfig(crc_width=crc_width, verbose=verbose))
