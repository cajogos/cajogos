# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is the special GitHub **profile** repository (`cajogos/cajogos`): its `README.md` renders directly on https://github.com/cajogos. There is no application, build system, test suite, or lint step. The deliverable is the rendered README.

It was previously a Python script that auto-generated the README from the GitHub API (cron + `autocommit.sh`); that generator was removed in favour of a hand-maintained static README. Do not reintroduce the generator unless asked.

## Working on the profile

- Edit `README.md` directly, then commit and push to `main`. The profile updates on push.
- There is no local preview server; verify rendering on the GitHub profile page after pushing, or check individual widget image URLs return `200` (see below).

## Widgets are third-party image services, not code

Most of the README's "widgets/badges/counters" are **dynamically-generated images** from external services (GitHub markdown cannot run JavaScript). Everything is themed `tokyonight` (accent `#7AA2F7`). Services in use:

- `readme-typing-svg.demolab.com` - animated typing subtitle
- `skillicons.dev` - tech logo row
- `img.shields.io` - social badges (LinkedIn/X/Website)
- `komarev.com/ghpvc` - profile views counter
- `github-readme-activity-graph.vercel.app` - contribution activity graph

**When an image looks broken, the service is usually down, not the URL.** `curl -s -o /dev/null -w "%{http_code}"` each image URL to confirm. History of live services dying: `github-readme-stats.vercel.app` (503) and `github-profile-trophy.vercel.app` (402) were replaced by `github-profile-summary-cards`, which was in turn **retired in favour of the self-hosted `metrics.svg`** (see below) for reliability. The overall direction is to move stats off flaky live services onto Action-generated committed assets. If a live service dies, prefer a self-hosted/committed alternative over another live one.

## Committed assets and the workflows that generate them

Some visuals are NOT live services: an Action generates the asset and the README points at a static file. These are broken until their Action has run at least once (trigger manually via the Actions tab). All need Actions enabled with read/write permissions.

- **`assets/banner.svg`** - hand-authored custom header banner (no Action, no external service). Edit it directly. Uses SMIL animation (the blinking cursor); keep any text at full opacity so it stays visible in static renderers.
- **`.github/workflows/assets.yml`** - the single generator for the image assets. Builds the snake, the 3D contribution graph, and (if `METRICS_TOKEN` is set) the metrics dashboard into a `dist/` folder, then publishes that folder to a dedicated **`output` branch** with `crazy-max/ghaction-github-pages`. The README reads them from `raw.githubusercontent.com/cajogos/cajogos/output/...` (`github-snake-dark.svg`, `profile-3d-contrib/profile-night-view.svg`, `metrics.svg`). Runs on push to `main` + daily + dispatch.
  - **Why one workflow, not three:** the publish step *replaces* the entire `output` branch each run, so separate workflows pushing there would clobber each other. Keeping all assets in one `dist/` build avoids that. This also keeps `main` free of bot commits and makes `push` triggers loop-safe (it writes to `output`, never `main`).
  - **Metrics** (`lowlighter/metrics`) runs with `output_action: none` (it generates the file, never commits itself) and is gated on `env.METRICS_TOKEN != ''`, so a missing secret just skips metrics while snake and 3D still publish. `METRICS_TOKEN` is a classic PAT with `repo` + `read:org`.
- **`.github/workflows/activity.yml`** - the one workflow that still writes to `main`, because it rewrites the content between the `<!--START_SECTION:activity-->` / `<!--END_SECTION:activity-->` markers directly inside `README.md` (that content cannot live on the `output` branch). Cron + dispatch only. Do not remove those markers.

## Conventions

- **No em dash character (`—`) anywhere.** Use a comma, colon, parentheses, or a hyphen (`-`).
- Non-social images link back to the profile (`https://github.com/cajogos`); the three social badges (LinkedIn, X, Website) link to their own destinations.
- Social badge labels are intentionally terse: `in/cajogos`, `X @cajogos`, `carlos.fyi`.

## Local secrets

`config.yaml` (gitignored, never committed) is a leftover from the old generator and holds an unused GitHub token. It is not needed by anything now.
