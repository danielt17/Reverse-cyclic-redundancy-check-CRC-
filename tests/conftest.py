import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture(scope="session")
def crc40_golden_fixture() -> dict[str, Any]:
    fixture_path = Path(__file__).resolve().parent / "fixtures" / "crc40_golden.json"
    return json.loads(fixture_path.read_text(encoding="utf-8"))
