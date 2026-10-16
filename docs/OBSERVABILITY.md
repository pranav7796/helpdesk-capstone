# Local observability stack

`local-stack.yaml` installs a Prometheus Deployment and Service with an explicit scrape job for `relaydesk-backend.relaydesk.svc.cluster.local:8000/metrics`. Grafana provisions that Prometheus datasource and loads the Relaydesk HTTP dashboard from a ConfigMap.

```sh
kubectl -n relaydesk create configmap grafana-dashboard \
  --from-file=relaydesk-dashboard.json=monitoring/relaydesk-dashboard.json \
  --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f monitoring/local-stack.yaml
kubectl -n relaydesk rollout status deploy/prometheus --timeout=120s
kubectl -n relaydesk rollout status deploy/grafana --timeout=120s
kubectl -n relaydesk port-forward svc/grafana 3001:3000
```

Open <http://localhost:3001> and sign in as `admin` with the local demo password `relaydesk-demo-only`. Generate requests against the application. In Prometheus, check **Status → Targets** and query `up{job="relaydesk-backend"}`; it should be `1`. In Grafana, open the Relaydesk HTTP traffic dashboard and inspect the HTTP requests per second panel. These credentials are for local demo use only. Do not reuse them outside this disposable cluster.

The cluster-independent `servicemonitor.yaml` is for installations that provide the Prometheus Operator CRD. The local static scrape config avoids that CRD dependency and performs the same application metrics scrape.
