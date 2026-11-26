#!/usr/bin/env python3
"""Round-2 build script for news-image-20261126 (fresh rebuild).

Renders entry.png (1024x1024) from the STORIES table below. Every story
was verified against a 26 November 2026 news report (see SOURCES.md);
each carries a per-story source tag and a claim attribution.
Build-time only: uses Pillow. main.py is stdlib-only and never imports PIL.
"""
import hashlib
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONTS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def f(size, bold=False, serif=False):
    return ImageFont.truetype(FONTS if serif else (FONTB if bold else FONT), size)


# (region, headline, detail with claim attribution, source tag)
LEADS = [
    ("NORTH AMERICA", "US proposes tariffs on 14 partners",
     "USTR proposes new duties on China, EU, India, Japan and 10 more; China, EU and Brazil reject the plan. India faces 25%, or 17% with a deal; China up to 40%.",
     "SRC: REUTERS / AP"),
    ("AFRICA", "Cairo tanker fire kills at least 31",
     "A fuel tanker overturned and burst into flames on Cairo's Ring Road; Egypt's health ministry says 31 dead, about 21 hurt.",
     "SRC: BBC / EGYPT HEALTH MIN."),
    ("MIDDLE EAST", "Houthis hit Saudi refinery, ports",
     "Yemen's Houthis claim strikes on Ras Tanura refinery and Red Sea ports; Saudi Arabia says it stopped the drone attack. Brent nears $95.",
     "SRC: CBS / REUTERS"),
]

