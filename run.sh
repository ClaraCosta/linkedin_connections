#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEBUGGER_HOST="${DEBUGGER_HOST:-127.0.0.1}"
DEBUGGER_PORT="${DEBUGGER_PORT:-9222}"
DEBUGGER_URL="http://${DEBUGGER_HOST}:${DEBUGGER_PORT}/json/version"
CHROME_BINARY="${CHROME_BINARY:-google-chrome}"
CHROME_USER_DATA_DIR="${CHROME_USER_DATA_DIR:-$PROJECT_DIR/.chrome-profile}"
CHROME_PROFILE_DIRECTORY="${CHROME_PROFILE_DIRECTORY:-Default}"
CHROME_LOG="${CHROME_LOG:-/tmp/linkedin-connections-chrome.log}"

cd "$PROJECT_DIR"

check_debugger() {
  python3 - "$DEBUGGER_URL" <<'PY'
import sys
import urllib.error
import urllib.request

try:
    urllib.request.urlopen(sys.argv[1], timeout=1).close()
except urllib.error.URLError:
    raise SystemExit(1)
PY
}

if ! check_debugger; then
  echo "Abrindo Google Chrome com perfil de automacao em: $CHROME_USER_DATA_DIR"
  "$CHROME_BINARY" \
    --remote-debugging-port="$DEBUGGER_PORT" \
    --user-data-dir="$CHROME_USER_DATA_DIR" \
    --profile-directory="$CHROME_PROFILE_DIRECTORY" \
    >"$CHROME_LOG" 2>&1 &

  for _ in {1..30}; do
    if check_debugger; then
      break
    fi

    sleep 1
  done
fi

if ! check_debugger; then
  cat <<EOF >&2
Nao consegui conectar ao Chrome pela porta ${DEBUGGER_PORT}.

O Chrome atual nao permite DevTools remote debugging com o diretorio de perfil padrao.
Por isso este script usa um perfil de automacao separado em:
${CHROME_USER_DATA_DIR}

Faca assim:
1. Feche a janela de automacao que abriu, se houver.
2. Rode de novo:
   ./run.sh
3. Se o LinkedIn pedir login, faca login nessa janela uma vez e rode novamente.

Log do Chrome:
${CHROME_LOG}
EOF
  exit 1
fi

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install -r requirements.txt

echo "Rodando RPA no Chrome controlado pelo Selenium..."

ATTACH_TO_EXISTING_CHROME=true \
CHROME_DEBUGGER_ADDRESS="${DEBUGGER_HOST}:${DEBUGGER_PORT}" \
CHROME_USER_DATA_DIR="$CHROME_USER_DATA_DIR" \
CHROME_PROFILE_DIRECTORY="$CHROME_PROFILE_DIRECTORY" \
python main.py
