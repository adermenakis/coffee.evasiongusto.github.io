# ☕ coffee.evasiongusto.be

Multilingual static website (FR / EN / NL) for **Évasion Gusto Coffee** — barista courses on a Victoria Arduino Prima Pro and specialty coffee sales in Beaumont, Belgium. Built for GitHub Pages, zero hosting cost.

**Design:** Scandinavian minimal — white, thin defined hairlines, no rounded corners, black / oak brown / white palette, animated SVG espresso machine, optional full-screen hero video with frosted-glass panels.

---

## 🚀 GitHub Pages Setup

This repository is configured for GitHub Pages deployment:

- **Source:** Main branch, root directory (/)
- **Custom domain:** coffee.evasiongusto.be (CNAME already in place)
- **SSL/TLS:** Automatic via GitHub

### Next steps:

1. **Push to GitHub** — This repo is ready to push to `coffee-evasiongusto/coffee-site` (or similar)
2. **GitHub Settings** — Go to repo → **Settings → Pages**:
   - Source: *Deploy from a branch* → `main` / `/ (root)`
   - Custom domain: `coffee.evasiongusto.be` (will read from `CNAME` file)
   - Tick **Enforce HTTPS** once the certificate is issued (~5 min)
3. **DNS Configuration** — In your DNS zone for `evasiongusto.be`, add:
   ```
   coffee    CNAME    <your-github-username>.github.io.
   ```
4. Wait for DNS propagation → visit https://coffee.evasiongusto.be

Every `git push` to `main` redeploys automatically (~1 min).

---

## 📖 Full Documentation

### 1. Repository structure

```
index.html            Generated page — French (default language, site root)
en/index.html         Generated page — English
nl/index.html         Generated page — Dutch
css/style.css         All styling: palette, layout, animations, GDPR modal
js/main.js            Consent manager, GTM loader, nav, reveals, form, video
build/
  translations.json   ★ ALL content & configuration (edit this)
  build.py            Site generator (python3 build/build.py)
images/               Coffee photos + promo banner photo (you add these)
media/                Hero background video (you add hero.mp4)
robots.txt            Crawlers incl. AI bots (GPTBot, ClaudeBot, Perplexity…)
llms.txt              AI-search summary of the business
sitemap.xml           Generated, with hreflang alternates
CNAME                 coffee.evasiongusto.be (GitHub Pages custom domain)
.nojekyll             Disables Jekyll processing on GitHub Pages
```

**Golden rule:** never edit `index.html`, `en/index.html`, `nl/index.html`,
or `sitemap.xml` by hand — they are generated. Edit
`build/translations.json`, then regenerate:

```bash
python3 build/build.py
```

---

## 2. Quick start — edit content locally

All content lives in `build/translations.json`. After editing:

```bash
python3 build/build.py      # Regenerates HTML files
git add -A && git commit -m "Update content"
git push origin main        # Automatic deployment ~1 min later
```

### Local preview

Pages use absolute paths (`/css/...`), so serve from the repo root:

```bash
python3 -m http.server 8080
# open http://localhost:8080  (and /en/, /nl/)
```

---

## 3. Configuration — placeholders to replace before launch

All in `build/translations.json` under `"site"`. After any change:
`python3 build/build.py` → commit → push.

| Key                | Replace with                              | Purpose |
|--------------------|-------------------------------------------|---------|
| `gtm_id`           | Your GTM container ID (`GTM-…`)           | Analytics via Google Tag Manager |
| `formspree`        | `https://formspree.io/f/<your-form-id>`   | Contact form → your email |
| `calcom_username`  | Your Cal.com username                     | Per-course online booking |
| `hero_video`       | Keep `/media/hero.mp4` or set a full URL  | Hero background video |
| `hero_poster`      | Optional poster image path                | Shown before video loads |
| `banner_image`     | Keep `/images/banner.jpg` (add the photo) | Gift-voucher promo band |
| `email`, `phone_*`, `address`, `whatsapp` | Already set from evasiongusto.be | Contact details |
| `logo`             | Hot-linked from evasiongusto.be           | See §8 note |

