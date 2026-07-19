# 🚀 GitHub Pages Deployment for coffee.evasiongusto.be

This repository is ready to deploy to GitHub Pages. Follow these steps to go live:

---

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Create a **public** repository named `coffee-site` (or `coffee-evasiongusto.github.io` if you prefer)
3. Initialize it (we'll push existing history)

---

## Step 2: Push Repository to GitHub

```bash
# Add your GitHub origin
git remote set-url origin https://github.com/YOUR_USERNAME/coffee-site.git

# Push to main branch
git push -u origin main
```

---

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (left sidebar)
3. Under "Source":
   - Select: *Deploy from a branch*
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**

---

## Step 4: Configure Custom Domain in GitHub

1. In the same **Settings → Pages** section
2. Under "Custom domain", enter: `coffee.evasiongusto.be`
3. Click **Save**

This will:
- GitHub will read the `CNAME` file in your repo ✓ (already there)
- Generate an SSL certificate (takes ~5 minutes)

---

## Step 5: Configure DNS (CNAME Record)

**For your domain registrar** (where you manage `evasiongusto.be`):

Add a new CNAME record:

| Type  | Name   | Target |
|-------|--------|--------|
| CNAME | coffee | `<YOUR_GITHUB_USERNAME>.github.io.` |

**Example:**
```
coffee    CNAME    your-username.github.io.
```

---

## Step 6: Verify Setup

1. Wait 2–10 minutes for DNS propagation
2. Visit https://coffee.evasiongusto.be
3. You should see the website
4. Check that the SSL lock appears (green lock icon)

### If HTTPS shows a warning:
- DNS may still be propagating (wait longer)
- Or GitHub's certificate is still being issued
- Check Settings → Pages to see certificate status

---

## Step 7: Enable HTTPS Enforcement (Optional but Recommended)

Once the SSL certificate is issued:
1. Go to **Settings → Pages**
2. Tick **"Enforce HTTPS"**
3. Save

This ensures all visitors are redirected to HTTPS automatically.

---

## ✅ You're Live!

Every time you push to `main`:
```bash
python3 build/build.py   # Regenerate HTML from translations.json
git add -A
git commit -m "Update content"
git push origin main
```

**Deployment happens automatically (~1 minute after push).**

---

## 🔗 Link from Main Site (SEO)

From your main site (evasiongusto.be):
1. Add a "Coffee" or "Courses" link → `https://coffee.evasiongusto.be`
2. This helps Google recognize both sites as related
3. Strongest SEO signal you control

---

## 📋 Pre-Launch Checklist

Before you tell people about the site, ensure:

- [ ] Repository pushed to GitHub
- [ ] GitHub Pages enabled
- [ ] Custom domain configured
- [ ] DNS CNAME record added and propagated
- [ ] HTTPS enforced
- [ ] Website loads at https://coffee.evasiongusto.be
- [ ] All 3 languages work (/en/, /nl/)
- [ ] Google Search Console property created & sitemap submitted
- [ ] Bing Webmaster Tools property created & sitemap submitted
- [ ] Link added from evasiongusto.be
- [ ] Configuration placeholders filled (see README section 3):
  - [ ] `gtm_id` set (Google Tag Manager)
  - [ ] `formspree` endpoint configured (contact form)
  - [ ] `calcom_username` set (online booking)
  - [ ] Images added to `/images/`
  - [ ] Hero video added to `/media/hero.mp4` (optional)

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Site not deployed | Push to `main` and wait 1-2 minutes; check Actions tab |
| Domain not pointing | DNS may need time to propagate (24h max); use `nslookup coffee.evasiongusto.be` to verify |
| HTTPS warning | Certificate may be pending; check Settings → Pages; wait ~5 min |
| Content not updating | Did you run `python3 build/build.py` before pushing? |
| 404 error on /en/ | Check that `en/index.html` exists in repo root |

---

**Questions?** See the full [README.md](README.md) for content editing, analytics setup, and more.
