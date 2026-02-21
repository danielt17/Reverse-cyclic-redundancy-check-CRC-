# Contributing

Thanks for contributing to this project.

## Development setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -e ".[dev]"
```

3. Run tests:

```bash
python -m pytest
```

## Code changes

- Keep changes focused and small when possible.
- Add or update tests for behavioral changes.
- Preserve backwards compatibility for public API in `src/crc_reverse/__init__.py` when possible.
- Update documentation (`README.md`) when usage changes.

## Pull requests

- Use a clear title and explain why the change is needed.
- Include a short validation section with executed commands.
- Link related issues.
- Ensure CI passes before requesting review.

## Reporting bugs

Use the Bug Report issue form and include:

- Expected behavior
- Actual behavior
- Minimal reproducible example
- Python version and OS
