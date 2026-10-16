"""Calculate a transparent estimate from the captured AWS Price List response."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rates = json.loads((ROOT / "evidence/sydney/aws-price-summary.json").read_text())


def rate(group, usage):
    return next(float(r["pricePerUnit"]["USD"]) for r in rates[group] if r["usage_type"] == usage)


items = {
    "EKS standard support x1": rate("eks", "APS2-AmazonEKS-Hours:perCluster"),
    "t3.medium Linux workers x2": 2 * rate("worker", "APS2-BoxUsage:t3.medium"),
    "NAT gateway x1": rate("nat", "APS2-NatGateway-Hours"),
    "NAT public IPv4 x1": rate("ipv4", "APS2-PublicIPv4:InUseAddress"),
    "40 GiB root disks (budget gp2)": 40 * rate("gp2", "APS2-EBS:VolumeUsage.gp2") / 730,
    "2 GiB PostgreSQL gp3 disk": 2 * rate("gp3", "APS2-EBS:VolumeUsage.gp3") / 730,
    "Classic ELB x1": rate("clb", "APS2-LoadBalancerUsage"),
    "ELB public IPv4 estimate x2": 2 * rate("ipv4", "APS2-PublicIPv4:InUseAddress"),
}
print("SYDNEY ESTIMATE, USD BEFORE CREDITS/TAX — NO RESOURCES PROVISIONED")
print("Source: evidence/sydney/aws-price-summary.json (official AWS Price List API)")
for name, value in items.items():
    print(f"{name:40} ${value:.6f}/hour")
total = sum(items.values())
print(f"BASELINE: ${total:.6f}/hour; budget $0.32/hour plus variable charges")
for hours in (3, 10, 24, 72, 730):
    print(f"{hours:3} hours: ${total * hours:.2f}")
print("Extra: NAT $0.059/GB; ELB $0.008/GB; egress, cross-AZ, CPU surplus, tax.")
print("Credits reported by account API: $120; grant applicability is UNVERIFIED.")
print("IPv4 count may vary; storage conversion assumes 730 hours/month.")
