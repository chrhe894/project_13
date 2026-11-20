# FIRST WORKFLOW -- Första arbetsflödet (steg 1)

**Version:** 0.1 (utkast)\
**Status:** Beskriver det minsta första steget, inte hela applikationen.

Målbilden finns i [IDEAL_STATE.md](IDEAL_STATE.md) och utgångsläget i
[IDENTITY.md](IDENTITY.md).

Automatisk hämtning, flera källor och ett gränssnitt behövs, men en första
version med allt det på en gång är ett för långt steg. Därför beskriver det
här dokumentet bara det minsta flödet. Resten finns som kommande steg längre
ner.

## Flödet i en mening

En omgång matas in för hand, och applikationen visar för varje match hur
sannolikt varje tecken (1, X och 2) är och var oddsens bild och
streckfördelningen skiljer sig mycket.

## Indata

- En omgång med 13 matcher, inlagd för hand.
- Per match: vilken match det gäller, odds för 1, X och 2 samt
  streckfördelning (procent) för 1, X och 2.
- Exempeldata läggs in av projektets ägare. Formatet är inte bestämt.

## Analysresultat

För varje match visas:

- Sannolikhet för 1, X och 2.
- En markering där oddsens bild och streckfördelningen skiljer sig mycket.

Hur sannolikheterna räknas fram, och vad "mycket" betyder, är inte bestämt.

## Utanför steg 1 (kommande steg)

Det här behövs men ingår inte i steg 1. Varje punkt blir en egen handling.

- Automatisk hämtning av omgången.
- Automatisk hämtning av odds, troligen från flera källor.
- Ett gränssnitt. Tills det finns räcker en enkel utskrift.
- Kunskapsbas och lärande.
- Historik och uppföljning av utfall.
- Flera omgångar.
- Spelförslag: rader, system, insatser och risknivåer.

## Antaganden och öppna frågor

Antaganden:

- Streckfördelningen ingår i indata från början. Underlaget nämner den som
  marknadsinformation vid sidan av odds.
- Resultatet visas som en enkel utskrift i steg 1, eftersom gränssnittet är
  ett senare steg. Ägaren har sagt att ett gränssnitt behövs. Om det ska ingå
  redan i steg 1 behöver dokumentet ändras.

Öppet:

- Vilka oddskällor och vilka oddsfält som ska användas.
- Hur sannolikheter räknas fram ur odds, och var gränsen för "mycket" går.
- Vilket format indata ska ha.
