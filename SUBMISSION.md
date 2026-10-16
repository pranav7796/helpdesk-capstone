# Capstone submission package

Required visual evidence for the running local application, tests, Git, Docker, CI/security, Kubernetes, and monitoring is captured and reviewed. AWS deployment/destroy evidence is blocked. The repository submission and presentation remain student actions. See [EVIDENCE-AUDIT.md](EVIDENCE-AUDIT.md) for the full audit and qualifications.

## Links to submit

- Public repository: https://github.com/pranav7796/helpdesk-capstone
- Successful source/evidence baseline pipeline: https://github.com/pranav7796/helpdesk-capstone/actions/runs/38894949621
- Successful pipeline used for the actual Minikube release: https://github.com/pranav7796/helpdesk-capstone/actions/runs/38893336596
- [Scorecard](PROGRESS.md), [verification record](VERIFICATION.md), [full evidence audit](EVIDENCE-AUDIT.md)
- Public packages: [backend](https://github.com/pranav7796/helpdesk-capstone/pkgs/container/helpdesk-capstone%2Fbackend), [frontend](https://github.com/pranav7796/helpdesk-capstone/pkgs/container/helpdesk-capstone%2Ffrontend)

The deployed release uses full SHA `d07bca6accc35f0224aaae8c4057076a9c4c9261`:

```text
ghcr.io/pranav7796/helpdesk-capstone/backend:d07bca6accc35f0224aaae8c4057076a9c4c9261
ghcr.io/pranav7796/helpdesk-capstone/frontend:d07bca6accc35f0224aaae8c4057076a9c4c9261
```

The package screenshots also show later documentation-only commit tags. They do not imply those tags were rolled out; exact deployed references are in the Helm screenshot and `live-demo.txt`.

## Primary screenshots by module

| Module | Evidence to attach or show | Status |
|---|---|---|
| M1 Application | [App at localhost:3000](evidence/m4-compose-browser.png), [health/readiness/Alembic/PostgreSQL](evidence/m1-health-database.png), [ticket editor](evidence/m1-ticket-editor.png) | COMPLETE |
| M1 Responsive UI | [Mobile ticket list](evidence/m1-mobile-tickets.png), [mobile actions after horizontal scrolling](evidence/m1-mobile-actions.png) | COMPLETE; table scrolls horizontally on a narrow screen |
| M2 Tests | [Actual pytest -v terminal](evidence/m2-pytest.png), [raw current output](evidence/audit/m2-pytest.txt), [JUnit XML](evidence/pytest.xml) | COMPLETE: 16 passed |
| M3 Git | [14 meaningful commits and remote URL](evidence/m3-git-history.png) | Screenshot COMPLETE; teacher form still pending |
| M4 Docker | [up --build and healthy services/non-root users](evidence/m4-compose.png), [browser](evidence/m4-compose-browser.png) | COMPLETE; --no-recreate preserved existing container IDs |
| M5 CI/CD | [Green pipeline](evidence/m5-actions-success.png), [backend GHCR SHA tags](evidence/m5-ghcr-backend.png), [frontend GHCR SHA tags](evidence/m5-ghcr-frontend.png) | COMPLETE; package pages are public |
| M6 Trivy | [Backend pipeline output](evidence/m6-trivy-backend.png), [frontend pipeline output](evidence/m6-trivy-frontend.png), [full source log](evidence/actions-run.txt), [CVE explanation](docs/SECURITY.md) | COMPLETE with scan filters/exceptions disclosed |
| M7 Terraform | [init/fmt/validate](evidence/m7-terraform-validation.png), [historical saved plan](evidence/m7-terraform-plan-saved.png), [actual AWS restrictions](evidence/m7-aws-restriction.png) | PARTIAL; saved plan is a no-refresh dry run, not a fresh authenticated plan |
| M8 Kubernetes/Helm | [Running Pods/replicas/HPA/PVC](evidence/m8-pods.png), [Services/endpoints](evidence/m8-services.png), [helm list/status and image SHAs](evidence/m8-helm.png), [app through Ingress](evidence/m8-ingress-browser.png) | COMPLETE; local Minikube, Helm revision 10 |
| M9 Monitoring | [curl /metrics](evidence/m9-metrics.png), [Prometheus Targets UP](evidence/m9-prometheus-targets.png), [populated Grafana panel](evidence/m9-grafana-current.png) | COMPLETE |
| M10 Documentation/demo | [README](README.md), [historical technical sequence](evidence/live-demo.txt), [automated browser walkthrough](evidence/m10-automated-walkthrough.webm), [captions](evidence/m10-automated-walkthrough.vtt) | README COMPLETE; actual presentation/recorded commit-to-rollout sequence pending |

## Trivy result explanation for the submission

Trivy scanned operating-system packages and application libraries in both final release images. The configured HIGH/CRITICAL gate, `ignore-unfixed: true`, and disclosed exact-package SBOM exceptions left zero reported findings, so the successful pipeline published both images. This applies to those images and that scan policy; it does not establish that every vulnerability or unfixable finding is absent.

## Still missing or qualified

- [ ] Paste the public repository URL into the teacher's submission form and attach the primary screenshots.
- [ ] Complete the live presentation or an instructor-accepted recording showing a commit, its pipeline run, and the deployment update. The automated visual walkthrough reviews existing state and historical CI; it does not record a new commit/rollout or student explanation.
- [ ] AWS Console VPC screenshot in `ap-south-1` — BLOCKED: no VPC was provisioned.
- [ ] AWS Console EKS/managed-node-group screenshot in `ap-south-1` — BLOCKED: no EKS cluster was provisioned.
- [ ] Successful `terraform destroy` completion screenshot — BLOCKED: no Terraform apply occurred, so there is no deployment to destroy.
- [ ] Fresh authenticated Terraform plan — not available; the included 22-resource `-refresh=false` output is historical and must be described that way.

EC2 currently returns `OptInRequired`; EKS returns `SubscriptionRequiredException`. No cloud operation was performed to work around those restrictions. Do not substitute a restriction screenshot for proof of a deployed VPC/EKS or successful destroy.

## Readiness and mark estimate

This is ready to submit as a disclosed AWS-limited project once the student submission/presentation steps are completed. It is not a fully complete 100-point submission. The current estimate is 86/100, including 2 qualified historical-plan marks; 2 repository-form marks and 3 presentation marks remain pending. Completing those steps would support the earlier 91/100 non-AWS estimate. Only the instructor awards marks; requiring a fresh plan could reduce the estimate by another 2.

New capture sources, timestamps, exit codes, HTTP statuses, and hashes are recorded under [`evidence/audit/`](evidence/audit/). Terminal screenshots are from real terminal windows and browser screenshots from real pages. Use backend `http://127.0.0.1:8000/metrics` for metrics evidence; Ingress `/metrics` falls through to the frontend.
