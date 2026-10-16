# Helpdesk capstone progress

Started: 2026-10-16 05:10 UTC / 10:40 IST. Exact deadline requested; not yet supplied. Reserve final hour once confirmed.

Source: https://github.com/Nency-Ravaliya/devops-heros/tree/main/session21-python
Teacher commit: a4e39b6b3a54dab1efd386c75ab86bf1d8a23454. Full rubric preserved in docs/TEACHER-GRADING.md.

Status: VERIFIED requires observed evidence; IMPLEMENTED means files only; BLOCKED requires an external dependency; FAILED means an unsuccessful verification attempt; NOT STARTED means no work yet.

Verified estimate: **0/100**. Potential marks are not awarded marks; only the instructor awards the final score.

| Module | Criterion | Marks | Status | Evidence |
|---|---|---:|---|---|
| M1 | FastAPI backend starts and responds to `/health` | 2 | NOT STARTED | — |
| M1 | Minimum 4 REST API endpoints implemented (GET, POST, PUT, DELETE) | 3 | NOT STARTED | — |
| M1 | PostgreSQL database with at least one table managed by Alembic migrations | 2 | NOT STARTED | — |
| M1 | React/HTML frontend renders and makes API calls | 2 | NOT STARTED | — |
| M1 | Responsive and usable UI (not a blank page) | 1 | NOT STARTED | — |
| M2 | `pytest` runs without errors | 3 | NOT STARTED | — |
| M2 | Minimum 5 test cases covering at least 3 API endpoints | 4 | NOT STARTED | — |
| M2 | Tests use a test database or mock, not the production database | 2 | NOT STARTED | — |
| M2 | `pytest.ini` or `conftest.py` is present and correctly configured | 1 | NOT STARTED | — |
| M3 | Public GitHub repository linked in the submission form | 2 | NOT STARTED | — |
| M3 | Meaningful commit messages (not "update", "fix", "test") | 2 | NOT STARTED | — |
| M3 | `.gitignore` excludes `.env`, `__pycache__`, `node_modules`, `.venv` | 1 | NOT STARTED | — |
| M4 | `backend/Dockerfile` builds successfully | 2 | NOT STARTED | — |
| M4 | `frontend/Dockerfile` uses multi-stage build (Node build + Nginx runtime) | 3 | NOT STARTED | — |
| M4 | Docker images run as non-root users | 2 | NOT STARTED | — |
| M4 | `docker compose up --build` starts all three services (frontend, backend, postgres) | 3 | NOT STARTED | — |
| M5 | `.github/workflows/` contains at least one workflow file | 1 | NOT STARTED | — |
| M5 | Pipeline triggers on push to `main` | 1 | NOT STARTED | — |
| M5 | `pytest` runs as a pipeline job and fails the build on test failure | 3 | NOT STARTED | — |
| M5 | Frontend is built as part of the pipeline | 2 | NOT STARTED | — |
| M5 | Docker images are built for both frontend and backend | 3 | NOT STARTED | — |
| M5 | Images are pushed to GitHub Container Registry (GHCR) | 3 | NOT STARTED | — |
| M5 | Image tags use the Git commit SHA (not `latest`) | 2 | NOT STARTED | — |
| M6 | Trivy scan runs in the CI pipeline on both backend and frontend images | 3 | NOT STARTED | — |
| M6 | Pipeline is configured to fail on HIGH or CRITICAL CVEs | 1 | NOT STARTED | — |
| M6 | Student can explain one CVE found (or explain a clean scan result) | 1 | NOT STARTED | — |
| M7 | `terraform/` directory with valid HCL files | 2 | NOT STARTED | — |
| M7 | `terraform init` completes without errors | 1 | NOT STARTED | — |
| M7 | `terraform plan` produces a non-empty plan with no errors | 2 | NOT STARTED | — |
| M7 | VPC with at least two public subnets is provisioned | 3 | NOT STARTED | — |
| M7 | EKS cluster is provisioned with at least one worker node group | 4 | NOT STARTED | — |
| M7 | `terraform destroy` tears down all resources cleanly | 2 | NOT STARTED | — |
| M7 | `terraform.tfvars.example` present (no real credentials committed) | 1 | NOT STARTED | — |
| M8 | `k8s/namespace.yaml` exists and applies cleanly | 1 | NOT STARTED | — |
| M8 | Helm chart in `helm/` directory with `Chart.yaml`, `values.yaml`, and templates | 3 | NOT STARTED | — |
| M8 | `helm upgrade --install` deploys the application without errors | 3 | NOT STARTED | — |
| M8 | Backend and frontend Deployments are running with at least 2 replicas each | 2 | NOT STARTED | — |
| M8 | ClusterIP Services expose backend and frontend | 2 | NOT STARTED | — |
| M8 | Ingress resource routes `/` to frontend and `/api` to backend | 2 | NOT STARTED | — |
| M8 | `kubectl get pods -n <namespace>` shows all pods in `Running` state | 2 | NOT STARTED | — |
| M9 | `/metrics` endpoint on the backend returns Prometheus-formatted output | 2 | NOT STARTED | — |
| M9 | Prometheus is installed in the cluster and scraping the application | 3 | NOT STARTED | — |
| M9 | Grafana is installed and accessible | 2 | NOT STARTED | — |
| M9 | At least one Grafana panel shows live application metrics (HTTP requests, latency, or error rate) | 3 | NOT STARTED | — |
| M10 | `README.md` in the project root explaining what the application does | 2 | NOT STARTED | — |
| M10 | Live demo: commit a change, watch the pipeline run, see the deployment update | 3 | NOT STARTED | — |
