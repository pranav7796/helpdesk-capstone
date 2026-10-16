# Kubernetes troubleshooting

## Executed isolated local lab

Run `python scripts/troubleshooting-lab.py` with access to the **local** `helpdesk-capstone` context. It refuses any pre-existing `relaydesk-lab` namespace, creates only disposable lab resources, captures real events/logs and HTTP errors, repairs them, then removes its own namespace. It does not modify the working release or AWS. The two assignment exercise manifests are in `troubleshooting/`.

The verified run is in [`evidence/sydney/troubleshooting.txt`](../evidence/sydney/troubleshooting.txt): image-pull backoff, repeated exit-1 crashes with kubelet BackOff events, selector without endpoints, HTTP 404 readiness failure, and HTTP 503 database readiness failure. All replacement deployments rolled out successfully, the fixed Service returned HTTP 200, and the temporary namespace was deleted.

Two observation/startup failures are retained in the evidence folder. The script initially required a transient literal `CrashLoopBackOff` waiting state, while this cluster kept reporting `Error` with restart increments and BackOff events. It now checks repeated exit-1 crashes plus actual kubelet BackOff events. It also waits for HTTP startup before asserting 404/503; the first attempt hit connection refused during CPU-throttled startup. These fixes did not weaken the application's readiness probe.

The intentionally invalid-image exercise encountered real Minikube registry DNS errors (`192.168.58.1:53: server misbehaving`) before the registry could reject its missing tag. Recovery used the already cached immutable image. This proves diagnosis/recovery of ImagePullBackOff; it does not establish external registry DNS works inside the local node. Host-side GHCR pulls and image preloading remain the local workaround. Previous-container logs were unavailable for one crashed container, so restart counts, current state and BackOff events provide that failure evidence.

Run commands with `kubectl -n relaydesk ...`. Start with current state, pod events, logs, and rollout state before changing resources:

```sh
kubectl get pods,svc,endpoints,hpa,pvc
kubectl describe pod POD_NAME
kubectl get events --sort-by=.lastTimestamp
kubectl logs POD_NAME --all-containers --previous
kubectl rollout status deploy/relaydesk-backend --timeout=90s
kubectl rollout history deploy/relaydesk-backend
```

## ImagePullBackOff

`describe pod` shows `Failed to pull image`, registry DNS, authentication, or tag errors. Check the exact image and policy with `kubectl get pod POD_NAME -o jsonpath='{.spec.containers[*].image} {.spec.containers[*].imagePullPolicy}'`. Verify the tag exists and the node can reach the registry. For offline Minikube, preload the image with `minikube image load IMAGE -p helpdesk-capstone` and use `IfNotPresent` (or `Never` for a strictly local image). After fixing the tag, restart the deployment and verify the replacement pod is Ready.

## CrashLoopBackOff

Read current and previous logs, then inspect environment references, probes, and recent events. Common causes include application exceptions, incorrect database settings, and a liveness probe that fires before startup. Fix the configuration or probe delay, apply it, and wait for `kubectl rollout status`. Do not hide the error by weakening readiness checks.

## Service has no endpoints / wrong selector

Compare `kubectl get svc SERVICE -o yaml` selector labels with `kubectl get pods --show-labels`. Confirm `kubectl get endpoints SERVICE` lists ready Pod IPs. Correct the selector or pod labels through the Helm chart, upgrade the release, then verify the Service endpoints and request path.

## Readiness probe fails

Use `kubectl describe pod` to see probe failures and `kubectl logs` to inspect startup. Test the configured path and port from inside the pod or via `kubectl port-forward`. For Relaydesk, API readiness is `/ready` and checks PostgreSQL; frontend readiness is `/healthz`. Confirm containerPort, Service targetPort, and probe port agree before changing timings.

## Database connection failure

Check PostgreSQL pod readiness and logs, then check that the database Service has endpoints. Confirm `DATABASE_URL` and PostgreSQL secret keys match the same database, user, and password. Verify DNS/service name and network policy. Allow the database to become ready before backend migrations; inspect the `database-migrations` init container logs if the API pods remain in Init state. Keep PVCs when restarting pods; deleting the PVC destroys stored ticket data.

## Restoring the working state

Fix the chart values or templates, then run `helm upgrade --install relaydesk helm/helpdesk -n relaydesk --create-namespace -f helm/helpdesk/values-local.yaml --wait --timeout 180s`. Confirm all application Pods are Ready, Services have endpoints, and a test ticket round-trips through the API before collecting final evidence.
