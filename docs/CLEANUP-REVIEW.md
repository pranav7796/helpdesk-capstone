# Sydney resource inventory and cleanup review

**Cleanup NOT approved or executed.** Deployment approval did not authorize deletion. Preserve the environment for the demonstration. Deleting the PostgreSQL PVC erases ticket data.

Account `525426877661`, profile `devops-new`, region `ap-southeast-2`. Local state: `terraform/terraform.tfstate`; private backup `evidence/private/terraform-state-post-apply.json`. Isolated kubeconfig: `evidence/private/kubeconfig-sydney`, context `relaydesk-sydney`. Do not publish these files.

| Resource | Actual identifier |
|---|---|
| VPC | `vpc-0f1334a144012db46` |
| EKS and managed group | `relaydesk-capstone`, `relaydesk-capstone-workers` |
| Workers | `i-0ae1eaa988c9eac8d`, `i-05ebd008f8142bee8` |
| NAT / EIP | `nat-01f3eac1072f1cadf`, `eipalloc-0a682ae835ce6b924` |
| Classic ELB (Kubernetes-created) | `af43a3e33d68945548232885350507ff` |
| PostgreSQL PVC / encrypted 2-GiB disk | `relaydesk/relaydesk-postgres-data`, `vol-05a891d9a7dce0955` |
| Worker root disks | `vol-059e7140240f20306`, `vol-0c2635d6fa9ef9ce2` |

## Required order after separate owner approval

1. Confirm demonstration/evidence complete and whether a private database backup is required. Recheck identity/account and actual resource inventory.
2. Monitoring is owned by Kustomize, not a Helm release: after approval remove only its resources with `kubectl --context relaydesk-sydney delete -k monitoring --ignore-not-found`. Then uninstall the `relaydesk` and `traefik` Helm releases in their own namespaces. The chart declares its data PVC directly, so uninstall may delete it; approve data erasure and take any required private backup first. Explicitly check/delete any remaining project PVC with `--ignore-not-found` while EBS CSI remains available. Wait for the recorded data EBS disk and Classic ELB/security group to disappear. Do not destroy CSI/VPC first.
3. Refresh/review the Terraform destroy plan after Kubernetes cleanup; use the credential adapter and correct account. The current read-only preview has **28 deletions**, no creates/changes; it was not executed. Preview: `evidence/sydney/terraform-destroy-plan.txt`, audit `cleanup-plan-audit.json`. Saved hash is a record of that preview, not authorization to bypass a later review.
4. Execute only the approved destroy, save genuine output/screenshot, then independently verify the project EKS, workers, NAT, EIP, VPC, ELB and all recorded volumes are gone. Capture actual destroy completion for the remaining two M7 marks.

Do not touch unrelated default VPC `vpc-042b78e34824a4dfb`, billing, account security, or other projects. The monitoring-only headless Service `relaydesk-backend-metrics` is covered by the Kustomize cleanup and has no separate AWS bill. Current running budget approximately $0.32/hour before variable charges/tax; see the cost ledger.

## Exact Terraform addresses in the current read-only preview

- `aws_eip.nat`
- `aws_eks_addon.ebs_csi`
- `aws_eks_addon.metrics_server`
- `aws_eks_addon.pod_identity`
- `aws_eks_cluster.this`
- `aws_eks_node_group.this`
- `aws_eks_pod_identity_association.ebs_csi`
- `aws_iam_role.cluster`
- `aws_iam_role.ebs_csi`
- `aws_iam_role.nodes`
- `aws_iam_role_policy_attachment.cluster`
- `aws_iam_role_policy_attachment.ebs_csi`
- `aws_iam_role_policy_attachment.nodes["AmazonEC2ContainerRegistryPullOnly"]`
- `aws_iam_role_policy_attachment.nodes["AmazonEKSWorkerNodePolicy"]`
- `aws_iam_role_policy_attachment.nodes["AmazonEKS_CNI_Policy"]`
- `aws_internet_gateway.this`
- `aws_nat_gateway.this`
- `aws_route_table.private`
- `aws_route_table.public`
- `aws_route_table_association.private["ap-southeast-2a"]`
- `aws_route_table_association.private["ap-southeast-2b"]`
- `aws_route_table_association.public["ap-southeast-2a"]`
- `aws_route_table_association.public["ap-southeast-2b"]`
- `aws_subnet.private["ap-southeast-2a"]`
- `aws_subnet.private["ap-southeast-2b"]`
- `aws_subnet.public["ap-southeast-2a"]`
- `aws_subnet.public["ap-southeast-2b"]`
- `aws_vpc.this`
