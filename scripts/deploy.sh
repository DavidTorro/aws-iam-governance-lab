#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Preflight contra el endpoint local; el proveedor Terraform también lo fija.
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 \
  aws --endpoint-url http://localhost:4566 iam list-users >/dev/null

terraform -chdir=envs/floci init -input=false
terraform -chdir=envs/floci apply -input=false -auto-approve
