"""Varje test som docs/REQUIREMENTS.md hänvisar till ska finnas."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_every_test_named_in_requirements_exists():
    doc = (ROOT / "docs" / "REQUIREMENTS.md").read_text(encoding="utf-8")
    named = set(re.findall(r"`(test_\w+)`", doc))
    source = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "tests").glob("test_*.py"))
    defined = set(re.findall(r"^def (test_\w+)", source, re.MULTILINE))
    assert named, "inga tester angivna"
    assert not named - defined, f"saknas: {sorted(named - defined)}"
