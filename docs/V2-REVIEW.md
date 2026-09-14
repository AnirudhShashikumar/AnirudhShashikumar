# Research → Production / V2 review

**Delivery state:** local changes only; no V2 commit, push, publication, or remote workflow dispatch. Baseline: `b2f9084a623ec00ae80f39b61d7062c2b2e002b9`.

## V1 → V2

| V1 | V2 |
| :--- | :--- |
| Orbit around a neural globe | Directed intelligence network with phased packets, responding nodes, a slow orbit, and a scan |
| Dark panels in both themes | Deliberately separate graphite and pale scientific-instrument palettes |
| Paragraph-led profile | Human introduction plus compact mode/current/base/mission readout |
| SatQuery illustration | Observe → analyze → investigate workflow, with schematic inputs and evidence |
| Three large project cards | Four-project connection map plus three concise implementation cards; SatQuery stays the flagship |
| Research bullets | Perception → generation → reasoning → deployment diagram, with readable text expansion |
| Technology list | Capability-to-tool matrix |
| Recognition table | Compact engineering log preserving the two actual supplied results |
| Contribution animation | Same working generator and outputs, reframed as a contribution signal |
| No live repository snapshot | Dated first-party API telemetry with a source record and clear scope |
| Portfolio placeholder | Only verified LinkedIn, email, and GitHub links |

The conceptual path is **observe → reason → build → validate → deploy**. It describes an engineering approach, not a claim that every research model is deployed or every product is independently production-certified.

## Research principles

