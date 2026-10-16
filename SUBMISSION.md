# Capstone submission checklist

## Submit these links

- Public source: https://github.com/pranav7796/helpdesk-capstone
- Rubric scorecard: [PROGRESS.md](PROGRESS.md)
- Evidence and command record: [VERIFICATION.md](VERIFICATION.md)
- Successful GitHub Actions run: https://github.com/pranav7796/helpdesk-capstone/actions/runs/38893336596
- GitHub Container Registry images (immutable SHA `d07bca6accc35f0224aaae8c4057076a9c4c9261`):
  - `ghcr.io/pranav7796/helpdesk-capstone/backend:d07bca6accc35f0224aaae8c4057076a9c4c9261`
  - `ghcr.io/pranav7796/helpdesk-capstone/frontend:d07bca6accc35f0224aaae8c4057076a9c4c9261`

## Evidence included in the repository

- Compose screenshot: [`evidence/relaydesk-compose.png`](evidence/relaydesk-compose.png)
- Minikube app screenshot: [`evidence/relaydesk-minikube.png`](evidence/relaydesk-minikube.png)
- Responsive 390 px app screenshot: [`evidence/relaydesk-mobile.png`](evidence/relaydesk-mobile.png)
- Successful SHA image rollout screenshot: [`evidence/relaydesk-minikube-sha.png`](evidence/relaydesk-minikube-sha.png)
- Commit → passing workflow → Helm rollout → ingress CRUD evidence: [`evidence/live-demo.txt`](evidence/live-demo.txt)
- Full GitHub Actions logs: [`evidence/actions-run.txt`](evidence/actions-run.txt)
- Grafana populated dashboard: [`evidence/grafana-relaydesk-dashboard.png`](evidence/grafana-relaydesk-dashboard.png)
- API test output and JUnit XML: [`evidence/pytest.txt`](evidence/pytest.txt), [`evidence/pytest.xml`](evidence/pytest.xml)
- Compose CRUD persistence and container users: [`evidence/docker-smoke.txt`](evidence/docker-smoke.txt), [`evidence/docker-compose-ps.txt`](evidence/docker-compose-ps.txt)
- Prometheus target and request results: [`evidence/prometheus-target.json`](evidence/prometheus-target.json), [`evidence/prometheus-requests-query.json`](evidence/prometheus-requests-query.json)
- Trivy local reports: [`evidence/trivy-backend.json`](evidence/trivy-backend.json), [`evidence/trivy-frontend.json`](evidence/trivy-frontend.json)
- Terraform validation and saved no-refresh plan: [`evidence/terraform-validate.txt`](evidence/terraform-validate.txt), [`evidence/terraform-plan-refresh-false.txt`](evidence/terraform-plan-refresh-false.txt)
- Helm and Kubernetes state: [`evidence/helm-rendered.yaml`](evidence/helm-rendered.yaml), [`evidence/minikube-status.txt`](evidence/minikube-status.txt)

## Final checks before submitting

- [x] GitHub Actions run 38893336596 completed green; test, image, scan, publish, and Helm jobs succeeded.
- [x] Both GHCR SHA images were pulled and used in the Helm rollout.
- [x] Commit-to-CI-to-deployment demonstration and ingress CRUD were captured in `evidence/live-demo.txt`.
- [ ] Paste the repository URL into the teacher's submission form.
- [ ] Attach or show the included screenshots and test/deployment evidence as requested by the instructor.

## AWS limitation

No VPC/EKS resources were created. Read-only AWS checks found an EC2 opt-in restriction and an EKS subscription restriction in `ap-south-1`, so the Terraform apply and destroy criteria are unverified. Do not claim cloud deployment. See [AWS plan and eligibility](docs/AWS-PLAN.md).
