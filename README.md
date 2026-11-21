# AutoContract official website

Static bilingual website served by GitHub Pages at https://autocontract.myprintx.com/.

## Source and generation

- `src/home.template.html` and `src/home-content.json`: one homepage template with Romanian/English content.
- `src/legal-content.json`: privacy policy approved on 21 November 2026 and historical licence terms from 2 November 2026. The current Terms of Service in both languages are rendered from `src/terms-content.json`. Material legal changes require the owner's approval before publication.
- `assets/site.css` / `site.js`: responsive homepage and local language preference. `assets/legal.css` / `legal-language.js`: readable legal pages using the same preference key.
- `assets/promo-current*.jpg` and `social-card.jpg`: browser-rendered graphics using the existing logo and authentic current app captures. Older promo WebP assets are retained only as historical files.
- `assets/screens/`: authentic, privacy-reviewed emulator screenshots of version 1.23.0 (85), in Trial, with blank fields and no fabricated purchase state. The English guided OCR illustration reuses the Romanian interface capture and is labelled accordingly.

Render with Python 3 (standard library; no framework/build dependency):

```text
python tools/build_site.py
python tools/build_legal.py
python tools/check_site.py
```

For local preview: `python -m http.server 8765 --bind 127.0.0.1` from the repository root.

## Publication

Existing Pages configuration: `main`, repository root `/`, HTTPS enforced. The current deployment is the Pages build triggered by pushing to `main`. Preserve `CNAME`, `.nojekyll`, `logo.png` and `google95c7b1d2d13a0fc0.html`; do not change DNS while updating content.

The original `/index.html` and `/confidentialitate.html` addresses remain functional. English lives under `/en/`. The two canonical terms URLs are `/termeni.html` (Romanian) and `/en/termeni.html` (English). Direct links retain their language, with an explicit RO / EN switch on each page. The former GitHub Pages privacy URL follows GitHub's existing custom-domain redirect.

The website does not collect payments or identity documents and has no analytics or remote-font dependencies. It only stores the selected language in browser localStorage. Google Play installation links are for authorised Closed Testing accounts; they do not claim Production availability. Reference RON prices must match Google Play before future publication; the in-app Play price is authoritative.

Private evidence, approvals and verified before/after backups are retained outside this public repository in the AutoContract workspace. Never commit purchase tokens, credentials, signing keys, raw Logcat or real document photographs.

## Revision 21 November 2026

Four access choices: free previews, Single (RON 39.99 per agreement), Personal (RON 149.99 one-time), Pro (RON 49.99/month or 399.99/year). Current Google Play checkout remains authoritative. The owner approved the updated Romanian/English Terms and Privacy pages for publication, covering local Single editing, uninstall limits and opaque Billing identifiers. Existing licence rights are preserved. Homepage images and six feature cards describe the current guide, front/back import, review, document-copy PDFs, working copies and bilingual interface. Android sources, Play products, Data Safety and tester lists are outside this website change.
