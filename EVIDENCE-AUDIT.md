# Evidence audit against GRADING.md

## Current approved cloud deployment audit — October 16, 2026

**Estimated verified score: 96/100.** This section supersedes all pre-apply conclusions below. Terraform created 28 resources; actual VPC/subnets, ACTIVE EKS, two Ready workers, application CRUD, bound encrypted PostgreSQL disk and monitoring are verified. [Complete criterion mapping](GRADING-CHECKLIST.md), [submission guide](SUBMISSION.md).

- **55 public PNGs** audited: 28 original, 14 pre-apply Sydney and 13 actual cloud/release captures. The new cloud screenshots were visually opened and are readable. AWS VPC/subnet/EKS Console pages show genuine resources; terminal captures show actual apply/runtime/network/HTTP/metrics results; browser captures show the real ELB app, Prometheus target UP and populated Grafana panel.
- New primary cloud files: `aws-vpc-console.png`, `aws-subnets-console.png`, `aws-eks-console.png`, `aws-apply-verified.png`, `aws-network-verified.png`, `eks-pods-helm.png`, `eks-services-ingress.png`, `eks-metrics.png`, `eks-application-browser.png`, `eks-prometheus-targets.png`, `eks-grafana-dashboard.png`, all under `evidence/sydney/`.
- Source commands/URLs/timestamps/hashes are recorded in Sydney terminal, AWS Console and EKS browser manifests. PNG CRC/decompression, JSON parsing and manifest hashes are checked in `evidence/sydney/inventory.json`. Private state, passwords, kubeconfig and diagnostic captures are excluded from the public inventory and Git.
- The initial Grafana loading capture was replaced after actual series appeared. The metrics transcript/output filename collision was corrected; pure metrics are `eks-application-metrics.txt`. The empty migration log is supplemented by actual PostgreSQL migration/table queries and successful init-container status.
- One initial traffic-loop connection reset is retained and disclosed; subsequent bounded-retry verification passed. Existing Compose and Minikube were preserved.
- **Still missing:** real destroy completion/screenshot (separate approval required), teacher-form receipt, and instructor acceptance of the supplied automated release recording. No manual screenshot is currently necessary. No resources have been deleted.

Historical records below describe their capture times; old AWS restriction/missing-resource statements do not describe the now-deployed Sydney account.


## Historical pre-apply Sydney audit — October 16, 2026

This section and [the current submission guide](SUBMISSION.md) supersede the old-account/Mumbai restriction and historical-plan-only conclusions below. Current target: `525426877661 / devops-new / ap-southeast-2`; deadline October 19. Sydney reads and account-guarded planning pass; **AWS apply is awaiting approval, not blocked by the former account's subscription error**.

- Every rubric row is mapped to implementation, actual verification and screenshot filenames in [GRADING-CHECKLIST.md](GRADING-CHECKLIST.md); estimated verified marks remain 86/100. Missing: VPC/EKS/destroy 9, teacher form 2, accepted student presentation 3.
- **14 new screenshots** in `evidence/sydney/` were captured from actual terminal windows/browser pages and visually opened for review: plan, account, pricing, validation, tests, runtime, failure recovery, Compose/Ingress app, Prometheus UP, Grafana populated panel, and current successful CI/GHCR pages. All are genuine, readable, and support their stated scope; terminal plan/cost captures explicitly do not claim deployment.
- Current plan screenshot shows all 28 create actions, plan result and account/profile/region/CIDR/source/hash checks. The original 22-resource plan is preserved separately; it lacked later safeguards. [Complete current plan](evidence/sydney/terraform-plan.txt).
- Real serial AWS checks report the correct assumed role, available Sydney AZs, empty EKS/project-VPC inventory and PAID/ACTIVE with USD120 credits. Credit grant coverage/expiry/sharing remains unverified.
- Local rechecks: 16 tests passed; frontend build passed; Compose and Ingress CRUD passed; all seven main Pods Ready; HPA CPU metrics valid; Prometheus up=1; populated current Grafana screenshot.
- Five local failure exercises recovered; the temporary namespace was removed. The capture labels its exact saved-log excerpts and also runs current Pod/namespace checks. Initial observation/startup failures and the local external-registry DNS limitation are disclosed in [troubleshooting](docs/TROUBLESHOOTING.md).
- Source commands/URLs, capture timestamps, exit codes/status and SHA-256 hashes: `evidence/sydney/terminal-capture-manifest.json` and `browser-capture-manifest.json`. Extended inventory: `evidence/sydney/inventory.json`.
- The existing local release remains Helm revision 10 with unchanged data path/storage class. EKS storage/ingress/monitoring manifests are locally validated **IMPLEMENTED**, not verified cloud deployments.
- Still missing: actual AWS Console resource screenshots and successful destroy output, accepted presentation/actual commit-to-rollout recording, and teacher form receipt. These cannot be replaced by generated files, a plan screenshot, or current-state video.

## Historical first-account screenshot audit

The following records the earlier audit and its conclusions at that time; use the current section and submission guide for the new account.

Subsequent AWS setup update: [fresh authenticated plan](evidence/terraform-plan-aws-login.txt) now succeeds using the project's credential-process adapter. This supersedes the plan-replay failure and potential 2-mark deduction described in the historical audit below. The existing plan screenshot still shows the historical artifact. EC2/EKS deployment remains unverified and EKS still rejects service access. See [AWS setup](docs/AWS-PLAN.md). Newly added AWS artifacts postdate the screenshot audit inventory.

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

## Actual recorded release demonstration — October 16

The prior current-state-only video is superseded for M10 by [the continuous 304.68-second release recording](evidence/sydney/m10-real-release-walkthrough.webm) and [separate result-verification continuation](evidence/sydney/m10-release-result-continuation.webm). The latter is explicitly separate: the original GitHub browser UI lagged behind its completed API status. No synthetic status or spliced event is presented.

Actual sequence: commit `04108043563d24dfc2ceb70e050fd56b5e9cc577` clarifies the HIGH/URGENT count; push triggered [CI 38946277016](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38946277016); all jobs passed; Helm upgraded only the EKS frontend to that immutable SHA; release revision 2 and two Ready frontend replicas were verified; the public page displayed “High & urgent”; CRUD passed afterward. Backend, database and Minikube images were preserved.

Evidence: `evidence/sydney/release-demo-manifest.json` records timestamps/events/hash; `release-demo-ci.json` and `.txt` record actual success; `release-demo-commands.txt` contains real commands/results; `release-video-review.json` records codec/dimensions and visual sample review; `.vtt` provides event captions. This is an automated technical recording, without student narration or any claim of instructor acceptance. [Presentation notes and submission text](docs/PRESENTATION.md).

**Estimated demonstrated technical score: 96/100.** The remaining four marks require actual approved cleanup (2) and linking the repository in the teacher's form (2). Neither has occurred. No cleanup or final submission is authorized by a request to increase the score.
