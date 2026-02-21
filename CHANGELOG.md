# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project follows Semantic Versioning.

## [Unreleased]

### Added

- Standard `src/` package layout (`crc_reverse`).
- Public API for programmatic CRC reversal (`reverse_crc_from_packets`, `reverse_crc_from_hex_packets`).
- CLI improvements:
  - non-interactive mode (`--crc-width`, `--packets-file`, `--packet-hex`)
  - machine-readable output (`--json`)
- Pytest test suite including end-to-end sample verification.
- Property-based tests (Hypothesis), input-fuzz validation tests, and benchmark tests.
- Golden fixture dataset under `tests/fixtures/`.
- API stability tests for public exports/signatures.
- Strict typed models (`PacketSample`, `ReverseConfig`, `ReverseRequest`).
- Project-specific error hierarchy (`InputValidationError`, `PacketFormatError`, `ReversalFailureError`).
- Optional performance path with Numba acceleration toggle (`CRC_REVERSE_USE_NUMBA=1`).
- GitHub CI workflow for automated testing.
- Release automation:
  - `release-please` workflow/config
  - tag-based publish workflow
- Pre-commit hooks with ruff/black/pyright/pytest.
- Developer environment support:
  - `Dockerfile`
  - `.devcontainer/devcontainer.json`
- Architecture/method extension docs under `docs/`.
- Governance and community files:
  - `CONTRIBUTING.md`
  - `CODE_OF_CONDUCT.md`
  - `SECURITY.md`
  - `SUPPORT.md`
  - issue/PR templates
  - CODEOWNERS
  - Dependabot
  - CodeQL workflow
