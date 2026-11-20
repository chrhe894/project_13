"""Startpunkt: python -m project_13

    python -m project_13                          visar version
    python -m project_13 read-round FIL [--out UT.json] [--label TEXT] [--week 47]
                                                  läser in en omgång ur text som
                                                  kopierats från Stryktipset-sidan
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from project_13 import __version__
from project_13.round_info import round_info
from project_13.round_text import RoundTextError, check_round, parse_round_text

SOURCE = "Svenska Spel, Stryktipset (text kopierad från sidan)"


def _use_utf8_output() -> None:
    """Skriv alltid UTF-8, så att å, ä och ö klarar rör och Windows kodsidor."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def read_round(args) -> int:
    try:
        raw = Path(args.file).read_bytes()
    except OSError as e:
        print(f"Kunde inte läsa {args.file}: {e}", file=sys.stderr)
        return 2
    # Anteckningar sparas ibland med BOM eller i Windows-teckenkodning, så båda prövas.
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        print(f"Kunde inte läsa {args.file}: okänd teckenkodning. Spara filen som UTF-8.", file=sys.stderr)
        return 2
    try:
        data = parse_round_text(text)
    except RoundTextError as e:
        print(f"Kunde inte läsa in omgången: {e}", file=sys.stderr)
        return 2
    now = datetime.now()
    try:
        info = round_info(now.date(), args.week)
    except ValueError as e:
        print(f"Kunde inte räkna ut omgången: {e}", file=sys.stderr)
        return 2
    result = {
        "label": args.label,
        "source": SOURCE,
        "round": info["round"],
        "draw_date": info["draw_date"],
        "read_at": now.isoformat(timespec="seconds"),
        "matches": data["matches"],
    }
    for warning in check_round(result):
        print(f"Varning: {warning}", file=sys.stderr)
    out = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8", newline="\n")
        print(f"{len(result['matches'])} matcher sparade i {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(out)
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="project_13")
    sub = parser.add_subparsers(dest="command")
    rr = sub.add_parser("read-round", help="läs in en omgång ur kopierad text")
    rr.add_argument("file", help="textfil med det du kopierat från Stryktipset-sidan")
    rr.add_argument("--out", help="skriv JSON hit i stället för till skärmen")
    rr.add_argument("--label", default="Omgång inläst från kopierad text",
                    help="beskrivning av omgången (fältet label)")
    rr.add_argument("--week", help="omgångens vecka, till exempel 47 eller 2026-W47 "
                    "(annars närmaste lördag från idag)")
    args = parser.parse_args(argv or [])
    if args.command == "read-round":
        return read_round(args)
    print(f"project_13 {__version__}")
    return 0


if __name__ == "__main__":
    _use_utf8_output()
    raise SystemExit(main(sys.argv[1:]))
