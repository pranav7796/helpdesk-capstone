# Verification record

Observed on 2026-10-16. Evidence files are under `evidence/`; only actual command and runtime results are called VERIFIED in [PROGRESS.md](PROGRESS.md).

## Application, tests, and containers

- `backend/.venv/bin/pytest -v --junitxml=../evidence/pytest.xml` — **16 passed**, one Starlette deprecation warning; output: [`evidence/pytest.txt`](evidence/pytest.txt). The suite uses an isolated SQLite test database.
- `npm run build` in `frontend/` — Vite production build passed; output: [`evidence/npm-build.txt`](evidence/npm-build.txt).
- `docker compose ps` — PostgreSQL, API, frontend all healthy; both app containers run as non-root (UIDs 10001 and 101): [`evidence/docker-compose-ps.txt`](evidence/docker-compose-ps.txt).
- `python scripts/smoke.py` against the Compose frontend proxy — create/list/read/edit/status/priority/delete all returned expected HTTP codes and persisted data: [`evidence/docker-smoke.txt`](evidence/docker-smoke.txt).

## Kubernetes and observability

- Minikube profile `helpdesk-capstone`; namespace `relaydesk`; Helm release status `deployed`, revision 9. Backend and frontend each have two Ready replicas, PostgreSQL has a bound 2 GiB PVC, and HPA reports current CPU against its target. See [`evidence/minikube-status.txt`](evidence/minikube-status.txt).
- Ingress at `http://192.168.58.2/` returned the app; `/api/tickets` returned API data. CRUD smoke through ingress passed after backend rollout. Screenshot: [`evidence/relaydesk-minikube.png`](evidence/relaydesk-minikube.png).
- Prometheus and Grafana Pods ran in Minikube. Prometheus target query returned `up=1`; request counter query returned traffic for API paths. Saved responses: [`prometheus-target.json`](evidence/prometheus-target.json), [`prometheus-requests-query.json`](evidence/prometheus-requests-query.json). Grafana has a populated HTTP requests panel: [`grafana-relaydesk-dashboard.png`](evidence/grafana-relaydesk-dashboard.png). Application exposition: [`application-metrics.txt`](evidence/application-metrics.txt).
- Helm lint/template validation ran in the CI workflow; local rendered chart: [`helm-rendered.yaml`](evidence/helm-rendered.yaml).

## Security and CI/CD

- Trivy scanned both local built images at HIGH/CRITICAL severity. Reports contain no findings at those severities: [`trivy-backend.json`](evidence/trivy-backend.json), [`trivy-frontend.json`](evidence/trivy-frontend.json). The backend scan uses the package-URL-scoped ignore file documented in [`docs/SECURITY.md`](docs/SECURITY.md).
- Repository push triggered workflow run [38893336596](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38893336596) for commit `d07bca6accc35f0224aaae8c4057076a9c4c9261`; **all jobs succeeded**. The run passed 16 API tests, the React production build, both image builds, both HIGH/CRITICAL scans, GHCR publication, Helm lint, and manifest rendering. Captured workflow logs and run metadata: [`actions-run.txt`](evidence/actions-run.txt), [`actions-run.json`](evidence/actions-run.json).
- Published images, pulled by their immutable commit SHA and deployed via Helm revision 10:
  - `ghcr.io/pranav7796/helpdesk-capstone/backend:d07bca6accc35f0224aaae8c4057076a9c4c9261` (digest `sha256:c8fbaf5265f683753e70332a148aa5d0db4035530da98ccedcbba865f27ba205`)
  - `ghcr.io/pranav7796/helpdesk-capstone/frontend:d07bca6accc35f0224aaae8c4057076a9c4c9261` (digest `sha256:8023382eb19a37c9a5787efe15036c8e9e11010ef870712ce413b4fc2be73cb1`)
- Both application Deployments rolled out with two Ready replicas each; the Pods used those exact image references. `python scripts/smoke.py` against the Minikube ingress completed create/list/read/edit/status/priority/delete and retained data in PostgreSQL: [`live-demo.txt`](evidence/live-demo.txt). Final runtime screenshot: [`relaydesk-minikube-sha.png`](evidence/relaydesk-minikube-sha.png).
- Earlier run [38886640390](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38886640390) failed on four HIGH findings associated with stale upstream Python build SBOM entries and a vulnerable setuptools version. The app dependency was upgraded; exact stale SBOM package URLs are scoped in `.trivyignore.yaml`. The reports from the current local images are clean.

## Terraform and AWS

- `terraform init -input=false` completed successfully with the locked AWS provider; `terraform fmt -check -recursive` and `terraform validate` passed. Validation output: [`evidence/terraform-validate.txt`](evidence/terraform-validate.txt).
- [`evidence/terraform-plan-refresh-false.txt`](evidence/terraform-plan-refresh-false.txt) is a saved no-refresh, 22-resource dry-run artifact from the earlier successful local plan. It is not a refreshed plan, not an approval artifact, and its cluster-admin CIDR is the documentation placeholder `203.0.113.9/32`. Re-running the plan in this environment later failed because Terraform could not resolve credentials from the AWS profile (`No valid credential sources found`); do not apply the saved artifact.
- Read-only AWS CLI identity check with `--profile devops-capstone --region ap-south-1` returned account `365382429266`, root ARN. The earlier service checks returned EC2 `OptInRequiredException` and EKS `SubscriptionRequiredException`. No AWS resources were created; no AWS writes or billing/security changes were made. No destroy was needed.
- The profile did not provide Terraform with usable credentials on replay, and the account's EC2/EKS service restrictions block deployment regardless. AWS infrastructure deployment and cleanup are **not verified**.

## Repository and evidence scope

- Public repository: https://github.com/pranav7796/helpdesk-capstone
- Public `main` contains 12 meaningful commits through `d07bca6`.
- UI screenshots: [`relaydesk-compose.png`](evidence/relaydesk-compose.png), [`relaydesk-minikube.png`](evidence/relaydesk-minikube.png), [`relaydesk-minikube-sha.png`](evidence/relaydesk-minikube-sha.png), [`grafana-relaydesk-dashboard.png`](evidence/grafana-relaydesk-dashboard.png).
- No live AWS screenshots are claimed because no cloud resources were deployed. The saved evidence is genuine local command output and local-cluster screenshots.
