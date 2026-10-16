# Verification record — October 16, 2026

Target: account `525426877661`, profile `devops-new`, Sydney `ap-southeast-2`. Deadline October 19, 2026. Historical Mumbai/account restriction evidence is retained but does not describe the current Sydney session.

## Current executed checks

| Command/check | Actual result | Evidence |
|---|---|---|
| `backend/.venv/bin/pytest -v` | 16 passed; 1 Starlette deprecation warning; isolated in-memory SQLite | [output](evidence/sydney/pytest.txt), [JUnit](evidence/sydney/pytest.xml), [screenshot](evidence/sydney/m2-tests-current.png) |
| `npm run build` | Vite production build passed | [build](evidence/sydney/npm-build.txt) |
| `docker compose ps` | PostgreSQL/backend/frontend healthy | [status](evidence/sydney/docker-status.txt); [build/non-root screenshot](evidence/m4-compose.png) |
| `python scripts/smoke.py` | CRUD/status/priority round-trip passed through Compose proxy | [HTTP codes](evidence/sydney/docker-smoke.txt) |
| Same smoke through Minikube Ingress | CRUD passed through `/api`; demo ticket retained | [HTTP codes](evidence/sydney/ingress-smoke.txt) |
| Backend `/health`, `/ready`, `/metrics` | UP, READY, actual Prometheus text | [metrics](evidence/sydney/application-metrics.txt) |
| Minikube Pods/Helm/HPA/PVC | 7 Running/Ready Pods; app replicas 2 each; revision 10 deployed; CPU 4%/70%; PVC Bound | [status](evidence/sydney/minikube-status.txt), [screenshot](evidence/sydney/m8-runtime-current.png) |
| Prometheus application query | `up=1` | [actual query](evidence/sydney/prometheus-up.json), [Targets screenshot](evidence/m9-prometheus-targets.png) |
| Grafana | Previously captured populated real HTTP request panel | [dashboard](evidence/m9-grafana-current.png) |
| Helm lint (local and EKS values) | Both passed; optional icon recommendation only | [EKS render](evidence/sydney/helm-eks-rendered.yaml) |
| Traefik chart 42.0.0 lint/template | Passed with the EKS values; not installed in AWS | [render](evidence/sydney/traefik-rendered.yaml) |
| `kubectl kustomize monitoring` | Renders successfully; EKS Grafana uses private Secret reference | [render](evidence/sydney/monitoring-eks-rendered.yaml) |
| Local chart compatibility | PGDATA/storageClass unchanged for existing local values | Local render assertion passed; no Helm mutation performed |
| Terraform init / fmt-check / validate | Passed with locked AWS provider 5.100.0 | [init](evidence/sydney/terraform-init.txt), [validate](evidence/sydney/terraform-validate.txt), [screenshot](evidence/sydney/m7-sydney-validation.png) |
| Reviewed Terraform plan | 28 additions; no changes/destruction | [complete plan](evidence/sydney/terraform-plan.txt), [screenshot](evidence/sydney/m7-sydney-plan.png) |
| `python scripts/audit-plan.py` | Account/profile/region/admin-CIDR/resource-count/source-snapshot checks all true | [machine audit/hash](evidence/sydney/plan-audit.json) |
| STS, Sydney EC2/AZ discovery, EKS listing | Correct account assumed role; zones available; EKS listing succeeds | [identity](evidence/sydney/aws-identity.json), [zones](evidence/sydney/aws-zones.json), [clusters](evidence/sydney/aws-clusters.json) |
| EKS 1.35 availability | STANDARD_SUPPORT, supported through March 27, 2027 | [API response](evidence/sydney/aws-version.json) |
| Credit read | PAID/ACTIVE; API reports USD120; applicability/expiry/sharing unverified | [API response](evidence/sydney/aws-credits.json) |
| Price List reads / cost calculation | Current Sydney SKUs; baseline $0.31444/hour before extras | [rates](evidence/sydney/aws-price-summary.json), [calculation](evidence/sydney/cost-estimate.txt) |

Initial sandbox attempts could not start the Terraform provider/test client or access network/Docker sockets. Successful runtime checks ran with approved execution permissions. An initial parallel CLI token refresh returned 429; serialized checks succeeded. No credentials or debug credential logs were captured.

## CI and immutable release evidence

Last checked successful public CI: [38905586773](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38905586773), commit `79b27b9f86d5688876bd7823361e4df9202921a3`. The actual Minikube image release was produced by [38893336596](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38893336596), commit `d07bca6accc35f0224aaae8c4057076a9c4c9261`. Both images built, passed the configured Trivy gates and were pushed to GHCR. [Full release logs](evidence/actions-run.txt), [deployed-image evidence](evidence/live-demo.txt).

- Backend: `ghcr.io/pranav7796/helpdesk-capstone/backend:d07bca6accc35f0224aaae8c4057076a9c4c9261`
- Frontend: `ghcr.io/pranav7796/helpdesk-capstone/frontend:d07bca6accc35f0224aaae8c4057076a9c4c9261`

Trivy HIGH/CRITICAL findings with available fixes fail the pipeline; `ignore-unfixed` and exact-PURL exceptions are explicitly disclosed. Zero reported findings is scoped to those images and that policy, not absence of every vulnerability. [Security explanation](docs/SECURITY.md), [backend screenshot](evidence/m6-trivy-backend.png), [frontend screenshot](evidence/m6-trivy-frontend.png).

## Troubleshooting recovery

`python scripts/troubleshooting-lab.py` exited 0 after diagnosing and recovering all five failures in the isolated local namespace. Actual HTTP 404/503 probe responses, empty selector endpoints, repeated exit-1 crashes with BackOff events, fixed rollouts and HTTP 200 are captured in [full output](evidence/sydney/troubleshooting.txt) and [recovery screenshot](evidence/sydney/troubleshooting-recovery.png). The namespace was removed; the working release stayed healthy. Initial observation/startup failures are retained and explained in [the troubleshooting guide](docs/TROUBLESHOOTING.md). The invalid-image exercise also exposed a local Minikube registry-DNS failure; cached-image recovery succeeded and no claim is made that node-external DNS was repaired.

## Original plan and cloud boundary

The supplied 22-resource `terraform/tfplan` matched its original source snapshot, Sydney and the actual admin CIDR, but lacked account binding/storage/metrics prerequisites. It remains preserved and ignored. The replacement `tfplan-reviewed` enforces the intended account and includes 28 resources. All current `.tf` files match its snapshot. Neither plan has been applied.

EBS CSI, Pod Identity, Metrics Server, gp3 PVC selection and Traefik are **IMPLEMENTED / locally validated**, not verified on EKS. AWS VPC/EKS/worker/application/ELB deployment and eventual destroy are **NOT VERIFIED** and await explicit approvals. Public reads/planning do not prove write permissions under Organizations SCPs.

## Submission boundary

Current estimated verified marks: **86/100**, subject to instructor judgment. AWS runtime/destroy (9), teacher-form submission (2), and accepted student presentation (3) remain pending. The existing automated browser video is a current-state walkthrough, not a recording of its original commit-to-rollout event. [Per-criterion checklist](GRADING-CHECKLIST.md), [submission guide](SUBMISSION.md), [cloud approval/runbook](docs/AWS-PLAN.md).
