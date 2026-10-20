# October 20 audit evidence

Fresh sanitized outputs; original PNG/WebM evidence remains in its dated canonical folders. Start with [final report](../../docs/FINAL-REPORT.md), [criterion mapping](criterion-evidence.json), [command exit codes](collection-results.json), [supplement](supplement-results.json), [HTTP results](http-check-results.json), [context/limits](audit-context.json), and [integrity](evidence-integrity.json).

`collection-tools/` preserves the exact one-off helpers used on this machine; they contain original absolute repository/temp paths and are execution provenance, not a portable CLI. `http_checks.py` and `local_checks.py` deliberately create/update/delete only their own synthetic audit ticket; other collection tools are read-only against AWS/Kubernetes. Do not rerun against another environment without inspecting paths and scope. No AWS apply/destroy, credentials, state, plans or kubeconfig are included.

`collection-results.json` retains the original NAT CLI flag error and top-nodes timeout. Successful corrected checks are in `supplement-results.json`. Latest CI logs are a fresh fetch of the dated published-source run, not a new scan. Empty log files honestly represent the returned log window.
