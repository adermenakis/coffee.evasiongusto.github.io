#!/usr/bin/env python3
"""Build coffee.evasiongusto.be — generates index.html (FR), en/, nl/, sitemap.xml
Usage: python3 build/build.py   (run from repo root)"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "build", "translations.json"), encoding="utf-8"))
SITE = DATA["site"]

def cal_link(course):
    """Cal.com booking URL for a course, or None if not configured yet."""
    user = SITE.get("calcom_username", "")
    slug = course.get("calcom_event", "")
    if user and "YOUR_" not in user and slug:
        return f"https://cal.com/{user}/{slug}"
    return None
LANGS = DATA["langs"]

e = html.escape

def acc(text):
    """Escape, then turn *word* into an oak italic accent."""
    return re.sub(r"\*(.+?)\*", r'<em class="accent">\1</em>', e(text))

# ---------------------------------------------------------------- SVG icons
ICONS = {
"portafilter": '<path d="M3 7h14v3a5 5 0 0 1-5 5h-4a5 5 0 0 1-5-5V7Z"/><path d="M17 8h3a1 1 0 0 1 0 3h-3"/><path d="M8 15v2M12 15v2"/>',
"drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/><path d="M9.5 14a2.5 2.5 0 0 0 2.5 2.5"/>',
"flower": '<circle cx="12" cy="12" r="2.4"/><path d="M12 4.5a2.6 2.6 0 0 1 0 5.2M12 14.3a2.6 2.6 0 0 1 0 5.2M4.5 12a2.6 2.6 0 0 1 5.2 0M14.3 12a2.6 2.6 0 0 1 5.2 0"/>',
"cherry": '<circle cx="8.5" cy="15.5" r="3.2"/><circle cx="15.5" cy="16" r="2.8"/><path d="M8.5 12.3C9 8.5 11 6 14.5 4.5M15.5 13.2c-.2-3 1-5.5 3-7"/>',
"bean": '<path d="M6.3 6.3a8 8 0 0 1 11.4 11.4A8 8 0 0 1 6.3 6.3Z"/><path d="M6.3 6.3c3.5 1 4.2 4 4 6s.6 4.6 3.4 5.4"/>',
"moon": '<path d="M20 13.5A8 8 0 1 1 10.5 4 6.5 6.5 0 0 0 20 13.5Z"/>',
"clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
"users": '<circle cx="9" cy="8.5" r="3"/><path d="M3.5 19a5.5 5.5 0 0 1 11 0"/><path d="M15.5 5.8a3 3 0 0 1 0 5.4M17 13.6a5.5 5.5 0 0 1 3.5 5.4"/>',
"tag": '<path d="M4 4h7l9 9-7 7-9-9V4Z"/><circle cx="8.5" cy="8.5" r="1.4"/>',
"pin": '<path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11Z"/><circle cx="12" cy="10" r="2.5"/>',
"mail": '<rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="m4.5 7 7.5 6 7.5-6"/>',
"phone": '<path d="M6.5 3.5h3l1.5 4-2 1.5a12 12 0 0 0 6 6l1.5-2 4 1.5v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.5 5.7 2 2 0 0 1 6.5 3.5Z"/>',
"whatsapp": '<path d="M12 3.8a8.2 8.2 0 0 0-7 12.4L4 20l3.9-1a8.2 8.2 0 1 0 4.1-15.2Z"/><path d="M9.3 8.6c-.3.8-.3 2 .8 3.6 1.2 1.7 2.4 2.4 3.5 2.7.9.2 1.6-.4 1.8-1l-1.9-1.1-.9.7c-.8-.4-1.6-1.2-2.1-2.1l.8-.8-1-2h-1Z"/>',
"arrow": '<path d="M5 12h13M13 6.5 18.5 12 13 17.5"/>',
"globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c-4.5 4.7-4.5 12.3 0 17 4.5-4.7 4.5-12.3 0-17Z"/>',
}

def icon(name, cls="icn"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')

# ---------------------------------------------------------------- Hero artwork
HERO_ART = '''
<div class="hero-art" aria-hidden="true">
<svg viewBox="0 0 340 400" class="brew" role="img" aria-label="">
  <!-- gauge -->
  <g class="gauge">
    <circle cx="272" cy="64" r="34" class="gauge-face"/>
    <g class="ticks">
      <line x1="272" y1="36" x2="272" y2="42"/><line x1="248" y1="50" x2="253" y2="53"/>
      <line x1="296" y1="50" x2="291" y2="53"/><line x1="244" y1="72" x2="250" y2="71"/>
      <line x1="300" y1="72" x2="294" y2="71"/>
    </g>
    <line x1="272" y1="64" x2="272" y2="40" class="needle"/>
    <circle cx="272" cy="64" r="3.2" class="hub"/>
  </g>
  <!-- group head -->
  <rect x="90" y="40" width="130" height="52" rx="10" class="head"/>
  <rect x="118" y="92" width="74" height="16" rx="5" class="collar"/>
  <!-- portafilter -->
  <path d="M126 108h58v10a14 14 0 0 1-14 14h-30a14 14 0 0 1-14-14v-10Z" class="pf"/>
  <rect x="184" y="110" width="64" height="9" rx="4.5" class="pf-handle"/>
  <path d="M146 132v8M164 132v8" class="spouts"/>
  <!-- streams -->
  <line x1="146" y1="142" x2="146" y2="236" class="stream s1"/>
  <line x1="164" y1="142" x2="164" y2="236" class="stream s2"/>
  <!-- cup -->
  <g class="cup">
    <path d="M118 238h74l-7 46a12 12 0 0 1-12 10h-36a12 12 0 0 1-12-10l-7-46Z" class="cup-body"/>
    <path d="M192 246h14a12 12 0 0 1 0 24h-10" class="cup-handle"/>
    <clipPath id="cupclip"><path d="M118 238h74l-7 46a12 12 0 0 1-12 10h-36a12 12 0 0 1-12-10l-7-46Z"/></clipPath>
    <rect x="112" y="294" width="88" height="60" class="coffee-fill" clip-path="url(#cupclip)"/>
    <path d="M122 250h66" class="crema"/>
  </g>
  <!-- steam -->
  <g class="steam">
    <path d="M140 222c-5-8 5-12 0-20" class="wisp w1"/>
    <path d="M156 218c-5-9 5-13 0-22" class="wisp w2"/>
    <path d="M172 222c-5-8 5-12 0-20" class="wisp w3"/>
  </g>
  <!-- base line -->
  <line x1="70" y1="300" x2="270" y2="300" class="base"/>
</svg>
</div>'''

# ---------------------------------------------------------------- JSON-LD
def jsonld(L, url):
    biz = {
        "@context": "https://schema.org", "@type": "LocalBusiness",
        "name": "Évasion Gusto Coffee", "url": url,
        "image": SITE["og_image"], "logo": SITE["logo"],
        "description": L["description"],
        "telephone": "+32480658012", "email": SITE["email"],
        "parentOrganization": {"@type": "Organization", "name": "Évasion Gusto", "url": "https://www.evasiongusto.be"},
        "address": {"@type": "PostalAddress", "streetAddress": "Rue Orger Meurice 12",
                    "postalCode": "6500", "addressLocality": "Beaumont", "addressCountry": "BE"},
        "areaServed": ["Beaumont", "Mons", "Charleroi", "Thuin", "Chimay", "Hainaut", "Belgique"],
        "sameAs": ["https://www.evasiongusto.be", "https://www.facebook.com/profile.php?id=61563989882231"],
        "makesOffer": []
    }
    for c in L["courses"]:
        link = cal_link(c)
        offer = {
            "@type": "Offer",
            "priceCurrency": "EUR",
            "price": "".join(ch for ch in c["price"] if ch.isdigit() or ch == "."),
            "itemOffered": {
                "@type": "Course", "name": c["name"], "description": c["desc"],
                "provider": {"@type": "Organization", "name": "Évasion Gusto Coffee", "url": url},
                "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Onsite",
                                      "location": {"@type": "Place", "name": "Évasion Gusto, Beaumont"}}
            }}
        if link:
            offer["url"] = link
        biz["makesOffer"].append(offer)
    for p in L["coffees"]:
        biz["makesOffer"].append({
            "@type": "Offer", "priceCurrency": "EUR",
            "price": "".join(ch for ch in p["price"] if ch.isdigit() or ch in ".,").replace(",", "."),
            "itemOffered": {"@type": "Product", "name": p["name"] + " — " + p["weight"],
                            "description": f'{p["origin"]} · {p["process"]} · {p["notes"]}',
                            "brand": {"@type": "Brand", "name": "Évasion Gusto Coffee"}}})
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": f["q"],
                           "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in L["faq"]]}
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                  "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Évasion Gusto",
                                       "item": "https://www.evasiongusto.be"},
                                      {"@type": "ListItem", "position": 2, "name": "Coffee", "item": url}]}
    return "\n".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>'
                     for d in (biz, faq, breadcrumb))

# ---------------------------------------------------------------- page pieces
def head(L, code):
    url = SITE["domain"] + "/" + L["path"]
    alt = "\n".join(
        f'  <link rel="alternate" hreflang="{LANGS[k]["html_lang"]}" href="{SITE["domain"]}/{LANGS[k]["path"]}">'
        for k in LANGS)
    return f'''<!DOCTYPE html>
<html lang="{L["html_lang"]}" data-gtm="{SITE["gtm_id"]}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(L["title"])}</title>
  <meta name="description" content="{e(L["description"])}">
  <meta name="keywords" content="{e(L["keywords"])}">
  <meta name="author" content="Évasion Gusto">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{url}">
{alt}
  <link rel="alternate" hreflang="x-default" href="{SITE["domain"]}/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Évasion Gusto Coffee">
  <meta property="og:locale" content="{L["locale"]}">
  <meta property="og:title" content="{e(L["title"])}">
  <meta property="og:description" content="{e(L["description"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE["og_image"]}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(L["title"])}">
  <meta name="twitter:description" content="{e(L["description"])}">
  <meta name="twitter:image" content="{SITE["og_image"]}">
  <meta name="theme-color" content="#17110C">
  <link rel="icon" href="{SITE["logo"]}" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,560;0,9..144,640;1,9..144,460&family=Archivo:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
{jsonld(L, url)}
</head>'''

def nav(L, code):
    n = L["nav"]
    links = "".join(f'<li><a href="#{k}">{e(v)}</a></li>'
                    for k, v in (("courses", n["courses"]), ("machine", n["machine"]),
                                 ("coffees", n["coffees"]), ("faq", n["faq"])))
    langsw = "".join(
        f'<a href="/{LANGS[k]["path"]}" class="lang{" active" if k == code else ""}" '
        f'hreflang="{LANGS[k]["html_lang"]}" lang="{LANGS[k]["html_lang"]}">{k.upper()}</a>'
        for k in LANGS)
    ann = f'<div class="announce"><div class="wrap">{e(L["announcement"])}</div></div>\n' if L.get("announcement") else ""
    return ann + f'''<header class="site-header" id="top">
  <div class="wrap nav-wrap">
    <a class="brand" href="/{L["path"]}" aria-label="Évasion Gusto Coffee">
      <img src="{SITE["logo"]}" alt="Évasion Gusto" width="46" height="46" loading="eager">
      <span class="brand-word">Coffee</span>
    </a>
    <nav class="main-nav" aria-label="Main">
      <ul>{links}<li><a class="nav-cta" href="#contact">{e(n["contact"])}</a></li></ul>
    </nav>
    <div class="lang-switch" role="navigation" aria-label="Languages">{icon("globe","icn icn-s")}{langsw}</div>
    <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>'''

def hero(L):
    h = L["hero"]
    vid = ""
    if SITE.get("hero_video"):
        poster = f' poster="{SITE["hero_poster"]}"' if SITE.get("hero_poster") else ""
        vid = (f'<video class="hero-video" autoplay muted loop playsinline '
               f'preload="metadata"{poster} aria-hidden="true" tabindex="-1">'
               f'<source src="{SITE["hero_video"]}" type="video/mp4"></video>\n  ')
    return f'''<section class="hero">
  {vid}
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">{e(h["eyebrow"])}</p>
      <h1>{acc(h["title"])}</h1>
      <p class="lede">{e(h["sub"])}</p>
      <div class="cta-row">
        <a class="btn btn-solid" href="#courses">{e(h["cta_courses"])} {icon("arrow","icn icn-s")}</a>
        <a class="btn btn-line" href="#contact">{e(h["cta_book"])}</a>
      </div>
    </div>
    {HERO_ART}
  </div>
</section>'''

def courses(L):
    s = L["courses_section"]
    cards = ""
    for i, c in enumerate(L["courses"], 1):
        pts = "".join(f"<li>{e(p)}</li>" for p in c["points"])
        link = cal_link(c)
        if link:
            booking_btn = (f'<a class="btn btn-solid btn-sm" href="{link}" target="_blank" '
                           f'rel="noopener">{e(s.get("book_online", s["book"]))} {icon("arrow","icn icn-s")}</a>')
        else:
            booking_btn = f'<a class="btn btn-solid btn-sm" href="#contact" data-interest="{i-1}">{e(s["book"])}</a>'
        cards += f'''
    <article class="course-card reveal" id="course-{c["id"]}">
      <div class="course-head">{icon(c["icon"], "icn icn-l")}<span class="course-no">N°{i}</span></div>
      <h3>{e(c["name"])}</h3>
      <p class="tagline">{e(c["tagline"])}</p>
      <p>{e(c["desc"])}</p>
      <ul class="points">{pts}</ul>
      <dl class="course-meta">
        <div>{icon("clock","icn icn-s")}<dt>{e(s["duration_label"])}</dt><dd>{e(c["duration"])}</dd></div>
        <div>{icon("tag","icn icn-s")}<dt>{e(s["price_label"])}</dt><dd>{e(c["price"])}</dd></div>
        <div>{icon("users","icn icn-s")}<dt>{e(s["group_label"])}</dt><dd>{e(c["group"])}</dd></div>
      </dl>
      {booking_btn}
    </article>'''
    return f'''<section class="section section-light" id="courses">
  <div class="wrap">
    <p class="eyebrow reveal">{e(s["eyebrow"])}</p>
    <h2 class="reveal">{acc(s["title"])}</h2>
    <p class="section-intro reveal">{e(s["intro"])}</p>
    <div class="course-grid">{cards}</div>
  </div>
</section>'''

def machine(L):
    m = L["machine"]
    specs = "".join(f'<div class="spec reveal"><dt>{e(x["k"])}</dt><dd>{e(x["v"])}</dd></div>' for x in m["specs"])
    return f'''<section class="section section-dark" id="machine">
  <div class="wrap machine-grid">
    <div>
      <p class="eyebrow reveal">{e(m["eyebrow"])}</p>
      <h2 class="reveal">{acc(m["title"])}</h2>
      <p class="section-intro on-dark reveal">{e(m["desc"])}</p>
    </div>
    <dl class="spec-list">{specs}</dl>
  </div>
</section>'''

def coffees(L):
    s = L["coffees_section"]
    cards = ""
    for p in L["coffees"]:
        pic = p.get("picture", "")
        img = f'<img src="{pic}" alt="{e(p["name"])}" width="280" height="180" loading="lazy" class="coffee-pic">' if pic else ""
        cards += f'''
    <article class="coffee-card reveal">
      {img}
      <div class="coffee-content">
        <div class="coffee-icon">{icon(p["icon"], "icn icn-l")}</div>
        <h3>{e(p["name"])}</h3>
        <dl class="coffee-meta">
          <div><dt>{e(s["origin_label"])}</dt><dd>{e(p["origin"])}</dd></div>
          <div><dt>{e(s["process_label"])}</dt><dd>{e(p["process"])}</dd></div>
          <div><dt>{e(s["notes_label"])}</dt><dd>{e(p["notes"])}</dd></div>
        </dl>
        <div class="coffee-buy">
          <span class="price">{e(p["price"])} <small>/ {e(p["weight"])}</small></span>
          <a class="btn btn-line btn-sm" href="#contact" data-interest="2">{e(s["buy"])}</a>
        </div>
      </div>
    </article>'''
    return f'''<section class="section section-cream" id="coffees">
  <div class="wrap">
    <p class="eyebrow reveal">{e(s["eyebrow"])}</p>
    <h2 class="reveal">{acc(s["title"])}</h2>
    <p class="section-intro reveal">{e(s["intro"])}</p>
    <div class="coffee-grid">{cards}</div>
  </div>
</section>'''

def banner(L):
    bn = L.get("banner")
    if not bn:
        return ""
    img = SITE.get("banner_image", "")
    style = f' style="background-image:url({img})"' if img else ""
    return f'''<section class="banner"{style} id="gift">
  <div class="wrap banner-inner">
    <p class="eyebrow reveal">{e(bn["eyebrow"])}</p>
    <h2 class="reveal">{acc(bn["title"])}</h2>
    <p class="banner-text reveal">{e(bn["text"])}</p>
    <a class="btn btn-banner reveal" href="#contact" data-interest="3">{e(bn["cta"])}</a>
  </div>
</section>'''

def faq(L):
    s = L["faq_section"]
    items = "".join(
        f'<details class="faq-item reveal"><summary>{e(f["q"])}</summary><p>{e(f["a"])}</p></details>'
        for f in L["faq"])
    return f'''<section class="section section-light" id="faq">
  <div class="wrap wrap-narrow">
    <p class="eyebrow reveal">{e(s["eyebrow"])}</p>
    <h2 class="reveal">{acc(s["title"])}</h2>
    <div class="faq-list">{items}</div>
  </div>
</section>'''

def contact(L):
    c = L["contact"]
    opts = "".join(f'<option>{e(o)}</option>' for o in c["interest_options"])
    return f'''<section class="section section-dark" id="contact">
  <div class="wrap contact-grid">
    <div>
      <p class="eyebrow reveal">{e(c["eyebrow"])}</p>
      <h2 class="reveal">{acc(c["title"])}</h2>
      <p class="section-intro on-dark reveal">{e(c["intro"])}</p>
      <div class="contact-details reveal">
        <h3 class="details-title">{e(c["details_title"])}</h3>
        <p>{icon("pin","icn icn-s")} {e(SITE["address"])}</p>
        <p>{icon("mail","icn icn-s")} <a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>
        <p>{icon("phone","icn icn-s")} <a href="{SITE["phone_link"]}">{e(SITE["phone_display"])}</a></p>
      </div>
      <p class="or reveal">{e(c["or"])}</p>
      <a class="btn btn-wa reveal" href="{SITE["whatsapp"]}" target="_blank" rel="noopener">{icon("whatsapp","icn")} {e(c["whatsapp"])}</a>
    </div>
    <form class="contact-form reveal" action="{SITE["formspree"]}" method="POST"
          data-sending="{e(c["sending"])}" data-success="{e(c["success"])}" data-error="{e(c["error"])}">
      <label>{e(c["name"])}<input type="text" name="name" required autocomplete="name"></label>
      <label>{e(c["email"])}<input type="email" name="email" required autocomplete="email"></label>
      <label>{e(c["interest"])}<select name="interest" id="interest">{opts}</select></label>
      <label>{e(c["message"])}<textarea name="message" rows="5" required></textarea></label>
      <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off">
      <button type="submit" class="btn btn-solid">{e(c["send"])}</button>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>'''

def footer(L):
    f = L["footer"]
    c = L.get("consent", {})
    prefs = L.get("consent_preferences", {})
    return f'''<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="{SITE["logo"]}" alt="Évasion Gusto" width="52" height="52" loading="lazy">
      <p>{e(f["tagline"])}</p>
    </div>
    <div class="footer-links">
      <a href="https://www.evasiongusto.be">{e(f["main_site"])}</a>
      <a href="{SITE["whatsapp"]}" rel="noopener" target="_blank">WhatsApp</a>
      <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>
      <a href="#" data-open-prefs aria-label="Manage cookies">{e(prefs.get("manage_cookies", "Manage cookies"))}</a>
    </div>
  </div>
  <p class="footer-motto">{e(f.get("motto",""))}</p>
  <div class="wrap footer-legal">
    <p>© 2026 Évasion Gusto — {SITE["vat"]}. {e(f["rights"])}</p>
  </div>
</footer>

<!-- GDPR Consent Banner -->
<div class="consent" hidden role="dialog" aria-labelledby="consent-title">
  <div class="consent-content">
    <div class="consent-header">
      <div>
        <h3 id="consent-title">{e(c.get("title", "Your privacy matters"))}</h3>
        <p>{e(c.get("text", "We use cookies to improve your experience, analyze traffic, and serve relevant content. You can choose what you're comfortable with."))}</p>
      </div>
      <div class="consent-lang-switcher" role="navigation" aria-label="Languages in consent">
        <svg class="icn icn-xs" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c-4.5 4.7-4.5 12.3 0 17 4.5-4.7 4.5-12.3 0-17Z"/></svg>
        <a href="/" class="consent-lang" hreflang="fr" lang="fr" data-lang="fr">FR</a>
        <a href="/en/" class="consent-lang" hreflang="en" lang="en" data-lang="en">EN</a>
        <a href="/nl/" class="consent-lang" hreflang="nl" lang="nl" data-lang="nl">NL</a>
      </div>
    </div>
    <div class="consent-buttons">
      <button class="btn btn-sm btn-solid" data-consent="accept-all">{e(c.get("accept_all", "Accept all"))}</button>
      <button class="btn btn-sm btn-line" data-consent="reject-all">{e(c.get("reject_all", "Reject all"))}</button>
      <button class="btn btn-sm btn-line" data-consent="preferences">{e(c.get("manage", "Manage preferences"))}</button>
    </div>
  </div>
</div>

<!-- Preferences Modal -->
<div class="consent-preferences-modal" hidden role="dialog" aria-labelledby="prefs-title">
  <div class="consent-prefs-overlay"></div>
  <div class="consent-prefs-panel">
    <div class="consent-prefs-head">
      <h2 id="prefs-title">{e(prefs.get("title", "Privacy preferences"))}</h2>
    </div>
    <div class="consent-prefs-body">
      <div class="consent-pref-group">
        <label class="pref-label">
          <input type="checkbox" disabled checked class="pref-check">
          <div>
            <strong>{e(prefs.get("necessary", "Essential cookies"))}</strong>
            <p>{e(prefs.get("necessary_desc", "Required for the site to function (security, consent tracking)."))}</p>
          </div>
        </label>
      </div>
      <div class="consent-pref-group">
        <label class="pref-label">
          <input type="checkbox" checked data-pref-analytics class="pref-check">
          <div>
            <strong>{e(prefs.get("analytics", "Analytics"))}</strong>
            <p>{e(prefs.get("analytics_desc", "Help us understand how you use the site (page views, form submissions) via Google Analytics."))}</p>
          </div>
        </label>
      </div>
      <div class="consent-pref-group">
        <label class="pref-label">
          <input type="checkbox" checked data-pref-marketing class="pref-check">
          <div>
            <strong>{e(prefs.get("marketing", "Marketing & remarketing"))}</strong>
            <p>{e(prefs.get("marketing_desc", "Let Google show you relevant ads based on your visit (Google Ads, YouTube)."))}</p>
          </div>
        </label>
      </div>
    </div>
    <div class="consent-prefs-footer">
      <button class="btn btn-solid" data-save-prefs>{e(prefs.get("save", "Accept and close"))}</button>
      <p class="consent-prefs-note">{e(prefs.get("note", "You can change these settings anytime via the footer link."))}</p>
    </div>
  </div>
</div>

<script src="/js/main.js" defer></script>
</body>
</html>'''

def build_page(code):
    L = LANGS[code]
    page = (head(L, code) + "\n<body>\n" + nav(L, code) + "\n<main id=\"main\">\n"
            + hero(L) + courses(L) + machine(L) + coffees(L) + banner(L) + faq(L) + contact(L)
            + "\n</main>\n" + footer(L))
    out = os.path.join(ROOT, L["path"], "index.html")
    os.makedirs(os.path.dirname(out) or ROOT, exist_ok=True)
    open(out, "w", encoding="utf-8").write(page)
    print("built", out)

def build_sitemap():
    urls = ""
    for code, L in LANGS.items():
        loc = SITE["domain"] + "/" + L["path"]
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{LANGS[k]["html_lang"]}" '
                       f'href="{SITE["domain"]}/{LANGS[k]["path"]}"/>' for k in LANGS)
        urls += f'<url><loc>{loc}</loc>{alts}<changefreq>monthly</changefreq><priority>{"1.0" if code=="fr" else "0.9"}</priority></url>\n'
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + '</urlset>\n')
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(xml)
    print("built sitemap.xml")

if __name__ == "__main__":
    for code in LANGS:
        build_page(code)
    build_sitemap()
