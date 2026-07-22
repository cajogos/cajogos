# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is the special GitHub **profile** repository (`cajogos/cajogos`): its `README.md` renders directly on https://github.com/cajogos. There is no application, build system, test suite, or lint step. The deliverable is the rendered README.

It was previously a Python script that auto-generated the README from the GitHub API (cron + `autocommit.sh`); that generator was removed in favour of a hand-maintained static README. Do not reintroduce the generator unless asked.

## Working on the profile

- Edit `README.md` directly, then commit and push to `main`. The profile updates on push.
- There is no local preview server; verify rendering on the GitHub profile page after pushing, or check individual widget image URLs return `200` (see below).

## Widgets are third-party image services, not code

The README's "widgets/badges/counters" are all **dynamically-generated images** from external services (GitHub markdown cannot run JavaScript). Everything is themed `tokyonight` (accent `#7AA2F7`). Services in use:

- `capsule-render.vercel.app` - waving header banner
- `readme-typing-svg.demolab.com` - animated typing subtitle
- `skillicons.dev` - tech logo row
- `img.shields.io` - social badges (LinkedIn/X/Website)
- `komarev.com/ghpvc` - profile views counter
- `github-profile-summary-cards.vercel.app` - stats / languages / productive-time cards
- `github-readme-activity-graph.vercel.app` - contribution activity graph

**When an image looks broken, the service is usually down, not the URL.** `curl -s -o /dev/null -w "%{http_code}"` each image URL to confirm. History: `github-readme-stats.vercel.app` (503 paused) and `github-profile-trophy.vercel.app` (402 disabled) both died and were replaced by `github-profile-summary-cards`. If a service dies again, find a working alternative rather than assuming a config error.

## The snake animation (only moving part with real logic)

`.github/workflows/snake.yml` (Platane/snk) runs on push to `main`, daily cron, and manual dispatch. It generates the contribution-snake SVG and pushes it to a dedicated **`output` branch**; the README references it at `raw.githubusercontent.com/cajogos/cajogos/output/github-snake-dark.svg`. The snake image is broken until this Action has run at least once. The workflow needs `contents: write` (already declared) and Actions enabled with read/write permissions on the repo.

## Conventions

- **No em dash character (`—`) anywhere.** Use a comma, colon, parentheses, or a hyphen (`-`).
- Non-social images link back to the profile (`https://github.com/cajogos`); the three social badges (LinkedIn, X, Website) link to their own destinations.
- Social badge labels are intentionally terse: `in/cajogos`, `X @cajogos`, `carlos.fyi`.

## Local secrets

`config.yaml` (gitignored, never committed) is a leftover from the old generator and holds an unused GitHub token. It is not needed by anything now.
