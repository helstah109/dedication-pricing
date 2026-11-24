# dedication-pricing

A public, searchable list of what gardens, senior living communities, neighborhoods, campuses and clubs charge for tree dedications. The name leaves room for other kinds of dedications later, like park benches.

## What's here

- `index.html`: the page people see.
- `data.json`: the price list the page reads. Updating prices means replacing only this file.
- `tools/gen.py`: rebuilds `data.json` from the research spreadsheets in TRB-tribute-platform. With both repos side by side, run `python3 -I tools/gen.py --json data.json` from this folder (or set TRB_PRICING_DIR to the research folder).
- `inbox/`: drop files here to be processed later.

`tools/`, `inbox/` and this README are not published on the website.

Every change pushed to `main` goes live on Vercel by itself.
