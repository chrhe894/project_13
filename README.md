# project_13

Ett utforskande projekt kring en lärande Stryktipsapplikation i Python.
Målbilden och utgångsläget finns i [docs/IDEAL_STATE.md](docs/IDEAL_STATE.md)
och [docs/IDENTITY.md](docs/IDENTITY.md).

Arbetet drivs genom the_engine, där konkreta mål och uppdrag växer fram.
Målbilden låser inte datakällor, arkitektur, lagringslösning, Pythonbibliotek
eller gränssnitt i förväg. Därför har projektet inga beroenden utöver Pythons
standardbibliotek. Bara testverktyget pytest behövs, och bara för utveckling.

## Kom igång

Utvecklat och provat med Python 3.14.

```
python -m venv .venv
```

Aktivera miljön:

- Windows (PowerShell): `.venv\Scripts\Activate.ps1`
- Windows (Git Bash): `source .venv/Scripts/activate`
- macOS och Linux: `source .venv/bin/activate`

```
pip install -r requirements-dev.txt
```

## Köra

```
python -m project_13
```

## Läsa in en omgång

Kopiera omgången från Stryktipset-sidan, spara texten i en fil och kör:

```
python -m project_13 read-round omgang.txt --out data/omgang.json
```

Omgång (till exempel `2026-W47`) och speldag räknas ut från dagens datum,
eftersom texten inte innehåller dem. Gäller omgången en annan vecka, lägg till
`--week 48`.

Formatet och vad som kontrolleras står i [docs/DATA_FORMAT.md](docs/DATA_FORMAT.md).

## Testa

```
python -m pytest
```

## Struktur

```
project_13/   programkoden (startpunkt: __main__.py)
tests/        tester (exempeltexter från sidan i tests/fixtures/)
docs/         identitet, målbild, första arbetsflödet och dataformat
data/         exempeldata (en omgång kopierad för hand)
```
