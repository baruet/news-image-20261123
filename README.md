# THE WORLD TODAY — Monday 23 November 2026

[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/baruet/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/baruet/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

One image summing up the world's news of **Monday 23 November 2026** — a front page
drawn 100% programmatically (PIL + DejaVu, no network, no AI image generation).

Entry for [news-image-20261123](https://make.fun/bounty/news-image-20261123) on make.fun.
`main.ts` (Node 22) copies `entry.png` to `/output/entry.png` (honouring
`MAKEFUN_OUTPUT_DIR`), validating PNG magic, 1 MiB cap and 1024×1024 cap.
`draw.py` renders the image deterministically from the story list below.

## The front page — 17 stories + 3 ticker

**Lead — HUANG IS BACK (Markets / Wall Street).** Nvidia reinstates Jensen Huang
as CEO, eleven days after he resigned amid scandal, under pressure from Trump;
shares soar 31% Monday, Nasdaq +6%, S&P 500 +5%. Sources: Reuters, 23 Nov 2026
("Trading Day": "one of the most extraordinary days in US market history").

1. **Russian strikes kill 14 near Kyiv** (Europe / Ukraine) — Dymer block collapses;
   153 drones overnight; Zelenskiy warns of new strikes; Moscow signals new
   trilateral talks soon. Reuters / AFP / SANA, 23 Nov.
2. **COP31 fallout: blame game begins** (Climate / Antalya) — calls for Australian
   minister Bowen to quit; Pacific nations despair; first COP failure since
   Copenhagen 2009. The Hindu BusinessLine, 23 Nov.
3. **24 dead in Cikande factory fire** (Asia / Indonesia) — toll confirmed Monday;
   about 30 still missing; AC short circuit suspected. Reuters, 23 Nov.
4. **Wellington Test ends in draw** (Sport / Cricket) — NZ 239/5 hold India
   (720/9 dec); Mitchell 49* off 186 balls. Stuff / Reuters, 23 Nov.
5. **Puigdemont free to return** (Europe / Spain) — Supreme Court shelves case;
   last hurdle gone after a decade in exile. Reuters, 23 Nov.
6. **Trump pauses lead blast** (USA / Iowa) — Army told to halt detonation of 68
   barrels of toxic lead azide. Reuters, 23 Nov.
7. **US to train Syrian troops** (Middle East / Syria) — first US training mission
   since rebels took Damascus in 2024. Reuters, 23 Nov.
8. **Strikes kill 3 in Gaza** (Middle East / Gaza) — UNRWA worker Adel Al-Helo
   killed in Jabalia; vehicle hit in Gaza City. Reuters, 23 Nov.
9. **N. Korea may shut Swiss office** (Asia / Korea) — Pyongyang weighs closing
   its mission over sanctions on a children's camp. Reuters / KCNA, 23 Nov.
10. **$576M ferries for Kaliningrad** (Europe / Russia) — two giant rail ferries to
    secure supplies to the Baltic exclave. Reuters, 23 Nov.
11. **EU budget rejected** (Europe / EU Budget) — Czechs and Hungarians spurn the
    €1.582tn plan; summit set for Nov 26–27. Reuters, 23 Nov.
12. **Congo halts cobalt exports** (Africa / Congo) — top producer suspends
    shipments from Nov 30 to lift prices. Reuters, 23 Nov.
13. **M6.5 quake hits Vanuatu** (Pacific / Vanuatu) — deep tremor, 600 km down; no
    damage or casualties reported. Xinhua / USGS, 23 Nov.
14. **EU unveils 22nd sanctions** (Europe / Sanctions) — new package targets
    Russia's shadow fleet, energy and visas. 23 Nov.
15. **490,000 Russian dead: leak** (War / Russia) — stolen Rosstat data points to
    at least 490,000 military deaths by late Sept 2026. 23 Nov.
16. **49ers beat Vikings 35–10** (Sport / NFL) — Mexico City rout tightens grip on
    the NFC's No. 1 seed. Played Sunday night US time, reported Monday 23 Nov.

**Ticker — ALSO TODAY:** Cyclone Xavier churns at 241 km/h (GDACS, 23 Nov) •
US flights resume after Friday's FAA ground stop (recovery reported 23 Nov) •
China sentences an official to death for leaking state secrets (reported Monday,
Reuters world news summary, 23 Nov).

## Date discipline (verified 24 Nov 2026)

Every story above happened or was first reported on 23 November 2026. Excluded
as NOT 23 Nov, even though they were in Monday's news cycle:

- COP31 collapse itself, Iran's strikes on US bases in Bahrain, Verstappen's Las
  Vegas win, Alcaraz's Turin win, India 720/9 declared — all **22 Nov**.
- North Carolina House majority (Hubbard beats Foxx) — called **22 Nov**.
- Miley Cyrus wedding — ceremony **21 Nov**, confirmed 22 Nov.
- Princess Kate "Heal" documentary — announced **21 Nov**.
- The FAA nationwide ground stop itself — **Friday 20 Nov** (only the recovery
  is a 23 Nov development, hence the ticker wording).
- Nigeria boat capsizing (24 mourners), Basra power-station fire, Peru M6.7
  quake — **21 Nov**.
- South Africa's 408-run whitewash of India in Guwahati — date could not be
  verified cleanly against the overlapping New Zealand tour; skipped rather
  than risk a misdated claim.

Note on the NFL cell: the 49ers–Vikings game kicked off Sunday evening in the
Americas (01:20 UTC Monday) and its result was reported on Monday 23 Nov; it is
included as Monday's sports result, as a newspaper would carry it.

## Build & verify

```sh
python3 draw.py          # renders entry.png (1024x1024, deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies to /output
```

`main.ts` run twice writes byte-identical output. Image verified by direct
reading: masthead, lead, all 16 cells and ticker legible; 300px downscale keeps
headlines, lead and ticker readable.
