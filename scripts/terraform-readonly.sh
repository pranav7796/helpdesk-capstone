#!/usr/bin/env bash
set -euo pipefail

# Support the existing AWS CLI console login without persisting temporary keys.
# Only read-only Terraform operations are permitted through this helper.
case "${1:-}" in
  init|plan|validate|fmt|show|version|providers) ;;
  *) echo 'Usage: bash scripts/terraform-readonly.sh {init|plan|validate|fmt|show|version|providers} [arguments]' >&2; exit 2 ;;
esac
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export AWS_CONFIG_FILE="$project_dir/terraform/aws-login.config"
export AWS_PROFILE=devops-new
export AWS_REGION=ap-southeast-2
export AWS_EC2_METADATA_DISABLED=true
export AWS_SDK_LOAD_CONFIG=1
exec terraform -chdir="$project_dir/terraform" "$@"
