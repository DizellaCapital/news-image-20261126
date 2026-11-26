[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/DizellaCapital/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/DizellaCapital/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# THE THURSDAY LEDGER — Thursday 26 November 2026: 36 dated stories, 7 regions, drawn leads, pin map, date check

One front page that sums up Thursday 26 November 2026's world news: 36 dated,
source-tagged stories across 7 regions, with a giant date masthead, three drawn
leads (two tankers hit mines in the Strait of Hormuz; Kyiv sets two Rosneft
refineries ablaze; Shenzhou-24 docks at Tiangong with Pakistan's first
astronaut), five more illustrated stories, a six-number red strip, a dotted
world map with pins 1–8, and a 28-item ALSO list in which every item carries
a region tag and a source.

Leads: two oil tankers strike naval mines and explode in the Strait of Hormuz,
with a third tanker burning on Sunday and an LNG carrier exploding on Wednesday
evening · Ukrainian drones set the Syzran and Kuibyshev refineries on fire
hours after Putin calls retaliation "inevitable" · Shenzhou-24 docks at
China's Tiangong station carrying Muhammad Zeeshan Ali, Pakistan's first
astronaut. All 36 stories are listed with dates, regions and sources in
`stories_20261126.json`; every number on the page matches the JSON and this
README. Stories were verified against Reuters, IRNA, Xinhua, WHO and
Financial Times reporting on 26 November 2026.

Numbers on the page: 2 tankers hit mines in Hormuz · 37 ships attacked in the
Strait in October · 45% of Russian refining output cut since late October ·
50,018 — the Dow's first close above 50,000 · 490,334 Russian soldiers killed,
per Moscow's own figures · 6.16% — the KOSPI's fall.

## How it runs

`main.py` (Python 3.13, standard library only) copies the bundled
`entry.png` (1024×1024, under 1 MiB) verbatim to `/output/entry.png`. No
network, no timestamps, no rendering at run time — two runs write
byte-identical files (verified by SHA-256 in the grader simulation below).

## How it was drawn

`render.py` (Pillow, local only — never run by the grader) draws
`entry.png` from `stories_20261126.json`. It is deterministic: two runs
produce byte-identical output.

```sh
python3 render.py   # writes entry.png (172,963 bytes, 1024x1024,
                    # sha256 772b50ab1c942b668b3ccad182730ddc21eb65f2d521a5e9898b9680874aff36)
```

Grader simulation (read-only repo dir, `MAKEFUN_OUTPUT_DIR` set):

```sh
MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py   # exit 0, byte-identical output
```

## Date check

Every story above happened, or was first reported, on Thursday
26 November 2026. Deliberately left out: the UN court ruling on Myanmar
(22 Nov) · GTA 6's launch (19 Nov) · the Trump–Xi–Putin meeting in
Shenzhen (20 Nov) · Nepal's prime minister in Delhi (22–23 Nov).

## Bounty

[Sum up 26 November's world news in one image](https://make.fun/bounty/news-image-20261126)
— $100 prize pool, top 50 paid. Entry: the program in this repository.
