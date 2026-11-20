"""Läser in en omgång ur text som kopierats från Svenska Spels Stryktipset-sida.

Ingen hämtning från nätet sker här. Du kopierar texten själv i webbläsaren och
sparar den i en fil. Funktionerna gör om den till formatet i docs/DATA_FORMAT.md.

Bara standardbiblioteket används.

Sidan har visat oddsen på två sätt, och båda går att läsa in:
- en rad "Odds" med tre värden (1, X, 2)
- raderna "Aktuellt odds" och "Startodds", var och en med tre värden

"Aktuellt odds" och "Odds" blir `odds`, och "Startodds" blir `start_odds`.
Om texten inte ser ut som väntat ges ett tydligt felmeddelande med radnummer,
i stället för att programmet gissar.
"""

import re

SIGNS = ("1", "X", "2")
EXPECTED_MATCHES = 13

_SEPARATORS = {"-", "\u2013", "\u2014"}
_ODDS_LABELS = {"odds": "odds", "aktuellt odds": "odds", "startodds": "start_odds"}
_PERCENT = re.compile(r"(\d{1,3})\s*%")
_DECIMAL = re.compile(r"\d+(?:[.,]\d+)?")
_TIPINFO = re.compile(r"tipsinformation för match nummer (\d+)", re.IGNORECASE)


class RoundTextError(ValueError):
    """Texten kunde inte läsas in. Meddelandet säger var och varför."""


class _Reader:
    def __init__(self, text):
        # Tomma rader hoppas över, men radnumren i felmeddelanden är originalets.
        self.items = [(no, line.replace("\u00a0", " ").strip())
                      for no, line in enumerate(text.splitlines(), 1) if line.strip()]
        self.pos = 0
        self.lineno = 0

    def peek(self):
        return self.items[self.pos][1] if self.pos < len(self.items) else None

    def take(self, what):
        if self.pos >= len(self.items):
            raise RoundTextError(f"Texten tar slut innan {what}.")
        self.lineno, line = self.items[self.pos]
        self.pos += 1
        return line

    def fail(self, expected, found):
        raise RoundTextError(f"Rad {self.lineno}: väntade {expected}, men fann '{found}'.")

    def expect(self, value, what=None):
        line = self.take(what or f"'{value}'")
        if line != value:
            self.fail(what or f"'{value}'", line)

    def three_values(self, parse, what):
        values = []
        for sign in SIGNS:
            values.append(parse(self.take(f"{what} för {sign}")))
        return dict(zip(SIGNS, values))


def _percent(reader):
    def parse(line):
        m = _PERCENT.fullmatch(line)
        if not m:
            reader.fail("en procentsiffra som '18%'", line)
        return int(m.group(1))
    return parse


def _decimal(reader):
    def parse(line):
        if not _DECIMAL.fullmatch(line):
            reader.fail("ett odds som '1,57'", line)
        return float(line.replace(",", "."))
    return parse


def _read_match(reader, number):
    line = reader.take(f"matchnummer {number}")
    if not line.isdigit() or int(line) != number:
        reader.fail(f"matchnummer {number}", line)
    home = reader.take("hemmalaget")
    separator = reader.take("ett streck mellan lagen")
    if separator not in _SEPARATORS:
        reader.fail("ett '-' mellan lagen", separator)
    away = reader.take("bortalaget")
    for sign in SIGNS:
        reader.expect(sign)
    info = reader.take("raden 'Tipsinformation för match nummer ...'")
    m = _TIPINFO.fullmatch(info)
    if not m or int(m.group(1)) != number:
        reader.fail(f"'Tipsinformation för match nummer {number}'", info)
    reader.expect("Tipsinfo")
    for sign in SIGNS:
        reader.expect(sign)
    reader.expect("Svenska folket")
    streck = reader.three_values(_percent(reader), "streckprocent")

    match = {"number": number, "home": home, "away": away}
    found = {}
    while (reader.peek() or "").lower() in _ODDS_LABELS:
        label = reader.take("oddsrubriken")
        key = _ODDS_LABELS[label.lower()]
        if key in found:
            reader.fail("en rubrik som inte redan använts för den här matchen", label)
        found[key] = reader.three_values(_decimal(reader), f"{label.lower()}")
    if "odds" not in found:
        raise RoundTextError(f"Match {number} ({home} - {away}): hittade ingen rad med 'Odds' eller 'Aktuellt odds'.")
    match["odds"] = found["odds"]
    if "start_odds" in found:
        match["start_odds"] = found["start_odds"]
    match["streck_percent"] = streck
    return match


def parse_round_text(text, expected_matches=EXPECTED_MATCHES):
    """Gör om inklistrad text till {"matches": [...]}.

    `expected_matches` är hur många matcher som ska finnas (13 för Stryktipset).
    Sätt None för att läsa så många matcher som finns. Är antalet fel är det ofta
    ett tecken på att kopieringen blev ofullständig, och då ges ett fel.
    """
    reader = _Reader(text)
    matches = []
    while reader.peek() is not None:
        number = len(matches) + 1
        if expected_matches is not None and number > expected_matches:
            break  # text efter sista matchen ignoreras
        if expected_matches is None and not (reader.peek().isdigit() and int(reader.peek()) == number):
            break
        matches.append(_read_match(reader, number))
    if not matches:
        raise RoundTextError("Hittade inga matcher i texten.")
    if expected_matches is not None and len(matches) != expected_matches:
        raise RoundTextError(f"Hittade {len(matches)} matcher, men väntade {expected_matches}. "
                             "Kopierade du hela omgången?")
    return {"matches": matches}


def check_round(data, expected_matches=EXPECTED_MATCHES):
    """Ger varningar (inte fel) om något ser konstigt ut. Tom lista betyder att inget märktes."""
    warnings = []
    matches = data.get("matches", [])
    if expected_matches is not None and len(matches) != expected_matches:
        warnings.append(f"{len(matches)} matcher i stället för {expected_matches}.")
    for m in matches:
        who = f"Match {m['number']} ({m['home']} - {m['away']})"
        for name in ("odds", "start_odds"):
            for sign, value in m.get(name, {}).items():
                if value <= 1:
                    warnings.append(f"{who}: {name} för {sign} är {value}, väntade över 1.")
        total = sum(m["streck_percent"].values())
        if not 98 <= total <= 102:
            warnings.append(f"{who}: streckprocenten summerar till {total}, väntade ungefär 100.")
    return warnings
