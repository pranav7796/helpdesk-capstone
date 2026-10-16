# Sydney AWS deployment review — approval required

Current target: **525426877661 / devops-new / ap-southeast-2**. Deadline: **October 19, 2026**. No Terraform apply or cloud mutation has been performed by the agent.

## Account and eligibility actually checked

- STS authenticates as `AccountFullAccessRole` in the intended account, not the old account's root identity. [Captured identity](../evidence/sydney/aws-identity.json).
- Sydney Availability Zones a/b/c are available; EKS ListClusters succeeds and currently returns no clusters. No VPC with project tag `relaydesk-capstone` exists. [Zones](../evidence/sydney/aws-zones.json), [clusters](../evidence/sydney/aws-clusters.json), [VPCs](../evidence/sydney/aws-project-vpcs.json).
- EKS 1.35 is in STANDARD_SUPPORT through March 27, 2027. [API response](../evidence/sydney/aws-version.json).
- The account-plan API reports **PAID / ACTIVE and 120 USD remaining credits**. [Credit response](../evidence/sydney/aws-credits.json). This is the new account's reported balance; it is not the earlier account's balance.
- Mumbai is excluded from the deployment because the owner reports an Organizations SCP there. Sydney reads and planning succeed; neither proves that all create/IAM actions are allowed by SCPs. No policy, billing, or organization settings were changed.
- One parallel token-refresh request was throttled; serializing the CLI checks resolved it. The audit helper now serializes access to the shared login cache.

## Saved plan verification

The supplied `terraform/tfplan` was decoded and preserved. Its SHA-256 is `5f7c1d1d90e2da4f453c7c1cf6d2ded8f6c73257486ad6d6a651b6c8b35a0412`. It matches the original four `.tf` files, Sydney region, and `202.131.146.146/32` admin CIDR, with 22 additions. It lacked an account guard and EKS storage/metrics prerequisites. [Original plan output](../evidence/terraform-sydney-original-plan.txt).

**Use the new reviewed plan, not the original:** `terraform/tfplan-reviewed`. The provider explicitly selects `devops-new` and allows only account `525426877661`. Every current `.tf` file matches the new plan snapshot. [Machine checks and plan SHA-256](../evidence/sydney/plan-audit.json), [complete plan](../evidence/sydney/terraform-plan.txt).

The reviewed plan is **28 additions, 0 changes, 0 destructions**:

| Resource | Count and exact project scope |
|---|---|
| VPC | 1: `relaydesk-capstone-vpc`, `10.42.0.0/16` |
| Subnets | 2 public (`10.42.100.0/24`, `10.42.101.0/24`) and 2 private (`10.42.1.0/24`, `10.42.2.0/24`), Sydney a/b |
| Routing | 1 Internet Gateway, 1 NAT Gateway, 1 Elastic IP, 2 route tables, 4 associations |
| IAM | 3 project roles (cluster, nodes, EBS CSI), 5 AWS-policy attachments; no IAM users or keys |
| EKS | `relaydesk-capstone`, version 1.35; private API enabled, public API restricted to `202.131.146.146/32` |
| Managed workers | `relaydesk-capstone-workers`, 2 On-Demand Linux `t3.medium`, min/max 2, 20-GiB root disks each |
| Storage/metrics | 1 Pod Identity association and 3 pinned add-ons: Pod Identity Agent, EBS CSI, Metrics Server |

AWS-managed supporting security groups, network interfaces, node instances/ASG, root volumes, and any required service-linked roles are implicit EKS/node-group dependencies; the Terraform count is not a count of every underlying AWS object.

After infrastructure approval, Kubernetes deployment additionally creates **one Classic ELB** for Traefik and **one encrypted 2-GiB gp3 EBS PostgreSQL volume**, outside Terraform's resource count. Ingress accepts HTTP/80 from `202.131.146.146/32` only. Backend/frontend remain ClusterIP; Grafana and Prometheus remain private and are accessed by local port-forward. No RDS, Route53, paid TLS certificate, extra NAT, or EKS Auto Mode is planned.

## Prices and expected charges (USD, before credits/tax)

Rates were retrieved from the official **AWS Price List API** on October 16, 2026. [Compact rates with SKU/effective dates](../evidence/sydney/aws-price-summary.json). Original API responses and exact query arguments are alongside that file.

| Component | Quantity | Rate | Estimated hourly amount |
|---|---:|---:|---:|
| EKS standard-support control plane | 1 | $0.10/hour | $0.1000 |
| EC2 Linux t3.medium | 2 | $0.0528/instance-hour | $0.1056 |
| Single zonal NAT Gateway | 1 | $0.059/hour | $0.0590 |
| NAT public IPv4 | 1 | $0.005/address-hour | $0.0050 |
| Worker root EBS | 40 GiB | budget at gp2 $0.12/GiB-month | $0.00658 |
| PostgreSQL EBS gp3 | 2 GiB | $0.096/GiB-month | $0.00026 |
| Classic Load Balancer | 1 | $0.028/hour or partial hour | $0.0280 |
| Load balancer public IPv4 estimate | 2 | $0.005/address-hour | $0.0100 |
| **Baseline with ingress** | | | **$0.31444/hour (budget $0.32/hour)** |

Storage conversion uses 730 hours/month only for estimation. Root disks use the AWS-managed node-group volume type; the table conservatively budgets gp2 (gp3 is cheaper). The actual number of load balancer public addresses can vary and must be measured after deployment. NAT and ELB can bill partial hours as complete hours. Pre-ingress baseline is approximately $0.27644/hour including the planned application disk.

| Runtime | Baseline estimate |
|---|---:|
| 3 hours | $0.94 |
| 10 hours | $3.14 |
| 24 hours | $7.55 |
| 72 hours | $22.64 |
| 730 hours | $229.54 |

**Variable extras:** NAT processes data at $0.059/GB; Classic ELB processes data at $0.008/GB. Cross-AZ traffic (including the second private subnet using the single NAT), internet egress, T3 Unlimited surplus CPU, extra IPv4 addresses/storage, snapshots, optional logs and tax can increase the total. No cost ceiling is implied. Existing account charges are outside this project estimate. EKS extended-support pricing is excluded because 1.35 is currently in standard support; monitor its lifecycle if keeping the cluster.

**Credits:** The API balance does not expose grant restrictions, expiry, service eligibility, or Organizations sharing rules. Those remain unverified. The account owner should inspect Billing → Credits in this new account (and, if managed centrally, ask the payer/organization owner). Credits do not guarantee that EKS, NAT, ELB or every tax/fee is covered. See [AWS credit application rules](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/useconsolidatedbilling-credits.html). Budget alerts are not spending limits.

## Authentication and approval boundary

The helper uses the existing console session through [AWS's credential-process workaround](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html). It stores no keys in the project and rejects apply/destroy.

```bash
# Only if the existing session expires:
aws login --profile devops-new --region ap-southeast-2
# Safe checks:
bash scripts/terraform-readonly.sh validate
python scripts/audit-plan.py
```

Before an approved apply, recheck identity, current public IP/CIDR, source snapshot and plan hash. Do not modify a plan silently after approval. Any changed resource scope or cost model requires another review. Use the credential adapter environment when applying the reviewed plan; do not run the old plan. Local state will be at `terraform/terraform.tfstate` (ignored and sensitive); do not commit the plan, state, generated passwords, or debug credential logs.

Explicit approval must cover **the 28-resource reviewed Terraform plan plus the ingress ELB and 2-GiB application volume**, with the costs above. Cleanup needs separate approval after evidence/demo capture. [Deployment/verification/cleanup runbook](EKS-RUNBOOK.md).
