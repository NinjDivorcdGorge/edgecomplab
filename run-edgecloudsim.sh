#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${SCRIPT_DIR}/EdgeCloudSim/scripts/sample_app1"

if [ ! -d "${APP_DIR}" ]; then
  echo "EdgeCloudSim sample app directory not found at: ${APP_DIR}" >&2
  echo "Did you clone the project under ${SCRIPT_DIR}/EdgeCloudSim?" >&2
  exit 1
fi

cd "${APP_DIR}"
./compile.sh
./run_scenarios.sh "${1:-1}" "${2:-1}"
