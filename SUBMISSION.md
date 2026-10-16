# Final submission guide — deadline October 19, 2026

**Not ready for a complete 100-point submission yet.** Local application and DevOps evidence are verified; AWS deployment/destroy awaits explicit approval and actual execution. Estimated verified marks: **86/100**, subject to instructor grading. Teacher-form submission (2), accepted student presentation (3), and AWS provisioning/cleanup (9) remain pending.

## Submit these links

- Public repository: https://github.com/pranav7796/helpdesk-capstone
- Verified Sydney-source green pipeline: https://github.com/pranav7796/helpdesk-capstone/actions/runs/38935978045
- Pipeline that produced the actual Minikube release: https://github.com/pranav7796/helpdesk-capstone/actions/runs/38893336596
- Public GHCR [backend](https://github.com/pranav7796/helpdesk-capstone/pkgs/container/helpdesk-capstone%2Fbackend) and [frontend](https://github.com/pranav7796/helpdesk-capstone/pkgs/container/helpdesk-capstone%2Ffrontend).
- [Every grading criterion](GRADING-CHECKLIST.md), [scorecard](PROGRESS.md), [executed checks](VERIFICATION.md).

New source CI commit `e33b8bdcc61c4fdd658e5827044fe868d9dea1ad` passed tests/builds/Trivy/GHCR and both local/EKS Helm checks. [Actual run metadata](evidence/sydney/actions-run.json), [complete log](evidence/sydney/actions-run.txt). Its published images are available for a later reviewed promotion.

Current deployed backend/frontend tags: `d07bca6accc35f0224aaae8c4057076a9c4c9261`. Documentation or infrastructure commits can publish later SHA tags without implying those images were deployed; inspect actual Pod image references.

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
| M7 Terraform/AWS | PARTIAL — real deployment/destroy missing | 6/15 | [Sydney plan](evidence/sydney/m7-sydney-plan.png), [init/fmt/validate](evidence/sydney/m7-sydney-validation.png), [account check](evidence/sydney/m7-sydney-account.png), [plan audit](evidence/sydney/plan-audit.json) |
| M8 Kubernetes/Helm | PASS on Minikube; EKS pending | 15/15 | [current Pods/replicas/HPA/PVC/Helm](evidence/sydney/m8-runtime-current.png), [Services/endpoints](evidence/m8-services.png), [Ingress browser](evidence/sydney/m8-ingress-browser.png) |
| M9 Monitoring | PASS on Minikube | 10/10 | [metrics curl](evidence/m9-metrics.png), [Targets UP](evidence/sydney/m9-prometheus-targets.png), [populated Grafana](evidence/sydney/m9-grafana-current.png), [up query](evidence/sydney/prometheus-up.json) |
| M10 Documentation/demo | PARTIAL | 2/5 | [README](README.md), [current-state video](evidence/m10-automated-walkthrough.webm); accepted student presentation/commit-to-rollout recording still pending |
| Troubleshooting (README lab) | PASS | Included in presentation scope | [five failures recovered](evidence/sydney/troubleshooting-recovery.png), [complete commands/results](evidence/sydney/troubleshooting.txt) |

Trivy scanned the OS and application packages in both final release images. The gate fails on HIGH/CRITICAL findings with available fixes; `ignore-unfixed` and exact-PURL false-positive exceptions are disclosed. Zero reported findings applies to those images and that scan policy, not absence of every vulnerability.

## Exact remaining actions

1. **Approve cloud deployment** only after reviewing [28 exact Terraform additions plus ingress ELB and 2-GiB disk, costs and credit limits](docs/AWS-PLAN.md). Baseline approximately $0.315/hour before variable charges/tax; $0.94/3h, $7.55/24h, $22.64/72h. Account is PAID/ACTIVE and reports $120 credits; applicability/expiry/sharing unverified. [Runbook](docs/EKS-RUNBOOK.md).
2. After deployment, capture actual **Sydney** VPC/subnet and EKS/node-group Console screenshots plus actual AWS/HTTP/Kubernetes evidence. No such resource screenshot currently exists, because no apply has run.
3. Complete the student live presentation or an instructor-accepted recording of a meaningful commit → pipeline → immutable images → Helm rollout → working application. The existing automated video reviews current/historical state and does not replace that event or student explanation.
4. Submit the public repository URL, requested screenshots and presentation through the teacher's actual form. No form submission has been performed by the agent.
5. After demo/evidence, **separately approve cleanup**. Capture real destroy completion and verify Kubernetes-created ELB/EBS resources as well as Terraform resources are gone. Do not tear down before the demo.

## Evidence integrity / limitations

The original screenshot audit and provenance are in [EVIDENCE-AUDIT.md](EVIDENCE-AUDIT.md) and `evidence/audit/`. New Sydney captures/logs are in `evidence/sydney/`, with source commands, timestamps and hashes. Terminal screenshots show actual Foot windows; browser screenshots show real pages. Plan and cost screenshots are explicitly planning/estimate evidence, not deployed-resource proof.

The original `terraform/tfplan` is preserved but superseded by `tfplan-reviewed`; both are ignored. State and generated passwords must stay private. Mumbai SCP restrictions are owner-reported; Sydney reads/planning passed, but create permissions remain unverified until approved apply. Minikube has a registry-DNS issue for uncached images; host-side image pulls/preloading are the local workaround. One test-client deprecation warning remains non-failing.
