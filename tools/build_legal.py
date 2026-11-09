"""Render the bilingual privacy and terms pages for GitHub Pages."""
from datetime import date
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://autocontract.myprintx.com"
LABELS = {
    "ro": {"privacy": "Politica de confidențialitate", "terms": "Termeni și Condiții", "home": "Acasă", "privacyNav": "Confidențialitate", "termsNav": "Termeni", "skip": "Sari la conținut", "updated": "Actualizat: 2 noiembrie 2026", "contents": "Pe această pagină", "references": "Referințe și servicii externe", "navigation": "Navigare principală", "language": "Limba site-ului", "description": "AutoContract: OCR local, sesiuni temporare, arhivă Pro și Google Drive opțional, achiziții Google Play și condițiile licențelor Personal și Professional."},
    "en": {"privacy": "Privacy policy", "terms": "Terms of Service", "home": "Home", "privacyNav": "Privacy", "termsNav": "Terms", "skip": "Skip to content", "updated": "Updated: 2 November 2026", "contents": "On this page", "references": "References and external services", "navigation": "Main navigation", "language": "Website language", "description": "AutoContract: local OCR, temporary sessions, Pro archive, optional Google Drive, Google Play purchases and Personal and Professional licence conditions."},
}
REFERENCES = [
    ("Google ML Kit", "https://developers.google.com/ml-kit/android-data-disclosure"),
    ("Google API Services User Data Policy", "https://developers.google.com/terms/api-services-user-data-policy"),
    ("Google Privacy", "https://policies.google.com/privacy"),
    ("GitHub Privacy", "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement"),
    ("Google Play subscriptions", "https://support.google.com/googleplay/answer/7018481"),
]


TERMS_REFERENCES = {
    "ro": [
        ("Condițiile Google Play în SEE", "https://play.google.com/about/play-terms/eea/"),
        ("Gestionarea și anularea abonamentelor", "https://support.google.com/googleplay/answer/7018481?hl=ro"),
        ("Rambursări în SEE și Regatul Unit", "https://support.google.com/googleplay/answer/15576634?hl=ro"),
        ("Solicită o rambursare în Google Play", "https://support.google.com/googleplay/workflow/9813244?hl=ro"),
        ("OUG nr. 34/2014 · drepturile consumatorilor", "https://legislatie.just.ro/Public/DetaliiDocument/158913"),
        ("OUG nr. 141/2021 · conținut și servicii digitale", "https://legislatie.just.ro/Public/FormaPrintabila/00000G2C6B82UM8PJ173NHZTP6BIFKMF"),
        ("ANPC · soluționarea alternativă a litigiilor", "https://reclamatiisal.anpc.ro/"),
    ],
    "en": [
        ("Google Play terms in the EEA", "https://play.google.com/about/play-terms/eea/"),
        ("Managing and cancelling subscriptions", "https://support.google.com/googleplay/answer/7018481?hl=en"),
        ("Refunds in the EEA and United Kingdom", "https://support.google.com/googleplay/answer/15576634?hl=en"),
        ("Request a refund in Google Play", "https://support.google.com/googleplay/workflow/9813244?hl=en"),
        ("Romanian Emergency Ordinance No 34/2014 · consumer rights", "https://legislatie.just.ro/Public/DetaliiDocument/158913"),
        ("Romanian Emergency Ordinance No 141/2021 · digital content and services", "https://legislatie.just.ro/Public/FormaPrintabila/00000G2C6B82UM8PJ173NHZTP6BIFKMF"),
        ("ANPC · alternative dispute resolution in Romania", "https://reclamatiisal.anpc.ro/"),
    ],
}


def provider_contact(provider):
    name, address, phone, email = (html.escape(provider[key]) for key in ("name", "address", "phone", "email"))
    return (f'<address class="provider-contact"><strong>{name}</strong><br>{address}<br>'
            f'<a href="tel:{phone.replace(" ", "")}">{phone}</a><br>'
            f'<a href="mailto:{email}">{email}</a></address>')


def terms_date(iso, lang):
    day = date.fromisoformat(iso)
    months = ("ianuarie februarie martie aprilie mai iunie iulie august septembrie octombrie noiembrie decembrie"
              if lang == "ro" else "January February March April May June July August September October November December")
    label = "Ultima actualizare" if lang == "ro" else "Last updated"
    return f'{label} · <time datetime="{iso}">{day.day} {months.split()[day.month - 1]} {day.year}</time>'


