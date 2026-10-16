# Evidence audit against GRADING.md

Audit date: 2026-10-16. Baseline public commit: `15b303b` (14 commits). Scope: all files in `evidence/`, every module's "What to Submit", and the teacher's final submission checklist in [docs/TEACHER-GRADING.md](docs/TEACHER-GRADING.md). Per-criterion grading status remains in [PROGRESS.md](PROGRESS.md).

**Result:** visual evidence for M1–M6, M8, and M9 is complete. M7 is partial. M10 has a README and a supplementary automated visual walkthrough, but the required student presentation or a recording of the actual commit → pipeline → rollout event remains unverified. The teacher's submission form has not been completed. This is an AWS-limited submission package, not proof of all 100 marks.

## Required submission evidence

| Module | Required submission item | Audit result | Primary artifact |
|---|---|---|---|
| M1 | Backend source, migration, requirements, frontend source, Compose | COMPLETE | Source files checked in `evidence/audit/source-checks.json`; PostgreSQL schema and Alembic head in `m1-health-database.png` |
| M1 | Running application browser screenshot | COMPLETE | `m4-compose-browser.png`; `m1-ticket-editor.png` supplements it |
| M2 | Tests and pytest configuration | COMPLETE | 16 tests, isolated SQLite fixture, pytest.ini; current run `audit/m2-pytest.txt` and prior valid `pytest.xml` |
| M2 | Terminal screenshot of pytest -v passing | COMPLETE | `m2-pytest.png`: all 16 tests pass, one visible deprecation warning, exit 0 |
| M3 | Public repository URL linked in teacher form | PENDING SUBMISSION | Public repository is accessible; no form receipt or confirmation exists |
| M3 | Commit-history screenshot with 10+ commits | COMPLETE | `m3-git-history.png`: 14 meaningful messages plus remote URL |
| M4 | Two Dockerfiles and Compose definition | COMPLETE | Files present; build output captures both images; runtime UIDs 10001/101 verified |
| M4 | Terminal screenshot of Compose up --build | COMPLETE, SAFETY FLAGS DISCLOSED | `m4-compose.png`: actual build/up with --no-recreate --no-deps; containers healthy; before/after container IDs unchanged; full build in `audit/compose-build-no-recreate.txt` |
| M4 | Browser at localhost:3000 | COMPLETE | `m4-compose-browser.png`; source URL and HTTP 200 recorded in browser manifest |
| M5 | Workflow YAML and successful run URL | COMPLETE | `.github/workflows/ci.yml`; `m5-actions-success.png`; [green baseline run](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38894949621) |
| M5 | GHCR package page with SHA tags | COMPLETE | `m5-ghcr-backend.png` and `m5-ghcr-frontend.png`; both actual public pages, SHA tags readable |
| M6 | Trivy steps in workflow | COMPLETE WITH FILTERS DISCLOSED | HIGH/CRITICAL, exit-code 1, ignore-unfixed true, scoped `.trivyignore.yaml` exceptions |
| M6 | Pipeline Trivy output screenshot | COMPLETE | `m6-trivy-backend.png`, `m6-trivy-frontend.png`: actual terminal display of a labeled excerpt from genuine saved CI output; full `actions-run.txt` retained |
| M6 | 2–3 sentence scan explanation | COMPLETE | `SUBMISSION.md` includes three sentences; `docs/SECURITY.md` explains CVE-2025-47273 and exact SBOM exceptions |
| M7 | Terraform .tf files and example tfvars | COMPLETE | Source checks; no actual credentials or state tracked |
| M7 | init, format, validate evidence | COMPLETE | `m7-terraform-validation.png`: init/fmt/validate passed during this audit |
| M7 | Plan output screenshot | QUALIFIED HISTORICAL EVIDENCE | `m7-terraform-plan-saved.png`: a real terminal displaying the saved 22-resource no-refresh dry-run output; not a fresh authenticated plan, not an apply approval artifact; later plan replay failed |
| M7 | AWS Console VPC and EKS in expected region | MISSING / BLOCKED | No VPC/EKS was provisioned. `m7-aws-restriction.png` shows current EC2 OptInRequired and EKS SubscriptionRequiredException; both underlying commands exited 254 |
| M7 | terraform destroy completion screenshot | MISSING / BLOCKED | No apply occurred and no project cloud deployment exists to destroy; no synthetic destroy output was created |
| M8 | Namespace/bootstrap manifests and Helm chart | COMPLETE | Files present; chart lint/render passed in saved green CI; running release revision 10 |
| M8 | Running Pods screenshot | COMPLETE | `m8-pods.png`: all seven Pods Running/Ready, backend/frontend 2 replicas, valid HPA CPU metrics, bound PVC |
| M8 | Services screenshot | COMPLETE | `m8-services.png`: ClusterIP Services and populated backend/frontend EndpointSlices |
| M8 | helm list screenshot | COMPLETE | `m8-helm.png`: release deployed, revision 10, exact SHA image references |
| M8 | App through Ingress/LoadBalancer | COMPLETE | `m8-ingress-browser.png`, HTTP 200 from http://192.168.58.2/; original CRUD smoke in `live-demo.txt` |
| M9 | Monitoring values/configuration | COMPLETE | Prometheus values, static scrape equivalent, Grafana datasource/dashboard configuration present |
| M9 | curl backend /metrics screenshot | COMPLETE; BAD OLD CAPTURE FIXED | `m9-metrics.png`: HTTP 200 + Prometheus content type + real HTTP counters; corrected `application-metrics.txt` |
| M9 | Prometheus Targets page UP screenshot | COMPLETE | `m9-prometheus-targets.png`: relaydesk-backend 1/1 UP, actual cluster service /metrics endpoint, recent scrape; current API response also saved |
| M9 | Populated Grafana dashboard screenshot | COMPLETE | `m9-grafana-current.png`: actual /api/tickets, /health, /ready request-rate series; current Grafana health API saved |
| M10 | Root README | COMPLETE | README.md explains domain, execution, API, tests, platform, security and AWS limitations |
| M10 | Live presentation or accepted recorded walkthrough including commit → CI → deployment update | PENDING PRESENTATION | Historical sequence is supported by actual `live-demo.txt` and CI logs. New `m10-automated-walkthrough.webm` reviews current UI/monitoring and historical CI; it does not capture a new commit or rollout, and has no student narration |

