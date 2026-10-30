#!/usr/bin/env python3
"""Renderiza como PNG los JSON y los resultados reales guardados por verify.py."""

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "capturas"
FONT = "/System/Library/Fonts/Menlo.ttc"


def render(name, text):
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt") as source:
        source.write(text)
        source.flush()
        subprocess.run(
            [
                "magick", "-background", "#0f172a", "-fill", "#e2e8f0",
                "-font", FONT, "-pointsize", "18", "-interline-spacing", "5",
                f"label:@{source.name}", "-bordercolor", "#0f172a", "-border", "32",
                str(OUT / name),
            ],
            check=True,
        )


def main():
    for group in ("ops-team", "secops-team"):
        filename = f"{group}-policy.json"
        content = (ROOT / "policies" / filename).read_text(encoding="utf-8")
        render(f"{group}-policy.png", f"policies/{filename}\n\n{content}")

    evidence = json.loads((ROOT / "evidence" / "verification.json").read_text(encoding="utf-8"))
    for user, data in evidence["simulations"].items():
        rows = [
            f"{item['EvalActionName']:<30} {item['EvalDecision']}"
            for item in data["results"]
        ]
        content = (
            f"Floci IAM simulator  |  {user}\n"
            f"ARN: {data['arn']}\n"
            f"Fecha UTC: {evidence['verified_at_utc']}\n\n"
            "ACCION                         DECISION\n"
            + "\n".join(rows) + "\n"
        )
        render(f"simulacion-{user}.png", content)


if __name__ == "__main__":
    main()
