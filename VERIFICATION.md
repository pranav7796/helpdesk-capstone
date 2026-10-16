# Verification record

Observed on 2026-10-16. Evidence files are under `evidence/`; only actual command and runtime results are called VERIFIED in [PROGRESS.md](PROGRESS.md).

## Application, tests, and containers

- `backend/.venv/bin/pytest -v --junitxml=../evidence/pytest.xml` — **16 passed**, one Starlette deprecation warning; output: [`evidence/pytest.txt`](evidence/pytest.txt). The suite uses an isolated SQLite test database.
- `npm run build` in `frontend/` — Vite production build passed; output: [`evidence/npm-build.txt`](evidence/npm-build.txt).
- `docker compose ps` — PostgreSQL, API, frontend all healthy; both app containers run as non-root (UIDs 10001 and 101): [`evidence/docker-compose-ps.txt`](evidence/docker-compose-ps.txt).
- `python scripts/smoke.py` against the Compose frontend proxy — create/list/read/edit/status/priority/delete all returned expected HTTP codes and persisted data: [`evidence/docker-smoke.txt`](evidence/docker-smoke.txt).

## Kubernetes and observability

- Minikube profile `helpdesk-capstone`; namespace `relaydesk`; Helm release status `deployed`, revision 10. Backend and frontend each have two Ready replicas, PostgreSQL has a bound 2 GiB PVC, and HPA reports current CPU against its target. Current screenshots: [`m8-pods.png`](evidence/m8-pods.png), [`m8-services.png`](evidence/m8-services.png), [`m8-helm.png`](evidence/m8-helm.png).
- Ingress at `http://192.168.58.2/` returned the app; `/api/tickets` returned API data. CRUD smoke through ingress passed after backend rollout. Screenshot: [`evidence/relaydesk-minikube.png`](evidence/relaydesk-minikube.png).
- Prometheus and Grafana Pods ran in Minikube. Prometheus target query returned `up=1`; request counter query returned traffic for API paths. Saved responses: [`prometheus-target.json`](evidence/prometheus-target.json), [`prometheus-requests-query.json`](evidence/prometheus-requests-query.json). Grafana has a populated HTTP requests panel: [`grafana-relaydesk-dashboard.png`](evidence/grafana-relaydesk-dashboard.png). Application exposition: [`application-metrics.txt`](evidence/application-metrics.txt).
- Helm lint/template validation ran in the CI workflow; local rendered chart: [`helm-rendered.yaml`](evidence/helm-rendered.yaml).

## Security and CI/CD

- Historical local Trivy reports contain no reported findings after their HIGH/CRITICAL, ignore-unfixed, and scoped exception filters: [`trivy-backend.json`](evidence/trivy-backend.json), [`trivy-frontend.json`](evidence/trivy-frontend.json). Their `Metadata.ImageID` identifies the scanned images; mutable local tags and running Compose images need not match. Primary release evidence is the CI scan of the immutable `d07bca6` images deployed to Minikube. The filters do not establish absence of all vulnerabilities. See [`docs/SECURITY.md`](docs/SECURITY.md).
- Repository push triggered workflow run [38893336596](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38893336596) for commit `d07bca6accc35f0224aaae8c4057076a9c4c9261`; **all jobs succeeded**. The run passed 16 API tests, the React production build, both image builds, both HIGH/CRITICAL scans, GHCR publication, Helm lint, and manifest rendering. Captured workflow logs and run metadata: [`actions-run.txt`](evidence/actions-run.txt), [`actions-run.json`](evidence/actions-run.json).
- Published images, pulled by their immutable commit SHA and deployed via Helm revision 10:
  - `ghcr.io/pranav7796/helpdesk-capstone/backend:d07bca6accc35f0224aaae8c4057076a9c4c9261` (digest `sha256:c8fbaf5265f683753e70332a148aa5d0db4035530da98ccedcbba865f27ba205`)
  - `ghcr.io/pranav7796/helpdesk-capstone/frontend:d07bca6accc35f0224aaae8c4057076a9c4c9261` (digest `sha256:8023382eb19a37c9a5787efe15036c8e9e11010ef870712ce413b4fc2be73cb1`)
