"""Omgång och speldag räknas ut ur datum (project_13/round_info.py)."""
import json
import re
from datetime import date
from pathlib import Path

import pytest

from project_13.__main__ import main
from project_13.round_info import draw_date_for_week, next_draw_date, parse_week, round_info, round_name

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "round_text_odds_only.txt"


def test_next_draw_date_is_the_coming_saturday_for_every_weekday():
    # 2026-11-16 är en måndag
    expected = date(2026, 11, 21)
    for day in range(16, 22):
        assert next_draw_date(date(2026, 11, day)) == expected
    assert next_draw_date(date(2026, 11, 22)) == date(2026, 11, 28)  # söndag


def test_round_name_and_week_53():
    assert round_name(date(2026, 11, 21)) == "2026-W47"
    assert round_name(date(2027, 1, 2)) == "2026-W53"


def test_parse_week_variants():
    assert parse_week("47", 2026) == (2026, 47)
    assert parse_week("W47", 2026) == (2026, 47)
    assert parse_week("2027-W03", 2026) == (2027, 3)
    assert parse_week(" 2026-47 ", 2025) == (2026, 47)


@pytest.mark.parametrize("bad", ["", "abc", "0", "54", "2026-W54", "47a"])
def test_parse_week_rejects_bad_input(bad):
    with pytest.raises(ValueError):
        parse_week(bad, 2026)


def test_round_info_computed_and_overridden():
    assert round_info(date(2026, 11, 20)) == {"round": "2026-W47", "draw_date": "2026-11-21"}
    assert round_info(date(2026, 11, 20), "48") == {"round": "2026-W48", "draw_date": "2026-11-28"}
    assert draw_date_for_week(2026, 47) == date(2026, 11, 21)


def test_cli_adds_round_and_draw_date(tmp_path):
    out = tmp_path / "r.json"
    assert main(["read-round", str(FIXTURE), "--out", str(out), "--week", "2026-W47"]) == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["round"] == "2026-W47"
    assert data["draw_date"] == "2026-11-21"


def test_cli_default_draw_date_is_a_saturday(tmp_path):
    out = tmp_path / "r.json"
    assert main(["read-round", str(FIXTURE), "--out", str(out)]) == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert date.fromisoformat(data["draw_date"]).weekday() == 5
    assert data["round"] == round_name(date.fromisoformat(data["draw_date"]))


def test_cli_bad_week_exits_2(tmp_path, capsys):
    out = tmp_path / "r.json"
    assert main(["read-round", str(FIXTURE), "--out", str(out), "--week", "99"]) == 2
    assert not out.exists()


def test_example_round_has_round_and_saturday():
    data = json.loads((ROOT / "data" / "example_round.json").read_text(encoding="utf-8"))
    assert re.fullmatch(r"\d{4}-W\d{2}", data["round"])
    draw = date.fromisoformat(data["draw_date"])
    assert draw.weekday() == 5
    assert round_name(draw) == data["round"]


def test_cli_week_overrides_the_computed_round(tmp_path):
    # 2020-W10 kan aldrig vara veckan för närmaste lördag från idag
    out = tmp_path / "r.json"
    assert main(["read-round", str(FIXTURE), "--out", str(out), "--week", "2020-W10"]) == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["round"] == "2020-W10"
    assert data["draw_date"] == "2020-03-07"
