# Verification — final audit October 17, 2026

**44/46 criteria demonstrated; estimated 96/100 before instructor judgment/late policy.** Correct AWS account `525426877661`, profile `devops-new`, Sydney `ap-southeast-2` confirmed by STS. [Exact commands, timestamps and exit codes](evidence/final-2026-10-17/collection-results.json), [criterion mapping](GRADING-CHECKLIST.md).

## Executed checks

| Command / check | Observed result | Actual output |
|---|---|---|
| `backend/.venv/bin/pytest -v` | 16 passed, 1 non-failing Starlette deprecation warning; isolated SQLite | [text](evidence/final-2026-10-17/pytest.txt), [JUnit](evidence/final-2026-10-17/pytest.xml), [screenshot](evidence/screenshots/2026-10-17-m2-pytest.png) |
| `npm run build` | Vite build passed | [build](evidence/final-2026-10-17/frontend-build.txt) |
| `docker compose up --build -d --wait` | Successful; frontend/backend/PostgreSQL healthy; migration service completed | [full build](evidence/final-2026-10-17/compose-build.txt), [runtime/non-root screenshot](evidence/screenshots/2026-10-17-m4-compose.png) |
| `python scripts/smoke.py` against Compose and EKS | Both passed: POST 201, GET/PUT 200, DELETE 204; retained demo rows prove persistence | [Compose](evidence/final-2026-10-17/compose-smoke.txt), [EKS](evidence/final-2026-10-17/eks-smoke.txt) |
| Read-only Terraform `init`, `fmt -check`, `validate` | All passed, locked provider | [init](evidence/final-2026-10-17/terraform-init.txt), [fmt](evidence/final-2026-10-17/terraform-fmt.txt), [validate](evidence/final-2026-10-17/terraform-validate.txt) |
| `terraform plan -detailed-exitcode` via guarded helper | Exit 0: no changes; real AWS resources refreshed | [complete plan](evidence/final-2026-10-17/terraform-plan.txt), [screenshot](evidence/screenshots/2026-10-17-m7-terraform.png) |
| AWS EKS / managed group / add-ons | ACTIVE; two private t3.medium workers Ready; 3 ACTIVE add-ons | [EKS](evidence/final-2026-10-17/aws-eks.json), [node group](evidence/final-2026-10-17/aws-nodegroup.json), [nodes](evidence/final-2026-10-17/eks-nodes.json) |
| VPC / subnets / routes / NAT / IAM | Two public + two private subnets; NAT available; 3 roles/5 policy attachments; scoped EBS Pod Identity | [assertions](evidence/final-2026-10-17/infrastructure-assertions.json), [API collection](evidence/final-2026-10-17/collection-results.json) |
| Classic ELB / storage | Both workers InService; three gp3 disks in-use; 2-GiB PostgreSQL disk encrypted/Bound | [ELB health](evidence/final-2026-10-17/aws-elb-health.json), [volumes](evidence/final-2026-10-17/aws-volumes.json), [PVC](evidence/final-2026-10-17/eks-pvc.json) |
| Kubernetes / Helm / HPA | 7 Ready app/monitoring Pods, app replicas 2 each, release revision 2 deployed, valid HPA CPU | [runtime](evidence/final-2026-10-17/eks-runtime.txt), [Helm](evidence/final-2026-10-17/eks-helm.txt), [screenshot](evidence/screenshots/2026-10-17-m8-pods-deployments.png) |
| PostgreSQL SQL query | Alembic revision 0001_tickets and actual persisted ticket rows | [SQL](evidence/final-2026-10-17/eks-postgres.txt) |
| Backend health / readiness / metrics | UP / READY / real Prometheus HTTP counters | [health](evidence/final-2026-10-17/health.txt), [readiness](evidence/final-2026-10-17/readiness.txt), [metrics](evidence/final-2026-10-17/application-metrics.txt) |
| Prometheus / Grafana | Two independent targets each up=1, correct positive request rates; Grafana database ok, panel configured; populated panel visually checked | [query](evidence/final-2026-10-17/prometheus-up-after.json), [traffic](evidence/final-2026-10-17/prometheus-traffic-after.json), [dashboard screenshot](evidence/screenshots/2026-10-17-grafana-corrected-rates.png) |
| Helm lint local and EKS / monitoring render | All pass; optional chart-icon recommendation only | [local](evidence/final-2026-10-17/helm-local-lint.txt), [EKS](evidence/final-2026-10-17/helm-eks-lint.txt), [render](evidence/final-2026-10-17/monitoring-rendered.yaml) |
| Latest published source CI | Run 38947267271, commit 3679f58: all jobs succeeded, both scans and GHCR pushes passed | [metadata](evidence/final-2026-10-17/actions-run.json), [full logs](evidence/final-2026-10-17/actions-run.txt), [screenshot](evidence/screenshots/2026-10-17-ci-green.png) |
| Git hygiene / public repository | 10+ meaningful commits, ignore rules pass, private state not tracked, repository PUBLIC | [hygiene](evidence/final-2026-10-17/git-hygiene.json), [repository](evidence/final-2026-10-17/github-repository.json) |

## Deployment and original approval proof

