name: Auto PR Merge

on:
  push:                      # ✅ run on any push (branch or main)
    branches: ['**']
  pull_request:
    types: [opened, synchronize, reopened]
  workflow_dispatch: {}

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    runs-on: ubuntu-latest

    # ✅ Skip unsafe fork PRs, and prevent infinite reruns on sanitizer commits
    if: >
      (github.event_name != 'pull_request' ||
       github.event.pull_request.head.repo.full_name == github.repository) &&
      (github.event_name != 'push' ||
       !contains(github.event.head_commit.message, '[actions-sanitize]'))

    env:
      PR_NUMBER: ${{ github.event.pull_request.number }}
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref || github.ref_name }}
          fetch-depth: 0
          persist-credentials: true

      # 🔧 Sanitize placeholders & merge-conflict markers across the repo
      - name: Sanitize repo
        run: |
          python - <<'PY'
          import subprocess, pathlib, re

          BAD_LINES = {
              "bootstrap-empty-github-repo-for-blender-project",
              "main",
          }
          CONFLICT_RE = re.compile(r'^(<<<<<<<|=======|>>>>>>>)( .*)?$')

          files = subprocess.check_output(["git", "ls-files"], text=True).splitlines()
          changed = False

          for f in files:
              p = pathlib.Path(f)
              if not p.exists() or p.is_dir():
                  continue
              try:
                  data = p.read_text(encoding="utf-8", errors="strict").splitlines()
              except UnicodeDecodeError:
                  continue

              cleaned = []
              for line in data:
                  stripped = line.strip()
                  if stripped in BAD_LINES:
                      continue
                  if CONFLICT_RE.match(line):
                      continue
                  cleaned.append(line)

              if cleaned != data:
                  # Preserve trailing newline if the file had one
                  p.write_text("\n".join(cleaned) + ("\n" if data and data[-1] == "" else ""), encoding="utf-8")
                  changed = True

          if changed:
              subprocess.check_call(["git", "config", "user.name", "github-actions[bot]"])
              subprocess.check_call(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"])
              subprocess.check_call(["git", "add", "-A"])
              # 🔁 mark commit so the push-triggered run skips itself (see job-level if)
              subprocess.check_call(["git", "commit", "-m", "ci: sanitize repo (remove placeholders & conflict markers) [actions-sanitize]"])
          PY

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
          python -m pip install black isort flake8 mypy pytest || true

      - name: Run lint and tests
        id: initial
        continue-on-error: true
        run: |
          black --check .
          isort --check-only .
          flake8 .
          mypy addons tests
          pytest -q

      - name: Apply auto fixes
        if: steps.initial.outcome == 'failure'
        run: |
          if [ -f scripts/auto_fix.py ]; then python scripts/auto_fix.py || true; fi
          black .
          isort .

      - name: Commit & push fixes
        if: steps.initial.outcome == 'failure'
        run: |
          if [ -n "$(git status --porcelain)" ]; then
            git config user.name "github-actions[bot]"
            git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
            git add -A
            git commit -m "ci: apply auto fixes [actions-sanitize]"
            git push origin HEAD:${{ github.head_ref || github.ref_name }}
            gh pr comment "$PR_NUMBER" -b "Auto fixes applied. Re-running checks."
          fi

      - name: Re-run lint and tests
        if: steps.initial.outcome == 'failure'
        id: retry
        continue-on-error: true
        run: |
          black --check .
          isort --check-only .
          flake8 .
          mypy addons tests
          pytest -q

      - name: Comment failure
        if: steps.initial.outcome == 'failure' && steps.retry.outcome == 'failure'
        run: gh pr comment "$PR_NUMBER" -b "Checks failed. Manual review required."

      - name: Merge PR
        if: steps.initial.outcome == 'success' || steps.retry.outcome == 'success'
        run: |
          gh pr comment "$PR_NUMBER" -b "All checks passed. Merging PR."
          gh pr merge "$PR_NUMBER" --merge --auto
          
