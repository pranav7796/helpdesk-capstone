# Relaydesk — Helpdesk Ticket Management

Latest audit: **[October 20 final report](docs/FINAL-REPORT.md)** — 44 PASS, 2 BLOCKED criteria; live AWS/Kubernetes, ingress CRUD/SQL, monitoring APIs, local tests/build/Compose and Terraform no-drift checks pass. Form receipt and actual approved destroy remain outstanding. Existing screenshots/videos keep their Oct 16/17 dates; this commit includes the audit report and sanitized evidence. [Current submission guide](SUBMISSION.md).


Relaydesk is an independently built helpdesk application for creating, searching, prioritizing, editing, and resolving support tickets. React and Vite provide the responsive agent inbox; FastAPI exposes the API; SQLAlchemy and PostgreSQL store tickets; Alembic manages schema changes.

## Run locally

Requirements: Docker Engine and Docker Compose.

```sh
docker compose up --build -d --wait
```

Open <http://localhost:3000>. The REST API is at <http://localhost:8000>; interactive docs are at `/docs`. Compose starts PostgreSQL, applies Alembic migrations, then starts the API and Nginx frontend. Nginx proxies `/api` requests to FastAPI. Local-only settings are in `.env.example`; never commit `.env`.

Stop the containers with `docker compose down`. The named database volume stays on disk so tickets survive container restarts. Remove it only when you explicitly want to erase local data: `docker compose down -v`.

## API and health

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/tickets` | List tickets; API status filter, with frontend search |
| POST | `/api/tickets` | Create a ticket |
| GET | `/api/tickets/{id}` | Read one ticket |
| PUT | `/api/tickets/{id}` | Edit fields, status, or priority |
| DELETE | `/api/tickets/{id}` | Delete a ticket |
| GET | `/health` | Process health |
| GET | `/ready` | Database readiness |
| GET | `/metrics` | Prometheus HTTP counters and latency |

## Tests and frontend build

```sh
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
cd ../frontend
npm ci
npm run build
```

Pytest overrides the database URL with an isolated in-memory SQLite database. The application database is never used by tests.

## Kubernetes and monitoring

The chart is in `helm/helpdesk`; cluster defaults are in `values.yaml`. For the preloaded local Minikube images use:

```sh
helm upgrade --install relaydesk helm/helpdesk --kube-context helpdesk-capstone -n relaydesk --create-namespace \
  -f helm/helpdesk/values-local.yaml --wait --timeout 180s
kubectl --context helpdesk-capstone -n relaydesk get pods,svc,hpa,pvc
```

Set `ingress.enabled=true` and install an ingress controller for routed access. `monitoring/local-stack.yaml` deploys Prometheus/Grafana for a local cluster after creating the dashboard ConfigMap as described in `docs/OBSERVABILITY.md`.

## CI, security, and infrastructure

The GitHub Actions workflow tests the API, builds the frontend and both images, runs HIGH/CRITICAL Trivy gates, validates Helm, then pushes images to GHCR tagged with the source commit SHA. Terraform under `terraform/` describes a VPC and EKS cluster. Applying it creates chargeable AWS resources and requires a separately reviewed plan and explicit approval; this repository does not run `terraform apply` in CI.

The first security scan found a `setuptools` path-traversal CVE and stale versions from an upstream Python build SBOM. The backend now pins fixed versions, and `.trivyignore.yaml` scopes the SBOM false-positive exclusions to the exact reported package URLs. See [security scan notes](docs/SECURITY.md) and the saved scan reports in `evidence/`.

## Capstone evidence

- [Progress scorecard](PROGRESS.md) — each rubric row and current verified marks.
- [Verification record](VERIFICATION.md) — commands and observed outcomes.
- [Submission checklist](SUBMISSION.md) — required links and evidence.
- [Evidence audit](EVIDENCE-AUDIT.md) — required screenshots, provenance, and remaining submission gaps.
- [Troubleshooting guide](docs/TROUBLESHOOTING.md) and recovery exercise templates in `troubleshooting/`.
- [AWS plan, eligibility, and cost estimate](docs/AWS-PLAN.md).
- Screenshots and captured outputs are in [`evidence/`](evidence/).
- Teacher rubric and source snapshot reference: [`docs/TEACHER-GRADING.md`](docs/TEACHER-GRADING.md).

The current AWS target is account `525426877661`, profile `devops-new`, Sydney `ap-southeast-2`. The owner-approved 28-resource plan was applied successfully on October 16. EKS has two Ready workers; application CRUD, persistent PostgreSQL, Ingress, Prometheus and Grafana are verified. Cleanup awaits separate approval after the demonstration. The old Mumbai/account restriction evidence is historical. See [scope and current costs](docs/AWS-PLAN.md), [deployment runbook](docs/EKS-RUNBOOK.md), and [grading checklist](GRADING-CHECKLIST.md). Owner target was October 19, 2026; the accepted deadline/extension remains unverified.

Recorded release demonstration: [real commit → green CI → EKS Helm rollout → changed application](evidence/videos/m10-real-release-walkthrough.webm), [completed result continuation](evidence/videos/m10-release-result-continuation.webm), and [presentation notes](docs/PRESENTATION.md). Current EKS frontend SHA is `04108043563d24dfc2ceb70e050fd56b5e9cc577` (Helm revision 2); the EKS backend and Minikube retain their documented d07 release. Compose was rebuilt from current source during the October 17 audit.

Final evidence is organized in [screenshots](evidence/screenshots/) and [videos](evidence/videos/), with all 46 criteria linked in [the grading checklist](GRADING-CHECKLIST.md). Monitoring now scrapes each backend replica separately to keep request-rate counters correct; see [observability notes](docs/OBSERVABILITY.md). Form submission uses the repository URL only. The latest owner target is October 19, but the supplied form said October 16 at 11:59 PM IST; extension/submission confirmation remain unverified.

Final monitoring-fix CI [38997737911](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38997737911) passed all jobs for commit `2fbc48485411ff7239bb92b4290062b7e58d86fb`, including tests, React/image builds, both Trivy gates, GHCR SHA publication, Helm checks and monitoring-manifest validation. [Actual metadata](evidence/final-2026-10-17/monitoring-fix-ci.json), [complete logs](evidence/final-2026-10-17/monitoring-fix-ci.txt), [green screenshot](evidence/screenshots/2026-10-17-ci-monitoring-fix-green.png). Deployed application image SHAs remain unchanged.

Optional evidence integrity check: `python scripts/audit-evidence.py` (Python 3 and `ffprobe` from FFmpeg required). It checks the 46-row mapping, public capture hashes/PNG structure, and video metadata; it excludes private files.
