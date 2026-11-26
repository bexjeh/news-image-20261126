# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/bexjeh/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/bexjeh/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Sums up the world's news of Thursday 26 November 2026 in one 1024×1024 image: a lead panel on Trump's new tariff salvo against 14 trading partners, with the proposed capped rates charted (China 20%, Vietnam 35%, India 25%, EU and Taiwan 15%), the Houthi claim of a strike on Saudi Arabia's Ras Tanura refinery as Brent settles at $94.61, and panels on Mumbai's 26/11 remembrance and Constitution Day, Thanksgiving in the US, Game 3 of the Gukesh–Sindarov World Chess Championship, ESA's Hera images of Dimorphos, and the Cairo tanker fire — plus six more briefs from the day. Every story is from the 26 November 2026 news cycle. All text is code-rendered with PIL; the image is built by `build_overlay.py` and shipped as `entry.png`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` only copies the pre-built `entry.png` into the output directory (standard library only, no network, byte-identical every run, hash-verified). To rebuild the image from scratch, run `python3 build_overlay.py` (needs Pillow) — it re-renders the same deterministic PNG.

---

<sub>Entered on [make.fun](https://make.fun/?ref=feheg61h&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
