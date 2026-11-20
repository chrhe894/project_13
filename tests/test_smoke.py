"""Rökprov: projektet går att importera och starta."""

import subprocess
import sys
from pathlib import Path

import project_13
from project_13.__main__ import main

ROOT = Path(__file__).resolve().parent.parent


def test_version_is_set():
    assert project_13.__version__


def test_main_returns_zero_and_prints_name_and_version(capsys):
    assert main() == 0
    out = capsys.readouterr().out
    assert "project_13" in out
    assert project_13.__version__ in out


def test_runs_as_a_module():
    result = subprocess.run(
        [sys.executable, "-m", "project_13"],
        cwd=ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0
    assert "project_13" in result.stdout
