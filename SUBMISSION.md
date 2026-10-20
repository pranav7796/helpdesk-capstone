# Submission package — audited October 20, 2026

**44 PASS, 0 FAIL, 2 BLOCKED across 46 criteria.** Demonstrated evidence covers 96/100 rubric points under the disclosed Trivy policy; this is not an awarded grade. C10 (form receipt) and C32 (actual destroy) remain blocked. Instructor acceptance of scan exceptions, the automated recording, and the deadline/extension are unverified.

## Submit this repository URL

**https://github.com/pranav7796/helpdesk-capstone**

The supplied form requires the repository URL only. Confirm whether the single submission already exists and retain its receipt; do not duplicate it. No form was submitted during this audit. The audit report and sanitized evidence are included in this repository update.

## Review entry points

- [Final report with all 46 PASS/FAIL/BLOCKED rows](docs/FINAL-REPORT.md).
- [Grading checklist](GRADING-CHECKLIST.md), [fresh verification](VERIFICATION.md), [dated raw evidence](evidence/final-2026-10-20/), [machine-readable mapping](evidence/final-2026-10-20/criterion-evidence.json).
- [78 genuine dated screenshots](evidence/screenshots/) and [four recordings](evidence/videos/); [fresh integrity check](evidence/final-2026-10-20/evidence-integrity.json).
- [Presentation notes](docs/PRESENTATION.md), [security explanation](docs/SECURITY.md), [troubleshooting](docs/TROUBLESHOOTING.md), [cleanup review](docs/CLEANUP-REVIEW.md).

## Primary visual evidence

| Requirement | Existing genuine capture |
|---|---|
| Running EKS application and ingress | [Application](evidence/screenshots/2026-10-17-application-eks.png), [Services/Ingress](evidence/screenshots/2026-10-17-m8-services-ingress.png) |
| Passing tests and working Compose | [16 tests](evidence/screenshots/2026-10-17-m2-pytest.png), [Compose](evidence/screenshots/2026-10-17-m4-compose.png), [local app](evidence/screenshots/2026-10-17-application-compose.png) |
| Git/CI/GHCR/security | Exact screenshot mapping for C11, C17–C26 in [grading checklist](GRADING-CHECKLIST.md) |
| AWS VPC/EKS and Terraform | [VPC Console](evidence/screenshots/2026-10-17-aws-vpc-console.png), [EKS Console](evidence/screenshots/2026-10-17-aws-eks-console.png), [original non-empty plan](evidence/screenshots/2026-10-16-archive-sydney--m7-sydney-plan.png), [validation](evidence/screenshots/2026-10-17-m7-terraform.png) |
| Ready Pods and Helm release | [Pods/deployments/Helm/HPA/PVC](evidence/screenshots/2026-10-17-m8-pods-deployments.png) |
| Real backend metrics and monitoring | [Metrics](evidence/screenshots/2026-10-17-m9-metrics.png), [two UP targets](evidence/screenshots/2026-10-17-prometheus-replicas-up.png), [populated Grafana](evidence/screenshots/2026-10-17-grafana-corrected-rates.png) |
| Actual destroy completion | **MISSING — prohibited without separate cleanup approval** |

These are Oct 16/17 captures, not new Oct 20 screenshots. Fresh API/CLI checks support the same running deployment. Browser capture was unavailable; no image was relabeled or fabricated.

## Recorded demonstration

1. [Real release walkthrough](evidence/videos/m10-real-release-walkthrough.webm): 304.68 seconds, actual 0410804 commit/push, successful CI 38946277016, immutable frontend promotion, Helm revision 2, changed page and CRUD.
2. [Separate completed-result continuation](evidence/videos/m10-release-result-continuation.webm): separate because the original GitHub UI lagged behind the completed API status; no spliced sequence claimed.
3. [Oct 17 platform walkthrough](evidence/videos/2026-10-17-platform-walkthrough.webm): genuine platform/current views plus clearly labeled historical local troubleshooting.
4. [Monitoring correction](evidence/videos/2026-10-17-monitoring-correction.webm): separate healthy backend targets and corrected rates; supersedes the earlier mixed-Service graph.

Hashes and media metadata passed fresh checks. These recordings are automated and lack student narration; instructor acceptance/student explanation remain external. Download WebMs if GitHub does not preview them. No new commit/rollout was created for this audit.

## Live deployment

Account `525426877661`, profile `devops-new`, Sydney `ap-southeast-2`; EKS `relaydesk-capstone` ACTIVE 1.35. Two private Ready t3.medium workers, seven relaydesk Pods and two Traefik Pods Ready. Application replicas 2 each, encrypted 2-GiB gp3 PVC Bound, valid HPA CPU; live CRUD/SQL/health/metrics and Grafana panel-data query passed. Terraform has no drift. Helm revision 2 and deployed image SHAs are unchanged.

Application: http://af43a3e33d68945548232885350507ff-719760255.ap-southeast-2.elb.amazonaws.com

**Access is restricted to `202.131.146.146/32`.** A grader on another network cannot directly access it. Existing videos/screenshots and local Compose instructions are available. No network permissions were widened. Monitoring uses localhost-only forwards.

Latest published source CI: https://github.com/pranav7796/helpdesk-capstone/actions/runs/38998365240 — SHA a52cd91, all jobs successful. This is a dated Oct 17 run rechecked Oct 20, not a newly triggered pipeline or automatic EKS deployment. Trivy's ignore-unfixed/exact-PURL exceptions are disclosed; strict all-finding acceptance is not assumed.

## Remaining actions

1. Review the report and evidence included in this audit commit; publishing the repository does not submit the teacher form.
2. Confirm the form's existing single submission and preserve its receipt (C10).
3. Confirm accepted deadline/extension and whether the automated video suffices or a personal presentation is required. Prior form deadline Oct 16 and owner target Oct 19 are past at this audit; no extension is verified.
4. After evaluation, separately approve cleanup and ticket-data deletion if desired. Only then capture real successful Terraform destroy plus independent ELB/EBS cleanup proof (C32). Existing resources remain running and chargeable; current billing/credits were not rechecked.

Never submit private state, plan binaries, AWS credentials, generated passwords, kubeconfig or `evidence/private/`.