- Both application Deployments rolled out with two Ready replicas each; the Pods used those exact image references. `python scripts/smoke.py` against the Minikube ingress completed create/list/read/edit/status/priority/delete and retained data in PostgreSQL: [`live-demo.txt`](evidence/live-demo.txt). Final runtime screenshot: [`relaydesk-minikube-sha.png`](evidence/relaydesk-minikube-sha.png).
- Earlier run [38886640390](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38886640390) failed on four HIGH findings associated with stale upstream Python build SBOM entries and a vulnerable setuptools version. The app dependency was upgraded; exact stale SBOM package URLs are scoped in `.trivyignore.yaml`. The reports from the current local images are clean.

## Terraform and AWS

- `terraform init -input=false` completed successfully with the locked AWS provider; `terraform fmt -check -recursive` and `terraform validate` passed. Validation output: [`evidence/terraform-validate.txt`](evidence/terraform-validate.txt).
- [`evidence/terraform-plan-refresh-false.txt`](evidence/terraform-plan-refresh-false.txt) is a saved no-refresh, 22-resource dry-run artifact from the earlier successful local plan. It is not a refreshed plan, not an approval artifact, and its cluster-admin CIDR is the documentation placeholder `203.0.113.9/32`. Re-running the plan in this environment later failed because Terraform could not resolve credentials from the AWS profile (`No valid credential sources found`); do not apply the saved artifact.
- Read-only AWS CLI identity check with `--profile devops-capstone --region ap-south-1` returned account `365382429266`, root ARN. Audit-time EC2 `DescribeAvailabilityZones` returned `OptInRequired`, and EKS `ListClusters` returned `SubscriptionRequiredException`; both exited 254. See [`m7-aws-restriction.png`](evidence/m7-aws-restriction.png) and its [raw output](evidence/audit/m7-aws-restriction.txt). No AWS resources were created; no AWS writes or billing/security changes were made. No destroy was run.
- The profile did not provide Terraform with usable credentials on replay, and the account's EC2/EKS service restrictions block deployment regardless. AWS infrastructure deployment and cleanup are **not verified**.

## Repository and evidence scope

- Public repository: https://github.com/pranav7796/helpdesk-capstone
- The audit baseline, public commit `15b303b`, contains 14 meaningful commits; the history is captured in [`m3-git-history.png`](evidence/m3-git-history.png). An evidence-only audit commit follows this baseline.
- UI screenshots: [`relaydesk-compose.png`](evidence/relaydesk-compose.png), [`relaydesk-mobile.png`](evidence/relaydesk-mobile.png) at 390 px, [`relaydesk-minikube.png`](evidence/relaydesk-minikube.png), [`relaydesk-minikube-sha.png`](evidence/relaydesk-minikube-sha.png), [`grafana-relaydesk-dashboard.png`](evidence/grafana-relaydesk-dashboard.png).
- No live AWS screenshots are claimed because no cloud resources were deployed. The saved evidence is genuine local command output and local-cluster screenshots.

## Evidence audit and corrections

The complete required-deliverable mapping is in [EVIDENCE-AUDIT.md](EVIDENCE-AUDIT.md). Missing terminal screenshots, GHCR package pages, successful Actions overview, and Prometheus Targets page were captured automatically. Native terminal screenshots show real commands in a temporary Foot window captured using its own window geometry; browser screenshots show actual pages, with source URLs, timestamps, and SHA-256 hashes in [`evidence/audit/`](evidence/audit/).

The old `evidence/application-metrics.txt` was incorrectly captured from the frontend route and contained HTML. It has been replaced with actual backend `http://127.0.0.1:8000/metrics` output; [`m9-metrics.png`](evidence/m9-metrics.png) shows HTTP 200, Prometheus content type, and real application counters. No application route was changed.

Compose build evidence used `docker compose up --build --no-recreate --no-deps -d --wait backend frontend postgres`. The before/after container-ID assertion passed, all three services stayed healthy, and no running container was recreated. Helm and Kubernetes checks were read-only; release revision remained 10.

The 71.56-second [automated visual walkthrough](evidence/m10-automated-walkthrough.webm), with [captions](evidence/m10-automated-walkthrough.vtt), shows the current app and historical CI/GHCR proof plus live monitoring. It contains no new commit/rollout and no student narration. The required live presentation or accepted recorded commit-to-rollout walkthrough remains pending. Submission-form completion is also unverified. The earlier 91/100 estimate included those 5 pending marks; the audit-adjusted estimate is 86/100, including 2 qualified saved-plan marks.
