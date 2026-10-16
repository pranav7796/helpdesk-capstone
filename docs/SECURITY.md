# Container scan notes

CI runs Trivy on both final application images with `--severity HIGH,CRITICAL`, `--ignore-unfixed`, and `--exit-code 1`. It also asks BuildKit not to attach SBOM/provenance attestations to these images, so Trivy assesses the runtime filesystem and its installed packages.

The first CI scan reported four HIGH findings for `msgpack 1.1.2`, `setuptools 70.3.0`, and `urllib3 2.7.0` from an upstream Python image build SBOM. Those versions are not installed in the application container. The final runtime has `msgpack 1.2.3`, `setuptools 84.0.0`, and `urllib3 2.8.0`; the build checks these versions, and the evidence in `evidence/trivy-backend.json` records the local image scan. The old SBOM entries are excluded only by their exact PURLs in `.trivyignore.yaml`; a different package version or vulnerability remains subject to the HIGH/CRITICAL gate.

The initial real GitHub failure and report are available at [Actions run 38886640390](https://github.com/pranav7796/helpdesk-capstone/actions/runs/38886640390). Its `setuptools` finding was CVE-2025-47273, a path traversal issue fixed upstream in version 78.1.1. The runtime is pinned to 84.0.0. The other two libraries are similarly pinned at versions beyond their listed fixes.

Trivy supports package-URL-scoped exceptions in `.trivyignore.yaml`; see its [filtering documentation](https://trivy.dev/docs/latest/configuration/filtering/). Review these narrow exceptions if the base image or dependency build changes.
