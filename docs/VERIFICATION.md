# V2 verification — 2026-09-14

## Result and scope

The local V2 source passed the checks below. No V2 commit, push, publication, or remote workflow dispatch was performed. The live V1 contribution run was confirmed successful, and its five infrastructure/output files remain byte-identical to baseline `b2f9084a623ec00ae80f39b61d7062c2b2e002b9`.

The new telemetry script completed a real public GitHub API fetch locally. Its initial record is in `assets/generated/telemetry.json`: **5 qualifying source projects, 2 with repository pushes in the last 90 days**, with the original API-fetch timestamp retained. These figures are not mocked fixtures and do not include this profile repository or its bot commits.

## Checks

- **GitHub Markdown API:** the final README rendered successfully through `POST /markdown`. The sanitized result preserves responsive pictures, theme-link fragments, cards, tables, collapsed text, local asset references, repository links, and email.
- **Repository claims:** current public READMEs plus package/requirements and selected implementation files were inspected for all four featured projects. Details and sources are in `V2-REVIEW.md`.
- **Links:** each featured repository and the profile were read successfully through GitHub's API. All local image/link targets exist; all five navigation anchors resolve in the local render. LinkedIn remains the exact user-provided URL; it blocks automated checking. Email is a valid `mailto:` link; no email was sent.
- **Workflow lint:** both workflow files pass actionlint v1.7.12. ShellCheck was unavailable and disabled for the actionlint invocation; inline shell blocks were separately checked with `bash -n`.
- **Telemetry tests:** seven tests cover repository scope and the 90-day boundary, pagination, duplicate-page rejection, missing metadata, rate-limit/API failure preserving prior files, partial pagination, missing markers, escaping, preservation of other README content, and absent language/push data. No network is used by these tests.
- **SVGs:** all 24 SVGs parse as XML. No script, external raster embedding, `foreignObject`, or external font resource was added. Visual generators are deterministic when given the same input data.
- **Protected system:** contribution workflow, preparation script, and all three contribution SVGs match the live V1 baseline byte-for-byte. The newer generated-assets commit was incorporated by a local fast-forward before editing.
- **Rollback:** the full source patch was tested by applying it to a temporary V1 archive, then reversing it and comparing file checksums. It restores the baseline without Git history changes.

## Browser and theme matrix

The previews use GitHub-rendered HTML, GitHub-like Markdown styling, and an isolated headless Chrome session with exact device metrics. The review harness reproduces GitHub's current theme-link CSS selectors and the observed `themed-picture` theme-source rewriting. It contains preview-only CSS/JavaScript; none is shipped inside the README.

| Width | OS preference | GitHub mode | Result |
| :--- | :--- | :--- | :--- |
| 1440 px | Dark / light | Auto | Correct desktop composition and palette; no overflow. |
| 768 px | Dark | Auto | Correct desktop composition; no overflow. |
| 390 px | Dark / light | Auto | Correct mobile composition and palette; no overflow. |
| 360 px | Light | Auto | Correct mobile composition; no overflow. |
| 430 px | Dark | Auto | Correct mobile composition; no overflow. |
| 1440 px | Light / dark | Forced opposite theme | Exactly one visible hero; correct desktop layout and requested GitHub palette. |
| 390 px | Light / dark | Forced opposite theme | Exactly one visible hero; correct mobile layout and requested GitHub palette. |
| 390 px | Dark | Auto + reduced motion | Static contribution variant selected. |
| 390 px | Light | Forced dark + reduced motion | Dark mobile panels and static contribution variant selected. |

All requested preview images were produced: 1440 dark/light, 768 dark, and 390 dark/light, plus additional small-screen, reduced-motion, and forced-theme checks. No document/table horizontal overflow, missing image, missing navigation anchor, or out-of-bounds SVG text was found in the final checks.

### GitHub-specific issue found and fixed

