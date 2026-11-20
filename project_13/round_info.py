"""Omgångens vecka och speldag, uträknade i stället för inlästa.

Texten som kopieras från Stryktipset-sidan säger inte vilken omgång det gäller.
Här räknas den ut, med två antaganden som ägaren har bestämt:

- en omgång namnges efter veckan, som ISO-vecka, till exempel "2026-W47"
- spelet körs på lördagar

Omgången är alltså veckan för närmaste lördag, räknat från och med den dag
texten läses in. Svenska Spel har också ett eget omgångsnummer, men det finns inte
i den kopierade texten och används inte här.

Bara standardbiblioteket används.
"""

import re
from datetime import date, timedelta

SATURDAY = 5  # date.weekday(): måndag är 0

_WEEK = re.compile(r"(?:(\d{4})-)?W?(\d{1,2})", re.IGNORECASE)


def next_draw_date(read_date: date) -> date:
    """Närmaste lördag, från och med read_date (en lördag ger samma dag)."""
    return read_date + timedelta(days=(SATURDAY - read_date.weekday()) % 7)


def round_name(draw_date: date) -> str:
    """ISO-veckan för ett datum, som '2026-W47'."""
    year, week, _ = draw_date.isocalendar()
    return f"{year}-W{week:02d}"


def draw_date_for_week(year: int, week: int) -> date:
    """Lördagen i en ISO-vecka. Ogiltig vecka ger ValueError."""
    return date.fromisocalendar(year, week, SATURDAY + 1)


def parse_week(text: str, default_year: int) -> tuple:
    """Läser '47', 'W47', '2026-W47' eller '2026-47' till (år, vecka).

    Utan år används default_year. Ogiltigt värde ger ValueError.
    """
    m = _WEEK.fullmatch(text.strip())
    if not m:
        raise ValueError(f"Förstod inte veckan '{text}'. Skriv till exempel 47 eller 2026-W47.")
    year = int(m.group(1)) if m.group(1) else default_year
    week = int(m.group(2))
    draw_date_for_week(year, week)  # kastar ValueError om veckan inte finns det året
    return year, week


def round_info(read_date: date, week: str = None) -> dict:
    """{"round": "2026-W47", "draw_date": "2026-11-21"}.

    Utan `week` räknas den ut från inläsningsdagen. Med `week` (se parse_week) används den.
    """
    if week:
        year, number = parse_week(week, read_date.isocalendar()[0])
        draw = draw_date_for_week(year, number)
    else:
        draw = next_draw_date(read_date)
    return {"round": round_name(draw), "draw_date": draw.isoformat()}
