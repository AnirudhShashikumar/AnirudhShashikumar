# Profile maintenance

This profile is prepared for the public repository `AnirudhShashikumar/AnirudhShashikumar`. The supplied local directory was empty and had no Git history. The public profile repository returned HTTP 404 during the audit on 2026-09-14; no existing profile README or assets were overwritten.

## Publish

Create the public profile repository with the exact name `AnirudhShashikumar`, if needed, and commit these files to its `main` branch. GitHub displays a matching public repository's root README on the account profile. This delivery does not create or push a remote repository.

The initial push containing `snake.yml` starts the contribution workflow. You can also choose **Actions → Refresh contribution snake → Run workflow**. If your default branch is not `main`, update the workflow's push branch filter; scheduled and manual runs already use the configured default branch.

The workflow runs at **02:23 UTC / 07:53 IST daily**, on relevant pushes to `main`, and manually. GitHub can delay scheduled runs or disable schedules on inactive public repositories. It uses only the built-in `GITHUB_TOKEN`, with repository-content write permission scoped to the refresh job. No personal access token is required. Repository or organization policy must allow Actions and the bot's commits to the default branch. If branch protection blocks that write, adapt publishing to a pull request or dedicated assets branch before enabling the schedule.

Both actions are pinned to full upstream commit SHAs, verified through GitHub's API, and use Node 24. Dependabot checks GitHub Actions monthly. The workflow commits only the three generated SVGs, skips unchanged output, avoids force pushes, and serializes refresh runs. A concurrent human push can safely reject the bot's push; rerun the workflow in that case. The generated-file commit does not match the workflow's push paths.

## Design and structure

The visual concept is an orbital research interface: charcoal surfaces, cyan signal paths, blue model nodes, and a restrained violet accent. Native GitHub typography carries the content. The README reads in this order:

1. Responsive animated hero and navigation.
2. `SYSTEM://PROFILE` introduction.
3. Currently building: SatQuery AI, the flagship.
4. Selected projects: Dayflow, MediFit, Gesture Globe.
5. Research focus.
6. Engineering stack.
7. Recognition.
8. GitHub activity and an expandable contribution snake.
9. Connect.

The flagship plus three single-column HTML cards makes four featured projects. Each includes a repository link, purpose, technical description, and stack. Tables contain only one project per row and no fixed column widths. About, research, stack, and achievements remain selectable text that wraps with GitHub's own layout. Additional terminal/research/achievement SVGs were deliberately omitted because they would duplicate text and reduce mobile readability.

`assets/header.svg` uses a 42-second orbit and a 7-second soft node pulse. `header-mobile.svg` uses a 30-second compact orbit with larger type. `satquery.svg` uses a slow 10-second alternating scan restricted to a schematic observation tile. `satquery-mobile.svg` uses a static neural motif and larger text. All custom motion uses internal SVG CSS, has a legible still state, and stops under `prefers-reduced-motion`. `divider.svg` is intentionally static.

All graphics are native vectors with no fonts, raster data, scripts, `foreignObject`, or external resources embedded. Opaque dark panels preserve contrast in both GitHub themes. The mobile hero is selected with a `<picture>` media source. Essential project information is repeated as native text beneath the decorative flagship panel, so a scaled illustration never hides the content.

The contribution snake uses actual GitHub contribution data via [Platane/snk](https://github.com/Platane/snk). It is collapsed by default and chooses dark/light variants with `<picture>`. A static variant is selected for reduced-motion readers. The checked-in initial assets explicitly say they are waiting for a workflow run; they show no invented contribution grid. Failed runs leave the previous committed images available. Routine generated-asset commits are visible in repository history; do not interpret this animation as a productivity score.

## Source audit and editorial decisions

Public metadata, root READMEs, recursive file trees, and selected implementation files were inspected. No benchmark, adoption, accuracy, star, streak, follower, or contribution counts were copied into the profile.

| Project | Evidence and decision |
| :--- | :--- |
| [SatQuery AI](https://github.com/AnirudhShashikumar/SatQuery-AI) | Root README documents single-image, optical/SAR, and bi-temporal modes; Sentinel-1/2; FastAPI; PyTorch; Pix2Pix; experimental SARFusionFormer. Its source tree includes inference, evaluation, and model files. The profile retains the distinction between synthetic visualizations and observations. |
| [Dayflow](https://github.com/AnirudhShashikumar/Dayflow) | README and test tree support role-based HR workflows, Next.js, Supabase/PostgreSQL RLS, and Vitest. No claim of audited security, real customer adoption, or completed production acceptance testing is made. |
| [MediFit](https://github.com/AnirudhShashikumar/MediFit) | Root README is older than the nested application. [Nested README](https://github.com/AnirudhShashikumar/MediFit/blob/main/mediFit-main/README.md), `ai_engine.py`, frontend `package.json`, and fitness/lab/health components support React + TypeScript + Vite, FastAPI, and Gemini. The profile avoids the older Next.js/Supabase description and unverified clinical-grade claims. No public repository named MediTwin was found, so the card uses the verified MediFit name. Digital-twin ideas from the brief are not presented as a verified implemented system. |
| [Gesture Globe](https://github.com/AnirudhShashikumar/gesture-globe) | README and source tree support MediaPipe gesture tracking, Three.js, Next.js, TypeScript, and gesture-to-transform mapping. No frame-rate or device-performance promises were repeated. Selected as the fourth project because it demonstrates applied vision and graphics. |
| [TwinFit](https://github.com/AnirudhShashikumar/TwinFit) | Reviewed metadata and source tree; includes mock-data-driven application scaffolding and committed dependencies. Not selected over the stronger, more distinct four projects. |
| [VeilGraph](https://github.com/AnirudhShashikumar/VeilGraph) | Public metadata marks it as a fork. Omitted because the account's specific contribution/ownership was not established. |

Name, student status, Bengaluru location, interests, and achievements come from the user's supplied brief. In a follow-up the user confirmed that the 130-team win was Inception 2.0, so those two initial entries were combined into one award. Achievements were not independently verified, and no dates, team ownership, event affiliation, or awards were inferred from other repositories.

The GitHub profile API had no public email, blog, location, or bio. The reviewed public project documentation had no verified personal contact links. The user then explicitly supplied `https://www.linkedin.com/in/anirudh-shashikumar` and `Anirudh.shashikumar@gmail.com`; these exact contacts are included. Project deployment homepages existed in repository metadata, but were not treated as a personal portfolio or proof of a working backend.

## Information to add

- Personal portfolio URL. Replace the clearly marked text placeholder in the Connect section when available; do not publish a dummy link.
- Optional public award evidence. The supplied achievement wording is retained without invented dates.

## Compatibility and validation

GitHub-supported Markdown, HTML tables, `<picture>`, `<details>`, repository-hosted SVG images, and normal anchors are the only README building blocks. The README contains no custom HTML CSS or JavaScript. CSS exists only within external SVG image files.

Reference: [GitHub writing quickstart](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github), [collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections), [secure action usage](https://docs.github.com/en/actions/reference/security/secure-use), and [snake action documentation](https://github.com/Platane/snk).

The hosted profile and its first scheduled workflow can only be verified after publishing. Local browser checks and GitHub's Markdown rendering API are documented in `VERIFICATION.md`.
