"""Render both static homepages. No framework, network, or build dependency required."""
from __future__ import annotations

import json
import struct
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://autocontract.myprintx.com"


def e(value: object) -> str:
    return escape(str(value), quote=True)


def dimensions(path: Path, fallback: tuple[int, int]) -> tuple[int, int]:
    """Read intrinsic PNG/WebP dimensions without an image library."""
    if not path.exists():
        return fallback
    data = path.read_bytes()[:40]
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return struct.unpack(">II", data[16:24])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        if data[12:16] == b"VP8X":
            return int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1
        if data[12:16] == b"VP8 ":
            return struct.unpack("<H", data[26:28])[0] & 0x3FFF, struct.unpack("<H", data[28:30])[0] & 0x3FFF
        if data[12:16] == b"VP8L":
            packed = int.from_bytes(data[21:25], "little")
            return (packed & 0x3FFF) + 1, ((packed >> 14) & 0x3FFF) + 1
    raise ValueError(f"Unsupported image header: {path}")


def feature_list(items: list[str]) -> str:
    return "".join(f'<li><span aria-hidden="true">✓</span><span>{e(item)}</span></li>' for item in items)


def render(lang: str, content: dict, template: Template) -> str:
    values = {key: e(value) for key, value in content.items() if isinstance(value, str)}
    for section, data in content.items():
        if isinstance(data, dict):
            values.update({f"{section}_{key}": e(value) for key, value in data.items() if isinstance(value, str)})
    prefix = "" if lang == "ro" else "/en"
    width, height = dimensions(ROOT / "assets/promo-1795.webp", (1795, 876))
    values.update({
        "lang": lang,
        "canonical": DOMAIN + ("/" if lang == "ro" else "/en/"),
        "home_path": "/" if lang == "ro" else "/en/",
        "privacy_path": prefix + "/confidentialitate.html",
        "terms_path": prefix + "/termeni.html",
        "alternate_locale": "en_GB" if lang == "ro" else "ro_RO",
        "ro_current": ' aria-current="page"' if lang == "ro" else "",
        "en_current": ' aria-current="page"' if lang == "en" else "",
        "promo_width": str(width), "promo_height": str(height),
        "footer_links_label": "Informații și contact" if lang == "ro" else "Information and contact",
    })
    values["nav_links"] = "".join(f'<a href="#{e(anchor)}">{e(label)}</a>' for anchor, label in content["nav"])
    values["hero_facts"] = "".join(f'<div><span class="fact-mark" aria-hidden="true">↳</span><div><strong>{e(title)}</strong><span>{e(text)}</span></div></div>' for title, text in content["hero"]["facts"])
    values["workflow_steps"] = "".join(f'<article data-reveal><span class="step-number">{e(number)}</span><h3>{e(title)}</h3><p>{e(text)}</p></article>' for number, title, text in content["workflow"]["steps"])
    values["romanian_items"] = feature_list(content["contracts"]["romanianItems"])
    values["international_items"] = feature_list(content["contracts"]["internationalItems"])
    values["countries"] = "".join(f'<li><span>{e(code)}</span>{e(name)}</li>' for code, name in content["contracts"]["countries"])
    screens = []
    for filename, title, caption, alt in content["screens"]["items"]:
        sw, sh = dimensions(ROOT / "assets/screens" / filename, (1080, 2400))
        screens.append(f'<figure class="screen-figure" data-reveal><div class="screen-stage"><img src="/assets/screens/{e(filename)}" alt="{e(alt)}" width="{sw}" height="{sh}" loading="lazy" decoding="async"></div><figcaption><h3>{e(title)}</h3><p>{e(caption)}</p></figcaption></figure>')
    values["screens_items"] = "".join(screens)
    plans = []
    for key in ("free", "personal", "pro"):
        plan = content["pricing"][key]
        badge = f'<span class="plan-badge">{e(plan["badge"])}</span>' if plan.get("badge") else ""
        annual = f'<p class="annual-price">{e(plan["annual"])}</p>' if plan.get("annual") else '<div class="annual-spacer" aria-hidden="true"></div>'
        plans.append(f'<article class="price-plan plan-{key}" data-reveal>{badge}<p class="eyebrow">{e(plan["label"])}</p><h3>{e(plan["title"])}</h3><p class="price"><strong>{e(plan["amount"])}</strong><span>{e(plan["currency"])}</span></p><p class="price-period">{e(plan["period"])}</p>{annual}<ul class="feature-list">{feature_list(plan["items"])}</ul><p class="plan-limit">{e(plan["limit"])}</p><a class="button {"button-mint" if key == "pro" else "button-outline"}" href="#instalare">{e(plan["cta"])}<span aria-hidden="true">↗</span></a></article>')
    values["pricing_plans"] = "".join(plans)
    values["data_items"] = "".join(f'<article><span>{e(number)}</span><div><h3>{e(title)}</h3><p>{e(text)}</p></div></article>' for number, title, text in content["data"]["items"])
    values["faq_items"] = "".join(f'<details><summary>{e(question)}<span aria-hidden="true">+</span></summary><div><p>{e(answer)}</p></div></details>' for question, answer in content["faq"]["items"])
    result = template.substitute(values)
    if lang == "en":
        result = result.replace("ACTE ÎN ORDINE. DRUM LIBER.", "PAPERWORK IN ORDER. THE ROAD AHEAD.")
    return result


def main() -> None:
    source = json.loads((ROOT / "src/home-content.json").read_text(encoding="utf-8"))
    template = Template((ROOT / "src/home.template.html").read_text(encoding="utf-8"))
    for lang, content in source.items():
        target = ROOT / ("index.html" if lang == "ro" else "en/index.html")
        target.parent.mkdir(exist_ok=True)
        target.write_text(render(lang, content, template), encoding="utf-8", newline="\n")
        print(f"Rendered {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
