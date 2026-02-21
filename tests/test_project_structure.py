from pathlib import Path


def test_expected_project_layout_exists() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    expected_paths = [
        repo_root / "src" / "crc_reverse" / "__init__.py",
        repo_root / "src" / "crc_reverse" / "api.py",
        repo_root / "src" / "crc_reverse" / "cli.py",
        repo_root / "src" / "crc_reverse" / "models.py",
        repo_root / "src" / "crc_reverse" / "errors.py",
        repo_root / "src" / "crc_reverse" / "performance.py",
        repo_root / "pyproject.toml",
        repo_root / "requirements.txt",
        repo_root / ".pre-commit-config.yaml",
        repo_root / "Dockerfile",
        repo_root / ".dockerignore",
        repo_root / ".devcontainer" / "devcontainer.json",
        repo_root / "docs" / "ARCHITECTURE.md",
        repo_root / "docs" / "ALGORITHM_FLOW.md",
        repo_root / "docs" / "ADDING_METHOD.md",
        repo_root / "release-please-config.json",
        repo_root / ".release-please-manifest.json",
        repo_root / "CHANGELOG.md",
        repo_root / "CITATION.cff",
        repo_root / "CONTRIBUTING.md",
        repo_root / "CODE_OF_CONDUCT.md",
        repo_root / "SECURITY.md",
        repo_root / "SUPPORT.md",
        repo_root / ".github" / "CODEOWNERS",
        repo_root / ".github" / "dependabot.yml",
        repo_root / ".github" / "workflows" / "ci.yml",
        repo_root / ".github" / "workflows" / "codeql.yml",
        repo_root / ".github" / "workflows" / "release.yml",
        repo_root / ".github" / "workflows" / "release-please.yml",
        repo_root / ".github" / "pull_request_template.md",
        repo_root / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml",
        repo_root / ".github" / "ISSUE_TEMPLATE" / "feature_request.yml",
        repo_root / ".github" / "ISSUE_TEMPLATE" / "config.yml",
        repo_root / "tests" / "test_api.py",
        repo_root / "tests" / "test_cli.py",
        repo_root / "tests" / "test_math_utils.py",
        repo_root / "tests" / "test_api_stability.py",
        repo_root / "tests" / "test_input_validation.py",
        repo_root / "tests" / "test_performance_path.py",
        repo_root / "tests" / "test_property_math.py",
        repo_root / "tests" / "fixtures" / "crc40_golden.json",
        repo_root / "tests" / "benchmarks" / "test_benchmark_reversal.py",
    ]
    missing = [path for path in expected_paths if not path.exists()]
    assert not missing, f"Missing required project paths: {missing}"


def test_package_exports_required_api() -> None:
    import crc_reverse

    required_exports = [
        "CrcReverseResult",
        "CrcReverseError",
        "InputValidationError",
        "PacketFormatError",
        "ReversalFailureError",
        "PacketSample",
        "ReverseConfig",
        "ReverseRequest",
        "crc_reversing",
        "reverse_crc_from_hex_packets",
        "reverse_crc_from_packets",
        "reverse_crc_interactive",
        "run_reversal_pipeline",
    ]
    missing = [name for name in required_exports if not hasattr(crc_reverse, name)]
    assert not missing, f"Missing expected public exports: {missing}"