def render(kind, filename, lang, sections, terms=None):
    t = LABELS[lang]
    prefix = "/en" if lang == "en" else ""
    title = t[kind]
    canonical = f"{DOMAIN}{prefix}/{filename}"
    parts = []
    for i, (heading, text) in enumerate(sections, 1):
        paragraphs = "".join(f"<p>{html.escape(p)}</p>" for p in text.split("\n\n"))
        contact = provider_contact(terms["provider"]) if terms and i == 1 else ""
        parts.append(f'<section id="section-{i}"><h2>{i}. {html.escape(heading)}</h2>{paragraphs}{contact}</section>')
    body = "".join(parts)
    contents = "".join(f'<li><a href="#section-{i}">{html.escape(heading)}</a></li>' for i, (heading, _) in enumerate(sections, 1))
    if terms:
        contents += f'<li><a href="#references">{t["references"]}</a></li>'
    references = "".join(f'<li><a href="{url}">{name}<span aria-hidden="true"> ↗</span></a></li>'
                         for name, url in (TERMS_REFERENCES[lang] if terms else REFERENCES))
    updated = terms_date(terms["updated"], lang) if terms else f'{t["updated"]} · 1.20.5 (73)'
    fixed_language = ' data-fixed-language' if terms else ''
    description = t["description"]
    if terms:
        description = ("Termenii AutoContract pentru licențe, Google Play, drepturile consumatorilor, OCR și documentele generate."
                       if lang == "ro" else "AutoContract terms covering licences, Google Play, consumer rights, OCR and generated documents.")
    contents_nav = f'<nav aria-label="{t["contents"]}"><h2>{t["contents"]}</h2><ol>{contents}</ol></nav>'
    if terms:
        contents_nav = (f'<div class="terms-toc-desktop">{contents_nav}</div>'
                        f'<details class="terms-toc-mobile"><summary>{t["contents"]}</summary>'
                        f'<nav aria-label="{t["contents"]}"><ol>{contents}</ol></nav></details>')
    language_links = "".join(f'<a href="{("/en" if code == "en" else "")}/{filename}?lang={code}" lang="{code}" hreflang="{code}" data-language="{code}"' + (' aria-current="page"' if code == lang else '') + f'>{code.upper()}</a>' for code in ("ro", "en"))
    return f'''<!doctype html>
<html lang="{lang}"{fixed_language}><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — AutoContract</title><meta name="description" content="{description}">
<meta name="theme-color" content="#071820"><meta name="color-scheme" content="dark">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="ro" href="{DOMAIN}/{filename}">
<link rel="alternate" hreflang="en" href="{DOMAIN}/en/{filename}">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}/{filename}">
<meta property="og:type" content="website"><meta property="og:site_name" content="AutoContract">
<meta property="og:title" content="{title} — AutoContract"><meta property="og:description" content="{description}">
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
<aside><p class="eyebrow">AUTOCONTRACT</p>{contents_nav}</aside>
<article><div class="legal-title"><p class="eyebrow">AUTOCONTRACT · PERSONAL / PROFESSIONAL</p><h1>{title}</h1><p class="updated">{updated}</p></div>{body}<section id="references"><h2>{t['references']}</h2><ul class="references">{references}</ul></section></article>
</main><footer class="wrap"><span>© 2026 Selberg · AutoContract</span><a href="mailto:selberg90@gmail.com">selberg90@gmail.com</a></footer>
</body></html>'''


def main():
    source = json.loads((ROOT / "src/legal-content.json").read_text(encoding="utf-8"))
    terms = json.loads((ROOT / "src/terms-content.json").read_text(encoding="utf-8"))
    assert len(terms["ro"]) == len(terms["en"]) and all(terms["provider"].get(key) for key in ("name", "address", "phone", "email"))
    for kind, filename in (("privacy", "confidentialitate.html"), ("terms", "termeni.html")):
        for lang in ("ro", "en"):
            target = ROOT / ("en/" if lang == "en" else "") / filename
            revision = terms if kind == "terms" else None
            sections = (terms[lang] if revision else source[kind][lang])
            target.write_text(render(kind, filename, lang, sections, revision), encoding="utf-8", newline="\n")
            print("Rendered", target.relative_to(ROOT))


if __name__ == "__main__":
    main()
