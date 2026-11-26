# The World in One Day — Thursday 26 November 2026

[![Competition](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/DizellaCapital/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/DizellaCapital/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

One image that sums up Thursday 26 November 2026: **36 stories, 7 regions,
17 sources**. Entry for the [make.fun bounty](https://make.fun/bounty/news-image-20261126)
"Sum up 26 November's world news in one image" (v2).

## What's on the front page

- **Three leads, all drawn:** the Macy's 100th Thanksgiving parade postponed
  to Saturday — the first postponement in its 100-year history, as a
  nor'easter brings 60 mph gusts; the Cairo fuel-tanker fire that killed 31;
  and the U.S. plan for new Section 301 tariffs on 14 trading partners,
  China hardest at 20%.
- **The day in six numbers:** 100th · 31 · 14 · 20% · 60 mph · 27.
- **Five more illustrated stories:** two tankers hit mines in Hormuz, Kyiv
  drones burn two Samara refineries, Shenzhou-24 docks with Pakistan's first
  astronaut aboard, Tempus pays $600m cash for Personalis, and the Houthis
  claim a strike on Ras Tanura.
- **A world map with numbered pins 1–8**, plus ALSO 9–36 with a region,
  a source and a status tag on every story.
- **DATE CHECK** — what we deliberately left out: COP31 ended on Sunday
  22 November, and the Hamas security chief was killed on Tuesday 24
  November. Neither is 26 November news.
- **HOW SURE** legend: OFFICIAL (government or institution), CONFIRMED
  (two or more sources), REPORTED (figures still preliminary), CLAIM
  (one source, or a party's own claim). To press time 02:00 UTC.

## The 36 stories

| # | Story | Region | Source | Status |
|---|-------|--------|--------|--------|
| 1 | Parade postponed — a first in 100 years | North America | Reuters / WSJ | CONFIRMED |
| 2 | Tanker fire kills 31 near Cairo | Middle East | AP / CNN | REPORTED |
| 3 | U.S. tariffs aimed at 14 partners | North America | Reuters | CONFIRMED |
| 4 | 2 tankers hit mines in Hormuz | Middle East | Reuters / IRNA | CLAIM |
| 5 | Kyiv drones burn 2 Samara refineries | Europe | Reuters | REPORTED |
| 6 | Shenzhou-24 docks; Pakistan's first astronaut | Asia | Xinhua / Reuters | CONFIRMED |
| 7 | Tempus pays $600m cash for Personalis | North America | SEC filing | CONFIRMED |
| 8 | Houthis claim strike on Ras Tanura | Middle East | Houthi claim | CLAIM |
| 9 | Saudi-led strikes hit Hodeidah port | Middle East | Reuters | REPORTED |
| 10 | Libya vows revenge after Benghazi | Africa | Reuters | REPORTED |
| 11 | Huawei guilty on 10 of 12 counts | North America | Reuters | CONFIRMED |
| 12 | Dow crosses 50,000 as Asia sinks | Asia | Reuters | CONFIRMED |
| 13 | Solomons ink $740m Australia pact | Oceania | Reuters | CONFIRMED |
| 14 | EU votes 367–268 to ease nature law | Europe | Reuters | CONFIRMED |
| 15 | EU court: livestock cages must go | Europe | ECJ | CONFIRMED |
| 16 | EU pledges 50bn for quantum | Europe | EU Commission | CONFIRMED |
| 17 | RSF drone strike kills 19 in Sudan | Africa | Reuters | REPORTED |
| 18 | Bogor gold mine flood kills 6 | Asia | Reuters | REPORTED |
| 19 | Hostages freed in Cartagena siege | South America | Reuters | REPORTED |
| 20 | Dell Q3 revenue $54.9bn soars | North America | Dell | CONFIRMED |
| 21 | Spain train crash: bad welds | Europe | Reuters | REPORTED |
| 22 | Ebola toll in Congo reaches 5,775 | Africa | WHO | CONFIRMED |
| 23 | Gukesh v Sindarov: Game 3 in Geneva | Europe | FIDE | REPORTED |
| 24 | India: 26/11 and Constitution Day | Asia | Reuters | CONFIRMED |
| 25 | Norway pledges $7bn for Ukraine | Europe | Reuters | CONFIRMED |
| 26 | Hungary's Magyar meets Zelensky | Europe | Reuters | REPORTED |
| 27 | Zaporizhzhia plant loses power | Europe | IAEA | REPORTED |
| 28 | Zaporizhzhia: 2 dead, 40+ hurt | Europe | Reuters | REPORTED |
| 29 | Russian drones enter Polish airspace | Europe | Reuters | REPORTED |
| 30 | Duma: defence budget up 27% | Europe | Reuters | CONFIRMED |
| 31 | Putin vows retaliation 'inevitable' | Europe | Reuters | REPORTED |
| 32 | Leak: 490,334 Russian troops killed | Europe | Leaked figures | CLAIM |
| 33 | Kyiv: 3 MiG-31s, 2 Su-34s hit | Europe | Kyiv claim | CLAIM |
| 34 | Australia inflation jumps to 4.9% | Oceania | ABS | CONFIRMED |
| 35 | U.S. tells citizens: leave Iran | Middle East | U.S. State Dept | CONFIRMED |
| 36 | Iran says it downed 2 U.S. drones | Middle East | IRNA | CLAIM |

Regions: Europe 15 · Middle East 6 · North America 5 · Asia 4 · Africa 3 ·
Oceania 2 · South America 1.

## How it is built

- `stories_20261126.json` — the 36 stories: headline, deck, region,
  source, status, and map pin. Every number in the image matches this file.
- `render.py` — draws `entry.png` (1024×1024) from the JSON with Pillow.
  Deterministic: two runs produce byte-identical output.
- `main.py` — the graded entry program (standard library only). It copies
  `entry.png` to `MAKEFUN_OUTPUT_DIR`, validates it is a 1024×1024 PNG
  under 1 MiB, and verifies the copy's SHA-256 matches the source.

```sh
python3 render.py            # rebuild entry.png from the stories file
MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py   # graded entry run
```

## Bounty

- Competition: https://make.fun/bounty/news-image-20261126
- Prize pool $100, paid top 50 · Deadline 28 November 2026 00:00 UTC
- Version 2 of the entry: the whole top half is new — three leads the
  first version missed (Macy's parade, Cairo tanker fire, U.S. tariffs),
  a new six-number strip, and a status tag on every story.
