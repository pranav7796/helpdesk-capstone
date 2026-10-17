# Submission package — final audit October 17, 2026

**44 of 46 grading criteria demonstrated; estimated technical coverage 96/100.** The repository/evidence package is prepared. Form submission and actual approved cleanup remain unverified (2 points each). Only the instructor awards marks, including acceptance of the automated recorded presentation and any late policy.

## Submit exactly this repository URL

**https://github.com/pranav7796/helpdesk-capstone**

The Google Form instructions supplied by the owner require the **repository URL only**, with one submission considered. The evidence and videos are inside that repository. Do not put the AWS endpoint, Actions URL, or multiple links in the GitHub URL field. If already submitted, retain the confirmation and do not resubmit. No submission receipt is available to the agent; “Draft saved” does not prove submission.

**Deadline discrepancy:** the latest owner instruction says October 19, 2026. The form text previously supplied says **October 16, 2026 at 11:59 PM IST**. An extension has not been verified. Confirm the actual accepted deadline/receipt with the instructor; this technical estimate does not assume an extension or exclude possible late deductions. The teacher's current `GRADING.md` matches the complete local snapshot; its published directory has no `student-guide.md`.

## Evidence entry points

- [Every one of the 46 grading criteria](GRADING-CHECKLIST.md), with implementation, observed results, points, status and direct screenshot filenames.
- [Actual verification commands/results](VERIFICATION.md).
- [Screenshots](evidence/screenshots/) — current October 17 captures and clearly named byte-identical October 16 archive copies.
- [Videos](evidence/videos/) — actual release demonstration, separate result continuation, and current platform walkthrough.
- [Machine-readable criterion mapping](evidence/final-2026-10-17/criterion-evidence.json), [integrity audit](evidence/final-2026-10-17/evidence-audit.json).
- [Presentation notes](docs/PRESENTATION.md), [security explanation](docs/SECURITY.md), [troubleshooting](docs/TROUBLESHOOTING.md), [AWS resource/cost review](docs/AWS-PLAN.md).

## Module checklist

| Module | Result | Estimated demonstrated points | Primary evidence |
|---|---|---:|---|
| M1 Application | PASS | 10/10 | [EKS app](evidence/screenshots/2026-10-17-application-eks.png), [real HTTP/CRUD](evidence/final-2026-10-17/eks-smoke.txt), [migration/rows](evidence/final-2026-10-17/eks-postgres.txt); mobile screenshot paths in full checklist |
| M2 Tests | PASS | 10/10 | [16 passing tests](evidence/screenshots/2026-10-17-m2-pytest.png), [JUnit](evidence/final-2026-10-17/pytest.xml) |
| M3 Git/GitHub | PARTIAL | 3/5 | Public repository, meaningful commits and ignore rules verified; form receipt missing |
| M4 Docker | PASS | 10/10 | [actual build/healthy/non-root](evidence/screenshots/2026-10-17-m4-compose.png), [browser](evidence/screenshots/2026-10-17-application-compose.png) |
| M5 CI/CD | PASS | 15/15 | [real green CI](evidence/screenshots/2026-10-17-ci-green.png), [GHCR backend](evidence/screenshots/2026-10-17-ghcr-backend.png), [frontend](evidence/screenshots/2026-10-17-ghcr-frontend.png), [logs](evidence/final-2026-10-17/actions-run.txt) |
| M6 Trivy | PASS under disclosed policy | 5/5 | Actual pipeline scans and security explanation; genuine saved-run screenshots in full checklist |
| M7 Terraform/AWS | PARTIAL | 13/15 | [fresh no-drift verification](evidence/screenshots/2026-10-17-m7-terraform.png), [VPC Console](evidence/screenshots/2026-10-17-aws-vpc-console.png), [EKS Console](evidence/screenshots/2026-10-17-aws-eks-console.png); initial 28-addition plan/apply retained; destroy pending |
| M8 Kubernetes/Helm | PASS | 15/15 | [Pods/deployments/Helm/HPA/PVC](evidence/screenshots/2026-10-17-m8-pods-deployments.png), [Services/Ingress/HTTP](evidence/screenshots/2026-10-17-m8-services-ingress.png) |
| M9 Monitoring | PASS | 10/10 | [metrics](evidence/screenshots/2026-10-17-m9-metrics.png), [Targets UP](evidence/screenshots/2026-10-17-prometheus-replicas-up.png), [populated Grafana](evidence/screenshots/2026-10-17-grafana-corrected-rates.png) |
| M10 Documentation/demo | Technical sequence PASS; instructor acceptance external | 5/5 | README and verified real recorded commit → CI → rollout → changed application, linked below |

## Verified videos (four files)

1. [Real release demonstration](evidence/videos/m10-real-release-walkthrough.webm): **304.68 seconds**, real 0410804 commit/push, successful CI 38946277016, immutable frontend image promotion, Helm revision 2, changed EKS page, post-rollout CRUD.
2. [Separate completed-result continuation](evidence/videos/m10-release-result-continuation.webm): actual green CI page and updated app. This is deliberately separate; the original browser UI lagged behind the successful API status. No synthetic status or spliced sequence is claimed.
3. [October 17 platform walkthrough](evidence/videos/2026-10-17-platform-walkthrough.webm): genuine AWS Console resources, current application and editor, Prometheus/Grafana, clearly labeled captured Kubernetes/Helm/PostgreSQL output, and clearly labeled October 16 local troubleshooting recovery.

