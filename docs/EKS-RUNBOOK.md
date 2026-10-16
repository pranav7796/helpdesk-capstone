# Approved Sydney deployment, verification and cleanup

**Executed successfully against EKS October 16 after explicit deployment approval.** [Deploy output](../evidence/sydney/eks-deploy.txt), [runtime verification](../evidence/sydney/eks-verification-summary.json). Helpers: `scripts/deploy-eks.sh`, `scripts/verify-eks.py`. The instructions below preserve the reviewed procedure; do not reapply or delete resources casually. Cleanup still requires separate explicit approval. Scope/cost review: [AWS-PLAN.md](AWS-PLAN.md). Account `525426877661`, profile `devops-new`, region `ap-southeast-2`; deadline October 19, 2026.

## 1. After infrastructure approval only

From the project root, verify identity and `python scripts/audit-plan.py`; the plan hash must match the approval. Confirm `202.131.146.146/32` is still the actual admin egress address. If the configuration, source, IP, credentials, or plan changed, replan/review before apply.

```bash
aws sts get-caller-identity --profile devops-new --region ap-southeast-2
# Run ONLY after explicit approval of the reviewed plan and costs:
AWS_CONFIG_FILE="$PWD/terraform/aws-login.config" AWS_PROFILE=devops-new \
  terraform -chdir=terraform apply tfplan-reviewed
```

Capture stdout/stderr and the exit code under `evidence/sydney/terraform-apply.txt`. Do not enable debug credential logging. On failure inspect the exact failed resource/action and retained state. An SCP denial cannot be fixed by attaching AdministratorAccess; request the organization's permission for the specific action or report the blocker once. Do not switch regions/accounts or change organization/billing settings without review.

Expected Terraform state: `terraform/terraform.tfstate`, local and ignored. Keep a private backup after apply. Verify control plane ACTIVE, managed group ACTIVE, and two EC2 workers actually Ready; file existence and successful planning do not prove these outcomes.

## 2. Isolated kubectl configuration

```bash
mkdir -p evidence/private
chmod 700 evidence/private
export KUBECONFIG="$PWD/evidence/private/kubeconfig-sydney"
aws eks update-kubeconfig --profile devops-new --region ap-southeast-2 \
  --name relaydesk-capstone --alias relaydesk-sydney
kubectl --context relaydesk-sydney get nodes -o wide
aws eks describe-cluster --profile devops-new --region ap-southeast-2 --name relaydesk-capstone
aws eks describe-nodegroup --profile devops-new --region ap-southeast-2 \
  --cluster-name relaydesk-capstone --nodegroup-name relaydesk-capstone-workers
aws eks list-addons --profile devops-new --region ap-southeast-2 --cluster-name relaydesk-capstone
```

Never accidentally use the Minikube context for cloud verification. Renew an expired browser session with `aws login --profile devops-new --region ap-southeast-2`; passwords/MFA/authorization codes stay in the local login flow.

## 3. Deploy the application and ingress (also chargeable)

This phase creates one gp3 EBS disk and one Classic Load Balancer; include both in deployment approval. The EBS CSI/Pod Identity/Metrics Server add-ons are managed by Terraform. Confirm each is ACTIVE first.

Generate private application passwords locally, without printing them:

```bash
python - <<'PY'
import json, os, secrets
from pathlib import Path
private = Path('evidence/private')
private.mkdir(exist_ok=True)
os.chmod(private, 0o700)
for name, data in (
    ('eks-values.json', {'database': {'password': secrets.token_hex(24)}}),
    ('grafana-admin.json', {'apiVersion': 'v1', 'kind': 'Secret',
      'metadata': {'name': 'grafana-admin', 'namespace': 'relaydesk'},
      'type': 'Opaque', 'stringData': {'password': secrets.token_hex(24)}}),
):
    path = private / name
    if path.exists():
        raise SystemExit('Keep existing private credentials; do not overwrite them')
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as stream:
        json.dump(data, stream)
PY
kubectl --context relaydesk-sydney apply -f k8s/namespace.yaml
kubectl --context relaydesk-sydney apply -f k8s/storage-eks.yaml
helm upgrade --install relaydesk helm/helpdesk --kube-context relaydesk-sydney \
  -n relaydesk --create-namespace -f helm/helpdesk/values-eks.yaml \
  -f evidence/private/eks-values.json --wait --timeout 10m
helm upgrade --install traefik traefik --repo https://traefik.github.io/charts \
  --version 42.0.0 --kube-context relaydesk-sydney \
  -n ingress-system --create-namespace -f k8s/traefik-values-eks.yaml --wait --timeout 10m
```

