# Adding A New Reversing Method

This guide explains how to add a new polynomial/parameter estimation method.

## 1) Create a method module

Add a module under `src/crc_reverse/`:

- Example name: `polynomial_reversing_method_3.py`
- Include type annotations and docstrings.

## 2) Define method contract

Match existing shape:

```python
def estimate_poly_over_all_packets_method_3(
    first_step_packets: list[list[bytes]],
    crc_width: int,
) -> tuple[list[int], Any]:
    ...
```

## 3) Integrate into pipeline

Wire method into `run_reversal_pipeline` in `src/crc_reverse/crc_reversing.py`:

- execute method
- print optional ranking output
- merge with other candidate lists

## 4) Add tests

- Unit tests for internal helpers.
- Integration test using a fixture under `tests/fixtures/`.
- Add property checks if method is algebra-heavy.

## 5) Update docs

- Mention method in `README.md`.
- Update architecture docs if data flow changes.

## 6) Validate

```bash
python -m pyright
python -m pytest
```
