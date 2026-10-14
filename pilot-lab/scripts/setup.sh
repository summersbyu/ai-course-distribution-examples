#!/usr/bin/env bash
set -euo pipefail
LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$LAB_ROOT"
python -m venv .lab-runtime/venv
.lab-runtime/venv/bin/python -m pip install --disable-pip-version-check -r pilot-lab/requirements.lock.txt
echo "Accounting Lab setup is complete. Your data folder is preserved."