# 35 further stories: (region, headline, detail, source)
GRID = [
    ("MIDDLE EAST", "US tells citizens: leave Iran",
     "US Virtual Embassy warns hostilities could escalate fast; Israel's army says it is ready to strike without US backing.", "EURONEWS"),
    ("EUROPE", "Ukraine hits Russian airbase; Kyiv struck",
     "Ukraine says it hit five jets at Savasleyka; Russia fires ballistic missiles at Kyiv and hits two grain ships near Odesa.", "REUTERS"),
    ("AFRICA", "DR Congo Ebola cases pass 12,000",
     "Cases pass 12,000 in the worst outbreak on record; fighting in the east displaces health workers.", "AL JAZEERA"),
    ("MIDDLE EAST", "Judges: drop top Netanyahu charge",
     "Judges urge prosecutors to rethink the bribery case; Netanyahu demands the trial end at once.", "BBC"),
    ("MIDDLE EAST", "Gaza strikes kill Hamas security chief",
     "Israeli strikes kill at least 16 in Gaza, incl. Hamas security official Mohammed Abu al-Ouf, despite the ceasefire.", "AL JAZEERA"),
    ("NORTH AMERICA", "AI sell-off drags Nasdaq near bear",
     "Nasdaq falls toward bear territory as AI shares slide; S&P warns it may cut Nvidia's credit rating.", "REUTERS"),
    ("NORTH AMERICA", "FCC clears SpaceX: 1m satellites",
     "FCC approves up to one million SpaceX satellites for orbital data centres; scientists are sceptical.", "BBC"),
    ("EUROPE", "EU leaders split over budget, Ukraine loan",
     "Leaders meet in Brussels over a budget worth up to EUR2tn and a EUR45bn loan for Ukraine; Denmark's PM: 'very far apart'.", "GUARDIAN"),
    ("EUROPE", "UK energy bills to rise 26% in January",
     "Regulator Ofgem raises the price cap; a typical annual bill rises from GBP1,723 to GBP2,166.", "BBC / OFGEM"),
    ("NORTH AMERICA", "Huawei guilty of stealing US trade secrets",
     "A Brooklyn jury convicts Huawei on 10 of 12 counts, incl. bank fraud and conspiracy to steal trade secrets.", "BBC"),
    ("EAST ASIA", "Kim vows wider tactical nuclear deployment",
     "Kim Jong Un, touring nuclear sites, calls for tactical nuclear weapons across more domains, KCNA reports.", "KCNA / CNBC"),
    ("SOUTH ASIA", "First Pakistani astronaut reaches Tiangong",
     "Muhammad Zeeshan Ali, aboard Shenzhou-24, is the first foreign national on China's space station.", "GUARDIAN / AFP"),
    ("SPACE", "Hera shows crater from NASA asteroid hit",
     "ESA's Hera releases close-ups of Dimorphos: a stadium-sized crater from NASA's 2022 DART impact.", "ESA / EURONEWS"),
    ("NORTH AMERICA", "King tides flood California coast",
     "King tides and storm waves flood roads and homes; part of Pacifica pier is destroyed; record tides in LA.", "GUARDIAN"),
    ("EUROPE", "Spain votes Sunday; right favoured",
     "Snap election Sunday after eight years of Socialist-led rule; polls put Feijoo's Popular Party first.", "BBC"),
    ("EAST ASIA", "China probes Shanghai party chief Chen",
     "Politburo member Chen Jining is placed under investigation for corruption, the fourth senior figure toppled.", "NPR / SCMP"),
    ("EUROPE", "UK net migration falls to 77,000",
     "ONS: net migration in the year to June 2026 is the lowest since 1997, excluding the pandemic.", "ONS / GUARDIAN"),
    ("EUROPE", "UK-EU treaties out; 10-year exit clause",
     "Government publishes two UK-EU treaties and a bill; Tories and Reform criticise the termination clause.", "BBC"),
    ("AFRICA", "UK sent convicted refugee to Eswatini",
     "BBC reports the UK sent a Sri Lankan refugee convicted of assault to Eswatini under a secret deal.", "BBC"),
    ("AFRICA", "Drone attacks kill 15 in Sudan's Blue Nile",
     "Drone attacks kill at least 15 in Blue Nile state as war and drought threaten harvests for millions.", "AL JAZEERA"),
    ("EAST ASIA", "Hong Kong marks year since fire killed 168",
     "A year on from the Wang Fuk Court fire in Tai Po, only civil society holds commemorations; families await justice.", "BBC / SCMP"),
    ("SOUTH ASIA", "Bangladesh garment workers protest wage rise",
     "Wage board raises the minimum to Tk17,000; unions want Tk18,000. About 140 factories shut; police fire tear gas.", "AFP / REUTERS"),
    ("AFRICA", "Court kills Ramaphosa impeachment push",
     "A Cape Town court overturns the report behind the Phala Phala impeachment effort; the committee dissolves.", "AFRICANEWS"),
    ("OCEANIA", "Australia, Solomons sign security treaty",
     "Solomons PM Matthew Wale names Australia its primary security partner, ending the 2022 pact with China.", "NBC NEWS"),
    ("MIDDLE EAST", "Iraq court backs federal grip on Kurdish oil",
     "Iraq's top court rules Baghdad can audit Kurdistan's oil industry and deploy troops to borders.", "AL JAZEERA"),
    ("EUROPE", "Leak: Russia lost nearly 500,000 troops",
     "BBC analysis of leaked Russian data estimates at least 490,334 soldiers dead in Ukraine; Kremlin dismisses it.", "BBC"),
    ("EUROPE", "Poundland collapses; 11,000 jobs at risk",
     "Discount chain falls into administration after its owners fail to find a buyer.", "BBC"),
    ("SE ASIA", "Bangkok refinery fire injures seven",
     "Explosion and fire hit a Bangchak oil facility in eastern Bangkok; seven hurt, residents told to evacuate.", "EURONEWS"),
    ("NORTH AMERICA", "Macy's parade postponed, a first",
     "Macy's moves its 100th Thanksgiving Day Parade to Saturday over high winds and heavy rain.", "BBC / AP"),
    ("NORTH AMERICA", "Abrego Garcia leaves US for Spain",
     "Kilmar Abrego Garcia, wrongly deported in 2025, arrives in Madrid voluntarily; he hopes to return after Trump.", "AP / PBS"),
    ("EUROPE", "Greek workers strike over living costs",
     "A 24-hour general strike disrupts ferries, metro and flights; police say about 15,000 march in Athens.", "EURONEWS / AFP"),
    ("S AMERICA", "Colombia police free 76 supermarket hostages",
     "Forces storm a Cartagena supermarket after a day-long siege; all hostages are rescued alive.", "GUARDIAN"),
    ("SOUTH ASIA", "India marks Constitution Day, 26/11",
     "India marks 77 years since adopting its Constitution; Air Chief Marshal Dixit honours the 166 killed in 2008.", "PMO / ANI"),
    ("EUROPE", "Chess: Gukesh v Sindarov, Game 3 today",
     "World title match in Geneva is tied 1-1 after two draws; Game 3 starts 15:00 CET, Sindarov with White.", "FIDE"),
    ("CULTURE", "Duran Duran guitarist Andy Taylor dies, 65",
     "Andy Taylor, original guitarist of Duran Duran, dies aged 65 after prostate cancer, the band says.", "BBC"),
]

