"""Render approved legal text into both GitHub Pages language versions."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://autocontract.myprintx.com"
LABELS = {
    "ro": {"privacy": "Politica de confidențialitate", "terms": "Termenii licenței și utilizării", "home": "Acasă", "privacyNav": "Confidențialitate", "termsNav": "Termeni", "skip": "Sari la conținut", "updated": "Actualizat: 2 noiembrie 2026", "contents": "Pe această pagină", "references": "Referințe și servicii externe", "navigation": "Navigare principală", "language": "Limba site-ului", "description": "AutoContract: OCR local, sesiuni temporare, arhivă Pro și Google Drive opțional, achiziții Google Play și condițiile licențelor Personal și Professional."},
    "en": {"privacy": "Privacy policy", "terms": "Licence and usage terms", "home": "Home", "privacyNav": "Privacy", "termsNav": "Terms", "skip": "Skip to content", "updated": "Updated: 2 November 2026", "contents": "On this page", "references": "References and external services", "navigation": "Main navigation", "language": "Website language", "description": "AutoContract: local OCR, temporary sessions, Pro archive, optional Google Drive, Google Play purchases and Personal and Professional licence conditions."},
}
REFERENCES = [
    ("Google ML Kit", "https://developers.google.com/ml-kit/android-data-disclosure"),
    ("Google API Services User Data Policy", "https://developers.google.com/terms/api-services-user-data-policy"),
    ("Google Privacy", "https://policies.google.com/privacy"),
    ("GitHub Privacy", "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement"),
    ("Google Play subscriptions", "https://support.google.com/googleplay/answer/7018481"),
]


def render(kind, filename, lang, sections):
    t = LABELS[lang]
    prefix = "/en" if lang == "en" else ""
    title = t[kind]
    canonical = f"{DOMAIN}{prefix}/{filename}"
    body = "".join(f'<section id="section-{i}"><h2>{i}. {html.escape(heading)}</h2><p>{html.escape(text)}</p></section>' for i, (heading, text) in enumerate(sections, 1))
    contents = "".join(f'<li><a href="#section-{i}">{html.escape(heading)}</a></li>' for i, (heading, _) in enumerate(sections, 1))
    references = "".join(f'<li><a href="{url}">{name}<span aria-hidden="true"> ↗</span></a></li>' for name, url in REFERENCES)
    language_links = "".join(f'<a href="{("/en" if code == "en" else "")}/{filename}?lang={code}" lang="{code}" hreflang="{code}" data-language="{code}"' + (' aria-current="page"' if code == lang else '') + f'>{code.upper()}</a>' for code in ("ro", "en"))
    return f'''<!doctype html>
<html lang="{lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — AutoContract</title><meta name="description" content="{t['description']}">
<meta name="theme-color" content="#071820"><meta name="color-scheme" content="dark">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="ro" href="{DOMAIN}/{filename}">
<link rel="alternate" hreflang="en" href="{DOMAIN}/en/{filename}">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}/{filename}">
<meta property="og:type" content="website"><meta property="og:site_name" content="AutoContract">
<meta property="og:title" content="{title} — AutoContract"><meta property="og:description" content="{t['description']}">
<meta property="og:url" content="{canonical}"><meta property="og:locale" content="{'ro_RO' if lang == 'ro' else 'en_GB'}">
<meta property="og:image" content="{DOMAIN}/assets/social-card.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<link rel="icon" type="image/png" href="/assets/favicon-32.png"><link rel="apple-touch-icon" href="/assets/favicon-180.png">
<link rel="stylesheet" href="/assets/legal.css"><script defer src="/assets/legal-language.js"></script>
</head><body>
<a class="skip" href="#continut">{t['skip']}</a>
<header class="legal-header"><div class="wrap header-inner">
<a class="brand" href="{prefix}/"><img src="/assets/logo-96.webp" width="44" height="44" alt=""><span>Auto<span>Contract</span></span></a>
<nav aria-label="{t['navigation']}"><a href="{prefix}/">{t['home']}</a><a href="{prefix}/confidentialitate.html" {'aria-current="page"' if kind == 'privacy' else ''}>{t['privacyNav']}</a><a href="{prefix}/termeni.html" {'aria-current="page"' if kind == 'terms' else ''}>{t['termsNav']}</a></nav>
<nav class="language-switch" aria-label="{t['language']}">{language_links}</nav>
</div></header>
<main id="continut" class="wrap legal-layout">
<aside><p class="eyebrow">AUTOCONTRACT</p><nav aria-label="{t['contents']}"><h2>{t['contents']}</h2><ol>{contents}</ol></nav></aside>
<article><div class="legal-title"><p class="eyebrow">AUTOCONTRACT · PERSONAL / PROFESSIONAL</p><h1>{title}</h1><p class="updated">{t['updated']} · 1.20.5 (73)</p></div>{body}<section id="references"><h2>{t['references']}</h2><ul class="references">{references}</ul></section></article>
</main><footer class="wrap"><span>© 2026 Selberg · AutoContract</span><a href="mailto:selberg90@gmail.com">selberg90@gmail.com</a></footer>
</body></html>'''


def main():
    source = json.loads((ROOT / "src/legal-content.json").read_text(encoding="utf-8"))
    for kind, filename in (("privacy", "confidentialitate.html"), ("terms", "termeni.html")):
        for lang in ("ro", "en"):
            target = ROOT / ("en/" if lang == "en" else "") / filename
            target.parent.mkdir(exist_ok=True)
            target.write_text(render(kind, filename, lang, source[kind][lang]), encoding="utf-8", newline="\n")
            print("Rendered", target.relative_to(ROOT))


if __name__ == "__main__":
    main()
