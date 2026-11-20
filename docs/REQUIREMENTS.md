# REQUIREMENTS -- Vad programmet klarar i dag

Det här dokumentet beskriver bara det som redan finns och är testat. Vad
fälten i en omgång heter och betyder står i [DATA_FORMAT.md](DATA_FORMAT.md) och
upprepas inte här.

Varje krav har ett nummer och pekar ut de tester som visar att det gäller.
Testet `tests/test_requirements.py` kontrollerar att varje angivet test finns,
så att dokumentet och testerna hålls i takt. Det kontrollerar inte att testet
verkligen bevisar kravet. Det bedömer en människa.

## Inläsning av en omgång (`read-round`)

**K-1. Odds i båda sidans format.** Text kopierad från Stryktipset-sidan läses
in oavsett om sidan visar en rad "Odds" eller raderna "Aktuellt odds" och
"Startodds". Med "Odds" saknas `start_odds`.
Test: `test_odds_only_text_gives_exactly_the_example_round`,
`test_odds_only_text_has_no_start_odds`,
`test_current_and_start_odds_are_read_for_all_13_matches`,
`test_current_odds_become_odds_and_start_odds_stay_separate`,
`test_last_match_is_read_too`

**K-2. Tåliga mot vanliga skillnader i texten.** Windows-radslut, tomma rader,
extra mellanslag och text efter sista matchen påverkar inte resultatet.
Test: `test_windows_line_endings_blank_lines_and_spaces_do_not_matter`,
`test_text_after_the_last_match_is_ignored`

**K-3. Fel som går att åtgärda.** Ofullständig eller trasig text avvisas med
ett meddelande som säger vad som är fel, med radnummer där det går, och
programmet slutar med exitkod 2.
Test: `test_an_incomplete_copy_is_reported_with_the_number_found`,
`test_a_broken_line_is_reported_with_its_line_number`,
`test_missing_separator_between_teams_is_reported`,
`test_a_match_without_any_odds_is_reported`,
`test_matches_out_of_order_are_reported`, `test_empty_text_is_reported`,
`test_read_round_fails_clearly_on_bad_text`,
`test_read_round_fails_clearly_on_a_missing_file`

**K-4. Varning, inte fel, för konstiga värden.** Odds på 1 eller lägre,
streckprocent som inte summerar till ungefär 100 och fel antal matcher ger en
varning på stderr. Omgången sparas ändå.
Test: `test_check_round_warns_about_strange_values`,
`test_a_clean_round_gives_no_warnings`

**K-5. Exakt 13 matcher.** En omgång har 13 matcher. Läsaren kan konfigureras
att läsa färre, bara för test.
Test: `test_an_incomplete_copy_is_reported_with_the_number_found`,
`test_without_an_expected_count_as_many_matches_as_exist_are_read`

**K-6. Teckenkodning av indata.** Filer sparade som UTF-8, UTF-8 med BOM eller
Windows-kodsidan cp1252 läses in. En fil i annan kodning avvisas med besked
och exitkod 2.
Test: `test_read_round_accepts_files_saved_with_bom_or_windows_encoding`,
`test_read_round_rejects_a_file_in_an_unknown_encoding`

**K-7. Utdata.** Resultatet skrivs som JSON till `--out`, eller till skärmen
utan `--out`. Det innehåller `label`, `source` och `read_at`.
Test: `test_read_round_writes_json_with_label_source_and_read_at`,
`test_read_round_prints_json_to_the_screen_without_out`

## Omgång och speldag

**K-8. Speldag och omgång räknas ut.** Speldagen är närmaste lördag från och
med inläsningsdagen. Omgången är ISO-veckan för den lördagen, som `2026-W47`.
Vecka 53 hanteras.
Test: `test_next_draw_date_is_the_coming_saturday_for_every_weekday`,
`test_round_name_and_week_53`, `test_round_info_computed_and_overridden`,
`test_cli_default_draw_date_is_a_saturday`

**K-9. `--week` åsidosätter uträkningen.** Med `--week` (till exempel `47`,
`W47`, `2026-W47`) används den veckan, och speldagen blir den veckans lördag.
En ogiltig vecka ger felmeddelande och exitkod 2, och ingen fil skrivs.
Test: `test_parse_week_variants`, `test_parse_week_rejects_bad_input`,
`test_cli_adds_round_and_draw_date`, `test_cli_week_overrides_the_computed_round`,
`test_cli_bad_week_exits_2`

## Exempelomgången

**K-10. Exempelfilen följer formatet.** `data/example_round.json` har 13
numrerade matcher, odds större än 1, hela streckprocent som summerar till
ungefär 100, samt `round` och `draw_date` (en lördag som stämmer med `round`).
Test: `test_round_has_13_numbered_matches`,
`test_every_match_has_teams_and_all_three_signs`,
`test_odds_are_decimal_numbers_above_one`,
`test_streck_percent_are_whole_percent_that_roughly_add_up_to_100`,
`test_example_round_has_round_and_saturday`

## Allmänt

**K-11. Programmet startar.** `python -m project_13` skriver namn och version
och slutar med exitkod 0.
Test: `test_version_is_set`, `test_main_returns_zero_and_prints_name_and_version`,
`test_runs_as_a_module`, `test_without_a_command_the_version_is_still_printed`

## Inte täckt av test i dag

- Att utdata skrivs som UTF-8 med å, ä och ö. Koden gör det, men inget test
  kontrollerar tecknen.
- Att `read-round` utan `--week` ger ett visst fast värde. Kommandot använder
  dagens datum, så bara uträkningen (K-8) har ett fast testfall.

## Inte byggt än

(Tomt. Det som ska komma läggs hit utan kravnummer, och blir ett krav först när
det är byggt och testat.)
