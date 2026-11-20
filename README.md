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

## Testa

```
python -m pytest
```

## Struktur

```
project_13/   programkoden (startpunkt: __main__.py)
tests/        tester
docs/         identitet och målbild
```
