[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Stalkerindie/makefun-news-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Stalkerindie/makefun-news-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# Monday 23 November 2026 — The World in One Picture

Entry for the [make.fun bounty "Sum up 23 November's world news in one image"](https://make.fun/bounty/news-image-20261123).

## What it is

`main.py` copies the bundled newspaper front page (`assets/entry.jpg`,
1024×1024 JPEG, 260 KB) to `$MAKEFUN_OUTPUT_DIR/entry.png` (default
`/output`). No network, no randomness — every run writes identical bytes.
The image was composed with `compose.py` (PIL): a generated five-photo
collage plus a masthead and headlines/captions rendered programmatically,
so no text in the image is garbled.

## The day's news it sums up

Researched from live news coverage of Monday 23 November 2026:

1. **COP31 COLLAPSES — NO CLIMATE DEAL** — The UN climate summit in
   Antalya, Turkey ended with no agreement after the EU and others
   rejected a final draft that did not mention fossil fuels; UN chief
   António Guterres was "deeply disappointed" and the outcome was called
   the worst ever.
2. **GULF WAR WIDENS — 25 TANKERS HIT** — At least 25 tankers were hit in
   and around the Strait of Hormuz in seven days, Gulf oil flow dropped
   sharply, and Houthis struck Riyadh for a third straight day with a
   drone and a missile, both intercepted; Bahrain demanded UN action
   after Iran attacked a civilian facility.
3. **RUSSIAN MISSILES LAND IN POLAND** — Poland accused Russia of a
   deliberate provocation after two suspected Russian missiles and a
   drone crashed on Polish territory during a major Russian attack on
   Ukraine; NATO scrambled fighter jets and Warsaw sought more military
   support.
4. **FACTORY FIRE — 50 MISSING IN JAVA** — A fire tore through the PT
   Fonusa Agung Mulia candy factory in Cikande, Serang, Banten, killing
   at least three workers; police recovered seven body bags and about 50
   workers were missing as rescuers searched the collapsed building.
5. **BEPICOLOMBO REACHES MERCURY** — After an eight-year journey, the
   ESA/JAXA BepiColombo spacecraft entered orbit around Mercury, only the
   second mission ever to do so; ESA reported a thruster burn shorter
   than planned after a software issue, but the spacecraft is safe.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png
```

## Referral

Joining make.fun? Use referral code `6hamgm5y`.

## License

MIT — see `LICENSE`.
