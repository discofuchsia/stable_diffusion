#!/usr/bin/env bash
set -euo pipefail
PYTHON=${PYTHON:-python3}
BRIEF=${BRIEF:-briefs/sample_brief.yaml}
if [ ! -d ".venv" ]; then
  ${PYTHON} -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt -q
if [ "${GEN_PROVIDER:-placeholder}" = "sdxl" ]; then
  pip install -r requirements-extras.txt -q
fi
echo "[demo] Running generator=${GEN_PROVIDER:-placeholder}"
${PYTHON} app.py "${BRIEF}"
echo "[demo] Done. See output/ and the CSV report."
