"""Exempelomgången följer formatet i docs/DATA_FORMAT.md."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIGNS = ("1", "X", "2")


def load_example():
    with open(ROOT / "data" / "example_round.json", encoding="utf-8") as f:
        return json.load(f)


def test_round_has_13_numbered_matches():
    matches = load_example()["matches"]
    assert [m["number"] for m in matches] == list(range(1, 14))


def test_every_match_has_teams_and_all_three_signs():
    for m in load_example()["matches"]:
        assert m["home"].strip() and m["away"].strip()
        assert tuple(m["odds"]) == SIGNS
        assert tuple(m["streck_percent"]) == SIGNS


def test_odds_are_decimal_numbers_above_one():
    for m in load_example()["matches"]:
        for sign in SIGNS:
            assert isinstance(m["odds"][sign], float) and m["odds"][sign] > 1


def test_streck_percent_are_whole_percent_that_roughly_add_up_to_100():
    # Procenten är avrundade heltal, så summan kan avvika något från 100.
    for m in load_example()["matches"]:
        values = [m["streck_percent"][s] for s in SIGNS]
        assert all(isinstance(v, int) and 0 <= v <= 100 for v in values)
        assert 98 <= sum(values) <= 102