Owner-approved saved plan SHA `aa108fbd0b0538cf5a977a750e4de91879b1758c7b4039794835d55046e77f9c` was actually applied October 16: **28 added, 0 changed, 0 destroyed**, exit 0. [Approval](evidence/sydney/DEPLOYMENT-APPROVAL.md), [complete apply](evidence/sydney/terraform-apply.txt), [initial non-empty plan](evidence/sydney/terraform-plan.txt). The fresh no-change plan is drift verification, not a replacement for the rubric's initial non-empty-plan evidence.

EKS frontend `ghcr.io/pranav7796/helpdesk-capstone/frontend:04108043563d24dfc2ceb70e050fd56b5e9cc577`; backend `ghcr.io/pranav7796/helpdesk-capstone/backend:d07bca6accc35f0224aaae8c4057076a9c4c9261`. Helm revision 2. Minikube is retained at its documented d07 release; Compose was rebuilt from current source. No new billable cloud infrastructure, IAM mutation, or infrastructure deletion occurred. The existing monitoring configuration was corrected later in this audit, as detailed below.

Application: http://af43a3e33d68945548232885350507ff-719760255.ap-southeast-2.elb.amazonaws.com . Ingress and EKS API remain restricted to owner IP `202.131.146.146/32`; public repository access does not imply a grader can access that endpoint from another network. Monitoring is localhost-only through port-forwards. No exposure was widened.

## Genuine videos and troubleshooting

[Real release recording](evidence/videos/m10-real-release-walkthrough.webm) captures the actual 0410804 commit/push, green CI 38946277016, immutable frontend promotion, Helm rollout, updated EKS page and CRUD. [Result continuation](evidence/videos/m10-release-result-continuation.webm) separately shows completed green CI; the original GitHub UI lagged behind its actual API result. These are byte-identical verified copies, not spliced footage. [Platform walkthrough](evidence/videos/2026-10-17-platform-walkthrough.webm) supplements AWS Console, current app/monitoring, clearly labeled actual runtime outputs and historical lab recovery. No student narration/instructor acceptance is claimed.

Five intentional local failures were diagnosed and recovered October 16; [complete actual log](evidence/sydney/troubleshooting.txt), [clearly labeled saved-result/current-Pod screenshot](evidence/screenshots/2026-10-17-troubleshooting-recovery.png). No new failures were injected into EKS. The earlier local Minikube external-registry DNS issue remains a limitation; cached-image recovery did not prove external node DNS repaired.

## Limitations and remaining actions

- Form receipt unverified. Submit only the repository URL according to the supplied form; do not duplicate an existing single submission.
- Actual Terraform destroy and required completion screenshot remain unverified because cleanup has not been approved. The read-only 28-delete preview is not cleanup evidence.
- Instructor acceptance/student explanation of automated video remain external.
- Trivy gates fail HIGH/CRITICAL findings with available fixes, with ignore-unfixed and exact-PURL exceptions disclosed in [SECURITY.md](docs/SECURITY.md); no claim of zero possible vulnerabilities.
- Initial sandbox commands could not reach network/provider/test-client facilities; successful checks ran with approved permissions. One capture helper failed on AWS hash-route navigation and was corrected; a transient CLI export issue resolved after serialized verification. Credentials were never logged. Local EKS forwards were reopened; no cloud resource fix was needed.
- Latest owner target is October 19; supplied form said October 16, 11:59 PM IST. Extension/receipt not verified; any late penalty is outside the technical estimate.
- Resources remain running: approximately $0.313–$0.32/hour plus variable usage/tax. [Dated cost estimate](evidence/final-2026-10-17/running-cost-estimate.json); this is not an actual bill or guarantee of credit coverage.

## Monitoring correctness fix verified October 17

The initial Service-level scrape mixed two replicas’ process counters. The audit observed three apparent resets in five minutes even though both Pods were stable: [before query](evidence/final-2026-10-17/prometheus-service-counter-resets-before.json), [actual per-Pod counters](evidence/final-2026-10-17/backend-replica-counters-before.txt).

Fixed Prometheus DNS discovery to use an internal headless Service and one target per backend Pod. Grafana filters the new `scrape_mode="pod"` series. The application/backend/database workloads were unchanged, and no billable cloud resources were added. Promtool validation passed and Prometheus reloaded without a Pod restart. [Actual apply](evidence/final-2026-10-17/monitoring-fix-apply.txt), [validation/reload](evidence/final-2026-10-17/monitoring-fix-validation.txt).

After verification: [two UP targets](evidence/final-2026-10-17/prometheus-up-after.json), [real positive rates](evidence/final-2026-10-17/prometheus-traffic-after.json), [zero per-Pod resets observed](evidence/final-2026-10-17/prometheus-counter-resets-after.json). [Separate genuine correction video](evidence/videos/2026-10-17-monitoring-correction.webm) shows the final monitoring state. The earlier platform walkthrough includes the pre-correction graph and is retained with that limitation; use the correction clip and corrected screenshots as primary M9 evidence.

Final monitoring-fix CI [38997737911](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38997737911) passed all jobs for commit `2fbc48485411ff7239bb92b4290062b7e58d86fb`, including tests, React/image builds, both Trivy gates, GHCR SHA publication, Helm checks and monitoring-manifest validation. [Actual metadata](evidence/final-2026-10-17/monitoring-fix-ci.json), [complete logs](evidence/final-2026-10-17/monitoring-fix-ci.txt), [green screenshot](evidence/screenshots/2026-10-17-ci-monitoring-fix-green.png). Deployed application image SHAs remain unchanged.
