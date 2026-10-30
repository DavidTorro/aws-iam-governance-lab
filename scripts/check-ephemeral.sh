#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
endpoint="http://localhost:4566"
export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 AWS_PAGER=""
unset AWS_SESSION_TOKEN AWS_PROFILE

before="$(aws --endpoint-url "$endpoint" iam list-users --query 'Users[].UserName' --output json)"
floci stop
sleep 3
floci start
eval "$(floci env)"
after="$(aws --endpoint-url "$endpoint" iam list-users --query 'Users[].UserName' --output json)"

mkdir -p evidence
python3 - "$before" "$after" > evidence/ephemeral.json <<'PY'
import json
import sys
from datetime import datetime, timezone
before, after = (json.loads(value) for value in sys.argv[1:])
print(json.dumps({"verified_at_utc": datetime.now(timezone.utc).isoformat(), "users_before": before, "users_after": after}, indent=2, ensure_ascii=False))
if not before:
    raise SystemExit("ERROR: no había identidades antes de detener Floci")
if after:
    raise SystemExit("ERROR: los usuarios persisten; revisa el modo de almacenamiento de Floci")
PY
printf 'Floci reiniciado: los usuarios desaparecieron. Evidencia: evidence/ephemeral.json\n'
