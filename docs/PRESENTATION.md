# Presentation notes and final seven marks

Only the instructor awards marks. Do not claim submission, cleanup or student understanding from configuration files alone.

## Six-minute explanation to rehearse

1. **Application (45s).** Relaydesk tracks helpdesk tickets, requesters, owners, priority and status. Demonstrate create, list, edit, status/priority change and deletion. React calls `/api/tickets`; FastAPI validates requests and SQLAlchemy persists them in PostgreSQL. Alembic manages schema history.
2. **Quality and containers (45s).** Show the 16 passing tests and isolated SQLite fixture. Production uses PostgreSQL; explain the test-dialect limitation. Frontend builds in Node and serves static assets from Nginx. Application containers run as non-root users. Compose starts the complete local stack.
3. **Actual release recording (90s).** Play `evidence/videos/m10-real-release-walkthrough.webm` and its separate result continuation; the manifest confirms success. The summary originally counted HIGH and URGENT tickets under “High priority”; the new “High & urgent” label accurately describes that count. Show the actual Git diff, push-triggered pipeline, successful tests/builds/Trivy, immutable SHA image publication, Helm upgrade, and changed EKS page. CI publication and Helm promotion are separate steps; no automatic CI-to-EKS deploy job is claimed.
4. **AWS and Kubernetes (60s).** Terraform provisioned the Sydney VPC, public/private subnets, NAT, EKS and two private managed workers. Mumbai was unavailable under the organization policy; Sydney was explicitly approved. Traefik and a Classic ELB implement Ingress. ClusterIP Services select application Pods; two replicas and readiness probes support rolling updates. PostgreSQL uses an encrypted gp3 PVC. Stateful PostgreSQL in Kubernetes is a classroom choice; managed databases offer operational tradeoffs.
5. **Metrics and failure recovery (45s).** `/health` tests process health; `/ready` checks database access. `/metrics` exposes counters. Prometheus scrapes the application and Grafana plots real request rates. Explain an image pull failure, crash loop, bad Service selector, readiness failure and database outage using the documented logs/events/endpoints.
6. **Security and costs (45s).** Trivy scans OS and application dependencies. HIGH/CRITICAL findings with available fixes fail the gate; ignore-unfixed and scoped false-positive exceptions are disclosed. A clean report is not a guarantee of no vulnerabilities. Credentials, private state and passwords are not committed. AWS is approximately $0.32/hour plus variable usage/tax, and credits are not a hard cap. Cleanup requires explicit approval after evaluation; verify ELB/EBS deletion as well as Terraform destroy completion.

## Submission text

Repository: https://github.com/pranav7796/helpdesk-capstone

Original application: Relaydesk Helpdesk Ticket Management — React/Vite, FastAPI, PostgreSQL, SQLAlchemy and Alembic. Sixteen isolated API tests pass. Docker Compose, immutable GHCR publication, CI Trivy gates, real Sydney VPC/EKS deployment, Helm/Ingress/HPA, Prometheus and Grafana are evidenced in `SUBMISSION.md` and `GRADING-CHECKLIST.md`. Security scan exclusions and remaining submission/cleanup limitations are disclosed.

The supplied form accepts the repository URL only. The repository contains the recordings, manifests, selected screenshots, successful pipeline links and (after separate approval/execution) the actual destroy screenshot. Do not add extra links to the GitHub URL field. Do not submit private state, passwords, kubeconfig, plan binaries, or the entire local evidence/private folder.

## Owner actions still required

- Confirm the existing single submission and retain its receipt; do not resubmit if it is already complete. The latest owner target is October 19, but the earlier form text said October 16 at 11:59 PM IST; an extension remains unverified.
- Review the concrete submission before final external submission if required by the form.
- Confirm whether this recording is accepted for the remote presentation, or deliver the live explanation yourself.
- Explicitly approve project cleanup after the demonstration; it erases the cloud ticket database and stops the AWS application. Keep local Compose/Minikube available.

## Monitoring correction

The final setup discovers each backend replica separately through a headless Service. The old load-balanced scrape mixed process counters and produced three false resets in five minutes. The corrected targets carry `scrape_mode="pod"`; Grafana selects only these series. Show the separate monitoring-correction clip as the final state, following the platform walkthrough recorded before this correction. This change adds no billable AWS infrastructure.
