# Running AWS project cost tracking

Approved deployment began October 16, 2026, approximately 17:28 UTC (22:58 IST). Apply completed successfully: 28 additions. Two t3.medium workers, standard-support EKS 1.35, one NAT/EIP, one Classic ELB and three gp3 volumes are running. Actual data/root volumes: 2 + 20 + 20 = 42 GiB.

Official Sydney rates captured before apply: EKS $0.10/h; workers $0.0528/h each; NAT $0.059/h + $0.059/GB; Classic ELB $0.028/h + $0.008/GB; public IPv4 $0.005/address/h; gp3 $0.096/GiB-month. With one NAT and estimated two ELB public IPv4 addresses, baseline is approximately **$0.31312/h** (730h storage conversion). The approved conservative budget was **$0.31444/h**, rounded to **$0.32/h**. ELB address count can vary; no fixed IP count or actual bill is claimed.

Conservative estimates: 3h $0.94; 24h $7.55; 72h $22.64; 730h $229.54, before variable usage/tax. Component lifetimes differ. Additional potential charges include NAT/ELB processing, data transfer/inter-AZ traffic, T3 surplus CPU, logs, EBS extras and taxes. Credit coverage/expiry/Organizations sharing remain unverified; API reported PAID/ACTIVE and $120 credits. The Console project menu separately displayed a $20 monthly spend-limit label; its scope/enforcement/current spend were not verified and it is not treated as a hard cap. No billing settings were changed or billable Cost Explorer queries used.

Resource IDs and state/cleanup order: [cleanup review](../../docs/CLEANUP-REVIEW.md). State `terraform/terraform.tfstate` and private backup, passwords and isolated kubeconfig are ignored. **Cleanup is not approved.** Resources remain available for the demonstration and accrue costs until deleted with separate owner approval. Budget alerts do not cap spending.