4. [Final monitoring correction](evidence/videos/2026-10-17-monitoring-correction.webm): two independently scraped backend targets UP and correct real request-rate series. Watch this after the platform walkthrough, whose initial graph preceded the correction.

Files are validated and checksummed in the evidence audit. Download the `.webm` files if GitHub does not preview them. These are automated recordings without student narration; use the presentation notes to explain the system yourself. Instructor acceptance is not assumed.

## Actual deployment

- Account **525426877661**, profile **devops-new**, Sydney **ap-southeast-2**.
- EKS `relaydesk-capstone`, managed group `relaydesk-capstone-workers`, **two Ready private t3.medium nodes**.
- **Seven Ready application/monitoring Pods**; backend/frontend each 2 replicas; HPA CPU valid; PostgreSQL PVC Bound to encrypted 2-GiB gp3.
- VPC `vpc-0f1334a144012db46`: two public/two private subnets, required routing, one available NAT; actual IAM roles and policy attachments checked.
- Classic ELB has both worker backends **InService**. Three gp3 disks are in use (20+20+2 GiB).
- Backend GHCR SHA `d07bca6accc35f0224aaae8c4057076a9c4c9261`; frontend SHA `04108043563d24dfc2ceb70e050fd56b5e9cc577`; Helm revision 2. Later documentation commits/images are not silently deployed.
- [Actual application](http://af43a3e33d68945548232885350507ff-719760255.ap-southeast-2.elb.amazonaws.com). Access remains restricted to `202.131.146.146/32`; a grader on another network cannot directly access it. Screenshots, recordings and local execution instructions remain available. No exposure was widened without approval.
- Compose runs at <http://localhost:3000>; backend at <http://localhost:8000>. Local-only EKS forwards: backend 8001, Prometheus 9091, Grafana 3002. Grafana password stays in ignored private files.

Green published-source CI: https://github.com/pranav7796/helpdesk-capstone/actions/runs/38947267271 . Actual recorded release CI: https://github.com/pranav7796/helpdesk-capstone/actions/runs/38946277016 . [Metadata/logs](evidence/final-2026-10-17/actions-run.json).

## Remaining personal actions

1. Confirm the correct repository URL was accepted by the form, with your actual group, and retain its confirmation. Do not duplicate an already completed single submission. Verify the deadline discrepancy/extension directly.
2. Review the videos and rehearse the explanation in `docs/PRESENTATION.md`; deliver it if the instructor requires a live or narrated presentation.
3. **After evaluation/evidence, separately approve project cleanup including ticket-data deletion.** The required actual destroy screenshot does not exist yet. The preview is 28 Terraform deletions; Kubernetes-created ELB and data disk must be removed safely before VPC/CSI destruction. [Exact cleanup inventory/order](docs/CLEANUP-REVIEW.md). No resources have been deleted.

**Running costs:** approximately **$0.313–$0.32/hour**, about **$7.55 per additional 24 hours**, plus data/transfer, burst CPU, partial-hour rounding and tax. The dated elapsed baseline estimate is about **$3** as of this audit; it is not an actual bill. Current credit balance, applicability/expiry/sharing are unverified. [Dated estimate](evidence/final-2026-10-17/running-cost-estimate.json). Evidence collection is complete once the integrity report passes; resources remain running until explicitly approved for cleanup.

Never submit private state, plan binaries, AWS credentials, generated passwords, kubeconfig, or `evidence/private/`. No extra attachments or alternative URLs are required by the supplied Google Form; the repository contains the complete reviewable package.

## Monitoring correctness fix verified October 17

The initial Service-level scrape mixed two replicas’ process counters. The audit observed three apparent resets in five minutes even though both Pods were stable: [before query](evidence/final-2026-10-17/prometheus-service-counter-resets-before.json), [actual per-Pod counters](evidence/final-2026-10-17/backend-replica-counters-before.txt).

Fixed Prometheus DNS discovery to use an internal headless Service and one target per backend Pod. Grafana filters the new `scrape_mode="pod"` series. The application/backend/database workloads were unchanged, and no billable cloud resources were added. Promtool validation passed and Prometheus reloaded without a Pod restart. [Actual apply](evidence/final-2026-10-17/monitoring-fix-apply.txt), [validation/reload](evidence/final-2026-10-17/monitoring-fix-validation.txt).

After verification: [two UP targets](evidence/final-2026-10-17/prometheus-up-after.json), [real positive rates](evidence/final-2026-10-17/prometheus-traffic-after.json), [zero per-Pod resets observed](evidence/final-2026-10-17/prometheus-counter-resets-after.json). [Separate genuine correction video](evidence/videos/2026-10-17-monitoring-correction.webm) shows the final monitoring state. The earlier platform walkthrough includes the pre-correction graph and is retained with that limitation; use the correction clip and corrected screenshots as primary M9 evidence.

Final monitoring-fix CI [38997737911](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38997737911) passed all jobs for commit `2fbc48485411ff7239bb92b4290062b7e58d86fb`, including tests, React/image builds, both Trivy gates, GHCR SHA publication, Helm checks and monitoring-manifest validation. [Actual metadata](evidence/final-2026-10-17/monitoring-fix-ci.json), [complete logs](evidence/final-2026-10-17/monitoring-fix-ci.txt), [green screenshot](evidence/screenshots/2026-10-17-ci-monitoring-fix-green.png). Deployed application image SHAs remain unchanged.
