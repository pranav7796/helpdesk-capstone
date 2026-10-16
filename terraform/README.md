# Terraform AWS deployment

This directory declares an isolated VPC, two public and two private subnets across two Availability Zones, a single NAT Gateway, an EKS control plane, and two managed `t3.medium` workers. Every resource is named and tagged `relaydesk-capstone`.

The public EKS API accepts requests from only `cluster_admin_cidr` (`/32`). Set it to your trusted public IPv4 address in the ignored `terraform.tfvars` file. The example address is documentation-only.

Commands: `terraform init`, `terraform fmt -check`, `terraform validate`, and `terraform plan -var-file=terraform.tfvars`. These do not provision resources. Never run apply without reviewing the current plan, actual price, account eligibility, and explicit owner approval.

Plan access on this account currently returns AWS `OptInRequired` for EC2 and `SubscriptionRequiredException` for EKS in `ap-south-1`. Keep cloud deployment blocked until the account owner resolves eligibility; do not change account or billing settings.

The remote state is not configured yet. A local Terraform state file is sensitive and remains ignored by Git. Approved cleanup: `terraform destroy -var-file=terraform.tfvars`, followed by independent checks that EKS, NAT, EIP, and VPC resources tagged for Relaydesk are gone.