Reviewed current source from the [profile showcase](https://github.com/abhisheknaiidu/awesome-github-profile-readme), [Anthony Fu](https://github.com/antfu/antfu), [Andrej Karpathy](https://github.com/karpathy/karpathy), [Simon Willison](https://github.com/simonw/simonw), [DenverCoder1](https://github.com/DenverCoder1/DenverCoder1), and [Sindre Sorhus](https://github.com/sindresorhus/sindresorhus). These cover minimal, research, maintainer, self-updating, motion-heavy, and strongly personal approaches. Their current aesthetics vary; no design, assets, phrasing, or stats component was copied. Simon Willison's [self-updating README explanation](https://simonwillison.net/2020/Jul/10/self-updating-profile-readme/) supports the durable pattern of committing dated content rather than making the visitor depend on a runtime service.

| Criterion | Applied principle |
| :--- | :--- |
| Immediate clarity | Name, AI/vision/full-stack roles, and tagline precede metadata. |
| Visual hierarchy | One signature hero, one flagship, then compact supporting systems. |
| Originality | The imagery encodes this account's research-to-production progression and actual project relationships. |
| Technical credibility | Inputs, workflow, experimental boundaries, and repository links carry the story. |
| Information density | Small metadata labels and short cards; no trophy or badge wall. |
| Mobile readability | Separate compositions, native wrapping text, and larger mobile diagram labels. |
| Animation quality | Packets follow meaningful routes; unrelated decorative motion is omitted. |
| Loading performance | Local vector assets and static committed API output; no external image service. |
| Maintainability | Shared palette/geometry helpers, deterministic visual rebuilds, and unchanged contribution infrastructure. |
| Recruiter usefulness | All four repository links appear near the top; evidence of AI and full-stack work is distinct. |

## Visual and motion architecture

Dark: graphite/navy panels, cool white type, cyan signals, blue nodes, restrained violet replies. Light: pale blue paper, navy type, deeper teal signals, quieter borders. These are purpose-chosen colors, not an inversion filter. The small linked-line mark and consistent metadata typography recur across the page.

`build_visuals.py` produces the hero, flagship, project map, research pipeline, and divider. Every major module has desktop/mobile and dark/light compositions. V1's unused hero/flagship assets were removed from the current worktree but remain in Git history and the V1 archive.

- **Hero:** 16-second signal cycle, 8-second soft asynchronous node pulses, 48-second orbit, 18-second alternating scan. Mobile retains a smaller network and larger type.
- **SatQuery:** 16-second packets connect sensor input, model analysis, and spatial evidence; the second desktop path is phase-shifted.
- **Project map:** low-amplitude, phase-shifted signal paths connect project domains to the shared practice.
- **Divider:** one slowly traversing signal, with a meaningful static trace.
- **Research and telemetry:** static; adding motion would not improve the information.
- **Contribution signal:** the original working cyan snake path and data, unchanged.

All custom motion is internal SVG CSS and stops under `prefers-reduced-motion`. Still frames remain complete. There are no scripts, raster textures, external font loads, `foreignObject`, or filter stacks in these SVGs.

## Exact README structure

1. Signature hero and compact navigation.
2. `SYSTEM://PROFILE`: human introduction, identity readout, four project links.
3. Current mission: SatQuery AI, pipeline, scope, stack.
4. Project constellation: conceptual map, Dayflow, MediFit, Gesture Globe.
5. Intelligence pipeline: research interests and text equivalent.
6. Capability matrix: what can be built with the tools.
7. Engineering log: the two supplied achievements.
8. GitHub telemetry: dated public snapshot and scope.
9. Contribution signal: expandable original contribution visualization.
10. Connect: professional links.

## Complete source change list

**Modified:**

- `README.md`
- `assets/divider.svg`
- `docs/PROFILE-MAINTENANCE.md`
- `docs/VERIFICATION.md`

**Added:**

- `.github/workflows/telemetry.yml`
- `scripts/build_visuals.py`
- `scripts/generate_telemetry.py`
- `tests/test_telemetry.py`
- `docs/V2-REVIEW.md`
- `assets/hero-v2.svg`
- `assets/hero-v2-light.svg`
- `assets/hero-v2-mobile.svg`
- `assets/hero-v2-mobile-light.svg`
- `assets/satquery-v2.svg`
- `assets/satquery-v2-light.svg`
- `assets/satquery-v2-mobile.svg`
- `assets/satquery-v2-mobile-light.svg`
- `assets/project-map.svg`
- `assets/project-map-light.svg`
- `assets/project-map-mobile.svg`
- `assets/project-map-mobile-light.svg`
- `assets/research-pipeline.svg`
- `assets/research-pipeline-light.svg`
- `assets/research-pipeline-mobile.svg`
- `assets/research-pipeline-mobile-light.svg`
- `assets/generated/telemetry.svg`
- `assets/generated/telemetry-light.svg`
- `assets/generated/telemetry-mobile.svg`
- `assets/generated/telemetry-mobile-light.svg`
- `assets/generated/telemetry.json`

**Removed as unused V1 design assets:**

- `assets/header.svg`
- `assets/header-mobile.svg`
- `assets/satquery.svg`
- `assets/satquery-mobile.svg`

**Unchanged:** contribution workflow, contribution preparation script, all three working contribution SVGs, Dependabot configuration, and `.gitignore`.

Review-only files in ignored `.preview/` are not production changes: archived V1, rendered markup, preview CSS/harness, PNGs, browser/performance reports, comparison images, file checksums, and the reversible source patch.

## Data and claim audit

| Claim | Evidence / treatment |
| :--- | :--- |
| SatQuery inputs and workflows | Current public README and Python requirements support SAR/optical/temporal analysis, VQA, spatial grounding, FastAPI, PyTorch, and Transformers. Pix2Pix and SARFusionFormer retain their visualization/experimental qualifications. No accuracy or model-readiness numbers were added. |
| Dayflow systems engineering | Current README/package support Next.js, TypeScript, Supabase, PostgreSQL RLS, role-based portals, audit history, and Vitest. No user/adoption or independently audited-security claims. |
| MediFit | Nested current README, `ai_engine.py`, and frontend package support React/TypeScript, FastAPI, Gemini, medication-context analysis, and multimodal reports. Older root-README Next.js/Supabase wording is not repeated. “Clinical-grade” claims are deliberately omitted. |
| Gesture Globe | Current README/package support MediaPipe, Three.js, Next.js, TypeScript, hand landmarks, and gesture-to-transform interaction. No FPS promises or device-independent performance claims. |
| Achievements | User-confirmed Inception 2.0 / GDG win among 130 teams and third place at Push, Pull, Commit. No dates or extra wins inferred. These are user-supplied results, not independently verified award certificates. |
| Name, student status, Bengaluru, current mission | User-provided profile information; no fabricated job title or affiliation. |
| Contacts | User supplied LinkedIn and `Anirudh.shashikumar@gmail.com`. Portfolio omitted because no real URL was supplied. |
| Telemetry | Generated from public GitHub API records with explicit exclusions and timestamp. Profile-generated commits are excluded from project counts. No followers, stars, views, fake streaks, or synthetic contribution data. |

Project evidence: [SatQuery AI](https://github.com/AnirudhShashikumar/SatQuery-AI), [Dayflow](https://github.com/AnirudhShashikumar/Dayflow), [MediFit implementation](https://github.com/AnirudhShashikumar/MediFit/tree/main/mediFit-main), [Gesture Globe](https://github.com/AnirudhShashikumar/gesture-globe). [REST repository API](https://docs.github.com/en/rest/repos/repos) defines the metadata used by telemetry.

## Four-perspective critique and reduction

- **Product designer:** The identity needed a coherent process, not more widgets. Added the shared signal vocabulary and two deliberate palettes. Kept full mobile compositions. Removed the recognition entry-number column after it crowded the phone layout.
- **Staff frontend engineer:** Plain browser success was insufficient. Inspected GitHub's actual theme component and found that it drops combined width conditions; changed the wrapper architecture and tested forced themes opposite to the OS. Kept the proven contribution files byte-for-byte; isolated and tested telemetry failure behavior.
- **AI researcher:** Preserved observed-versus-generated imagery, experimental SARFusionFormer status, and evidence language. Avoided benchmark/clinical/deployment claims unsupported by inspection. The project map is explicitly conceptual.
- **Recruiter:** All four projects are linked before the flagship section; SatQuery differentiates the profile, Dayflow shows full-stack depth, and Gesture Globe makes applied vision tangible. Cards are shorter than V1. Student status remains clear.

Reduction removed the portfolio placeholder, redundant standalone SatQuery heading, an unnecessary recognition column, old unused visual assets, and any proposed extra stats or badge sections. The research pipeline and telemetry do not animate. Expanded technical details remain available without dominating the initial scan.

## Previews and comparison

The local preview set is under `.preview/v2/`: `1440-dark.png`, `1440-light.png`, `768-dark.png`, `390-dark.png`, `390-light.png`, plus 360/430px and forced-theme checks. `before-after-desktop.png` and `before-after-mobile.png` compare V1 with the final V2. The review page is `.preview/review.html`. These files are intentionally ignored by Git.

See [verification](VERIFICATION.md) for performance, compatibility, accessibility, tests, and remaining limitations. See [maintenance](PROFILE-MAINTENANCE.md) for exact publishing and pre/post-publication rollback commands. Publication requires the user's approval.
