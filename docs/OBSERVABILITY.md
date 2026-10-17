# Local observability stack

`local-stack.yaml` installs Prometheus/Grafana and an internal headless Service, `relaydesk-backend-metrics`. Prometheus DNS discovery resolves that Service to each ready backend Pod and scrapes each IP separately. Grafana provisions the datasource and HTTP dashboard from ConfigMaps.

Each replica must have its own `instance` time series. Scraping a load-balanced ClusterIP mixes process-local counters: switching between two different values can look like a reset and inflate `rate()`. The October 17 audit observed three false resets in five minutes before correcting this. New targets carry `scrape_mode="pod"`; the dashboard selects that label to exclude the old mixed series. [DNS discovery reference](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#dns_sd_config).

```sh
kubectl --context helpdesk-capstone -n relaydesk create configmap grafana-dashboard \
  --from-file=relaydesk-dashboard.json=monitoring/relaydesk-dashboard.json \
  --dry-run=client -o yaml | kubectl --context helpdesk-capstone apply -f -
kubectl --context helpdesk-capstone apply -f monitoring/local-stack.yaml
kubectl --context helpdesk-capstone -n relaydesk rollout status deploy/prometheus --timeout=120s
kubectl --context helpdesk-capstone -n relaydesk rollout status deploy/grafana --timeout=120s
kubectl --context helpdesk-capstone -n relaydesk port-forward svc/grafana 3001:3000
```

Open <http://localhost:3001> and sign in as `admin` with the local demo password `relaydesk-demo-only`. Generate requests against the application. In Prometheus, check **Status → Targets** and query `up{job="relaydesk-backend"}`; it should be `1`. In Grafana, open the Relaydesk HTTP traffic dashboard and inspect the HTTP requests per second panel. These credentials are for local demo use only. Do not reuse them outside this disposable cluster.

The cluster-independent `servicemonitor.yaml` is for installations that provide the Prometheus Operator CRD. DNS discovery avoids that CRD dependency and follows replica IP changes without Kubernetes API credentials.

## Existing EKS installation

Use the isolated Sydney kubeconfig and `kubectl --context relaydesk-sydney apply -k monitoring`. The Kustomize variant retains the private Grafana password Secret reference and disables anonymous login. Do not apply the local demo-password manifest directly to EKS.

Validate the projected Prometheus configuration with `kubectl --context relaydesk-sydney -n relaydesk exec deploy/prometheus -- promtool check config /etc/prometheus/prometheus.yml`. After the updated ConfigMap is mounted, reload the existing process with `kubectl --context relaydesk-sydney -n relaydesk exec deploy/prometheus -- sh -c 'kill -HUP 1'`. This does not restart or delete Pods. Check `up{job="relaydesk-backend",scrape_mode="pod"}`: one result per ready backend replica, all equal to 1. Check `resets(relaydesk_http_requests_total{scrape_mode="pod",route="/ready"}[2m])` and real positive rates after multiple scrapes. Initial single-Service captures are genuine historical evidence but superseded by the corrected per-replica screenshots.