Safe-by-default behaviour: while a placeholder is still in place, the
related feature degrades gracefully (form posts nowhere harmful, booking
buttons fall back to the contact form, video/banners simply don't show).

---

## 4. Editing content (courses, coffees, prices, texts)

Everything lives in `build/translations.json`, once per language
(`fr`, `en`, `nl`). The three blocks mirror each other — keep them in sync.

- **Courses** — `langs.<lang>.courses[]`: name, tagline, description,
  bullet points, duration, price, group size, icon
  (`portafilter`, `drop`, …) and `calcom_event` slug (see §6).
- **Coffees** — `langs.<lang>.coffees[]`: name, origin, process, tasting
  notes, price, weight, icon, and `picture` (see §5). Add or remove array
  entries freely — the grid adapts.
- **Headings** — wrap a phrase in asterisks for the oak italic accent:
  `"Deux cours, un seul objectif : *une meilleure tasse*"`.
- **Announcement bar** — `langs.<lang>.announcement`; set to `""` to hide.
- **Promo banner** — `langs.<lang>.banner` (gift vouchers / private groups).
- **Footer motto** — `langs.<lang>.footer.motto`.
- **GDPR texts** — `langs.<lang>.consent` and `consent_preferences`.

Rebuild after every edit: `python3 build/build.py`.

---

## 5. Images

### Coffee product photos
Each coffee has a `"picture"` field (defaults: `/images/coffee-1.jpg` …
`coffee-4.jpg`). Drop JPG/WebP files there — 560×360 px or larger,
landscape 14:9-ish. Missing file → card renders without a photo.

### Promo banner photo
`/images/banner.jpg` — a wide atmospheric shot (≥1600 px wide) shown behind
the gift-voucher band with a dark overlay. Missing file → solid dark band.

### Hero video
Drop a muted, loopable MP4 at `media/hero.mp4`:

- 10–20 s loop, 1920×1080, **< 8 MB**, no audio track
- Ideal subject: slow-motion espresso pour on the Prima Pro, milk steaming
- Compress with:

  ```bash
  ffmpeg -i input.mov -vf scale=1920:-2 -an -crf 28 -movflags +faststart media/hero.mp4
  ```

Behaviour: full-bleed behind the hero; the text and machine illustration
sit on frosted-glass panels (same blur as the sticky header). Missing
file → video removes itself, hero stays clean white. Paused automatically
for visitors with reduced-motion preferences. GitHub blocks files > 100 MB.

---

## 6. Online booking — Cal.com (free plan)

Each course is a separate Cal.com **event type** with its own availability,
so each course offers different dates.

1. Create a free account at https://cal.com, connect your Google Calendar.
2. Create two event types with **these exact slugs**:
   - `mastering-espresso` — 3 h
   - `water-espresso-filter` — 4 h

   For each: set your availability (recurring hours or specific date
   overrides for scheduled sessions), and make it a **group event with
   4 seats** to match the max-4 class size.
3. Set `site.calcom_username` in `translations.json`, rebuild, push.

Result: course buttons become "Choisir une date" links opening the Cal.com
calendar (visitor picks date & time; both sides get invites + email
confirmations). The booking URL is also injected into the Course JSON-LD
for SEO. Booking opens on cal.com in a new tab — no third-party script runs
on your site, so nothing extra to declare in the cookie banner.

To add a third course later: add the course object in all three languages
with a new `calcom_event` slug, create the matching event type on Cal.com,
rebuild.

---

## 7. Contact form, WhatsApp

- **Formspree** (free tier: 50 submissions/month): create a form pointing
  to your email, put the endpoint in `site.formspree`. The form submits via
  AJAX with translated sending/success/error states, a honeypot anti-spam
  field, and pushes a `contact_form_submit` event to the dataLayer on
  success (usable as a GTM conversion trigger).
- **WhatsApp**: buttons link to `wa.me/32480658012` (change in
  `site.whatsapp`).
- The "Réserver ce cours" fallback buttons and the coffee "Commander"
  buttons pre-select the matching subject in the form's dropdown.

---

## 8. Branding note — logo

The logo and OG image are hot-linked from evasiongusto.be
(`site.logo`, `site.og_image`). This works, but for independence copy
`logo-nobackground.svg` into `/images/` in this repo and update the paths —
then the coffee site never depends on the main site being up.

---

## 9. GDPR & analytics

### Consent model
Three categories, managed in `js/main.js`:

| Category   | Default in modal | Behaviour |
|------------|------------------|-----------|
| Essential  | always on        | Consent storage only |
| Analytics  | pre-checked      | GA4 via GTM |
| Marketing  | pre-checked      | Google Ads / remarketing via GTM |

- **Nothing loads before an explicit click.** GTM is injected only after
  the visitor clicks "Accepter tout" or saves preferences with at least one
  category enabled. (Pre-ticked boxes alone are not valid GDPR consent —
  the affirmative click is what makes it lawful.)
- Choice is stored in `localStorage` (`eg-coffee-consent-v1`) with a
  version and timestamp. Bump `consentVersion` in `main.js` to re-prompt
  everyone after a policy change.
- Banner: Accept all / Reject all / Manage preferences (modal with
  per-category checkboxes; closes via button, ✕, overlay click, or Esc).
- Footer link "Gérer les cookies" reopens the modal anytime (withdrawal).
- Consent state is pushed to the dataLayer as a `consent_update` event with
  `analytics_storage` / `ad_storage` granted/denied.

### GTM / GA4 setup
1. Create a GTM container, set `site.gtm_id`, rebuild.
2. In GTM add a **GA4 Configuration** tag. Recommended: fire it on the
   custom event `consent_update` with a condition
   `consent.analytics_storage equals granted` (or use GTM's built-in
   Consent Mode settings on the tag).
3. Optional conversion: trigger on custom event `contact_form_submit`.
4. Verify with GTM Preview mode + Google Tag Assistant.

---

## 10. SEO & AI search

Already built in — nothing to do besides launching:

- Per-language `<title>`, meta description/keywords, canonical URLs,
  `hreflang` alternates (+ `x-default`), Open Graph & Twitter cards.
- JSON-LD on every page: `LocalBusiness` (with parentOrganization
  Évasion Gusto, address, areaServed, offers for every course & coffee),
  `FAQPage`, `BreadcrumbList`.
- `sitemap.xml` with hreflang alternates; referenced from `robots.txt`.
- `robots.txt` explicitly welcomes AI crawlers (GPTBot, OAI-SearchBot,
  ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended…).
- `llms.txt` gives answer engines a concise structured summary.
- Semantic HTML5 landmarks, lazy-loaded images with width/height set.

**After launch:**
1. Google Search Console → add property `coffee.evasiongusto.be` → submit
   `sitemap.xml`.
2. Bing Webmaster Tools → same (feeds Bing + several AI answer engines).
3. Create a Google Business Profile for the courses in Beaumont and link
   the site.
4. Cross-link from evasiongusto.be (e.g. a "Coffee" menu item) — the
   strongest SEO signal you control.

---

## 11. Maintenance cheat-sheet

| Task | How |
|------|-----|
| Change a price | Edit `translations.json` (×3 languages) → rebuild → push |
| Add a coffee | Add object to `coffees[]` in each language → add photo → rebuild |
| New announcement | Edit `announcement` per language → rebuild |
| Hide announcement | Set `announcement` to `""` → rebuild |
| Pause bookings | Toggle the event type off in Cal.com (no site change) |
| Re-prompt cookie consent | Increment `consentVersion` in `js/main.js` |
| Update hero video | Replace `media/hero.mp4` → push |

### Troubleshooting

- **Page unstyled locally** — you opened the file directly; serve with
  `python3 -m http.server` instead (absolute paths).
- **Changes don't appear** — you edited a generated file, or forgot to run
  `python3 build/build.py` before pushing. Hard-refresh (Ctrl+F5).
- **Form does nothing** — `formspree` still contains `YOUR_FORM_ID`.
- **No analytics data** — GTM ID still placeholder, no GA4 tag inside the
  container, or you tested without accepting cookies.
- **Booking button goes to the form** — `calcom_username` still placeholder.
- **HTTPS warning on custom domain** — wait for GitHub's certificate, then
  enable *Enforce HTTPS*.

---

## 12. Pre-launch checklist

- [ ] `gtm_id` set + GA4 tag configured in GTM
- [ ] `formspree` endpoint set + test submission received by email
- [ ] Cal.com: 2 event types created, username set, test booking made
- [ ] Coffee photos in `/images/`, banner photo, hero video in `/media/`
- [ ] Real prices & coffee list reviewed in all 3 languages
- [ ] DNS CNAME added, HTTPS enforced
- [ ] Search Console + Bing: property added, sitemap submitted
- [ ] Link added on evasiongusto.be pointing here

---

© Évasion Gusto — BE 1009.024.385. Site generated with a custom static
build (no framework, no dependencies beyond Python 3 for the generator).
