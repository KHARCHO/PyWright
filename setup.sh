#!/usr/bin/env bash
# One-step local setup: virtualenv, dependencies, Playwright browser, .env
set -euo pipefail
cd "$(dirname "$0")"

[ -d .venv ] || python3 -m venv .venv
PY=.venv/bin/python

"$PY" -m pip install --upgrade pip
"$PY" -m pip install -r requirements.txt
# On a clean Linux/CI machine use: install --with-deps chromium
"$PY" -m playwright install chromium

[ -f .env ] || cp .env.example .env

echo "Setup complete. Run tests with: .venv/bin/python -m pytest"
