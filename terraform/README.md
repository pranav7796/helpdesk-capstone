# Terraform AWS deployment

Target: account **525426877661**, profile **devops-new**, Sydney **ap-southeast-2**. The provider rejects other accounts. EKS admin access is restricted by `cluster_admin_cidr`; the reviewed plan uses `202.131.146.146/32`.

From the repository root:

```bash
bash scripts/terraform-readonly.sh init -input=false -lockfile=readonly
bash scripts/terraform-readonly.sh fmt -check -recursive
bash scripts/terraform-readonly.sh validate
bash scripts/terraform-readonly.sh plan -input=false -var=cluster_admin_cidr=202.131.146.146/32 -out=tfplan-reviewed
python scripts/audit-plan.py
```

The credential-process adapter reuses the AWS CLI login; it contains no credentials. Renew an expired session with `aws login --profile devops-new --region ap-southeast-2`. The original `tfplan` is preserved for audit but lacks the later account/storage/metrics safeguards. Do not apply it.

The reviewed plan creates 28 Terraform resources, including VPC/networking, EKS, two private managed workers, EBS CSI with Pod Identity, and Metrics Server. Application Helm deployment also needs the gp3 StorageClass and an ingress controller. Kubernetes creates a chargeable ingress ELB and a 2-GiB EBS volume separately from this plan.

**Approved apply completed October 16: 28 resources added, no changes or deletions.** See [actual apply evidence](../evidence/sydney/terraform-apply.txt) and [scope/costs](../docs/AWS-PLAN.md). Follow [the deployment and cleanup runbook](../docs/EKS-RUNBOOK.md). Destroy also needs separate approval.

State is local at `terraform/terraform.tfstate`; state, plan files and real tfvars remain ignored. No shared/remote state backend is needed by this assignment; keep a private state backup for reliable cleanup.
