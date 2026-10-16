# Helpdesk capstone progress

Started 2026-10-16. Confirmed submission deadline: **October 19, 2026** (time of day not specified). Current cloud target: account `525426877661`, profile `devops-new`, region `ap-southeast-2`.

Source: [teacher repository](https://github.com/Nency-Ravaliya/devops-heros/tree/main/session21-python), commit `a4e39b6b3a54dab1efd386c75ab86bf1d8a23454`. Full rubric and submission instructions: [docs/TEACHER-GRADING.md](docs/TEACHER-GRADING.md).

**Verified estimate: 96/100; potential 100/100 after approved cleanup and teacher-form submission; the real recorded release demonstration is now evidenced, subject to instructor acceptance.** On October 16 the owner approved the reviewed Sydney deployment including ingress/storage. Terraform successfully created 28 resources; VPC/subnets, ACTIVE EKS/node group, two Ready workers, application CRUD and monitoring were actually verified. Only the instructor awards marks. [Cloud evidence](evidence/sydney/eks-verification-summary.json), [submission guide](SUBMISSION.md).

Run [38893336596](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38893336596) succeeded and its SHA images were deployed to Minikube. This technical sequence is evidenced by logs; a new continuous recording now captures a real 0410804 commit-to-EKS rollout; its separate result continuation shows completed green CI. No student narration or instructor acceptance is claimed. AWS deployment is verified; destroy remains pending separate approval (2 marks).

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
| M7 | Non-empty Terraform plan | 2 | VERIFIED | Account-guarded Sydney plan: `evidence/sydney/terraform-plan.txt`, `plan-audit.json`; 28 additions; actual admin CIDR; subsequently applied successfully |
| M7 | VPC with two public subnets provisioned | 3 | VERIFIED | `evidence/sydney/aws-vpc-live.json`, `aws-subnets-live.json`; actual Console screenshots |
| M7 | EKS and worker node group provisioned | 4 | VERIFIED | ACTIVE EKS 1.35/node group; two Ready t3.medium workers; `evidence/sydney/aws-eks-console.png`, `eks-nodes.json` |
| M7 | Terraform destroy demonstrated | 2 | IMPLEMENTED | Read-only cleanup plan has 28 deletions; no deletion executed; separate approval required |
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
| M10 | Live or recorded commit → CI → deployment update presentation | 3 | VERIFIED | `evidence/sydney/m10-real-release-walkthrough.webm`, separate result continuation, CI 38946277016, Helm revision 2 and real post-rollout app/CRUD; automated recording subject to instructor acceptance |

Current Sydney-source verification: [CI 38935978045](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38935978045) succeeded for `e33b8bdcc61c4fdd658e5827044fe868d9dea1ad`, including both image/security/publication gates and both Helm value variants. Real run evidence is under `evidence/sydney/`.

## Highest-value remaining work

1. Submit the public repository URL and the screenshot checklist in `SUBMISSION.md` to the teacher's form.
2. Review and submit the actual release recording with the presentation notes; be prepared to explain the implementation yourself.
3. After the demonstration, separately approve project cleanup (ticket data will be erased), capture destroy completion, then verify no project ELB/EBS/NAT/EIP resources remain.
