import json
from pathlib import Path

import pytest
from typing import cast

from crc_reverse.cli import main


def test_cli_non_interactive_json_output(
    capsys: pytest.CaptureFixture[str], tmp_path: Path, crc40_golden_fixture: dict[str, object]
) -> None:
    fixture_packets = cast(list[str], crc40_golden_fixture["packets_hex"])
    file_path = tmp_path / "packets.json"
    file_path.write_text(json.dumps({"packets_hex": fixture_packets}), encoding="utf-8")
    exit_code = main(
        [
            "--crc-width",
            str(crc40_golden_fixture["crc_width"]),
            "--packets-file",
            str(file_path),
            "--json",
        ]
    )
    assert exit_code == 0
    stdout = capsys.readouterr().out
    payload = json.loads(stdout)
    assert payload["status"] == "ok"
    assert payload["candidate_count"] >= 1
    assert any(item["poly_hex"] == "0x4820009" for item in payload["candidates"])
