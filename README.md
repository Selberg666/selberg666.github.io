# AutoContract official website

Static bilingual website served by GitHub Pages at https://autocontract.myprintx.com/.

## Source and generation

- `src/home.template.html` and `src/home-content.json`: one homepage template with Romanian/English content.
- `src/legal-content.json`: Romanian/English privacy policy and terms, approved by the owner on 2 November 2026. Material legal changes require the owner's approval before publication.
- `assets/site.css` / `site.js`: responsive homepage and local language preference. `assets/legal.css` / `legal-language.js`: readable legal pages using the same preference key.
- `assets/promo-*.webp`: proportionally resized user-supplied promotional banner, explicitly labelled illustrative; it is not a current app screenshot.
- `assets/screens/`: authentic, privacy-reviewed emulator screenshots of version 1.20.5 (73). No licence state was fabricated. Images were only resized/encoded.

Render with Python 3 (standard library; no framework/build dependency):

```text
python tools/build_site.py
python tools/build_legal.py
python tools/check_site.py
```

For local preview: `python -m http.server 8765 --bind 127.0.0.1` from the repository root.

## Publication

Existing Pages configuration: `main`, repository root `/`, HTTPS enforced. The current deployment is the Pages build triggered by pushing to `main`. Preserve `CNAME`, `.nojekyll`, `logo.png` and `google95c7b1d2d13a0fc0.html`; do not change DNS while updating content.

The original `/index.html` and `/confidentialitate.html` addresses remain functional. English lives under `/en/`. The former GitHub Pages privacy URL follows GitHub's existing custom-domain redirect.

The website does not collect payments or identity documents and has no analytics or remote-font dependencies. It only stores the selected language in browser localStorage. Google Play installation links are for authorised Closed Testing accounts; they do not claim Production availability. Reference RON prices must match Google Play before future publication; the in-app Play price is authoritative.

Private evidence, approvals and verified before/after backups are retained outside this public repository in the AutoContract workspace. Never commit purchase tokens, credentials, signing keys, raw Logcat or real document photographs.
