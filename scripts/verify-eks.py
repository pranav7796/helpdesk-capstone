"""Read-only cloud runtime/evidence checks; credentials are never printed."""
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/sydney"
ENV = {**os.environ, "KUBECONFIG": str(ROOT / "evidence/private/kubeconfig-sydney"), "AWS_PROFILE": "devops-new", "AWS_REGION": "ap-southeast-2"}
BASE = ["kubectl", "--context", "relaydesk-sydney"]


def command(args, file):
    result = subprocess.run(args, env=ENV, capture_output=True, text=True, timeout=120, check=True)
    (OUT / file).write_text(result.stdout)
    return result.stdout


def kube(args, file):
    if "--resume-infrastructure" in sys.argv and (OUT / file).exists():
        return json.loads((OUT / file).read_text())
    return json.loads(command([*BASE, *args, "-o", "json"], file))


def aws(args, file):
    if "--resume-infrastructure" in sys.argv and (OUT / file).exists():
        return json.loads((OUT / file).read_text())
    return json.loads(command(["aws", *args, "--profile", "devops-new", "--region", "ap-southeast-2", "--no-cli-pager"], file))


def get(url, headers=None):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=15) as response:
                return response.read().decode()
        except (urllib.error.URLError, ConnectionResetError, TimeoutError) as error:
            if isinstance(error, urllib.error.HTTPError) and error.code < 500:
                raise
            if attempt == 3:
                raise
            print(f"Transient GET failure {type(error).__name__}; retry {attempt + 1}/3: {url}", flush=True)
            time.sleep(2 ** attempt)


if __name__ == "__main__":
    if "--resume-infrastructure" in sys.argv:
        print("Reusing saved infrastructure API responses; HTTP, monitoring and final runtime/log checks execute live.", flush=True)
    identity = aws(["sts", "get-caller-identity"], "aws-identity-deployed.json")
    assert identity["Account"] == "525426877661"
    nodes = kube(["get", "nodes"], "eks-nodes.json")
    assert len(nodes["items"]) == 2
    assert all(any(c["type"] == "Ready" and c["status"] == "True" for c in n["status"]["conditions"]) for n in nodes["items"])
    pods = kube(["-n", "relaydesk", "get", "pods"], "eks-pods.json")
    assert len(pods["items"]) == 7
    assert all(p["status"]["phase"] == "Running" and all(c["ready"] for c in p["status"]["containerStatuses"]) for p in pods["items"])
    deploy = kube(["-n", "relaydesk", "get", "deploy"], "eks-deployments.json")
    assert all(d["status"].get("readyReplicas", 0) >= 2 for d in deploy["items"] if d["metadata"]["name"].startswith("relaydesk-"))
    kube(["-n", "relaydesk", "get", "services"], "eks-services.json")
    kube(["-n", "relaydesk", "get", "endpointslices"], "eks-endpoints.json")
    pvc = kube(["-n", "relaydesk", "get", "pvc", "relaydesk-postgres-data"], "eks-pvc.json")
    assert pvc["status"]["phase"] == "Bound"
    pv = kube(["get", "pv", pvc["spec"]["volumeName"]], "eks-pv.json")
    ids = [n["spec"]["providerID"].split("/")[-1] for n in nodes["items"]]
    instances = aws(["ec2", "describe-instances", "--instance-ids", *ids], "aws-workers-live.json")
    workers = [i for r in instances["Reservations"] for i in r["Instances"]]
    assert len(workers) == 2 and all(i["InstanceType"] == "t3.medium" for i in workers)
    volume_ids = [b["Ebs"]["VolumeId"] for i in workers for b in i["BlockDeviceMappings"]] + [pv["spec"]["csi"]["volumeHandle"]]
    volumes = aws(["ec2", "describe-volumes", "--volume-ids", *volume_ids], "aws-ebs-live.json")
    data_volume = next(v for v in volumes["Volumes"] if v["VolumeId"] == pv["spec"]["csi"]["volumeHandle"])
    assert data_volume["Size"] == 2 and data_volume["VolumeType"] == "gp3" and data_volume["Encrypted"]
    lb = kube(["-n", "ingress-system", "get", "svc", "traefik"], "eks-loadbalancer-service.json")
    hostname = lb["status"]["loadBalancer"]["ingress"][0]["hostname"]
    lb_name = hostname.split(".")[0].rsplit("-", 1)[0]
    aws(["elb", "describe-load-balancers", "--load-balancer-names", lb_name], "aws-elb-live.json")
    aws(["elb", "describe-instance-health", "--load-balancer-name", lb_name], "aws-elb-health.json")
    for name, path in (("health", "/health"), ("readiness", "/ready"), ("metrics", "/metrics")):
        body = get("http://127.0.0.1:8001" + path)
        (OUT / ("eks-application-metrics.txt" if name == "metrics" else "eks-" + name + ".txt")).write_text(body)
        if name == "metrics":
            assert "relaydesk_http_requests_total" in body
    for _ in range(20):
        get("http://" + hostname + "/api/tickets")
        time.sleep(1)
    query = "http://127.0.0.1:9091/api/v1/query?query="
    for attempt in range(12):
        up = json.loads(get(query + urllib.parse.quote('up{job="relaydesk-backend"}')))
        if up["data"]["result"] and up["data"]["result"][0]["value"][1] == "1":
            break
        time.sleep(5)
    else:
        raise RuntimeError("Prometheus target not UP")
    (OUT / "eks-prometheus-up.json").write_text(json.dumps(up, indent=2) + "\n")
    traffic = get(query + urllib.parse.quote('sum by(route)(rate(relaydesk_http_requests_total[5m]))'))
    (OUT / "eks-prometheus-traffic.json").write_text(traffic)
    password = json.loads((ROOT / "evidence/private/grafana-admin.json").read_text())["stringData"]["password"]
    auth = "Basic " + base64.b64encode(("admin:" + password).encode()).decode()
    dashboard = json.loads(get("http://127.0.0.1:3002/api/dashboards/uid/relaydesk-http", {"Authorization": auth}))
    assert dashboard["dashboard"]["panels"]
    (OUT / "eks-grafana-dashboard.json").write_text(json.dumps(dashboard, indent=2) + "\n")
    command([*BASE, "-n", "relaydesk", "get", "pods,deploy,svc,hpa,pvc,ingress", "-o", "wide"], "eks-runtime.txt")
    command([*BASE, "-n", "relaydesk", "logs", "deploy/relaydesk-backend", "--tail=25"], "eks-backend-logs.txt")
    command([*BASE, "-n", "relaydesk", "logs", "deploy/relaydesk-backend", "-c", "database-migrations", "--tail=25"], "eks-migration-logs.txt")
    summary = {"verified_at_utc": datetime.now(timezone.utc).isoformat(), "account": identity["Account"], "region": "ap-southeast-2", "application_url": "http://" + hostname, "workers": ids, "worker_count": 2, "ready_app_namespace_pods": 7, "data_volume": data_volume["VolumeId"], "load_balancer": lb_name, "checks": "Ready nodes/Pods, replicas, PVC, EC2 type, encrypted gp3 disk, real health/metrics, Prometheus UP, Grafana panel verified"}
    (OUT / "eks-verification-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
