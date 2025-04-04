# World Cube Association – Results Database Export

- Encoding: UTF-8
- Date: April  1, 2025
- Export Format Version: 1.0.0
- Contact: WCA Results Team (https://www.worldcubeassociation.org/contact?contactRecipient=wrt)
- Website: https://www.worldcubeassociation.org/export/results

## Description

This database export contains public information about all official WCA
competitions, WCA members, and WCA competition results.

## Goal

The goal of this database export is to provide members of the speedcubing
community a practical way to perform analysis on competition information for
statistical and personal purposes.

## Allowed Use

The information in this file may be re-published, in whole or in part, as long
as users are clearly notified of the following:

> This information is based on competition results owned and maintained by the
> World Cube Assocation, published at https://worldcubeassociation.org/results
> as of April  1, 2025.

## Acknowledgements

The WCA database was originally created and maintained by:

- Clément Gallet, France
- Stefan Pochmann, Germany
- Josef Jelinek, Czech Republic
- Ron van Bruchem, Netherlands

The database contents are now maintained by the WCA Results Team, and the
software for the database is maintained by the WCA Software Team:
https://www.worldcubeassociation.org/about

## Date and Format Version

The export contains a `metadata.json` file, with the following fields:

| Field                   | Sample Value              |
|-------------------------|---------------------------|
| `export_date`           | `"2025-04-01 00:29:15 UTC"` |
| `export_format_version` | `"1.0.0"` |

If you regularly process this export, we recommend that you check the
`export_format_version` value in your program and and review your code if the
major part of the version (the part before the first `.`) changes.

If you are processing the exported data using an automated system, we recommend
using a cron job to check the API endpoint at:
https://www.worldcubeassociation.org/api/v0/export/public
You can use the `export_date` to detect if there is a new export, and the
`sql_url` and `tsv_url` will contain the URLs for the corresponding downloads.

## Format (version 1.0.0)

The database export consists of these tables:

| Table                                   | Contents                                           |
|-----------------------------------------|----------------------------------------------------|
| Persons                                 | WCA competitors                                    |
| Competitions                            | WCA competitions                                   |
| Events                                  | WCA events (3x3x3 Cube, Megaminx, etc)             |
| Results                                 | WCA results per competition+event+round+person     |
| RanksSingle                             | Best single result per competitor+event and ranks  |
| RanksAverage                            | Best average result per competitor+event and ranks |
| RoundTypes                              | The round types (first, final, etc)                |
| Formats                                 | The round formats (best of 3, average of 5, etc)   |
| Countries                               | Countries                                          |
| Continents                              | Continents                                         |
| Scrambles                               | Scrambles                                          |
| championships                           | Championship competitions                          |
| eligible_country_iso2s_for_championship | See explanation below                              |

Most of the tables should be self-explanatory, but here are a few specific details:

### Countries

`Countries` stores include those from the Wikipedia list of countries at
http://en.wikipedia.org/wiki/List_of_countries, and may include some countries
that no longer exist. The ISO2 column should reflect ISO 3166-1 alpha-2
country codes, for countries that have them. Custom codes may be used in some
circumstances.

### Scrambles

`Scrambles` stores all scrambles.

For `333mbf`, an attempt is comprised of multiple newline-separated scrambles.
However, newlines can cause compatibility issues with TSV parsers. Therefore, in
the TSV version of the data we replace each newline in a `333mbf` scramble with
the `|` character.

### eligible_country_iso2s_for_championship

`eligible_country_iso2s_for_championship` stores information about which
citizenships are eligible to win special cross-country championship types.

For example, `greater_china` is a special championship type which contains 4
`iso2` values: `CN`, `HK`, `MC` and `TW`. This means that any competitor from
China, Hong Kong, Macau, or Taiwan is eligible to win a competition with
championship type `greater_china`.

### Results

Please see https://www.worldcubeassociation.org/regulations/#article-9-events
for information about how results are measured.

Values of the `Results` table can be interpreted as follows:

- The result values are in the following fields `value1`, `value2`, `value3`, `value4`, `value5`,
  `best`, and `average`.
- The value `-1` means DNF (Did Not Finish).
- The value `-2` means DNS (Did Not Start).
- The value `0` means "no result". For example a result in a `best-of-3` round
  has a value of `0` for the `value4`, `value5`, and `average` fields.
- Positive values depend on the event; see the column "format" in Events.

  - Most events have the format "time", where the value represents centiseconds.
    For example, 8653 means 1 minute and 26.53 seconds.
  - The format "number" means the value is a raw number, currently only used by
    "fewest moves" for number of moves.
    - Fewest moves averages are stored as 100 times the average, rounded.
  - The format "multi" is for old and new multi-blind, encoding the time as well
    as the number of cubes attempted and solved. This is a decimal value,
    which can be interpreted ("decoded") as follows:

        old: 1SSAATTTTT
             solved        = 99 - SS
             attempted     = AA
             timeInSeconds = TTTTT (99999 means unknown)
        new: 0DDTTTTTMM
             difference    = 99 - DD
             timeInSeconds = TTTTT (99999 means unknown)
             missed        = MM
             solved        = difference + missed
             attempted     = solved + missed

    In order to encode data, use the following procedure:

             solved        = # cubes solved
             attempted     = # cubes attempted
             missed        = # cubes missed = attempted - solved
             DD            = 99 - (solved - missed)
             TTTTT         = solve time in seconds
             MM            = missed

    Note that this is designed so that a smaller decimal value means a better
    result. This format does not support more than 99 attempted cubes, or times
    greater than 99999 seconds (about 27.7 hours).
