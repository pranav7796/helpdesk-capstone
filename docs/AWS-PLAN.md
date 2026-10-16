# AWS plan and service eligibility

## Terraform plan scope

[`evidence/terraform-plan-refresh-false.txt`](../evidence/terraform-plan-refresh-false.txt) is a saved local dry-run plan created with `-refresh=false`. It reports 22 resources to add: one VPC; two public and two private subnets across two Availability Zones; an Internet Gateway, a single NAT Gateway and Elastic IP, public/private route tables and associations; EKS control-plane and node IAM roles/policy attachments; one EKS cluster; and one managed node group configured for two `t3.medium` workers. The EKS API CIDR used for the dry run is the documentation-only `203.0.113.9/32`; set your actual public egress IP before a real plan.

This does not confirm the account can create these resources. A normal refreshed plan failed because the account is not opted into EC2 in `ap-south-1`, while the EKS version availability check returned `SubscriptionRequiredException`. No Terraform apply was run and no project AWS infrastructure exists.

## Indicative running cost

AWS lists an EKS cluster fee of **$0.10 per hour** for Kubernetes versions in standard support. Worker instances, EBS, NAT Gateway, public IPs, data transfer, and logs are billed separately. [EKS pricing](https://aws.amazon.com/eks/pricing/)

For a short demo, use **about $0.30 per hour** as an order-of-magnitude baseline for one standard-support EKS control plane, two Linux `t3.medium` workers in Mumbai (about $0.0448 each per hour using current price listings), one NAT Gateway, and two small worker volumes. That is roughly **$3 for 10 hours** or **$7.20 for 24 hours**, before NAT data processing, internet egress, cross-AZ traffic, EBS variation, public IPv4, load balancers, CloudWatch logs, and tax. This is not a quote or a bill ceiling. AWS prices the NAT Gateway per active hour and per GB, plus data transfer. [VPC pricing](https://aws.amazon.com/vpc/pricing/), [EC2 On-Demand pricing](https://aws.amazon.com/ec2/pricing/on-demand/)

At the same baseline, uninterrupted month-long use is roughly **$219/month before variable charges**. AWS credits may offset eligible line items but are not an eligibility guarantee or a hard spending limit. Check AWS Pricing Calculator and billing eligibility before any apply.

## Current account result

The read-only account checks found AWS account plan `FREE`, status `NOT_STARTED`. EKS returned `SubscriptionRequiredException` and EC2/AZ discovery returned `OptInRequired` with the message that the account is not subscribed to the service. Do not apply this plan while that restriction remains. Account plan, billing, security, and service subscriptions were not changed.

If AWS eligibility changes, the Terraform plan must first be refreshed using the actual admin CIDR and reviewed again. The current saved plan is deliberately not an approval artifact. Any AWS apply or cleanup requires a new cost and exact-resource review; no resources should be removed until the demo evidence is captured.
