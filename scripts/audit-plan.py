"""Verify the reviewed local plan's account guard, region, CIDR and source snapshot."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "terraform" / "tfplan-reviewed"
result = subprocess.run(["bash", str(ROOT / "scripts/terraform-readonly.sh"), "show", "-json", str(PLAN)],
                        check=True, capture_output=True, text=True)
plan = json.loads(result.stdout)
expressions = plan["configuration"]["provider_config"]["aws"]["expressions"]
variables = {k: v["value"] for k, v in plan["variables"].items()}
checks = {
    "account_guard": expressions["allowed_account_ids"]["constant_value"] == ["525426877661"],
    "profile": expressions["profile"]["constant_value"] == "devops-new",
    "region": variables["aws_region"] == "ap-southeast-2",
    "admin_cidr": variables["cluster_admin_cidr"] == "202.131.146.146/32",
    "only_creates": all(r["change"]["actions"] == ["create"] for r in plan["resource_changes"]),
    "resource_count": len(plan["resource_changes"]) == 28,
}
with zipfile.ZipFile(PLAN) as archive:
    for path in (ROOT / "terraform").glob("*.tf"):
        snapshot = "tfconfig/m-/" + path.name
        checks["source_matches_" + path.name] = snapshot in archive.namelist() and archive.read(snapshot) == path.read_bytes()
record = {
    "captured_at_utc": datetime.now(timezone.utc).isoformat(), "plan_timestamp": plan.get("timestamp"),
    "plan": "terraform/tfplan-reviewed", "sha256": hashlib.sha256(PLAN.read_bytes()).hexdigest(),
    "variables": variables, "checks": checks,
    "resources": [{"address": r["address"], "actions": r["change"]["actions"]} for r in plan["resource_changes"]],
    "notes": "Plan validation is read-only. No apply occurred. Account creation permissions/SCPs remain runtime checks.",
}
(ROOT / "evidence/sydney/plan-audit.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
if not all(checks.values()):
    raise SystemExit("FAIL: reviewed plan does not match the intended deployment")
