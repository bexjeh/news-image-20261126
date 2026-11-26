# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/bexjeh/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/bexjeh/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Sums up the world's news of Thursday 26 November 2026 in one 1024×1024 image: "One Day, One World" — a front page with 38 dated stories across 10 regions, each tagged with its source and claim attribution, a world map, a UTC timeline through the day, and a date-check note. Lead stories: the US tariff proposal for 14 trading partners, the Cairo tanker fire, and the Houthi strikes on Saudi Arabia's Ras Tanura refinery. Every story is from the 26 November 2026 news cycle; older stories were excluded, not re-dated — full per-story sources in `SOURCES.md`. All text is code-rendered with PIL; the image is built by `build_overlay_r2.py` and shipped as `entry.png`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` only copies the pre-built `entry.png` into the output directory (standard library only, no network, byte-identical every run, hash-verified). To rebuild the image from scratch, run `python3 build_overlay_r2.py` (needs Pillow) — it re-renders the same deterministic PNG.

---

<sub>Entered on [make.fun](https://make.fun/?ref=feheg61h&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
