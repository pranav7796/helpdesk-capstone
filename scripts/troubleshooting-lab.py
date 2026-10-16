"""Demonstrate and recover five failures in a new local namespace only."""
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/sydney/troubleshooting.txt"
CONTEXT, NS = "helpdesk-capstone", "relaydesk-lab"
IMAGE = "ghcr.io/pranav7796/helpdesk-capstone/backend:d07bca6accc35f0224aaae8c4057076a9c4c9261"
BASE = ["kubectl", "--context", CONTEXT, "-n", NS]
LOG = []


def run(*args, data=None, check=True):
    # Input documents are omitted from logs; no credential values are printed.
    result = subprocess.run([*BASE, *args], input=json.dumps(data) if data else None,
                            text=True, capture_output=True, timeout=150)
    entry = "$ kubectl --context " + CONTEXT + " -n " + NS + " " + " ".join(args) + "\n" + result.stdout + result.stderr
    LOG.append(entry)
    OUT.write_text("\n".join(LOG))
    print(entry, flush=True)
    if check and result.returncode:
        raise RuntimeError("kubectl failed: " + " ".join(args))
    return result


def deploy(name, command, probe=None, env=None, image=IMAGE):
    container = {"name": "backend", "image": image, "imagePullPolicy": "IfNotPresent", "command": command,
                 "resources": {"requests": {"cpu": "10m", "memory": "32Mi"}, "limits": {"cpu": "300m", "memory": "192Mi"}}}
    if probe:
        container["readinessProbe"] = {"httpGet": {"path": probe, "port": 8000}, "periodSeconds": 2, "initialDelaySeconds": 2}
    if env:
        container["env"] = [{"name": "DATABASE_URL", "value": env}]
    return {"apiVersion": "apps/v1", "kind": "Deployment", "metadata": {"name": name, "namespace": NS},
            "spec": {"replicas": 1, "selector": {"matchLabels": {"app": name}},
                     "template": {"metadata": {"labels": {"app": name}}, "spec": {"containers": [container]}}}}


def wait_for(predicate, description, seconds=110):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        pods = json.loads(subprocess.check_output([*BASE, "get", "pods", "-o", "json"], text=True))
        if predicate(pods["items"]):
            LOG.append("VERIFIED: " + description)
            print(LOG[-1], flush=True)
            return
        time.sleep(3)
    raise RuntimeError("Timed out: " + description)


def containers(pods, name):
    return [c for p in pods if p["metadata"]["labels"].get("app") == name for c in p["status"].get("containerStatuses", [])]


