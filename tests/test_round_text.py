"""Inläsning av omgången ur text som kopierats från Stryktipset-sidan."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from project_13.round_text import RoundTextError, check_round, parse_round_text

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
SIGNS = ("1", "X", "2")


def fixture(name):
    return (FIXTURES / name).read_text(encoding="utf-8")


def example_matches():
    with open(ROOT / "data" / "example_round.json", encoding="utf-8") as f:
        return json.load(f)["matches"]


# --- det äldre formatet: en rad "Odds" ---------------------------------------

def test_odds_only_text_gives_exactly_the_example_round():
    # data/example_round.json gjordes av samma text, så de ska vara identiska.
    assert parse_round_text(fixture("round_text_odds_only.txt"))["matches"] == example_matches()


def test_odds_only_text_has_no_start_odds():
    for m in parse_round_text(fixture("round_text_odds_only.txt"))["matches"]:
        assert "start_odds" not in m


# --- det nyare formatet: "Aktuellt odds" och "Startodds" ----------------------

def test_current_and_start_odds_are_read_for_all_13_matches():
    matches = parse_round_text(fixture("round_text_with_start_odds.txt"))["matches"]
    assert [m["number"] for m in matches] == list(range(1, 14))
    for m in matches:
        assert tuple(m["odds"]) == SIGNS and tuple(m["start_odds"]) == SIGNS
        assert tuple(m["streck_percent"]) == SIGNS


def test_current_odds_become_odds_and_start_odds_stay_separate():
    first = parse_round_text(fixture("round_text_with_start_odds.txt"))["matches"][0]
    assert (first["home"], first["away"]) == ("Newcastle", "Arsenal")
    assert first["odds"] == {"1": 6.40, "X": 4.40, "2": 1.56}
    assert first["start_odds"] == {"1": 6.00, "X": 4.35, "2": 1.60}
    assert first["streck_percent"] == {"1": 18, "X": 22, "2": 60}


def test_last_match_is_read_too():
    last = parse_round_text(fixture("round_text_with_start_odds.txt"))["matches"][12]
    assert (last["home"], last["away"]) == ("Wolverhampton", "Charlton")
    assert last["odds"] == {"1": 1.35, "X": 5.40, "2": 9.50}
    assert last["start_odds"] == {"1": 1.34, "X": 5.50, "2": 9.50}


def test_a_clean_round_gives_no_warnings():
    assert check_round(parse_round_text(fixture("round_text_with_start_odds.txt"))) == []


# --- tåligt mot hur texten kopierats --------------------------------------------

def test_windows_line_endings_blank_lines_and_spaces_do_not_matter():
    text = fixture("round_text_with_start_odds.txt")
    messy = "\n\n" + text.replace("\n", "\r\n\r\n").replace("18%", "18 %").replace("Newcastle", "Newcastle\u00a0")
    assert parse_round_text(messy) == parse_round_text(text)


def test_text_after_the_last_match_is_ignored():
    text = fixture("round_text_with_start_odds.txt") + "\nSpelstopp\nVälj rader\n"
    assert len(parse_round_text(text)["matches"]) == 13


# --- fel ska bli tydliga, inte gissningar -------------------------------------------

def test_an_incomplete_copy_is_reported_with_the_number_found():
    lines = fixture("round_text_with_start_odds.txt").split("\n")
    cut = lines.index("13")  # allt före match 13
    with pytest.raises(RoundTextError, match="12 matcher"):
        parse_round_text("\n".join(lines[:cut]))


def test_a_broken_line_is_reported_with_its_line_number():
    text = fixture("round_text_with_start_odds.txt").replace("18%", "arton procent", 1)
    with pytest.raises(RoundTextError, match=r"Rad \d+.*arton procent"):
        parse_round_text(text)


def test_missing_separator_between_teams_is_reported():
    text = fixture("round_text_with_start_odds.txt").replace("Newcastle\n-\nArsenal", "Newcastle\nArsenal\nArsenal", 1)
    with pytest.raises(RoundTextError, match="mellan lagen"):
        parse_round_text(text)


def test_a_match_without_any_odds_is_reported():
    text = fixture("round_text_with_start_odds.txt").replace("Aktuellt odds\n6,40\n4,40\n1,56\n", "", 1)
    with pytest.raises(RoundTextError, match="Aktuellt odds"):
        parse_round_text(text)


def test_matches_out_of_order_are_reported():
    text = fixture("round_text_with_start_odds.txt").replace("\n2\nChelsea", "\n3\nChelsea", 1)
    with pytest.raises(RoundTextError, match="matchnummer 2"):
        parse_round_text(text)


def test_empty_text_is_reported():
    with pytest.raises(RoundTextError, match="inga matcher"):
        parse_round_text("   \n\n")


def test_without_an_expected_count_as_many_matches_as_exist_are_read():
    lines = fixture("round_text_with_start_odds.txt").split("\n")
    partial = "\n".join(lines[:lines.index("13")])
    assert len(parse_round_text(partial, expected_matches=None)["matches"]) == 12


def test_check_round_warns_about_strange_values():
    data = parse_round_text(fixture("round_text_with_start_odds.txt"))
    data["matches"][0]["odds"]["1"] = 0.9
    data["matches"][1]["streck_percent"]["1"] = 20
    warnings = check_round(data)
    assert len(warnings) == 2
    assert any("Match 1" in w and "odds" in w for w in warnings)
    assert any("Match 2" in w and "summerar" in w for w in warnings)


# --- kommandot ------------------------------------------------------------------------

def run(*args):
    return subprocess.run([sys.executable, "-m", "project_13", *args], cwd=ROOT,
                          capture_output=True, text=True, encoding="utf-8", timeout=30)


def test_read_round_writes_json_with_label_source_and_read_at(tmp_path):
    out = tmp_path / "omgang.json"
    result = run("read-round", str(FIXTURES / "round_text_with_start_odds.txt"),
                 "--out", str(out), "--label", "Testomgång")
    assert result.returncode == 0, result.stderr
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["label"] == "Testomgång"
    assert "Svenska Spel" in data["source"]
    assert data["read_at"]
    assert len(data["matches"]) == 13


def test_read_round_prints_json_to_the_screen_without_out():
    result = run("read-round", str(FIXTURES / "round_text_odds_only.txt"))
    assert result.returncode == 0
    assert len(json.loads(result.stdout)["matches"]) == 13


def test_read_round_fails_clearly_on_bad_text(tmp_path):
    bad = tmp_path / "bad.txt"
    bad.write_text("1\nNewcastle\nArsenal\n", encoding="utf-8")
    result = run("read-round", str(bad))
    assert result.returncode == 2
    assert "Kunde inte läsa in omgången" in result.stderr and "Rad" in result.stderr


def test_read_round_fails_clearly_on_a_missing_file(tmp_path):
    result = run("read-round", str(tmp_path / "finns_inte.txt"))
    assert result.returncode == 2 and "Kunde inte läsa" in result.stderr


def test_without_a_command_the_version_is_still_printed():
    result = run()
    assert result.returncode == 0 and result.stdout.startswith("project_13 ")


@pytest.mark.parametrize("encoding", ["utf-8-sig", "cp1252"])
def test_read_round_accepts_files_saved_with_bom_or_windows_encoding(tmp_path, encoding):
    source = tmp_path / "omgang.txt"
    source.write_bytes(fixture("round_text_with_start_odds.txt").encode(encoding))
    result = run("read-round", str(source))
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert len(data["matches"]) == 13 and data["matches"][0]["home"] == "Newcastle"


def test_read_round_rejects_a_file_in_an_unknown_encoding(tmp_path):
    source = tmp_path / "konstig.txt"
    source.write_bytes(b"\x81\x8d\x8f\x90\x9d")
    result = run("read-round", str(source))
    assert result.returncode == 2 and "teckenkodning" in result.stderr
