"""Read-only AWS account/service and public-price evidence. Never prints credentials."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "sydney"
OUT.mkdir(parents=True, exist_ok=True)
PROFILE, REGION = "devops-new", "ap-southeast-2"


def invoke(name, args, region=REGION):
    command = ["aws", *args, "--profile", PROFILE, "--region", region, "--no-cli-pager"]
    result = subprocess.run(command, capture_output=True, text=True, timeout=100)
    record = {"command": command, "captured_at_utc": datetime.now(timezone.utc).isoformat(),
              "exit_code": result.returncode, "stderr": result.stderr.strip()}
    if result.returncode == 0:
        record["response"] = json.loads(result.stdout)
    (OUT / f"aws-{name}.json").write_text(json.dumps(record, indent=2) + "\n")
    print(name, "PASS" if result.returncode == 0 else f"BLOCKED ({record['stderr']})", flush=True)
    return record


def price(name, service, filters):
    args = ["pricing", "get-products", "--service-code", service, "--filters"]
    args += [f"Type=TERM_MATCH,Field={key},Value={value}" for key, value in filters.items()]
    record = invoke("price-" + name, args, "us-east-1")
    rows = []
    for raw in record.get("response", {}).get("PriceList", []):
        product = json.loads(raw)
        for term in product["terms"].get("OnDemand", {}).values():
            for dimension in term["priceDimensions"].values():
                rows.append({"sku": product["product"]["sku"],
                             "usage_type": product["product"]["attributes"].get("usagetype"),
                             "effective_date": term["effectiveDate"], **dimension})
    return name, rows


if __name__ == "__main__":
    checks = {
        "identity": ["sts", "get-caller-identity"],
        "zones": ["ec2", "describe-availability-zones"],
        "clusters": ["eks", "list-clusters"],
        "project-vpcs": ["ec2", "describe-vpcs", "--filters", "Name=tag:Project,Values=relaydesk-capstone"],
        "version": ["eks", "describe-cluster-versions", "--cluster-versions", "1.35"],
        "credits": ["freetier", "get-account-plan-state"],
    }
    # These processes share a refreshable CLI login cache; serialize to avoid
    # concurrent token-refresh requests and OAuth throttling.
    for item in checks.items():
        invoke(*item)
    location = {"location": "Asia Pacific (Sydney)"}
    queries = [
        ("worker", "AmazonEC2", {**location, "instanceType": "t3.medium", "operatingSystem": "Linux", "tenancy": "Shared", "preInstalledSw": "NA", "capacitystatus": "Used"}),
        ("nat", "AmazonEC2", {**location, "productFamily": "NAT Gateway"}),
        ("gp3", "AmazonEC2", {**location, "volumeApiName": "gp3", "productFamily": "Storage"}),
        ("gp2", "AmazonEC2", {**location, "volumeApiName": "gp2", "productFamily": "Storage"}),
        ("ipv4", "AmazonVPC", {**location, "usagetype": "APS2-PublicIPv4:InUseAddress"}),
        ("clb", "AWSELB", {**location, "productFamily": "Load Balancer"}),
        ("eks", "AmazonEKS", {**location, "usagetype": "APS2-AmazonEKS-Hours:perCluster"}),
    ]
    summary = dict(price(*args) for args in queries)
    (OUT / "aws-price-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    for name, rows in summary.items():
        print(name, [(row["usage_type"], row["pricePerUnit"]["USD"], row["unit"]) for row in rows])
