# Helpdesk capstone progress — October 17, 2026

**44/46 verified criteria; 96/100 estimated technical coverage, before any instructor acceptance or late-submission adjustments.** AWS account `525426877661`, profile `devops-new`, Sydney `ap-southeast-2`. Current verification passed; the monitoring scrape was corrected and verified. App is deployed; cleanup requires separate approval.

Working target supplied by owner: October 19, 2026. Earlier Google Form text states October 16, 11:59 PM IST. An extension and submission confirmation remain unverified; do not assume October 19 overrides the actual form. [Current submission guide](SUBMISSION.md), [full 46-row evidence mapping](GRADING-CHECKLIST.md), [actual checks](VERIFICATION.md).

| Module | Criterion | Marks | Status | Actual evidence |
|---|---|---:|---|---|
| M1 | FastAPI `/health` responds | 2 | VERIFIED | Actual Compose and EKS CRUD/status/priority checks pass; `/health` UP, `/ready` READY; PostgreSQL Alembic revision and retained rows queried. |
| M1 | GET/POST/PUT/DELETE ticket API | 3 | VERIFIED | Actual Compose and EKS CRUD/status/priority checks pass; `/health` UP, `/ready` READY; PostgreSQL Alembic revision and retained rows queried. |
| M1 | PostgreSQL table managed by Alembic | 2 | VERIFIED | Actual Compose and EKS CRUD/status/priority checks pass; `/health` UP, `/ready` READY; PostgreSQL Alembic revision and retained rows queried. |
| M1 | React frontend renders and calls API | 2 | VERIFIED | Actual Compose and EKS CRUD/status/priority checks pass; `/health` UP, `/ready` READY; PostgreSQL Alembic revision and retained rows queried. |
| M1 | Responsive usable UI | 1 | VERIFIED | 390px responsive table/actions captured genuinely; frontend CSS unchanged since that recording. |
| M2 | Pytest runs | 3 | VERIFIED | Fresh pytest -v: 16 passed, 1 non-failing Starlette warning. Isolated SQLite fixture; PostgreSQL runtime exercised separately. |
| M2 | At least 5 tests across 3 endpoints | 4 | VERIFIED | Fresh pytest -v: 16 passed, 1 non-failing Starlette warning. Isolated SQLite fixture; PostgreSQL runtime exercised separately. |
| M2 | Isolated test DB | 2 | VERIFIED | Fresh pytest -v: 16 passed, 1 non-failing Starlette warning. Isolated SQLite fixture; PostgreSQL runtime exercised separately. |
| M2 | Pytest config | 1 | VERIFIED | Fresh pytest -v: 16 passed, 1 non-failing Starlette warning. Isolated SQLite fixture; PostgreSQL runtime exercised separately. |
| M3 | Public GitHub repository linked in submission form | 2 | IMPLEMENTED | Public URL verified, but no form confirmation/receipt supplied. Draft saved does not prove submission. |
| M3 | At least 10 meaningful commits | 2 | VERIFIED | Public repository and 10+ meaningful commits verified; ignore rules and tracked-private-file checks pass. Form receipt remains unverified. |
| M3 | `.gitignore` excludes secrets/build caches | 1 | VERIFIED | Public repository and 10+ meaningful commits verified; ignore rules and tracked-private-file checks pass. Form receipt remains unverified. |
| M4 | Backend Docker image builds | 2 | VERIFIED | Actual docker compose up --build -d --wait passed; all three services healthy, backend UID 10001 and frontend UID 101; proxied CRUD passed. |
| M4 | Multi-stage frontend image | 3 | VERIFIED | Actual docker compose up --build -d --wait passed; all three services healthy, backend UID 10001 and frontend UID 101; proxied CRUD passed. |
| M4 | Both application images use non-root users | 2 | VERIFIED | Actual docker compose up --build -d --wait passed; all three services healthy, backend UID 10001 and frontend UID 101; proxied CRUD passed. |
| M4 | Compose runs frontend/backend/PostgreSQL | 3 | VERIFIED | Actual docker compose up --build -d --wait passed; all three services healthy, backend UID 10001 and frontend UID 101; proxied CRUD passed. |
| M5 | Workflow file exists | 1 | VERIFIED | Actual green CI 38947267271 for published commit 3679f58; tests/builds/Trivy/GHCR publication/Helm succeeded; immutable tags shown publicly. |
| M5 | Push-to-main trigger | 1 | VERIFIED | Actual green CI 38947267271 for published commit 3679f58; tests/builds/Trivy/GHCR publication/Helm succeeded; immutable tags shown publicly. |
| M5 | CI pytest job | 3 | VERIFIED | Actual green CI 38947267271 for published commit 3679f58; tests/builds/Trivy/GHCR publication/Helm succeeded; immutable tags shown publicly. |
| M5 | CI frontend build | 2 | VERIFIED | Actual green CI 38947267271 for published commit 3679f58; tests/builds/Trivy/GHCR publication/Helm succeeded; immutable tags shown publicly. |
| M5 | CI builds both container images | 3 | VERIFIED | Actual green CI 38947267271 for published commit 3679f58; tests/builds/Trivy/GHCR publication/Helm succeeded; immutable tags shown publicly. |
| M5 | GHCR image publication | 3 | VERIFIED | Actual green CI 38947267271 for published commit 3679f58; tests/builds/Trivy/GHCR publication/Helm succeeded; immutable tags shown publicly. |
| M5 | Immutable commit SHA tags | 2 | VERIFIED | Actual green CI 38947267271 for published commit 3679f58; tests/builds/Trivy/GHCR publication/Helm succeeded; immutable tags shown publicly. |
| M6 | CI Trivy scans both images | 3 | VERIFIED | Both configured scans passed in real green CI; HIGH/CRITICAL fixable findings fail. ignore-unfixed and exact-PURL exceptions disclosed in SECURITY.md. |
| M6 | HIGH/CRITICAL gate | 1 | VERIFIED | Both configured scans passed in real green CI; HIGH/CRITICAL fixable findings fail. ignore-unfixed and exact-PURL exceptions disclosed in SECURITY.md. |
| M6 | Explain a finding and disposition | 1 | VERIFIED | Both configured scans passed in real green CI; HIGH/CRITICAL fixable findings fail. ignore-unfixed and exact-PURL exceptions disclosed in SECURITY.md. |
| M7 | Valid Terraform HCL | 2 | VERIFIED | Actual approved apply created 28 resources October 16. Fresh init/fmt/validate pass; refreshed plan has no changes. ACTIVE VPC/EKS/workers verified by AWS APIs. |
| M7 | Terraform init | 1 | VERIFIED | Actual approved apply created 28 resources October 16. Fresh init/fmt/validate pass; refreshed plan has no changes. ACTIVE VPC/EKS/workers verified by AWS APIs. |
| M7 | Non-empty Terraform plan | 2 | VERIFIED | Actual approved apply created 28 resources October 16. Fresh init/fmt/validate pass; refreshed plan has no changes. ACTIVE VPC/EKS/workers verified by AWS APIs. |
| M7 | VPC with two public subnets provisioned | 3 | VERIFIED | Actual approved apply created 28 resources October 16. Fresh init/fmt/validate pass; refreshed plan has no changes. ACTIVE VPC/EKS/workers verified by AWS APIs. |
| M7 | EKS and worker node group provisioned | 4 | VERIFIED | Actual approved apply created 28 resources October 16. Fresh init/fmt/validate pass; refreshed plan has no changes. ACTIVE VPC/EKS/workers verified by AWS APIs. |
| M7 | Terraform destroy demonstrated | 2 | IMPLEMENTED | Read-only 28-delete preview and cleanup procedure exist. No deletion approved or executed; actual destroy screenshot missing. |
| M7 | Example tfvars, no secrets | 1 | VERIFIED | Actual approved apply created 28 resources October 16. Fresh init/fmt/validate pass; refreshed plan has no changes. ACTIVE VPC/EKS/workers verified by AWS APIs. |
| M8 | Namespace applies | 1 | VERIFIED | Live EKS: 7 Ready application/monitoring Pods, two replicas each app, Helm revision 2, ClusterIP endpoints, working Ingress, valid HPA, Bound encrypted gp3 PVC. |
| M8 | Helm chart structure | 3 | VERIFIED | Live EKS: 7 Ready application/monitoring Pods, two replicas each app, Helm revision 2, ClusterIP endpoints, working Ingress, valid HPA, Bound encrypted gp3 PVC. |
| M8 | Helm install/upgrade succeeds | 3 | VERIFIED | Live EKS: 7 Ready application/monitoring Pods, two replicas each app, Helm revision 2, ClusterIP endpoints, working Ingress, valid HPA, Bound encrypted gp3 PVC. |
| M8 | Frontend and backend each have 2 replicas | 2 | VERIFIED | Live EKS: 7 Ready application/monitoring Pods, two replicas each app, Helm revision 2, ClusterIP endpoints, working Ingress, valid HPA, Bound encrypted gp3 PVC. |
| M8 | ClusterIP services | 2 | VERIFIED | Live EKS: 7 Ready application/monitoring Pods, two replicas each app, Helm revision 2, ClusterIP endpoints, working Ingress, valid HPA, Bound encrypted gp3 PVC. |
| M8 | Ingress routes frontend and `/api` | 2 | VERIFIED | Live EKS: 7 Ready application/monitoring Pods, two replicas each app, Helm revision 2, ClusterIP endpoints, working Ingress, valid HPA, Bound encrypted gp3 PVC. |
| M8 | Pods running and ready | 2 | VERIFIED | Live EKS: 7 Ready application/monitoring Pods, two replicas each app, Helm revision 2, ClusterIP endpoints, working Ingress, valid HPA, Bound encrypted gp3 PVC. |
| M9 | Prometheus `/metrics` output | 2 | VERIFIED | Actual backend metrics; Prometheus up=1 and positive HTTP rates; Grafana health database=ok and a populated real request panel. |
| M9 | Prometheus scrapes application | 3 | VERIFIED | Actual backend metrics; Prometheus up=1 and positive HTTP rates; Grafana health database=ok and a populated real request panel. |
| M9 | Grafana installed and accessible | 2 | VERIFIED | Actual backend metrics; Prometheus up=1 and positive HTTP rates; Grafana health database=ok and a populated real request panel. |
| M9 | Live request metrics panel | 3 | VERIFIED | Actual backend metrics; Prometheus up=1 and positive HTTP rates; Grafana health database=ok and a populated real request panel. |
| M10 | Root README explains application | 2 | VERIFIED | README reviewed and corrected for the actual deployment, evidence paths and current submission instructions. |
| M10 | Live or recorded commit → CI → deployment update presentation | 3 | VERIFIED | README explains original application. Verified real 0410804 commit, green CI 38946277016, Helm revision 2 image rollout, changed EKS page and passing CRUD recorded; instructor acceptance remains external. Video: videos/m10-real-release-walkthrough.webm plus result continuation. |

## Remaining external actions

1. Confirm the teacher accepted the repository URL in the single-submission form; retain the receipt. Do not resubmit if already submitted.
2. Review the genuine videos/presentation notes and provide your own explanation or obtain acceptance of the automated recording.
3. After evaluation/evidence, explicitly approve project cleanup including database deletion; capture actual destroy completion and verify ELB/EBS cleanup. No approval or deletion is inferred from a request to maximize marks.