if __name__ == "__main__":
    # Refuse to touch a pre-existing namespace, even if it has the same name.
    exists = subprocess.run([*BASE, "get", "namespace", NS], capture_output=True).returncode == 0
    if exists:
        raise SystemExit("Refusing to modify a pre-existing lab namespace")
    run("create", "namespace", NS)
    try:
        good = ["python", "-m", "http.server", "8000"]
        uvicorn = ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
        for document in (
            deploy("healthy", good, "/"),
            deploy("crash", ["sh", "-c", "echo 'Intentional capstone lab crash'; sleep 1; exit 1"]),
            deploy("readiness", good, "/intentionally-missing"),
            deploy("database", uvicorn, "/ready", "postgresql+psycopg://invalid:invalid@127.0.0.1:1/invalid?connect_timeout=2"),
        ):
            run("apply", "-f", "-", data=document)
        for name in ("broken-image", "broken-service"):
            run("apply", "-f", str(ROOT / "troubleshooting" / (name + ".yaml")))
        run("rollout", "status", "deploy/healthy", "--timeout=90s")
        run("get", "pods", "-o", "wide")
        run("describe", "deploy/crash")
        wait_for(lambda p: any(c.get("restartCount", 0) >= 2 and (
            c.get("state", {}).get("waiting", {}).get("reason") == "CrashLoopBackOff" or
            c.get("lastState", {}).get("terminated", {}).get("exitCode") == 1
        ) for c in containers(p, "crash")), "Repeated exit-1 crashes observed (crash loop)")
        wait_for(lambda p: any(c.get("state", {}).get("waiting", {}).get("reason") == "ImagePullBackOff" for c in containers(p, "broken-image")), "ImagePullBackOff observed")
        wait_for(lambda p: any(c.get("state", {}).get("running") is not None and not c["ready"] for c in containers(p, "readiness")), "Running but unready probe-failure pod observed")
        run("get", "pods", "-o", "wide")
        run("get", "events", "--sort-by=.lastTimestamp")
        events = json.loads(run("get", "events", "-o", "json").stdout)
        assert any(e.get("reason") == "BackOff" and e.get("involvedObject", {}).get("name", "").startswith("crash-") for e in events["items"]), "Expected kubelet BackOff event for crash loop"
        run("logs", "deploy/crash", "--previous", check=False)
        run("logs", "deploy/database", "--tail=15")
        endpoints = json.loads(run("get", "endpointslices", "-l", "kubernetes.io/service-name=broken-service", "-o", "json").stdout)
        assert not any(item.get("endpoints") for item in endpoints["items"])
        LOG.append("VERIFIED: incorrect selector produces no endpoints")
        # Actual HTTP failures from another Pod, avoiding external port forwards.
        for name, path, expected in (("readiness", "/intentionally-missing", 404), ("database", "/ready", 503)):
            pods = json.loads(run("get", "pods", "-l", "app=" + name, "-o", "json").stdout)
            ip = pods["items"][0]["status"]["podIP"]
            code = "\n".join([
                "import urllib.request,urllib.error,time",
                "for attempt in range(60):",
                " try:",
                "  status=urllib.request.urlopen('http://" + ip + ":8000" + path + "',timeout=5).status",
                " except urllib.error.HTTPError as e: status=e.code",
                " except urllib.error.URLError: time.sleep(2);continue",
                f" assert status == {expected}, status",
                " print(status);break",
                "else: raise RuntimeError('HTTP server did not start')",
            ])
            assert str(expected) in run("exec", "deploy/healthy", "--", "python", "-c", code).stdout
            LOG.append(f"VERIFIED: {name} returns HTTP {expected}")
        for name in ("crash", "readiness", "broken-image"):
            run("apply", "-f", "-", data=deploy(name, good, "/"))
        # Read-only readiness checks against the existing local demo database.
        run("apply", "-f", "-", data=deploy("database", uvicorn, "/ready",
            "postgresql+psycopg://relaydesk:relaydesk-local-only@relaydesk-postgres.relaydesk.svc.cluster.local:5432/relaydesk"))
        run("patch", "svc/broken-service", "--type=merge", "-p", '{"spec":{"selector":{"app":"healthy"}}}')
        for name in ("crash", "readiness", "broken-image", "database"):
            run("rollout", "status", "deploy/" + name, "--timeout=120s")
        endpoints = json.loads(run("get", "endpointslices", "-l", "kubernetes.io/service-name=broken-service", "-o", "json").stdout)
        assert any(item.get("endpoints") for item in endpoints["items"])
        run("exec", "deploy/healthy", "--", "python", "-c", "import urllib.request;print(urllib.request.urlopen('http://broken-service:8000').status)")
        run("get", "pods", "-o", "wide")
        LOG.append("PASS: all five intentional failures diagnosed and recovered")
    except Exception:
        run("get", "pods", "-o", "wide", check=False)
        run("get", "pods", "-l", "app=crash", "-o", "json", check=False)
        run("get", "events", "--sort-by=.lastTimestamp", check=False)
        raise
    finally:
        # Cleanup only this script's newly created disposable local lab resources.
        run("delete", "namespace", NS, "--wait=true", "--timeout=90s")
        OUT.write_text("\n".join(LOG) + "\n")