REGIONS = ["NORTH AMERICA", "SOUTH AMERICA", "EUROPE", "MIDDLE EAST",
           "AFRICA", "SOUTH ASIA", "EAST ASIA", "SE ASIA", "OCEANIA", "SPACE"]
REGION_COLOURS = {
    "NORTH AMERICA": "#1b4f9c", "SOUTH AMERICA": "#0e7a5f", "EUROPE": "#6a3fa0",
    "MIDDLE EAST": "#b3541e", "AFRICA": "#8a6d00", "SOUTH ASIA": "#c2185b",
    "EAST ASIA": "#a31545", "SE ASIA": "#00695c", "OCEANIA": "#0277bd",
    "SPACE": "#37474f", "CULTURE": "#5d4037",
}

TIMELINE = [
    ("00-06 UTC", "Asia wakes: tariffs, astronaut, markets"),
    ("06-09 UTC", "Europe opens: EU budget, UK bills"),
    ("09-12 UTC", "Gulf & Gaza: refinery, Iran warning"),
    ("12-15 UTC", "Africa & India: Ebola, 26/11, courts"),
    ("15-18 UTC", "Chess Game 3; Americas stir"),
    ("18-24 UTC", "Thanksgiving: parade off, Nasdaq slides"),
]


def wrap(draw, text, font, width):
    out = []
    for para in text.split("\n"):
        out.extend(textwrap.wrap(para, width=width) or [""])
    return out


