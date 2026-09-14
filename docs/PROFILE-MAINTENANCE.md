# Profile V2 maintenance

V2 is a **local, uncommitted upgrade** of the working profile. No V2 commit, push, workflow dispatch, or publication was performed.

The checkout originally pointed at `9e3e3fa949de44bccc4697fcbe31ecb15300e9c3`. It was clean and one generated-assets commit behind the live repository. A local fast-forward brought in the already-published commit **`b2f9084a623ec00ae80f39b61d7062c2b2e002b9`**, which is the V1 rollback baseline. No new commit was created by that operation. A complete V1 copy and checksum manifest are preserved in ignored `.preview/v1/` and `.preview/v1-manifest.json`.

## Working contribution system: preserved

These five files are byte-identical to the live V1 baseline:

- `.github/workflows/snake.yml`
- `scripts/prepare_snake.py`
- `assets/generated/contributions.svg`
- `assets/generated/contributions-dark.svg`
- `assets/generated/contributions-static.svg`

The existing [contribution run](https://github.com/AnirudhShashikumar/AnirudhShashikumar/actions/runs/34778299282) was inspected and reported **success**. It runs at **02:23 UTC / 07:53 IST daily**, on relevant pushes, and manually. V2 changes its presentation to “Contribution signal”; the generator, paths, palettes, static fallback, schedule, permissions, and action pins remain intact.

## New public telemetry

`.github/workflows/telemetry.yml` runs at **02:43 UTC / 08:13 IST daily**, manually, and after changes to its workflow, generator, visual helpers, or tests are pushed to `main`. The scheduled/manual job also checks that it is on the repository's configured default branch. Update the push filter if the default branch is renamed.

The job uses the existing pinned `actions/checkout` version, runs the telemetry tests, fetches public data, then commits only `README.md` and the five telemetry outputs. It uses the built-in `GITHUB_TOKEN`; no PAT, external stats service, new account, or package install is required. Contents-write permission is scoped to the refresh job. Existing Dependabot configuration covers the new workflow.

Both workflows share the existing `contribution-snake` concurrency group. The new workflow adopts that group so the proven workflow does not need editing. The staggered schedules reduce overlap; the shared group serializes repository-writing runs. Neither job force-pushes. A concurrent human push can safely reject a bot push; rerun the affected job after reviewing the branch.

`python3 scripts/generate_telemetry.py` maintains:

- `assets/generated/telemetry.svg` and `telemetry-light.svg`
- `assets/generated/telemetry-mobile.svg` and `telemetry-mobile-light.svg`
- `assets/generated/telemetry.json`
- Only the region between `<!-- telemetry:start -->` and `<!-- telemetry:end -->` in `README.md`

Do not hand-edit that marker region. The image, its alt text, and the expandable text snapshot are rendered from the same data.

### Data definitions

The generator paginates GitHub's public user-repository endpoint. A source project is owned by this account, public, non-fork, non-archived, enabled, non-empty, and not the profile repository. “Pushed in 90 days” uses GitHub's `pushed_at`, not `updated_at`, commits authored, production status, or deployments. Primary languages are GitHub's dominant language classifications for those source repositories, ordered by repository frequency and then alphabetically for ties. They do not measure expertise or framework use.

The JSON records scope, timestamp, source endpoint, included repositories, counts, primary languages, and the two latest repository push dates. The renderer labels the data as a dated snapshot. The initial snapshot was fetched successfully from GitHub locally; the new hosted workflow has not yet run.

All API pages and metadata are checked before writing. Failed/partial responses, rate limits, duplicate pagination results, or missing marker pairs fail the refresh. Each local file replacement is atomic; CI only commits after the complete generator succeeds. A filesystem failure may leave incomplete *local* replacements, but the failed CI step prevents publishing them. A failed run never replaces the hosted snapshot with zeroes or a fake “live” status.

## Rebuild and check locally

```bash
python3 scripts/build_visuals.py
python3 -m unittest discover -s tests -v
python3 scripts/generate_telemetry.py
git diff --check
```

The first command rebuilds the 17 design SVGs and never touches the contribution files. It uses only Python's standard library. Telemetry performs a public API request and updates its timestamp; an optional `GITHUB_TOKEN` increases the available API quota. Never commit a token.

If actionlint is installed:

```bash
actionlint .github/workflows/snake.yml .github/workflows/telemetry.yml
```

## Responsive theme behavior

The design uses explicit dark/light SVG palettes and full mobile compositions. GitHub's current `themed-picture` component replaces the complete `media` value of color-scheme sources when a site theme is forced, which discards combined width conditions. This behavior was inspected in the live site's component before delivery.

For the five new responsive visual modules, V2 therefore separates concerns:

- A pair of links ending in GitHub's existing `#gh-dark-mode-only` / `#gh-light-mode-only` theme selectors chooses the palette.
- Each contains a standard `<picture>` whose source uses **only** `(max-width: 600px)` to choose the mobile composition.
- The existing contribution picture retains its working theme-only and reduced-motion queries.

The theme-link selectors were verified in GitHub's currently served global CSS. No custom HTML CSS or JavaScript is embedded in the README. The local preview harness reproduces those selectors and the site's picture-source rewriting. This avoids relying on a browser-only combined query that would break in GitHub's live renderer.

Outside GitHub, an ordinary Markdown renderer may show both palette variants. Use the supplied preview harness when reviewing locally. If GitHub removes its existing theme-link selectors, revisit this mechanism; the content remains readable, but duplicate visual modules could appear. Keep that limitation in mind when changing the image markup.

## Publishing — only after approval

These commands have **not** been run. They assume this checkout is still on `main`, with only the reviewed V2 changes. Inspect the diff before staging. The fresh telemetry command may change its dated snapshot if public repository data has changed.

```bash
cd '/Users/anirudhshashikumar/Documents/Projects/AnirudhShashikumar profile repository'
git status --short
python3 scripts/build_visuals.py
python3 -m unittest discover -s tests -v
python3 scripts/generate_telemetry.py
git diff --check
git add -A -- README.md assets scripts tests docs .github/workflows/telemetry.yml
git commit -m 'Upgrade profile to Research → Production V2'
git fetch origin main
git rebase origin/main
git push origin main
```

If rebase reports a conflict, resolve and review it before pushing; `git rebase --abort` returns to the local committed V2 state. Never force-push. The new workflow should start from its initial push. Inspect the hosted README and the first telemetry run after publishing. No GitHub Pages or hosting deployment is involved.

## Roll back before publishing

The ignored `.preview/v2/review.patch` contains the complete reviewed V1→V2 source change, including added/deleted files. Its forward and reverse application were tested against the V1 archive. These exact commands restore the reviewed worktree to V1 without changing Git history or remote state:

```bash
cd '/Users/anirudhshashikumar/Documents/Projects/AnirudhShashikumar profile repository'
git apply --reverse --check .preview/v2/review.patch
git apply --reverse .preview/v2/review.patch
```

If you have edited V2 since delivery, the check can fail; preserve those edits and inspect the conflict instead of forcing the patch. The patch is a review artifact, not a tracked runtime dependency.

## Roll back after publishing

Use a new rollback commit, not a history rewrite. The following restores the V1 design while retaining the latest contribution outputs and its working workflow. It removes only V2 files; keep additional work elsewhere out of this rollback.

```bash
cd '/Users/anirudhshashikumar/Documents/Projects/AnirudhShashikumar profile repository'
git switch main
git pull --ff-only origin main
git restore --source=b2f9084a623ec00ae80f39b61d7062c2b2e002b9 --worktree -- README.md assets/divider.svg assets/header.svg assets/header-mobile.svg assets/satquery.svg assets/satquery-mobile.svg docs/PROFILE-MAINTENANCE.md docs/VERIFICATION.md
git rm -- .github/workflows/telemetry.yml assets/hero-v2*.svg assets/satquery-v2*.svg assets/project-map*.svg assets/research-pipeline*.svg assets/generated/telemetry* scripts/build_visuals.py scripts/generate_telemetry.py tests/test_telemetry.py docs/V2-REVIEW.md
git add -- README.md assets/divider.svg assets/header.svg assets/header-mobile.svg assets/satquery.svg assets/satquery-mobile.svg docs/PROFILE-MAINTENANCE.md docs/VERIFICATION.md
git commit -m 'Restore V1 profile while preserving contribution updates'
git push origin main
```

Avoid running rollback while a telemetry job is writing; cancel or let that run finish first. The rollback removes the telemetry workflow and keeps `snake.yml`. These commands have been documented, not executed on the live repository.
