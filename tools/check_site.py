"""Focused offline checks of generated public pages and their local dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote, urljoin
import hashlib
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HOST = "autocontract.myprintx.com"
PAGES = ["index.html", "en/index.html", "confidentialitate.html", "en/confidentialitate.html", "termeni.html", "en/termeni.html", "404.html"]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))


def main():
    parsed = {name: Page((ROOT / name).read_text(encoding="utf-8")) for name in PAGES}
    count = 0
    for name, page in parsed.items():
        base = "https://" + HOST + "/" + name
        ids = [a["id"] for _, a in page.nodes if "id" in a]
        assert len(ids) == len(set(ids)), (name, "duplicate IDs")
        assert len([n for n in page.nodes if n[0] == "h1"]) == 1, (name, "one H1 required")
        assert next(a["lang"] for t, a in page.nodes if t == "html") == ("en" if name.startswith("en/") else "ro")
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "DRAFT —" not in text and "APPROVAL REQUIRED" not in text
        if name != "404.html":
            assert any(t == "meta" and a.get("name") == "description" and a.get("content") for t, a in page.nodes)
            assert any(t == "link" and a.get("rel") == "canonical" for t, a in page.nodes)
            assert {"ro", "en"}.issubset({a.get("hreflang") for t, a in page.nodes if t == "link" and a.get("rel") == "alternate"})
        urls = []
        for tag, attrs in page.nodes:
            if "href" in attrs:
                urls.append(attrs["href"])
            if "src" in attrs:
                urls.append(attrs["src"])
            if "srcset" in attrs:
                urls.extend(item.strip().split()[0] for item in attrs["srcset"].split(","))
            if tag == "img":
                assert "alt" in attrs and int(attrs.get("width", 0)) > 0 and int(attrs.get("height", 0)) > 0, (name, attrs)
            if tag == "script" and "src" in attrs:
                assert not urlparse(attrs["src"]).netloc, "No unnecessary remote script dependency"
            if tag == "meta" and attrs.get("property") == "og:image":
                urls.append(attrs["content"])
        for url in urls:
            absolute = urlparse(urljoin(base, url))
            if absolute.scheme not in ("http", "https") or absolute.netloc != HOST:
                continue
            path = unquote(absolute.path).lstrip("/")
            path += "index.html" if not path or path.endswith("/") else ""
            target = ROOT / path
            assert target.is_file(), (name, "missing link/asset", url)
            if absolute.fragment:
                assert path in parsed and absolute.fragment in {a.get("id") for _, a in parsed[path].nodes}, (name, url, "missing anchor")
            count += 1
    approved = hashlib.sha256((ROOT / "src/legal-content.json").read_bytes()).hexdigest()
    assert approved == "3fa3975f8406e62d185a16297f6533c274f258188e4f6821249ab8c926c3a725", "Legal text differs from owner-approved content"
    terms = json.loads((ROOT / "src/terms-content.json").read_text(encoding="utf-8"))
    for lang, name in (("ro", "termeni.html"), ("en", "en/termeni.html")):
        nodes = parsed[name].nodes
        html_tag = next(attrs for tag, attrs in nodes if tag == "html")
        assert "data-fixed-language" in html_tag
        assert len([1 for tag, attrs in nodes if tag == "section" and attrs.get("id", "").startswith("section-")]) == len(terms[lang])
        assert len(terms[lang]) == len(terms["ro"])
        assert ("time", {"datetime": terms["updated"]}) in nodes
        for href in ("mailto:" + terms["provider"]["email"], "tel:" + terms["provider"]["phone"].replace(" ", "")):
            assert any(tag == "a" and attrs.get("href") == href for tag, attrs in nodes)
        for language, target in (("ro", "/termeni.html"), ("en", "/en/termeni.html")):
            assert any(tag == "a" and attrs.get("href") == f"{target}?lang={language}"
                       and attrs.get("hreflang") == language for tag, attrs in nodes)
    home = json.loads((ROOT / "src/home-content.json").read_text(encoding="utf-8"))
    def keys(value, path=""):
        if isinstance(value, dict):
            return {(path, tuple(sorted(value)))} | set().union(*(keys(v, path + "/" + k) for k, v in value.items()))
        if isinstance(value, list):
            return {(path, "list", len(value))} | set().union(*(keys(v, path + "/" + str(i)) for i, v in enumerate(value)))
        return {(path, type(value).__name__)}
    assert keys(home["ro"]) == keys(home["en"]), "RO/EN content structure differs"
    assert (ROOT / "CNAME").read_text().strip() == HOST
    assert (ROOT / "google95c7b1d2d13a0fc0.html").read_text().strip() == "google-site-verification: google95c7b1d2d13a0fc0.html"
    assert (ROOT / ".nojekyll").exists()
    sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
    assert len(sitemap) == 6
    assert "Sitemap: https://autocontract.myprintx.com/sitemap.xml" in (ROOT / "robots.txt").read_text()
    print(json.dumps({"status": "passed", "pages": len(PAGES), "internalLinksAndAssetsChecked": count, "translationStructureMatches": True, "approvedLegalContentUnchanged": True, "updatedTermsValidated": True, "sitemapUrls": len(sitemap), "domainAndVerificationPreserved": True}))


if __name__ == "__main__":
    main()
