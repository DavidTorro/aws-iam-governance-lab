#!/usr/bin/env python3
"""Comprueba IAM en Floci y guarda evidencia obtenida del simulador real."""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENDPOINT = "http://localhost:4566"
ENV = os.environ.copy()
ENV.update(
    AWS_ACCESS_KEY_ID="test",
    AWS_SECRET_ACCESS_KEY="test",
    AWS_DEFAULT_REGION="us-east-1",
    AWS_PAGER="",
)
ENV.pop("AWS_SESSION_TOKEN", None)
ENV.pop("AWS_PROFILE", None)

GROUPS = {
    "Dev-Team": ("roberto", "sandra", "alicia"),
    "Ops-Team": ("marta", "alexis"),
    "SecOps-Team": ("camila", "alicia"),
}
POLICIES = {
    "Dev-Team": ("DevTeamPolicy", "dev-team-policy.json"),
    "Ops-Team": ("OpsTeamPolicy", "ops-team-policy.json"),
    "SecOps-Team": ("SecOpsTeamPolicy", "secops-team-policy.json"),
}
EXPECTED = {
    "roberto": {
        "s3:GetObject": "allowed",
        "s3:DeleteObject": "explicitDeny",
        "dynamodb:PutItem": "allowed",
        "ec2:StartInstances": "implicitDeny",
    },
    "alicia": {
        "s3:GetObject": "allowed",
        "s3:DeleteObject": "explicitDeny",
        "dynamodb:PutItem": "allowed",
        "cloudtrail:LookupEvents": "allowed",
        "iam:ListUsers": "allowed",
        "ec2:TerminateInstances": "explicitDeny",
        "dynamodb:DeleteTable": "explicitDeny",
    },
    "marta": {
        "ec2:DescribeInstances": "allowed",
        "ec2:StartInstances": "allowed",
        "ec2:StopInstances": "allowed",
        "lambda:ListFunctions": "allowed",
        "lambda:CreateFunction": "allowed",
        "s3:GetObject": "implicitDeny",
    },
    "camila": {
        "cloudtrail:LookupEvents": "allowed",
        "logs:FilterLogEvents": "allowed",
        "iam:ListUsers": "allowed",
        "s3:DeleteObject": "explicitDeny",
        "ec2:TerminateInstances": "explicitDeny",
        "dynamodb:PutItem": "implicitDeny",
    },
}


def aws(*args):
    command = ["aws", "--endpoint-url", ENDPOINT, "--no-cli-pager", *args, "--output", "json"]
    try:
        result = subprocess.run(
            command, env=ENV, cwd=ROOT, check=True, capture_output=True, text=True
        )
    except FileNotFoundError:
        raise RuntimeError("AWS CLI no está instalada") from None
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Falló {' '.join(command)}: {exc.stderr.strip()}") from exc
    return json.loads(result.stdout)


def check(actual, expected, description):
    if actual != expected:
        raise AssertionError(f"{description}: esperado {expected!r}; obtenido {actual!r}")


def main():
    users = {item["UserName"] for item in aws("iam", "list-users")["Users"]}
    check(users, {u for group in GROUPS.values() for u in group}, "usuarios")

    groups = {item["GroupName"] for item in aws("iam", "list-groups")["Groups"]}
    check(groups, set(GROUPS), "grupos")

    for group, expected_users in GROUPS.items():
        actual = {item["UserName"] for item in aws("iam", "get-group", "--group-name", group)["Users"]}
        check(actual, set(expected_users), f"miembros de {group}")
        policy_name, file_name = POLICIES[group]
        actual_names = aws("iam", "list-group-policies", "--group-name", group)["PolicyNames"]
        if policy_name not in actual_names:
            raise AssertionError(f"Falta {policy_name} en {group}")
        policy = aws("iam", "get-group-policy", "--group-name", group, "--policy-name", policy_name)
        expected_policy = json.loads((ROOT / "policies" / file_name).read_text(encoding="utf-8"))
        actual_policy = policy["PolicyDocument"]
        if isinstance(actual_policy, str):
            actual_policy = json.loads(actual_policy)
        check(actual_policy, expected_policy, f"política {group}")

    for user in users:
        expected_groups = {group for group, members in GROUPS.items() if user in members}
        actual_groups = {item["GroupName"] for item in aws("iam", "list-groups-for-user", "--user-name", user)["Groups"]}
        check(actual_groups, expected_groups, f"grupos de {user}")
        inline = aws("iam", "list-user-policies", "--user-name", user)["PolicyNames"]
        attached = aws("iam", "list-attached-user-policies", "--user-name", user)["AttachedPolicies"]
        check(inline, [], f"políticas directas inline de {user}")
        check(attached, [], f"políticas directas gestionadas de {user}")

    report = {"verified_at_utc": datetime.now(timezone.utc).isoformat(), "endpoint": ENDPOINT, "groups": GROUPS, "simulations": {}}
    lines = ["# Verificación IAM en Floci", "", f"Ejecutada: {report['verified_at_utc']}", "", "| Usuario | Acción | Esperado | Obtenido |", "| --- | --- | --- | --- |"]
    for user, expectations in EXPECTED.items():
        arn = aws("iam", "get-user", "--user-name", user)["User"]["Arn"]
        result = aws("iam", "simulate-principal-policy", "--policy-source-arn", arn, "--action-names", *expectations)
        decisions = {item["EvalActionName"]: item["EvalDecision"] for item in result["EvaluationResults"]}
        report["simulations"][user] = {"arn": arn, "results": result["EvaluationResults"]}
        for action, expected in expectations.items():
            actual = decisions.get(action)
            lines.append(f"| {user} | `{action}` | `{expected}` | `{actual}` |")
            check(actual, expected, f"simulación {user} {action}")

    output = ROOT / "evidence"
    output.mkdir(exist_ok=True)
    (output / "verification.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "verification.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Verificación correcta. Evidencias: {output / 'verification.md'} y {output / 'verification.json'}")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, RuntimeError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
