# Helpdesk capstone progress

Started 2026-10-16 10:40 IST. Working deadline estimate: 20:40 IST (10 hours from start); exact teacher deadline was not provided.

Source: [teacher repository](https://github.com/Nency-Ravaliya/devops-heros/tree/main/session21-python), commit `a4e39b6b3a54dab1efd386c75ab86bf1d8a23454`. Full rubric and submission instructions: [docs/TEACHER-GRADING.md](docs/TEACHER-GRADING.md).

**Audit-adjusted verified estimate: 86/100; achievable submission estimate: 91/100 after the form and presentation requirements are completed.** The earlier 91 estimate counted the public-repository submission and the presentation as complete; neither has confirmation. The saved no-refresh Terraform plan contributes 2 of these estimated marks, subject to instructor acceptance (84 if a fresh authenticated plan is required). Only the instructor awards marks. See [EVIDENCE-AUDIT.md](EVIDENCE-AUDIT.md).

Run [38893336596](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38893336596) succeeded and its SHA images were deployed to Minikube. This technical sequence is evidenced by logs; no recording of the actual commit-to-rollout event or completed student presentation exists. The new automated browser walkthrough is supplementary. AWS deployment/destroy remains blocked (9 marks).

Status: VERIFIED means observed in a running system or command output. IMPLEMENTED means configuration exists but the graded runtime result is not yet demonstrated. BLOCKED means an external restriction prevents the requirement. FAILED means an attempted verification failed. NOT STARTED means no work exists.

| Module | Criterion | Marks | Status | Evidence |
|---|---|---:|---|---|
| M1 | FastAPI `/health` responds | 2 | VERIFIED | Compose and Minikube; `evidence/docker-compose-ps.txt` |
| M1 | GET/POST/PUT/DELETE ticket API | 3 | VERIFIED | `evidence/docker-smoke.txt` |
| M1 | PostgreSQL table managed by Alembic | 2 | VERIFIED | Compose migration service and retained ticket; smoke evidence |
| M1 | React frontend renders and calls API | 2 | VERIFIED | Compose screenshot and proxied CRUD smoke |
| M1 | Responsive usable UI | 1 | VERIFIED | Desktop and 390 px screenshots: `evidence/relaydesk-compose.png`, `evidence/relaydesk-mobile.png` |
| M2 | Pytest runs | 3 | VERIFIED | `evidence/pytest.txt` (16 passed) |
| M2 | At least 5 tests across 3 endpoints | 4 | VERIFIED | `backend/tests/test_tickets.py`, 16 passed |
| M2 | Isolated test DB | 2 | VERIFIED | SQLite test fixture; `backend/tests/conftest.py` |
| M2 | Pytest config | 1 | VERIFIED | `backend/pytest.ini` |
| M3 | Public GitHub repository linked in submission form | 2 | IMPLEMENTED | Public URL verified; submission-form confirmation is still missing |
| M3 | At least 10 meaningful commits | 2 | VERIFIED | `evidence/m3-git-history.png` captures 14 meaningful commits before the audit follow-up |
| M3 | `.gitignore` excludes secrets/build caches | 1 | VERIFIED | Root `.gitignore`; no credentials tracked |
| M4 | Backend Docker image builds | 2 | VERIFIED | Compose runtime; `evidence/docker-compose-ps.txt` |
| M4 | Multi-stage frontend image | 3 | VERIFIED | `frontend/Dockerfile`; running Nginx frontend |
| M4 | Both application images use non-root users | 2 | VERIFIED | Backend UID 10001, frontend UID 101 in `evidence/docker-compose-ps.txt` |
| M4 | Compose runs frontend/backend/PostgreSQL | 3 | VERIFIED | All three healthy; `evidence/docker-compose-ps.txt` |
| M5 | Workflow file exists | 1 | VERIFIED | `.github/workflows/ci.yml` |
| M5 | Push-to-main trigger | 1 | VERIFIED | Push `d07bca6` triggered run 38893336596 |
| M5 | CI pytest job | 3 | VERIFIED | Run 38893336596 test job succeeded (16 tests) |
| M5 | CI frontend build | 2 | VERIFIED | Run 38893336596 Vite build succeeded |
| M5 | CI builds both container images | 3 | VERIFIED | Both build steps succeeded in run 38893336596 |
| M5 | GHCR image publication | 3 | VERIFIED | Both image pushes succeeded in run 38893336596 |
| M5 | Immutable commit SHA tags | 2 | VERIFIED | Full SHA tag `d07bca6accc35f0224aaae8c4057076a9c4c9261` |
| M6 | CI Trivy scans both images | 3 | VERIFIED | Both HIGH/CRITICAL scans succeeded in run 38893336596 |
| M6 | HIGH/CRITICAL gate | 1 | VERIFIED | `exit-code: 1`, `ignore-unfixed: true`; both scans passed |
| M6 | Explain a finding and disposition | 1 | VERIFIED | `docs/SECURITY.md`; scoped SBOM false-positive exceptions |
| M7 | Valid Terraform HCL | 2 | VERIFIED | `terraform validate`; `evidence/terraform-validate.txt` |
| M7 | Terraform init | 1 | VERIFIED | Successful init with locked AWS provider |
| M7 | Non-empty Terraform plan | 2 | VERIFIED | Historical 22-resource `-refresh=false` output only; screenshot `evidence/m7-terraform-plan-saved.png`; fresh plan replay failed; marks are qualified |
| M7 | VPC with two public subnets provisioned | 3 | BLOCKED | EC2 `OptInRequired`; no apply; `evidence/m7-aws-restriction.png` |
| M7 | EKS and worker node group provisioned | 4 | BLOCKED | EKS `SubscriptionRequiredException`; no apply |
| M7 | Terraform destroy demonstrated | 2 | BLOCKED | No AWS resources were created |
| M7 | Example tfvars, no secrets | 1 | VERIFIED | `terraform/terraform.tfvars.example` |
| M8 | Namespace applies | 1 | VERIFIED | Minikube namespace `relaydesk` |
| M8 | Helm chart structure | 3 | VERIFIED | `helm/helpdesk`; rendered output in `evidence/helm-rendered.yaml` |
| M8 | Helm install/upgrade succeeds | 3 | VERIFIED | Release `relaydesk`, status deployed, revision 10; `evidence/m8-helm.png` |
| M8 | Frontend and backend each have 2 replicas | 2 | VERIFIED | `evidence/minikube-status.txt` |
| M8 | ClusterIP services | 2 | VERIFIED | Backend, frontend, PostgreSQL service evidence |
| M8 | Ingress routes frontend and `/api` | 2 | VERIFIED | Minikube ingress `192.168.58.2`; frontend/API smoke passed |
| M8 | Pods running and ready | 2 | VERIFIED | `evidence/minikube-status.txt` |
| M9 | Prometheus `/metrics` output | 2 | VERIFIED | `evidence/application-metrics.txt` |
| M9 | Prometheus scrapes application | 3 | VERIFIED | `evidence/prometheus-target.json` (`up == 1`) |
| M9 | Grafana installed and accessible | 2 | VERIFIED | Running local service and dashboard screenshot |
| M9 | Live request metrics panel | 3 | VERIFIED | `evidence/grafana-relaydesk-dashboard.png`; traffic query evidence |
| M10 | Root README explains application | 2 | VERIFIED | `README.md` |
| M10 | Live or recorded commit → CI → deployment update presentation | 3 | IMPLEMENTED | Historical technical sequence verified in logs. Automated current-state browser walkthrough captured; actual student presentation/live sequence recording still pending |

## Highest-value remaining work

1. Submit the public repository URL and the screenshot checklist in `SUBMISSION.md` to the teacher's form.
2. Complete the live presentation or an accepted recorded commit → pipeline → deployment walkthrough.
3. Disclose the AWS limitation; VPC/EKS and destroy screenshots cannot be produced without a real approved deployment.
