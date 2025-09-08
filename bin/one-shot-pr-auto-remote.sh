#!/usr/bin/env bash
# file: bin/one-shot-pr-auto-remote.sh
# Usage:
#   bash bin/one-shot-pr-auto-remote.sh "feat: demo" "feature/demo" "recheck"

set -euo pipefail

PR_TITLE="${1:-"chore: batch updates"}"
BRANCH="${2:-"chore/batch-updates"}"
OPTIONAL_LABEL="${3:-""}"
DEFAULT_REPO_SLUG="cputer/naestro"   # change if pushing to a different fork

git config --global user.name  "Naestro Bot"
git config --global user.email "naestro-bot@example.com"

# --- ensure we're at repo root ---
if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "❌ Not a git repository. cd into your repo and retry."
  exit 1
fi
cd "$(git rev-parse --show-toplevel)"

# --- auto-detect or create 'origin' remote ---
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "ℹ️  No 'origin' remote found; attempting auto-detect..."
  # look for any other remote URL in .git/config
  DETECTED_URL=$(git config --get remote.fork.url \
                  || git config --get remote.github.url \
                  || git config --get remote.upstream.url \
                  || echo "")
  if [[ -n "$DETECTED_URL" ]]; then
    echo "🔁 Reusing existing remote: $DETECTED_URL"
    git remote add origin "$DETECTED_URL"
  else
    echo "➕ Adding default remote https://github.com/${DEFAULT_REPO_SLUG}.git"
    git remote add origin "https://github.com/${DEFAULT_REPO_SLUG}.git"
  fi
fi

# --- authentication (GH_TOKEN or gh auth login) ---
need_gh_cli=false
if [[ -n "${GH_TOKEN:-}" ]]; then
  echo "🔐 Using GH_TOKEN for authentication"
  ORIGIN_URL=$(git remote get-url origin)
  ORIGIN_URL_NO_SCHEME="${ORIGIN_URL#https://}"
  git remote set-url origin "https://${GH_TOKEN}@${ORIGIN_URL_NO_SCHEME}"
else
  echo "ℹ️  GH_TOKEN not set; will try GitHub CLI"
  command -v gh >/dev/null 2>&1 || need_gh_cli=true
fi

if [[ "$need_gh_cli" == "true" ]]; then
  echo "⬇️  Installing GitHub CLI"
  type apt-get >/dev/null 2>&1 && sudo apt-get update -y && sudo apt-get install -y gh || true
fi

if [[ -z "${GH_TOKEN:-}" ]]; then
  if gh auth status >/dev/null 2>&1; then
    echo "✅ gh already authenticated"
  else
    echo "🔐 Launching gh auth login..."
    gh auth login
    gh repo set-default || true
  fi
fi

# --- ensure pnpm is available ---
if ! command -v pnpm >/dev/null 2>&1; then
  echo "⬇️  Installing pnpm via corepack"
  if ! command -v corepack >/dev/null 2>&1; then
    type apt-get >/dev/null 2>&1 && sudo apt-get update -y && sudo apt-get install -y nodejs npm || true
  fi
  corepack enable || true
  corepack prepare pnpm@latest --activate || true
fi

# --- create or switch to branch ---
git fetch origin || true
git switch -c "$BRANCH" || git switch "$BRANCH"

# --- optional UI checks ---
if [ -d "ui" ]; then
  echo "🧪 UI checks"
  pushd ui >/dev/null
  pnpm install
  pnpm -s lint || true
  pnpm -s typecheck || true
  pnpm -s build || true
  if pnpm -s test:ci >/dev/null 2>&1; then
    pnpm -s test:ci
  elif pnpm -s vitest >/dev/null 2>&1; then
    pnpm -s vitest run --coverage
  fi
  popd >/dev/null
fi

# --- optional Python checks ---
if [ -d "server" ] || [ -d "python" ]; then
  echo "🧪 Python checks"
  if type python3 >/dev/null 2>&1; then
    python3 -m venv .venv || true
    source .venv/bin/activate || true
    [[ -f "requirements.txt" ]] && pip install -r requirements.txt || true
    [[ -f "pyproject.toml" ]]   && pip install -e . || true
    if python -c "import pytest" >/dev/null 2>&1 || pip install pytest >/dev/null 2>&1; then
      pytest -q || true
      if python -c "import coverage" >/dev/null 2>&1 || pip install coverage >/dev/null 2>&1; then
        coverage run -m pytest || true
        coverage xml -o coverage.xml || true
      fi
    fi
    deactivate || true
  fi
fi

# --- commit and push ---
git add -A
git diff --cached --quiet || git commit -m "$PR_TITLE"
git push -u origin "$BRANCH"

if command -v gh >/dev/null 2>&1; then
  echo "📬 Opening Pull Request"
  gh pr create --title "$PR_TITLE" --base main --head "$BRANCH" --fill || true
  [[ -n "$OPTIONAL_LABEL" ]] && gh pr edit --add-label "$OPTIONAL_LABEL" || true
else
  echo "👉 GitHub CLI not available; open a PR manually."
fi

echo "✅ Done."