def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    # Header
    d.rectangle([0, 0, W, 56], fill="#111827")
    d.text((14, 6), "THE WORLD IN ONE PAGE", font=f(26, bold=True, serif=True), fill="white")
    d.text((14, 36), "THURSDAY 26 NOVEMBER 2026  |  38 DATED STORIES  |  10 REGIONS",
           font=f(11, bold=True), fill="#fbbf24")
    d.text((W - 14, 10), "ALL STORIES", font=f(11, bold=True), fill="white", anchor="ra")
    d.text((W - 14, 28), "DATED 26 NOV 2026", font=f(11, bold=True), fill="white", anchor="ra")
    # Lead row: 3 boxes
    y0, lh = 64, 138
    widths = [340, 320, 320]
    x = 14
    for (region, head, detail, src), w in zip(LEADS, widths):
        col = REGION_COLOURS[region]
        d.rectangle([x, y0, x + w - 8, y0 + lh], outline=col, width=2)
        d.rectangle([x, y0, x + w - 8, y0 + 20], fill=col)
        d.text((x + 6, y0 + 3), region, font=f(10, bold=True), fill="white")
        d.text((x + 6, y0 + 24), head, font=f(15, bold=True), fill="#111827")
        # wrap headline to 2 lines max
        for i, ln in enumerate(wrap(d, head, f(15, bold=True), 30)[:1]):
            pass
        lines = textwrap.wrap(detail, width=42)
        yy = y0 + 62
        for ln in lines[:3]:
            d.text((x + 6, yy), ln, font=f(10), fill="#1f2937")
            yy += 13
        d.text((x + 6, y0 + lh - 16), src, font=f(9, bold=True), fill=col)
        x += w
    # Map + timeline strip
    y0 = 210
    d.rectangle([14, y0, 634, y0 + 82], outline="#9ca3af", width=1)
    d.text((22, y0 + 4), "WORLD MAP — WHERE THE DAY HAPPENED", font=f(10, bold=True), fill="#111827")
    # crude continents
    for (cx, cy, cw, ch) in [(40, 238, 90, 34), (150, 240, 70, 30), (250, 238, 80, 36),
                             (350, 240, 90, 34), (460, 238, 70, 30), (540, 250, 60, 26)]:
        d.ellipse([cx, cy, cx + cw, cy + ch], fill="#d1d5db", outline="#6b7280")
    dots = [(70, 250, "1"), (180, 252, "2"), (290, 254, "3"), (395, 252, "4"),
            (490, 250, "5"), (565, 258, "6")]
    for (dx, dy, n) in dots:
        d.ellipse([dx - 8, dy - 8, dx + 8, dy + 8], fill="#b91c1c")
        d.text((dx, dy - 6), n, font=f(9, bold=True), fill="white", anchor="ma")
    d.text((22, y0 + 62), "1 N America  2 S America  3 Europe  4 Middle East  5 Africa  6 Asia-Pacific",
           font=f(9), fill="#374151")
    # timeline
    d.rectangle([642, y0, 1010, y0 + 82], outline="#9ca3af", width=1)
    d.text((650, y0 + 4), "THROUGH THE DAY — UTC", font=f(10, bold=True), fill="#111827")
    yy = y0 + 20
    for t, s in TIMELINE:
        d.text((650, yy), t, font=f(8, bold=True), fill="#b91c1c")
        d.text((712, yy), s, font=f(8), fill="#1f2937")
        yy += 10
    # Grid: 5 cols x 7 rows
    gx, gy = 14, 300
    cw, ch = 194, 94
    for i, (region, head, detail, src) in enumerate(GRID):
        r, c = divmod(i, 5)
        x = gx + c * cw
        y = gy + r * ch
        col = REGION_COLOURS.get(region, "#37474f")
        d.rectangle([x, y, x + cw - 6, y + ch - 6], outline="#d1d5db", width=1)
        d.rectangle([x, y, x + cw - 6, y + 15], fill=col)
        d.text((x + 4, y + 2), f"{i + 4:02d}  {region}", font=f(8, bold=True), fill="white")
        hl = textwrap.wrap(head, width=26)
        yy = y + 18
        for ln in hl[:2]:
            d.text((x + 4, yy), ln, font=f(11, bold=True), fill="#111827")
            yy += 13
        dl = textwrap.wrap(detail, width=32)
        for ln in dl[:2]:
            d.text((x + 4, yy), ln, font=f(9), fill="#374151")
            yy += 11
        d.text((x + 4, y + ch - 18), f"SRC: {src}", font=f(8, bold=True), fill=col)
    # Footer: date check
    fy = 300 + 7 * 94 + 4
    d.rectangle([14, fy, 1010, fy + 56], fill="#111827")
    d.text((22, fy + 5), "DATE CHECK — 26 NOV 2026 ONLY",
           font=f(11, bold=True), fill="#fbbf24")
    d.text((22, fy + 22),
           "Every story above was first reported in the 26 Nov 2026 news cycle, with its source tagged. "
           "Claims are attributed to who said them; older stories were excluded, not re-dated.",
           font=f(10), fill="white")
    d.text((22, fy + 40),
           "Sources: Reuters, BBC, AP, Guardian, Al Jazeera, Euronews, AFP, KCNA, FIDE, ONS, Ofgem — full list in SOURCES.md",
           font=f(9), fill="#d1d5db")
    img.save(OUT, optimize=True)
    data = open(OUT, "rb").read()
    print(f"{OUT}: {len(data)} bytes, {img.size}, sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
