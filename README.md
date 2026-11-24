# dedication-pricing

A public, searchable list of what gardens, senior living communities, neighborhoods, campuses and clubs charge for tree dedications. The name leaves room for other kinds of dedications later, like park benches.

## What's here

- `index.html`: the page people see.
- `data.json`: the price list the page reads, built from the reviewed master list in TRB-tribute-platform. Don't edit it by hand.
- `tools/gen.py`: rebuilds `data.json` from the research master list.
- `.github/workflows/update-prices.yml`: does that rebuild once a day by itself.
- `00-Inbox/`: drop files here to be processed later.

Agents: read [AGENTS.md](AGENTS.md) for how prices get added and the site updated.

`tools/`, `00-Inbox/`, `.github/`, the agent files and this README are not published on the website.

Every change pushed to `main` goes live on Vercel by itself.
