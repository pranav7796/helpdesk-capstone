# Kubernetes troubleshooting

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
