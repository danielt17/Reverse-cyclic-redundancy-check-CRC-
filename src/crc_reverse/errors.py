"""Project-specific exception types."""


class CrcReverseError(Exception):
    """Base class for CRC reverse-engineering errors."""


class InputValidationError(CrcReverseError, ValueError):
    """Raised when user input is invalid."""


class PacketFormatError(InputValidationError):
    """Raised when packet content/representation is invalid."""


class ReversalFailureError(CrcReverseError):
    """Raised when CRC reversal cannot produce candidates."""
