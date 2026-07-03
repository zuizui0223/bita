"""Locate source-data assets associated with the eLife d_A C4 figures.

This module fetches the already-probed eLife XML, identifies figures referenced
from source sections containing both scent/reward and oviposition term families,
and records declared graphics, media, supplementary, or external data assets. It
performs only a bounded prefix probe of those exact assets. It does not retain the
article or assets, read datasets, estimate effects, or establish B2 eligibility.
"""

from __future__ import annotations

import csv
import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from .d_a_elife_screen import (
    ANTAGONIST_TERMS,
    MAX_XML_BYTES,
    TRAIT_TERMS,
    USER_AGENT,
    _matched,
    _plain,
    _text,
)


MAX_PREFIX_BYTES = 8192
XHREF = "{http://www.w3.org/1999/xlink}href"
ASSET_FIELDS = (
    "candidate_id", "doi", "xml_url", "figure_label", "asset_kind", "asset_href",
    "asset_url", "access_status", "http_status", "content_type", "prefix_signature",
    "do_not_infer",
)
DO_NOT_INFER = (
    "Asset locator only. Do not infer data variables, treatment/control, effect direction, "
    "denominator, uncertainty, or B2 eligibility until the asset and source context are read."
)


@dataclass(frozen=True)
class AssetReceipt:
    candidate_id: str
    doi: str
    xml_url: str
    figure_label: str
    asset_kind: str
    asset_href: str
    asset_url: str
    access_status: str
    http_status: str
    content_type: str
    prefix_signature: str
    do_not_infer: str = DO_NOT_INFER


def read_screen(path: str | Path) -> dict[str, str]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    matches = [row for row in rows if row.get("route_structure_signal") == "candidate_scent_reward_to_oviposition_structure_needs_numeric_context_check"]
    if len(matches) != 1:
        raise ValueError("expected exactly one viable eLife scent/reward C4 screen row")
    return matches[0]


def _fetch_xml(url: str) -> tuple[int, bytes]:
    request = Request(url, headers={"Accept": "application/xml,text/xml,*/*", "User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:  # nosec B310: exact public XML URL from source screen
        return int(getattr(response, "status", response.getcode())), response.read(MAX_XML_BYTES + 1)


def _prefix(url: str) -> tuple[int, str, bytes]:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Range": f"bytes=0-{MAX_PREFIX_BYTES - 1}", "Accept": "text/csv,application/json,application/vnd.ms-excel,application/zip,*/*"})
    with urlopen(request, timeout=60) as response:  # nosec B310: exact asset href inside public eLife XML
        return int(getattr(response, "status", response.getcode())), _text(response.headers.get("Content-Type")).lower(), response.read(MAX_PREFIX_BYTES)


def _href(element: ET.Element) -> str:
    return _text(element.get(XHREF) or element.get("href"))


def _asset_url(xml_url: str, href: str) -> str:
    if href.startswith(("https://", "http://")):
        return href
    # eLife XML may use bare asset names even when its XML itself is served via the
    # article route. The CDN article directory is the canonical companion base.
    article_id = xml_url.rstrip("/").split("/")[-1].split(".")[0]
    return f"https://cdn.elifesciences.org/articles/{article_id}/{href.lstrip('/')}"


def _figures_from_shared_sections(root: ET.Element) -> set[str]:
    figure_ids: set[str] = set()
    for section in root.findall(".//sec"):
        text = _plain(section)
        if not (_matched(text, TRAIT_TERMS) and _matched(text, ANTAGONIST_TERMS)):
            continue
        for ref in section.findall(".//xref"):
            if _text(ref.get("ref-type")).casefold() == "fig" and _text(ref.get("rid")):
                figure_ids.add(_text(ref.get("rid")))
    return figure_ids


def _assets_from_figure(figure: ET.Element) -> list[tuple[str, str]]:
    assets: list[tuple[str, str]] = []
    for element in figure.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        href = _href(element)
        if not href:
            continue
        if tag == "graphic":
            assets.append(("figure_graphic", href))
        elif tag == "media":
            assets.append(("figure_media", href))
        elif tag == "supplementary-material":
            assets.append(("figure_supplement", href))
        elif tag == "ext-link":
            assets.append(("figure_external_link", href))
    return assets


def locate_assets(
    screen: dict[str, str],
    *,
    fetch_xml: Callable[[str], tuple[int, bytes]] = _fetch_xml,
    fetch_prefix: Callable[[str], tuple[int, str, bytes]] = _prefix,
) -> list[AssetReceipt]:
    try:
        status, payload = fetch_xml(screen["xml_url"])
        if status >= 400:
            raise RuntimeError(f"HTTP {status}")
        if len(payload) > MAX_XML_BYTES:
            raise RuntimeError("XML response exceeds cap")
        root = ET.fromstring(payload)
    except Exception as error:
        return [AssetReceipt(screen["candidate_id"], screen["doi"], screen["xml_url"], "", "xml_access", "", "", "xml_access_or_parse_failed", "", "", "", f"Asset discovery failed: {type(error).__name__}: {error}")]

    figures = { _text(fig.get("id")): fig for fig in root.findall(".//fig") if _text(fig.get("id")) }
    receipts: list[AssetReceipt] = []
    for figure_id in sorted(_figures_from_shared_sections(root)):
        figure = figures.get(figure_id)
        if figure is None:
            continue
        label = _plain(figure.find("label")) or figure_id
        seen: set[str] = set()
        for kind, href in _assets_from_figure(figure):
            key = f"{kind}|{href}"
            if key in seen:
                continue
            seen.add(key)
            url = _asset_url(screen["xml_url"], href)
            try:
                http, content_type, prefix = fetch_prefix(url)
                state = "asset_prefix_recovered" if http < 400 else "asset_http_error"
                receipts.append(AssetReceipt(screen["candidate_id"], screen["doi"], screen["xml_url"], label, kind, href, url, state, str(http), content_type, prefix[:16].decode("latin1", errors="replace")))
            except HTTPError as error:
                receipts.append(AssetReceipt(screen["candidate_id"], screen["doi"], screen["xml_url"], label, kind, href, url, "asset_http_error", str(error.code), "", ""))
            except Exception:
                receipts.append(AssetReceipt(screen["candidate_id"], screen["doi"], screen["xml_url"], label, kind, href, url, "asset_access_failed", "", "", ""))
    return receipts


def write_outputs(out_dir: str | Path, rows: Iterable[AssetReceipt]) -> dict[str, object]:
    rows = list(rows)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_elife_asset_receipts.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ASSET_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    report = {
        "asset_count": len(rows),
        "assets_with_prefix_recovered": sum(row.access_status == "asset_prefix_recovered" for row in rows),
        "decision_boundary": DO_NOT_INFER,
    }
    (destination / "d_a_elife_asset_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report
