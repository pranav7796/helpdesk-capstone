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
| Traefik chart 42.0.0 lint/template | Passed; subsequently installed in EKS, release revision 1 deployed | [render](evidence/sydney/traefik-rendered.yaml) |
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

Current Sydney-source CI [38935978045](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38935978045), commit `e33b8bdcc61c4fdd658e5827044fe868d9dea1ad`, completed with all jobs successful, including local/EKS Helm lint/render. [Run metadata](evidence/sydney/actions-run.json), [complete logs](evidence/sydney/actions-run.txt), [green screenshot](evidence/sydney/m5-actions-success.png). The actual Minikube image release was produced by [38893336596](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38893336596), commit `d07bca6accc35f0224aaae8c4057076a9c4c9261`. Both images built, passed the configured Trivy gates and were pushed to GHCR. [Full release logs](evidence/actions-run.txt), [deployed-image evidence](evidence/live-demo.txt).

- Backend: `ghcr.io/pranav7796/helpdesk-capstone/backend:d07bca6accc35f0224aaae8c4057076a9c4c9261`
- Frontend: `ghcr.io/pranav7796/helpdesk-capstone/frontend:d07bca6accc35f0224aaae8c4057076a9c4c9261`

Trivy HIGH/CRITICAL findings with available fixes fail the pipeline; `ignore-unfixed` and exact-PURL exceptions are explicitly disclosed. Zero reported findings is scoped to those images and that policy, not absence of every vulnerability. [Security explanation](docs/SECURITY.md), [backend screenshot](evidence/m6-trivy-backend.png), [frontend screenshot](evidence/m6-trivy-frontend.png).

## Troubleshooting recovery

`python scripts/troubleshooting-lab.py` exited 0 after diagnosing and recovering all five failures in the isolated local namespace. Actual HTTP 404/503 probe responses, empty selector endpoints, repeated exit-1 crashes with BackOff events, fixed rollouts and HTTP 200 are captured in [full output](evidence/sydney/troubleshooting.txt) and [recovery screenshot](evidence/sydney/troubleshooting-recovery.png). The namespace was removed; the working release stayed healthy. Initial observation/startup failures are retained and explained in [the troubleshooting guide](docs/TROUBLESHOOTING.md). The invalid-image exercise also exposed a local Minikube registry-DNS failure; cached-image recovery succeeded and no claim is made that node-external DNS was repaired.

The successful CI log reported Ubuntu 24.04.5 and announced that `ubuntu-latest` starts migrating to Ubuntu 26 on October 19, the deadline. The workflow is now pinned to `ubuntu-24.04` to retain the verified runner OS; final run [38936702532](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38936702532) succeeded with all jobs green. [Metadata](evidence/sydney/actions-final.json), [full log](evidence/sydney/actions-final.txt). Existing action Node-runtime deprecation annotations are non-failing.

## Original plan and cloud boundary

The supplied 22-resource `terraform/tfplan` matched its original source snapshot, Sydney and the actual admin CIDR, but lacked account binding/storage/metrics prerequisites. It remains preserved and ignored. The replacement `tfplan-reviewed` enforces the intended account and includes 28 resources. All current `.tf` files match its snapshot. The reviewed plan was explicitly approved and applied: 28 added, 0 changed, 0 destroyed; exit 0. The original plan was not applied.

EBS CSI, Pod Identity and Metrics Server are ACTIVE; Traefik is deployed. The encrypted 2-GiB gp3 PVC is Bound. Actual cloud runtime and Console screenshots are verified; cleanup has not been executed and needs separate approval.

## Submission boundary

Current estimated verified marks: **93/100**, subject to instructor judgment. AWS destroy (2), teacher-form submission (2), and accepted student presentation (3) remain pending. The existing automated browser video is a current-state walkthrough, not a recording of its original commit-to-rollout event. [Per-criterion checklist](GRADING-CHECKLIST.md), [submission guide](SUBMISSION.md), [cloud approval/runbook](docs/AWS-PLAN.md).

## Approved Sydney deployment — executed October 16

- `terraform -chdir=terraform apply -no-color tfplan-reviewed`: exit 0, **28 added, 0 changed, 0 destroyed**. [Complete output](evidence/sydney/terraform-apply.txt), [terminal screenshot](evidence/sydney/aws-apply-verified.png), [owner approval](evidence/sydney/DEPLOYMENT-APPROVAL.md).
- `bash scripts/deploy-eks.sh`: exit 0. Isolated kubeconfig; two Ready workers; three ACTIVE add-ons; app and Traefik Helm releases deployed, revision 1. [Deploy log](evidence/sydney/eks-deploy.txt).
- Public ELB CRUD smoke: POST 201, GET/PUT 200, DELETE 204. [HTTP results](evidence/sydney/eks-http-smoke.txt), [app screenshot](evidence/sydney/eks-application-browser.png). Access restricted to `202.131.146.146/32`.
- `python scripts/verify-eks.py --resume-infrastructure`: exit 0. Reused already captured infrastructure JSON; HTTP/monitoring/final runtime/log checks executed live. Seven application-namespace Pods Ready, 2/2 frontend/backend replicas, valid HPA CPU, PVC Bound. [Summary](evidence/sydney/eks-verification-summary.json), [runtime](evidence/sydney/eks-runtime.txt).
- Initial traffic-loop GET encountered a transient connection reset; original failure retained in `eks-verification-initial-network-reset.txt`. Bounded GET retries and a slower traffic loop passed. Its underlying network cause is not established.
- Actual PostgreSQL query: tables `tickets`/`alembic_version`, migration `0001_tickets`, retained HIGH/IN_PROGRESS ticket. [SQL output](evidence/sydney/eks-postgres-persistence.txt). Init container exited 0; migration log is empty, so SQL and Pod status supply proof.
- `/health` UP, `/ready` READY, real `/metrics`; Prometheus `up=1`, positive HTTP rates; authenticated Grafana dashboard populated. [Metrics](evidence/sydney/eks-application-metrics.txt), [Targets](evidence/sydney/eks-prometheus-targets.png), [dashboard](evidence/sydney/eks-grafana-dashboard.png).
- Genuine AWS Console VPC/subnet/EKS captures: `aws-vpc-console.png`, `aws-subnets-console.png`, `aws-eks-console.png` under `evidence/sydney/`; capture manifests record URL/time/hash.
- Read-only destroy preview: **28 deletes**, not executed. [Plan](evidence/sydney/terraform-destroy-plan.txt), [audit](evidence/sydney/cleanup-plan-audit.json). Kubernetes-created ELB and data EBS need cleanup before VPC/CSI deletion. [Cleanup review](docs/CLEANUP-REVIEW.md).

Local Compose/Minikube were preserved. Deployment scripts changed; application source and deployed immutable d07 image tags did not. Sensitive Terraform state, kubeconfig and generated passwords remain ignored/private.

Deployment commit `20c2401e206f85d1c2901cead55160c1007bf0e0` passed [CI 38945382171](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38945382171): 16 tests, React/container builds, both Trivy scans, GHCR SHA publication and Helm validation. [Actual metadata](evidence/sydney/actions-deployment.json), [full logs](evidence/sydney/actions-deployment.txt). The earlier evidence-only run 38937333354 failed during GHCR publication with `unknown blob`; the new complete run passed. Deployed d07 images remain unchanged.
