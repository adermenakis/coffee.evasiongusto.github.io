/* Évasion Gusto Coffee — main.js */
(function () {
  "use strict";

  var GTM_ID = document.documentElement.getAttribute("data-gtm");
  var CONSENT_VERSION = 1;
  var CONSENT_KEY = "eg-coffee-consent-v" + CONSENT_VERSION;

  // Detect current language
  function getCurrentLang() {
    if (window.location.pathname.startsWith("/en/")) return "en";
    if (window.location.pathname.startsWith("/nl/")) return "nl";
    return "fr";
  }

  // Get stored consent
  function getStoredConsent() {
    try {
      var stored = localStorage.getItem(CONSENT_KEY);
      if (stored) return JSON.parse(stored);
    } catch (e) {}
    return null;
  }

  // Save consent
  function saveConsent(analytics, marketing) {
    var obj = {
      necessary: true,
      analytics: !!analytics,
      marketing: !!marketing,
      version: CONSENT_VERSION,
      timestamp: new Date().toISOString()
    };
    try {
      localStorage.setItem(CONSENT_KEY, JSON.stringify(obj));
    } catch (e) {}
    applyConsent(obj);
  }

  // Apply consent (push to GTM dataLayer)
  function applyConsent(consent) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: "consent_update",
      consent: {
        analytics_storage: consent.analytics ? "granted" : "denied",
        ad_storage: consent.marketing ? "granted" : "denied"
      }
    });

    // Load GTM if enabled
    if ((consent.analytics || consent.marketing) && GTM_ID && GTM_ID.indexOf("GTM-") === 0 && GTM_ID !== "GTM-XXXXXXX") {
      if (!window.gtmLoaded) {
        window.gtmLoaded = true;
        var script = document.createElement("script");
        script.async = true;
        script.src = "https://www.googletagmanager.com/gtm.js?id=" + GTM_ID;
        document.head.appendChild(script);
      }
    }
  }

  // Initialize on DOM ready
  function init() {
    var banner = document.querySelector(".consent");
    var modal = document.querySelector(".consent-preferences-modal");

    if (!banner) return;

    // Show banner only if no consent stored
    var stored = getStoredConsent();
    if (!stored || stored.version !== CONSENT_VERSION) {
      banner.hidden = false;
    }

    // Mark active language
    var currentLang = getCurrentLang();
    banner.querySelectorAll("[data-lang]").forEach(function(link) {
      if (link.getAttribute("data-lang") === currentLang) {
        link.classList.add("active");
      }
    });

    // Banner: Accept All
    var acceptBtn = banner.querySelector('[data-consent="accept-all"]');
    if (acceptBtn) {
      acceptBtn.addEventListener("click", function(e) {
        e.preventDefault();
        e.stopPropagation();
        saveConsent(true, true);
        banner.hidden = true;
      }, false);
    }

    // Banner: Reject All
    var rejectBtn = banner.querySelector('[data-consent="reject-all"]');
    if (rejectBtn) {
      rejectBtn.addEventListener("click", function(e) {
        e.preventDefault();
        e.stopPropagation();
        saveConsent(false, false);
        banner.hidden = true;
      }, false);
    }

    // Banner: Manage Preferences
    var manageBtn = banner.querySelector('[data-consent="preferences"]');
    if (manageBtn && modal) {
      manageBtn.addEventListener("click", function(e) {
        e.preventDefault();
        e.stopPropagation();
        var s = getStoredConsent() || { analytics: true, marketing: true };
        var analyticsCheckbox = document.querySelector("[data-pref-analytics]");
        var marketingCheckbox = document.querySelector("[data-pref-marketing]");
        if (analyticsCheckbox) analyticsCheckbox.checked = s.analytics;
        if (marketingCheckbox) marketingCheckbox.checked = s.marketing;
        modal.hidden = false;
      }, false);
    }

    // Modal: Save Preferences
    var saveBtn = document.querySelector('[data-save-prefs]');
    if (saveBtn) {
      saveBtn.addEventListener("click", function(e) {
        e.preventDefault();
        e.stopPropagation();
        var analytics = document.querySelector("[data-pref-analytics]");
        var marketing = document.querySelector("[data-pref-marketing]");
        saveConsent(analytics && analytics.checked, marketing && marketing.checked);
        if (modal) modal.hidden = true;
        banner.hidden = true;
      }, false);
    }

    // Modal: Prevent closing via overlay
    var overlay = document.querySelector(".consent-prefs-overlay");
    if (overlay) {
      overlay.addEventListener("click", function(e) {
        e.preventDefault();
        e.stopPropagation();
      }, false);
    }

    // Apply existing consent immediately
    if (stored) {
      applyConsent(stored);
    }
  }

  // Wait for DOM
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, false);
  } else {
    init();
  }

  // Preferences modal (if it exists)
  var prefsModal = document.querySelector(".consent-preferences-modal");
  var prefsOverlay = document.querySelector(".consent-prefs-overlay");
  
  function openPreferencesModal() {
    if (prefsModal) {
      var consent = getConsent() || defaultConsent; // pre-checked by default
      var analyticsChk = document.querySelector("[data-pref-analytics]");
      var marketingChk = document.querySelector("[data-pref-marketing]");
      if (analyticsChk) analyticsChk.checked = consent.analytics;
      if (marketingChk) marketingChk.checked = consent.marketing;
      prefsModal.hidden = false;
    }
  }

  function closePreferencesModal() {
    if (prefsModal) prefsModal.hidden = true;
  }

  // Close button
  var closePrefsBtn = document.querySelector("[data-close-prefs]");
  if (closePrefsBtn) {
    closePrefsBtn.addEventListener("click", closePreferencesModal);
  }

  // Save button
  var savePrefsBtn = document.querySelector("[data-save-prefs]");
  if (savePrefsBtn) {
    savePrefsBtn.addEventListener("click", function () {
      var analytics = document.querySelector("[data-pref-analytics]");
      var marketing = document.querySelector("[data-pref-marketing]");
      setConsent({
        necessary: true,
        analytics: analytics && analytics.checked,
        marketing: marketing && marketing.checked
      });
      closePreferencesModal();
      if (consentBox) consentBox.hidden = true;
    });
  }

  // Overlay click to close
  if (prefsOverlay) {
    prefsOverlay.addEventListener("click", closePreferencesModal);
  }

  // ESC key to close modal
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape" && !prefsModal.hidden) {
      closePreferencesModal();
    }
  });

  // Footer "manage cookies" link
  var manageCookiesLinks = document.querySelectorAll("[data-open-prefs]");
  if (manageCookiesLinks) {
    manageCookiesLinks.forEach(function (link) {
      link.addEventListener("click", function (ev) {
        ev.preventDefault();
        openPreferencesModal();
      });
    });
  }

  // Apply only a previously SAVED choice — no tags load before the user clicks
  if (storedConsent) applyConsent(storedConsent);

  /* ---------- Hero background video ---------- */
  var vid = document.querySelector(".hero-video");
  if (vid) {
    var heroEl = document.querySelector(".hero");
    vid.addEventListener("loadeddata", function () { heroEl.classList.add("has-video"); });
    var src = vid.querySelector("source");
    if (src) src.addEventListener("error", function () { vid.remove(); });
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      vid.removeAttribute("autoplay");
      vid.pause();
    }
  }

  /* ---------- Sticky header shadow ---------- */
  var header = document.querySelector(".site-header");
  window.addEventListener("scroll", function () {
    header.classList.toggle("scrolled", window.scrollY > 10);
  }, { passive: true });

  /* ---------- Mobile nav ---------- */
  var burger = document.querySelector(".burger");
  var nav = document.querySelector(".main-nav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      burger.classList.toggle("open", open);
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (ev) {
      if (ev.target.tagName === "A") {
        nav.classList.remove("open");
        burger.classList.remove("open");
        burger.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---------- Scroll reveals ---------- */
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var reveals = document.querySelectorAll(".reveal");
  if (reduced || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- "Book this course" pre-selects the interest ---------- */
  var interest = document.getElementById("interest");
  document.querySelectorAll("[data-interest]").forEach(function (a) {
    a.addEventListener("click", function () {
      if (!interest) return;
      var i = parseInt(a.getAttribute("data-interest"), 10);
      if (interest.options[i]) interest.selectedIndex = i;
    });
  });

  /* ---------- Contact form (Formspree, AJAX) ---------- */
  var form = document.querySelector(".contact-form");
  if (form) {
    form.addEventListener("submit", function (ev) {
      var action = form.getAttribute("action") || "";
      if (action.indexOf("YOUR_FORM_ID") !== -1) return; // not configured yet: normal submit
      ev.preventDefault();
      var status = form.querySelector(".form-status");
      var btn = form.querySelector("button[type=submit]");
      var original = btn.textContent;
      btn.disabled = true;
      btn.textContent = form.getAttribute("data-sending");
      status.className = "form-status";
      fetch(action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" }
      }).then(function (r) {
        if (r.ok) {
          form.reset();
          status.textContent = form.getAttribute("data-success");
          status.classList.add("ok");
          if (window.dataLayer) window.dataLayer.push({ event: "contact_form_submit" });
        } else { throw new Error("bad status"); }
      }).catch(function () {
        status.textContent = form.getAttribute("data-error");
        status.classList.add("err");
      }).finally(function () {
        btn.disabled = false;
        btn.textContent = original;
      });
    });
  }
})();
