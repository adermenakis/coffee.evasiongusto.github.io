# 🚀 GitHub Actions Deployment Workflow

This repository includes an automated GitHub Actions workflow for controlled deployments to GitHub Pages.

---

## How It Works

The workflow is triggered **manually** from the GitHub UI and allows you to:

1. **Choose a source** — Deploy from a branch (`main` or `dev`) or a specific commit
2. **Optionally regenerate** — Run `python3 build/build.py` to regenerate HTML from `translations.json`
3. **Auto-commit & push** — Changes are committed and pushed to `main` (GitHub Pages source)
4. **Deployment report** — View detailed summary with file counts and deployment metadata

---

## How to Use

### 1. Trigger the Workflow

**On GitHub:**
1. Go to your repository → **Actions** tab
2. Find **"Deploy to GitHub Pages (Manual)"** workflow
3. Click **"Run workflow"**

**Or via GitHub CLI:**
```bash
gh workflow run deploy.yml
```

### 2. Fill in the Options

A modal appears with these inputs:

| Input | Options | Example |
|-------|---------|---------|
| **Deploy type** | `branch` or `commit` | Choose `branch` for stable deployments |
| **Source branch** | `main` or `dev` | Select `main` for production |
| **Commit SHA** | Full or short hash | `abc123def456` (only if deploy_type = commit) |
| **Regenerate HTML?** | `yes` or `no` | `yes` to update from translations.json |

### 3. Examples

#### Example 1: Deploy latest main branch as-is
- Deploy type: `branch`
- Source branch: `main`
- Regenerate: `no`

→ Simply pushes current main to GitHub Pages

#### Example 2: Deploy a specific commit with regeneration
- Deploy type: `commit`
- Commit SHA: `f71f9eb`
- Regenerate: `yes`

→ Checks out that commit, regenerates HTML, then pushes

#### Example 3: Deploy dev branch with content regeneration
- Deploy type: `branch`
- Source branch: `dev`
- Regenerate: `yes`

→ Checks out dev, regenerates from translations.json, then pushes to main

---

## Workflow Details

### What It Does

1. **Checkout** — Clones the source (branch or commit)
2. **Setup Python** — Prepares Python 3.9
3. **Regenerate (optional)** — Runs `python3 build/build.py` if selected
4. **Report** — Counts HTML, CSS, JS, and media files
5. **Commit** — Creates a descriptive commit if changes exist
6. **Push** — Pushes to `main` branch (GitHub Pages source)
7. **Summary** — Displays status in GitHub Actions UI

### Deployment Report Includes

- Deploy type (branch vs. commit)
- Source information
- Deployed commit hash and message
- Deployment timestamp
- File counts (HTML pages, CSS, JS, media)
- Regeneration status

### No Changes = No Push

If the workflow detects no changes, it skips the commit and push (prevents empty commits).

---

## Typical Workflow

### Publishing Updated Content

```bash
# 1. Edit translations.json locally
nano build/translations.json

# 2. Test locally
python3 build/build.py
python3 -m http.server 8080  # Check http://localhost:8080

# 3. Commit and push to dev branch
git checkout dev
git add build/translations.json
git commit -m "Update course prices and descriptions"
git push origin dev

# 4. On GitHub Actions:
#    - Deploy type: branch
#    - Source: dev
#    - Regenerate: yes
#
# 5. Site updates automatically after ~1 minute
```

### Hotfix from Main

```bash
# If you need to deploy the current main immediately:
# Just use Actions UI with:
#    - Deploy type: branch
#    - Source: main
#    - Regenerate: no
```

### Roll Back to Previous Commit

```bash
# Find the commit hash you want to revert to
git log --oneline

# On GitHub Actions:
#    - Deploy type: commit
#    - Commit SHA: [your-hash]
#    - Regenerate: no
#
# This re-deploys exactly that state to GitHub Pages
```

---

## Branch Strategy

For optimal workflow:

- **`main`** — Stable, production-ready code. Deployed to GitHub Pages automatically.
- **`dev`** — Working branch. Test changes here before merging to main.

You can:
- Develop on `dev`
- Test with Actions (deploy `dev` to verify)
- Merge to `main` when ready
- Deploy `main` for production

---

## Security Notes

- Workflow uses default `GITHUB_TOKEN` (no external secrets needed)
- Git commits are attributed to `github-actions[bot]`
- Workflow can only push to your own repository
- No credentials or sensitive data in workflow file

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Workflow doesn't appear in Actions tab" | Go to **.github/workflows/** folder, ensure `deploy.yml` exists and is committed |
| "No input modal appears" | Refresh the page, try again, or use `gh workflow run deploy.yml` |
| "Commit SHA not recognized" | Use `git log --oneline` to find valid commits, try full hash vs. short hash |
| "Site doesn't update" | Check GitHub Actions log for errors; ensure `main` branch is the GitHub Pages source |
| "Build failed during regenerate" | Check `build/translations.json` syntax, run `python3 build/build.py` locally first |

---

## Related Files

- **Workflow**: `.github/workflows/deploy.yml`
- **Build script**: `build/build.py`
- **Content**: `build/translations.json`
- **GitHub Pages config**: Repository Settings → Pages
- **CNAME**: `CNAME` (points to `coffee.evasiongusto.be`)

---

For questions, check:
- [README.md](README.md) — Full content documentation
- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) — Initial GitHub Pages setup