The EKS backend retains the known passing immutable `d07bca6...` release. The frontend was promoted to green-CI SHA `04108043563d24dfc2ceb70e050fd56b5e9cc577` in the actual recorded release (Helm revision 2); `values-eks.yaml` tracks that verified promotion. If a later image SHA is deployed, first verify its real green CI scan/push and record the exact new reference. Do not silently use `latest`.

Traefik handles standard Kubernetes Ingress routes `/` and `/api`. The legacy EKS Service controller creates a Classic ELB for its LoadBalancer Service; no AWS Load Balancer Controller IAM deployment is needed for this demo. The LB accepts HTTP/80 only from the admin CIDR. Database, backend, monitoring and Traefik dashboard are not separately public. This is a classroom HTTP demo, not a public production service.

## 4. Verify real functionality

```bash
kubectl --context relaydesk-sydney -n relaydesk get pods,deploy,svc,pvc,hpa,ingress -o wide
kubectl --context relaydesk-sydney -n ingress-system get svc traefik
kubectl --context relaydesk-sydney -n relaydesk get endpointslices
kubectl --context relaydesk-sydney -n relaydesk rollout status deploy/relaydesk-backend --timeout=180s
kubectl --context relaydesk-sydney -n relaydesk rollout status deploy/relaydesk-frontend --timeout=180s
kubectl --context relaydesk-sydney -n relaydesk logs deploy/relaydesk-backend --tail=40
kubectl --context relaydesk-sydney -n relaydesk logs deploy/relaydesk-backend -c database-migrations --tail=30
kubectl --context relaydesk-sydney top nodes
helm --kube-context relaydesk-sydney list -n relaydesk
```

Use the actual ELB hostname in `BASE_URL=http://HOSTNAME python scripts/smoke.py`. This verifies actual create/list/get/update/status/priority/delete through ingress; take a browser screenshot of the same hostname. Forward backend port 8000 to check `/health`, `/ready`, and `/metrics` directly. `/metrics` on the public frontend route is not the backend metrics endpoint.

Verify PostgreSQL's PVC is Bound and record its real PV/volume ID and selected AZ. Inspect migration logs if API Pods are stuck in Init. `PGDATA` uses a subdirectory on EBS so the filesystem's `lost+found` does not prevent `initdb`. Record HPA CPU numbers; `<unknown>` does not count as valid metrics.

## 5. Deploy and verify monitoring

```bash
kubectl --context relaydesk-sydney apply -f evidence/private/grafana-admin.json
kubectl --context relaydesk-sydney apply -k monitoring
kubectl --context relaydesk-sydney -n relaydesk rollout status deploy/prometheus --timeout=180s
kubectl --context relaydesk-sydney -n relaydesk rollout status deploy/grafana --timeout=180s
kubectl --context relaydesk-sydney -n relaydesk port-forward svc/prometheus 9091:9090
# Separate terminal:
kubectl --context relaydesk-sydney -n relaydesk port-forward svc/grafana 3002:3000
```

Use distinct local ports from the existing Minikube forwards. Generate actual API traffic; verify Prometheus Targets UP and query `up{job="relaydesk-backend"}` and `rate(relaydesk_http_requests_total[5m])`. Log in to Grafana locally using the private generated admin secret (never copy it into evidence) and capture the populated dashboard. The Kustomize variant disables anonymous login and replaces the public local-demo password with a Secret reference.

## 6. Required evidence before cleanup

- Apply completion and plan-audit output; real resource IDs, account and region.
- AWS Console VPC, two public subnets, EKS cluster and managed nodes in Sydney.
- Running/Ready Pods, replica counts, ClusterIP Services/endpoints, Bound PVC, Helm list, valid HPA.
- Application at the real ELB hostname, CRUD/health/readiness responses and migration logs.
- Backend metrics, Prometheus UP target, populated Grafana panel.
- Record a meaningful commit → successful CI → immutable images → Helm rollout → HTTP verification demo. Student explanation/presentation and teacher form submission remain owner actions.

## 7. Separate cleanup approval required

Do not delete anything while awaiting demonstration or evidence. After approval, first remove the application/monitoring and Traefik releases, then explicitly remove the project's PostgreSQL PVC and wait for its gp3 volume to be deleted while the CSI controller is still running. Removing a Helm release alone can retain a PVC; deleting it erases ticket data. Wait for the Kubernetes-created Classic ELB and its security group to disappear before destroying the VPC.

Only then generate/review a Terraform destroy plan with the same credential adapter, account and region, and perform the approved destroy. Save the actual completion output and screenshot. Independently verify no project cluster/node group, VPC/NAT/EIP/ELB or recorded EBS volumes remain. Keep final sensitive state privately, never in Git. Do not broadly delete resources by name or touch unrelated infrastructure. No cleanup success is claimed until these checks actually pass.