GitHub's current theme component rewrites an enabled color-scheme source's whole `media` attribute to match both schemes. Combining a width condition with a color-scheme condition consequently loses the width constraint. The first implementation passed a plain browser preview but was unsuitable for forced GitHub themes.

The final implementation uses the currently served GitHub theme-link selectors to select a palette, and width-only picture queries to select mobile compositions. The existing contribution picture is unchanged because it has no combined width condition. Forced-theme tests include OS and GitHub preferences pointing in opposite directions. This was a concrete platform check, not an assumption that ordinary browser HTML equals GitHub rendering.

## Accessibility

- Custom SVG animations have `prefers-reduced-motion` overrides. Animation samples change at different timeline positions, and no custom CSS animations remain active when the preference is reduced.
- The research pipeline and telemetry are static. Motion never carries the only copy of information.
- Images have descriptive alt text. Research and telemetry have readable expanded text equivalents; project names, links, stacks, claims, and awards remain native Markdown/HTML text.
- All text palette colors have at least **5.00:1** contrast against the design's light surfaces and at least **7.86:1** against dark surfaces. Primary text is at least 12.80:1 (light) / 15.17:1 (dark). Decorative traces/grid lines use lower contrast intentionally; they carry no essential labels.
- The mobile views use dedicated layouts. Essential native text wraps at normal GitHub font sizes. Small SVG metadata is supplementary, with native text equivalents.
- No flashing, hover-only meaning, script-dependent content, or remote font dependency was introduced.

These are measured layout/palette checks, not a claim of a full screen-reader certification or a native iOS/Android app audit.

## Performance

All 24 SVG files, including both palettes, mobile variants, and the three existing contribution outputs, total **157,518 bytes**. Only the viewport-appropriate compositions are selected, but a browser may load the hidden palette alternative as well. The budget conservatively includes both palette images and the collapsed contribution image.

| Representative view | Unique SVG files | Uncompressed SVG total | Local gzip estimate |
| :--- | ---: | ---: | ---: |
| Desktop/tablet | 12 | 71,462 bytes | about 16.8 KB |
| Mobile | 12 | 61,622 bytes | about 15.2 KB |
| Mobile, reduced motion | 12 | 61,760 bytes | about 15.2 KB |

The gzip figures are local compression estimates, not measurements of GitHub's transfer headers or a promise about its image proxy. The asset budget will change as the real contribution calendar and telemetry evolve.

There are **zero third-party image services**, external fonts, videos, GIFs, or embedded raster payloads in V2. Visitor rendering does not call the GitHub API; Actions prepares committed local assets. Preview PNGs, archived V1, and the review harness are ignored and are not README payloads.

## Remaining limitations and deployment checks

1. The V2 profile has not been hosted; live image-proxy behavior and the first telemetry workflow run must be checked after the user approves publication. API sanitization, current theme behavior, and local rendering have been verified independently.
2. GitHub's theme-link selectors are platform behavior. If removed or changed, duplicate palette modules may appear. Ordinary Markdown renderers and native GitHub apps may differ; the supplied local harness is the intended preview.
3. Actions must be enabled and allowed to write to the default branch. Branch rules can reject bot commits. Shared concurrency prevents these two workflows from racing, but a human push can still reject a bot push safely.
4. GitHub can delay schedules or suspend them on inactive public repositories. API quotas/outages leave the last successfully committed snapshot, with its old timestamp. There is deliberately no fake “online” indicator.
5. The snapshot reflects public repository metadata, not private work, deployments, customer usage, or authored contribution totals. Primary languages are repository classifications.
6. Achievement results and personal/contact information are user-supplied; award certificates were not independently checked. No portfolio URL is shown because none was supplied.
7. The new telemetry workflow itself has not run remotely. Both workflow linting and the telemetry generator/tests succeeded locally; that does not replace inspecting the first hosted run.

Publishing and rollback commands are in `PROFILE-MAINTENANCE.md`. The entire upgrade remains ready for review before any remote change.
