"""Optional performance helpers (Numba-accelerated when enabled)."""

from __future__ import annotations

import os
from typing import Callable

USE_NUMBA = os.getenv("CRC_REVERSE_USE_NUMBA", "").strip().lower() in {"1", "true", "yes"}


def _poly_mod_py(a: int, b: int) -> int:
    """Pure-Python GF(2) polynomial modulo helper."""
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def _poly_gcd_py(a: int, b: int) -> int:
    """Pure-Python GF(2) polynomial GCD helper."""
    if b > a:
        a, b = b, a
    while b != 0:
        a, b = b, _poly_mod_py(a, b)
    return a


poly_mod_fast: Callable[[int, int], int] = _poly_mod_py
poly_gcd_fast: Callable[[int, int], int] = _poly_gcd_py
NUMBA_ENABLED = False

if USE_NUMBA:
    try:
        from numba import njit  # type: ignore[import-not-found]

        @njit(cache=True)
        def _poly_mod_numba(a: int, b: int) -> int:  # pragma: no cover - optional branch
            """Numba-accelerated GF(2) polynomial modulo helper."""
            while a.bit_length() >= b.bit_length():
                a ^= b << (a.bit_length() - b.bit_length())
            return a

        @njit(cache=True)
        def _poly_gcd_numba(a: int, b: int) -> int:  # pragma: no cover - optional branch
            """Numba-accelerated GF(2) polynomial GCD helper."""
            if b > a:
                a, b = b, a
            while b != 0:
                a, b = b, _poly_mod_numba(a, b)
            return a

        poly_mod_fast = _poly_mod_numba
        poly_gcd_fast = _poly_gcd_numba
        NUMBA_ENABLED = True
    except Exception:
        # Fall back to pure Python path if numba is unavailable.
        NUMBA_ENABLED = False
