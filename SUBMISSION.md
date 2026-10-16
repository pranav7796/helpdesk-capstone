# Final submission guide — deadline October 19, 2026

**Not ready for a complete 100-point submission yet.** Local and Sydney cloud deployments are verified. Estimated verified marks: **93/100**, subject to instructor grading. Teacher-form submission (2), accepted student presentation (3), and separately approved cleanup (2) remain pending.

Final runner-pin verification also passed: [38936702532](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38936702532), commit `d5ad1ab83c035fd75852e741e3f6482bb92afec5`. [Actual final run metadata](evidence/sydney/actions-final.json). A subsequent commit only records verification evidence.

## Submit these links

- Public repository: https://github.com/pranav7796/helpdesk-capstone
- Verified Sydney-source green pipeline: https://github.com/pranav7796/helpdesk-capstone/actions/runs/38935978045
- Pipeline that produced the actual Minikube release: https://github.com/pranav7796/helpdesk-capstone/actions/runs/38893336596
- Public GHCR [backend](https://github.com/pranav7796/helpdesk-capstone/pkgs/container/helpdesk-capstone%2Fbackend) and [frontend](https://github.com/pranav7796/helpdesk-capstone/pkgs/container/helpdesk-capstone%2Ffrontend).
- [Every grading criterion](GRADING-CHECKLIST.md), [scorecard](PROGRESS.md), [executed checks](VERIFICATION.md).

New source CI commit `e33b8bdcc61c4fdd658e5827044fe868d9dea1ad` passed tests/builds/Trivy/GHCR and both local/EKS Helm checks. [Actual run metadata](evidence/sydney/actions-run.json), [complete log](evidence/sydney/actions-run.txt). Its published images are available for a later reviewed promotion.

Current Minikube and EKS deployed backend/frontend tags: `d07bca6accc35f0224aaae8c4057076a9c4c9261`. Documentation or infrastructure commits can publish later SHA tags without implying those images were deployed; inspect actual Pod image references.

## PASS/FAIL checklist and primary evidence

PASS means the technical requirement was demonstrated, not that the teacher has awarded points. PARTIAL identifies missing submission or runtime requirements.

| Module | Result | Estimated verified points | Primary screenshots / output |
|---|---|---:|---|
| M1 Application | PASS | 10/10 | [app](evidence/sydney/m4-compose-browser.png), [DB/Alembic/health](evidence/m1-health-database.png), [editor](evidence/m1-ticket-editor.png), [mobile](evidence/m1-mobile-actions.png), [CRUD](evidence/sydney/docker-smoke.txt) |
| M2 Tests | PASS | 10/10 | [16 passing tests](evidence/sydney/m2-tests-current.png), [JUnit](evidence/sydney/pytest.xml) |
| M3 Git/GitHub | PARTIAL | 3/5 | [10+ meaningful commits](evidence/m3-git-history.png); public repo exists, teacher-form receipt missing |
| M4 Docker | PASS | 10/10 | [build/healthy/non-root](evidence/m4-compose.png), [localhost browser](evidence/sydney/m4-compose-browser.png), [current status](evidence/sydney/docker-status.txt) |
| M5 CI/CD | PASS | 15/15 | [green Actions](evidence/sydney/m5-actions-success.png), [backend SHA tags](evidence/sydney/m5-ghcr-backend.png), [frontend SHA tags](evidence/sydney/m5-ghcr-frontend.png), [release logs](evidence/actions-run.txt) |
| M6 Trivy | PASS with disclosed scan policy | 5/5 | [backend](evidence/m6-trivy-backend.png), [frontend](evidence/m6-trivy-frontend.png), [CVE explanation](docs/SECURITY.md) |
| M7 Terraform/AWS | PARTIAL — destroy pending | 13/15 | [Sydney plan](evidence/sydney/m7-sydney-plan.png), [init/fmt/validate](evidence/sydney/m7-sydney-validation.png), [account check](evidence/sydney/m7-sydney-account.png), [plan audit](evidence/sydney/plan-audit.json) |
| M8 Kubernetes/Helm | PASS on Minikube and EKS | 15/15 | [current Pods/replicas/HPA/PVC/Helm](evidence/sydney/m8-runtime-current.png), [Services/endpoints](evidence/m8-services.png), [Ingress browser](evidence/sydney/m8-ingress-browser.png) |
| M9 Monitoring | PASS on Minikube and EKS | 10/10 | [metrics curl](evidence/m9-metrics.png), [Targets UP](evidence/sydney/m9-prometheus-targets.png), [populated Grafana](evidence/sydney/m9-grafana-current.png), [up query](evidence/sydney/prometheus-up.json) |
| M10 Documentation/demo | PARTIAL | 2/5 | [README](README.md), [current-state video](evidence/m10-automated-walkthrough.webm); accepted student presentation/commit-to-rollout recording still pending |
| Troubleshooting (README lab) | PASS | Included in presentation scope | [five failures recovered](evidence/sydney/troubleshooting-recovery.png), [complete commands/results](evidence/sydney/troubleshooting.txt) |

Trivy scanned the OS and application packages in both final release images. The gate fails on HIGH/CRITICAL findings with available fixes; `ignore-unfixed` and exact-PURL false-positive exceptions are disclosed. Zero reported findings applies to those images and that scan policy, not absence of every vulnerability.

## Actual Sydney cloud evidence

Application: [http://af43a3e33d68945548232885350507ff-719760255.ap-southeast-2.elb.amazonaws.com](http://af43a3e33d68945548232885350507ff-719760255.ap-southeast-2.elb.amazonaws.com) (owner IP `202.131.146.146/32` only).

| Requirement | Primary genuine evidence under `evidence/sydney/` |
|---|---|
| Terraform apply / 28 created | `terraform-apply.txt`, `aws-apply-verified.png` |
| VPC / public and private subnets / routing | `aws-vpc-console.png`, `aws-subnets-console.png`, `aws-network-verified.png` |
| ACTIVE EKS / 2 Ready workers | `aws-eks-console.png`, `aws-apply-verified.png`, `eks-nodes.json` |
| Pods / replicas / Helm / HPA / persistent disk | `eks-pods-helm.png`, `eks-postgres-persistence.txt` |
| Services / endpoints / Ingress / CRUD | `eks-services-ingress.png`, `eks-http-smoke.txt`, `eks-application-browser.png` |
| Metrics / scrape / populated panel | `eks-metrics.png`, `eks-prometheus-targets.png`, `eks-grafana-dashboard.png` |

All cloud screenshots were captured automatically from real terminal/browser surfaces; no manual screenshot is currently needed. Resources remain running for demonstration, approximately $0.32/hour before variable charges/tax. [Cost ledger](evidence/sydney/COST-TRACKING.md), [resource/state/cleanup review](docs/CLEANUP-REVIEW.md).

## Exact remaining actions

1. **Deployment and cloud evidence are complete.** Keep the environment available for the demonstration.
2. Review the actual cloud evidence table above and the per-criterion checklist.
3. Complete the student live presentation or an instructor-accepted recording of a meaningful commit → pipeline → immutable images → Helm rollout → working application. The existing automated video reviews current/historical state and does not replace that event or student explanation.
4. Submit the public repository URL, requested screenshots and presentation through the teacher's actual form. No form submission has been performed by the agent.
5. After demo/evidence, **separately approve cleanup**. Capture real destroy completion and verify Kubernetes-created ELB/EBS resources as well as Terraform resources are gone. Do not tear down before the demo.

## Evidence integrity / limitations

The original screenshot audit and provenance are in [EVIDENCE-AUDIT.md](EVIDENCE-AUDIT.md) and `evidence/audit/`. New Sydney captures/logs are in `evidence/sydney/`, with source commands, timestamps and hashes. Terminal screenshots show actual Foot windows; browser screenshots show real pages. Plan and cost screenshots are explicitly planning/estimate evidence, not deployed-resource proof.

The original `terraform/tfplan` is preserved but superseded by `tfplan-reviewed`; both are ignored. State and generated passwords must stay private. Mumbai SCP restrictions are owner-reported; Sydney apply and deployment succeeded. Minikube has a registry-DNS issue for uncached images; host-side image pulls/preloading are the local workaround. One test-client deprecation warning remains non-failing.

Deployment commit `20c2401e206f85d1c2901cead55160c1007bf0e0` passed [CI 38945382171](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38945382171): 16 tests, React/container builds, both Trivy scans, GHCR SHA publication and Helm validation. [Actual metadata](evidence/sydney/actions-deployment.json), [full logs](evidence/sydney/actions-deployment.txt). The earlier evidence-only run 38937333354 failed during GHCR publication with `unknown blob`; the new complete run passed. Deployed d07 images remain unchanged.
