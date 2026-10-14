#!/usr/bin/env bash
set -euo pipefail
LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$LAB_ROOT"
mkdir -p .lab-runtime .lab-data
exec 9>.lab-runtime/start.lock
flock -x 9
PYTHON="$LAB_ROOT/.lab-runtime/venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
  echo "Setup is incomplete. Ask the instructor to inspect the creation log."
  exit 1
fi
if "$PYTHON" -c 'import urllib.request; urllib.request.urlopen("http://127.0.0.1:8501/_stcore/health", timeout=2)' >/dev/null 2>&1; then
  echo "Accounting Lab is already running. Open the Accounting Lab entry in Ports."
  exit 0
fi
nohup "$PYTHON" -m streamlit run "$LAB_ROOT/pilot-lab/app.py" \
  --server.address 0.0.0.0 --server.port 8501 --server.headless true \
  --browser.gatherUsageStats false \
  > .lab-runtime/app.log 2>&1 < /dev/null 9>&- &
echo "$!" > .lab-runtime/app.pid
for attempt in $(seq 1 45); do
  if "$PYTHON" -c 'import urllib.request; urllib.request.urlopen("http://127.0.0.1:8501/_stcore/health", timeout=2)' >/dev/null 2>&1; then
    echo "Accounting Lab is ready at http://localhost:8501"
    exit 0
  fi
  sleep 1
done
echo "The lab did not become ready. Instructor log: .lab-runtime/app.log"
exit 1
