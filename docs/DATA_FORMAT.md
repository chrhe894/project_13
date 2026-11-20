# DATA FORMAT -- Format för en omgång (steg 1)

**Version:** 0.2 (utkast)\
**Status:** Gäller manuell inmatning i steg 1, se [FIRST_WORKFLOW.md](FIRST_WORKFLOW.md).

En omgång är en JSON-fil. JSON valdes eftersom det ingår i Pythons
standardbibliotek, så formatet kräver inget bibliotek. Målbilden låser inte
bibliotek i förväg, och formatet kan bytas senare.

Ett exempel finns i [../data/example_round.json](../data/example_round.json).

## Struktur

```json
{
  "label": "fritext som beskriver omgången",
  "source": "var uppgifterna kommer ifrån",
  "round": "2026-W47",
  "draw_date": "2026-11-21",
  "read_at": "2026-11-20T15:30:00",
  "matches": [
    {
      "number": 1,
      "home": "Newcastle",
      "away": "Arsenal",
      "odds": { "1": 6.4, "X": 4.4, "2": 1.56 },
      "start_odds": { "1": 6.0, "X": 4.35, "2": 1.6 },
      "streck_percent": { "1": 18, "X": 22, "2": 60 }
    }
  ]
}
```

## Fält

| Fält | Typ | Betydelse |
|---|---|---|
| `label` | text | Beskrivning av omgången. |
| `source` | text | Varifrån uppgifterna kommer. |
| `round` | text | Omgångens namn: ISO-veckan för speldagen, som `2026-W47`. Räknas ut, se nedan. |
| `draw_date` | text | Speldagen (en lördag) som datum, `2026-11-21`. Räknas ut. |
| `read_at` | text (valfri) | När uppgifterna lästes in, som datum och tid. Oddsen ändras över veckan, så tidpunkten är värd att spara. |
| `matches` | lista | Exakt 13 matcher, i kupongens ordning. |
| `number` | heltal | Matchens nummer på kupongen, 1 till 13. |
| `home`, `away` | text | Hemmalag och bortalag, som de står på kupongen. |
| `odds` | objekt | Aktuella decimalodds för tecknen `"1"`, `"X"` och `"2"` (sidans "Aktuellt odds", eller "Odds" när sidan bara visar en uppsättning). Decimaltal med punkt, större än 1. |
| `start_odds` | objekt (valfri) | Oddsen när spelet öppnade ("Startodds"), på samma sätt som `odds`. Saknas när sidan inte visar dem. |
| `streck_percent` | objekt | Svenska folkets streckfördelning i hela procent för `"1"`, `"X"` och `"2"`. |

De möjliga tecknen är alltid `"1"`, `"X"` och `"2"`, och de används som
nycklar i både `odds` och `streck_percent`.

Procenten är hela tal, så summan per match kan avvika något från 100.

## Vad formatet inte har än

- Svenska Spels eget omgångsnummer. Det står inte i den kopierade texten.
- Flera oddskällor. I steg 1 finns aktuella odds och startodds från samma
  källa, och `source` anger varifrån de kommer.
- Resultat och utfall efter matchen.

## Läsa in en omgång från kopierad text

Kopiera texten från Stryktipset-sidan i webbläsaren, spara den i en textfil
och kör:

```
python -m project_13 read-round omgang.txt --out data/omgang.json --label "Omgång 47"
```

Utan `--out` skrivs JSON till skärmen. Kommandot ändrar inget i textfilen och
hämtar ingenting från nätet. Är texten ofullständig eller ser annorlunda ut
får du ett felmeddelande med radnummer. Konstiga värden (till exempel odds
under 1, eller streckprocent som inte summerar till ungefär 100) ger en
varning men sparas ändå.

Båda sätten som sidan visat oddsen på går att läsa in: en rad "Odds", eller
raderna "Aktuellt odds" och "Startodds". Exempeltexter finns i
`tests/fixtures/`.

## Omgång och speldag

Texten från sidan säger inte vilken omgång det är, så `round` och `draw_date`
räknas ut. Spelet körs på lördagar, och omgången är veckan för närmaste
lördag, räknat från och med dagen texten läses in. Läser du in fredag
2026-11-20 blir det `2026-W47` och `2026-11-21`. En lördag räknas som sin egen
speldag.

Gäller omgången en annan vecka (till exempel när du läser in efter lördagens
spelstopp, eller för en omgång som spelas en annan dag) anger du veckan själv:

```
python -m project_13 read-round omgang.txt --week 48
python -m project_13 read-round omgang.txt --week 2026-W48
```

## Exempelomgången

`data/example_round.json` är en omgång som kopierats för hand från Svenska
Spels Stryktipset-sida och sedan gjorts om till formatet ovan. Lagnamnen står
som på sidan.