## Screenshot quality and authenticity

All **28 PNGs** were opened and visually reviewed. **23 were captured during this audit**, supplementing five historical screenshots. No screenshot contains a fabricated terminal result, an artificial resource status, a login/error page substituted for successful evidence, or unrelated desktop content.

- Actual terminal screenshots were captured from temporary Foot terminal windows using the window's own geometry and `grim`. Each shows commands and output; raw output, UTC capture time, command text, exit code, and SHA-256 are in `audit/terminal-capture-manifest.json`. The AWS wrapper exits 0 because capture succeeded, but both actual AWS commands visibly exited 254; this is restriction evidence only.
- Browser screenshots were taken from actual pages using isolated Playwright/Chromium sessions. Source URL, response URL, HTTP status, title, capture timestamp, and SHA-256 are in `audit/browser-capture-manifest.json`. GHCR was accessible anonymously as Public; no manual authentication was needed. Focused 1440×1100 captures keep package SHA tags readable.
- The backend Trivy screenshot shows exact OS/Python summary rows from the saved CI table, not a newly executed scan. Detailed clean package rows are omitted from that screenshot for readability and remain in the full log. The extraction helper is retained as `audit/trivy-excerpt.py`. Scan policy exclusions are disclosed, so zero reported findings is not a claim of zero possible vulnerabilities.
- The historical app screenshots remain valid supplementary views, but do not show URL bars or image tags. The new browser captures are bound to their URLs in the manifest. The image-SHA claim relies on the actual Helm/Deployment output, not on the appearance of the UI alone.
- `relaydesk-mobile.png` shows only the upper mobile viewport. New `m1-mobile-tickets.png` and `m1-mobile-actions.png` show the ticket table and controls on a 390-pixel screen. The table deliberately scrolls horizontally; the pair proves left and right areas are reachable.
- `m7-terraform-plan-saved.png` is qualified historical output, visibly labeled as such. It does not prove AWS creation or present credential validity.
- The 71.56-second, 1280×900 VP9 WebM is a real isolated browser recording, with captions and a URL/timing manifest. Sampled frames were visually checked for the app, editor, successful CI, public package page, UP target, and populated Grafana panel. It is supplementary presentation material, not a recording of the original deployment event.

The full evidence inventory includes PNG dimension/CRC checks, file sizes, SHA-256 hashes, and screenshot review notes in `audit/inventory.json`.

## Corrections made

1. Replaced invalid `application-metrics.txt` (frontend HTML from the wrong route) with genuine backend metrics from `http://127.0.0.1:8000/metrics`. The Ingress `/metrics` path serves the frontend; no app routing was changed.
2. Added all obtainable missing screenshots: pytest, Git history, Compose build/health, GHCR packages, green Actions overview, pipeline Trivy output, Terraform validation/saved-plan/restriction, Pods, Services, Helm, metrics, and Prometheus Targets.
3. Refreshed the populated Grafana and app screenshots and added mobile table/action and editor views. No ticket was created, updated, or deleted during this audit; tests used the isolated fixture.
4. Corrected stale documentation from Helm revision 9 to the actual revision 10.
5. Reclassified the form submission and actual presentation as pending instead of complete. The strict estimate is now 86/100 including 2 qualified historical-plan marks; it is 84 if the instructor requires a fresh authenticated plan. Completing the form/presentation supports the former 91 non-AWS estimate, subject to grading.
6. Preserved the current running containers and Pods. Compose builds used --no-recreate and verified unchanged container IDs. No Helm upgrade, Kubernetes mutation, AWS apply/destroy, IAM, account, or billing change was performed.

## Entire-folder disposition

- Primary current screenshots: all `m1-` through `m9-` PNGs; use `SUBMISSION.md` to select them.
- Historical supplemental PNGs: `relaydesk-compose.png`, `relaydesk-minikube.png`, `relaydesk-minikube-sha.png`, `relaydesk-mobile.png`, `grafana-relaydesk-dashboard.png`.
- Valid text/runtime evidence: pytest output/XML, frontend build, Docker status/smoke, Minikube status, live-demo output, full Actions log/result, Prometheus responses, corrected metrics, rendered Helm YAML, and Terraform validation.
- Qualified historical artifacts: `terraform-plan-refresh-false.txt` and its screenshot; the plan cannot currently be replayed successfully. Local Trivy JSON reports apply to their recorded `Metadata.ImageID`, not any later image that reuses a mutable local tag. Primary security evidence is the successful immutable release CI scan.
- New audit records: raw terminal outputs, browser page text, monitoring API snapshots, source-file checks, capture manifests, limited known-secret-signature check, inventory, and walkthrough timeline/captions.
- Missing artifacts remain explicit: real AWS Console resource screenshots, real Terraform destroy completion, completed teacher submission, and an accepted student presentation or recording of the actual commit-to-rollout sequence.

## Submission readiness

**Ready to hand in with the AWS limitation disclosed; not complete for every requirement.** No manual screenshot is needed for the working local system. AWS resource screenshots cannot be supplied manually while those resources do not exist. Submit the repository and primary evidence through the teacher's form, and complete the presentation requirement. Keep the existing local stack available for the live presentation.
