#!/usr/bin/env bash
# Executes the owner's approved project deployment, not Terraform provisioning.
set -euo pipefail
umask 077
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_dir"
export AWS_PROFILE=devops-new
export AWS_REGION=ap-southeast-2
export KUBECONFIG="$project_dir/evidence/private/kubeconfig-sydney"
test -f evidence/private/eks-values.json
test -f evidence/private/grafana-admin.json
account=$(aws sts get-caller-identity --profile devops-new --region ap-southeast-2 --query Account --output text)
test "$account" = 525426877661
status=$(aws eks describe-cluster --profile devops-new --region ap-southeast-2 --name relaydesk-capstone --query cluster.status --output text)
test "$status" = ACTIVE
for addon in eks-pod-identity-agent aws-ebs-csi-driver metrics-server; do
  status=$(aws eks describe-addon --profile devops-new --region ap-southeast-2 --cluster-name relaydesk-capstone --addon-name "$addon" --query addon.status --output text)
  test "$status" = ACTIVE
done
aws eks update-kubeconfig --profile devops-new --region ap-southeast-2 --name relaydesk-capstone --alias relaydesk-sydney
kubectl --context relaydesk-sydney wait nodes --all --for=condition=Ready --timeout=300s
kubectl --context relaydesk-sydney apply -f k8s/namespace.yaml
kubectl --context relaydesk-sydney apply -f k8s/storage-eks.yaml
helm upgrade --install relaydesk helm/helpdesk --kube-context relaydesk-sydney \
  -n relaydesk --create-namespace -f helm/helpdesk/values-eks.yaml \
  -f evidence/private/eks-values.json --wait --timeout 10m
helm upgrade --install traefik traefik --repo https://traefik.github.io/charts \
  --version 42.0.0 --kube-context relaydesk-sydney -n ingress-system --create-namespace \
  -f k8s/traefik-values-eks.yaml --wait --timeout 10m
kubectl --context relaydesk-sydney apply -f evidence/private/grafana-admin.json
kubectl --context relaydesk-sydney apply -k monitoring
kubectl --context relaydesk-sydney -n relaydesk rollout status deploy/prometheus --timeout=300s
kubectl --context relaydesk-sydney -n relaydesk rollout status deploy/grafana --timeout=300s
kubectl --context relaydesk-sydney -n relaydesk get pods,deploy,svc,hpa,pvc,ingress -o wide
helm --kube-context relaydesk-sydney list -n relaydesk
