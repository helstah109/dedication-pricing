# AGENTS.md — dedication-pricing

Instructions for every agent working in this repo. `CLAUDE.md` contains only `@AGENTS.md`.

## What this is

The public price finder at https://dedication-pricing.vercel.app: what places charge to dedicate a tree. It is a plain web page (`index.html`) that reads one file, `data.json`. Every push to `main` goes live on Vercel within a minute. Helen is not technical: write to her in plain words.

## Where prices come from

**Never type prices into `data.json` by hand.** The prices live in the research, in the private repo `helstah109/TRB-tribute-platform`, file `TRB_Research/TRB_Dedication-Pricing/TRB_Dedication-Pricing-Master-Dataset.csv` (the master list). Only reviewed prices are in the master list; drafts in that repo's `workstreams/` folders never go live.

**To add or change a price,** work in the research repo and follow its agent instructions, section "Getting prices onto the public price finder": draft, second check, then add to the master list. That repo's rules apply, including Helen's yes before anything new goes public.

## Updating the live site from the master list

Use one of these, after a reviewed change reaches the master list:

1. **Automatic:** the GitHub Action "Update prices from research" runs once a day and saves a new `data.json` if the master list changed. Anyone can also open the repo's Actions tab, pick that action and press **Run workflow**. It only works once Helen has added the read-only research key as the repo secret `TRB_READ_TOKEN`; until then it stops with a note and changes nothing.
2. **By hand, with both repos side by side** (folders `dedication-pricing` and `TRB-tribute-platform` in the same parent folder):
   ```
   python3 -I tools/gen.py --json data.json
   ```
   Run it from this folder, check the place and offer counts it prints, then commit `data.json` and push. If the research folder is elsewhere, set `TRB_PRICING_DIR` to its `TRB_Research/TRB_Dedication-Pricing` folder.

If the script finds a problem in the master list (a changed header, an unknown `segment`, a price with `$` or commas, a repeated `record_id`) it stops, names the line, and `data.json` stays as it was. Fix the row in the research repo, not here.

## Other rules

- `tools/`, `00-Inbox/`, `.github/`, `AGENTS.md`, `CLAUDE.md` and `README.md` are not published on the website.
- Programs with no posted price ("ask" entries) are listed in `tools/gen.py`, in the research's own words.
- Design: understated and light, Regular weight or heavier (no Light type), works on a phone. Plain words. Prices are what places post, never a recommended price.
- Files Helen hands over go in `00-Inbox/` as given, with a line in its README.
- Commits use author `helstah109` / `papp.helen.m@gmail.com`. Report the commit SHA and check the live site after a change.
- Never commit keys or tokens. The research key lives only in the repo's secrets.
