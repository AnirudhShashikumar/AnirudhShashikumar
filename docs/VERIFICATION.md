# Verification — 2026-09-14

## Final results

- GitHub's `POST /markdown` endpoint rendered the final README successfully (HTTP 200). The returned sanitized HTML retained the responsive `<picture>` sources, HTML project cards, repository links, `<details>`, and `mailto:` link.
- All eight SVG files parse as XML. Combined initial SVG size: **13,691 bytes**. Every referenced local image exists.
- The published account and all four featured repository URLs returned HTTP 200. LinkedIn returned HTTP 999 to an automated request; the exact user-supplied URL is retained. Email was checked as a `mailto:` target; no message was sent.
- The workflow passed **actionlint v1.7.12** with no findings. ShellCheck was unavailable and explicitly disabled for that invocation; both inline shell blocks separately passed `bash -n`.
- Both action commit pins were resolved against their upstream GitHub repositories. `actions/checkout` v7.0.1 and the pinned `Platane/snk/svg-only` v3 action both declare Node 24.
- `prepare_snake.py` passed with a real SVG fixture downloaded from the upstream snake project's output branch. It preserved the calendar cells, generated a static copy, and rejected the initial placeholder as a generation result. That upstream user's calendar was used only in a temporary test directory and is **not** included in this profile.

## Visual review

The final GitHub-rendered HTML was loaded in an isolated headless Chrome instance with GitHub-like Markdown CSS. Chrome's device-metrics and media emulation supplied exact viewport widths, themes, and reduced-motion preferences.

| Viewport | Theme | Result |
| :--- | :--- | :--- |
| 320 px | Light | No horizontal document or table overflow; mobile hero and flagship selected. |
| 375 px | Light and dark | No overflow; all images loaded; correct theme variant selected. |
| 768 px | Light | No overflow; desktop hero and flagship selected. |
| 1440 px | Light and dark | No overflow; all cards fit the content column. |
| 375 px | Dark, reduced motion | Static contribution image selected. |

Desktop hero, mobile hero, and desktop flagship CSS were sampled over time: all three animate under normal preferences, and all resolve to `animation-name: none` under reduced motion. The mobile flagship is deliberately static.

Screenshots were reviewed at the top, project cards, research/stack, recognition, and contact sections. The mobile flagship was redesigned after the first visual pass because the desktop illustration's labels became too small. The final version gives it larger mobile type. The award entries were merged after the user confirmed that Inception 2.0 was the 130-team event.

Local review assets live in the ignored `.preview/` directory. They include the rendered HTML, preview-only CSS, and desktop/mobile screenshots. They are not README runtime dependencies and should not be committed.

## Scope of verification

This is verified GitHub-compatible source, with local visual checks using GitHub-rendered markup. The final profile has **not been published**, and GitHub's live profile image proxy/custom theme behavior has not been tested on a hosted commit. Native mobile apps may have their own rendering differences.

The actual contribution-generation job has **not run in the destination repository**. It requires the first push or manual workflow run there, plus Actions permission to commit generated assets. Until then, the checked-in placeholders prevent broken image links and do not display fictional contributions.

No repository statistics, model scores, clinical validation, customer adoption, or other unsupported quantitative claims were introduced. Project descriptions come from public documentation/source; personal details, contacts, and award results come from the user. The only remaining information placeholder is the portfolio URL.
