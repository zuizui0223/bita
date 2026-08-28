"""Recover the Kessler et al. (2008) Science supporting material fail-closed.

The goal is deliberately narrow: locate a public supporting-material PDF for
DOI 10.1126/science.1160072 and determine whether Fig. S8A / the day-by-genotype
capsule-production information is text-recoverable. The raw copyrighted PDF is
never copied to repository outputs or uploaded as an artifact; only access
provenance, a SHA-256 digest, page indices, and short targeted text snippets are
written.

This probe does not infer missing counts from the published four-genotype means.
If the supplement cannot be reached or S8A is image-only, the correct status is
an explicit access/extraction boundary rather than a reconstructed interaction
standard error.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import tempfile
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

DOI = "10.1126/science.1160072"
USER_AGENT = "biotic-interaction-trait-architecture-kessler-supplement-probe/1.0"
ALLOWED_HOSTS = {
    "www.science.org",
    "science.org",
    "science.sciencemag.org",
    "www.sciencemag.org",
    "sciencemag.org",
}
SEED_URLS = (
    "https://www.science.org/doi/10.1126/science.1160072",
    "https://science.sciencemag.org/content/suppl/2008/08/28/321.5893.1200.DC1",
    "http://www.sciencemag.org/cgi/content/full/321/5893/1200/DC1",
    "https://www.science.org/doi/suppl/10.1126/science.1160072/suppl_file/kessler.som.pdf",
    "https://www.science.org/doi/suppl/10.1126/science.1160072/suppl_file/1160072s1.pdf",
)
TARGET_PATTERNS = ("fig. s8", "fig s8", "s8a", "antherectom", "capsule")
MAX_URLS = 24
MAX_EXCERPT_CHARS = 1600


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for key, value in attrs:
            if key.lower() == "href" and value:
                self.links.append(html.unescape(value))


def _allowed(url: str) -> bool:
    return (urlparse(url).hostname or "").lower() in ALLOWED_HOSTS


def discover_candidate_links(base_url: str, html_text: str) -> list[str]:
    parser = _LinkParser()
    parser.feed(html_text)
    found: list[str] = []
    for href in parser.links:
        absolute = urljoin(base_url, href)
        low = absolute.lower()
        if not _allowed(absolute):
            continue
        if any(token in low for token in ("1160072", "suppl", "supplement", "dc1", "som.pdf")):
            found.append(absolute)
    return sorted(dict.fromkeys(found))


@dataclass(frozen=True)
class FetchResult:
    requested_url: str
    final_url: str
    status: int
    content_type: str
    payload: bytes


def fetch_url(url: str, timeout: int = 20) -> FetchResult:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/pdf,*/*"})
    with urlopen(request, timeout=timeout) as response:  # nosec B310: fixed public publisher hosts
        payload = response.read()
        return FetchResult(
            requested_url=url,
            final_url=str(response.geturl()),
            status=int(getattr(response, "status", response.getcode())),
            content_type=str(response.headers.get("Content-Type", "")),
            payload=payload,
        )


def _is_pdf(result: FetchResult) -> bool:
    return result.payload.startswith(b"%PDF") or "application/pdf" in result.content_type.lower()


def _looks_supplementary(url: str) -> bool:
    low = url.lower()
    return any(token in low for token in ("suppl", "supplement", "dc1", "som.pdf", "s1.pdf"))


def _extract_target_text(pdf_bytes: bytes) -> dict[str, object]:
    try:
        from pypdf import PdfReader
    except Exception as error:  # pragma: no cover - workflow installs pypdf
        return {"text_extraction_status": f"pypdf_unavailable:{type(error).__name__}", "matched_pages": []}

    with tempfile.NamedTemporaryFile(suffix=".pdf") as handle:
        handle.write(pdf_bytes)
        handle.flush()
        reader = PdfReader(handle.name)
        matches: list[dict[str, object]] = []
        for page_index, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            low = text.lower()
            if not any(pattern in low for pattern in TARGET_PATTERNS):
                continue
            lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines() if line.strip()]
            targeted = [line for line in lines if any(pattern in line.lower() for pattern in TARGET_PATTERNS)]
            excerpt = "\n".join(targeted)[:MAX_EXCERPT_CHARS]
            matches.append({"page_index_zero_based": page_index, "excerpt": excerpt})
        return {
            "text_extraction_status": "success",
            "page_count": len(reader.pages),
            "matched_pages": matches,
        }


def probe(fetch: Callable[[str], FetchResult] = fetch_url) -> dict[str, object]:
    queue = list(SEED_URLS)
    seen: set[str] = set()
    attempts: list[dict[str, object]] = []
    recovered: dict[str, object] | None = None

    while queue and len(seen) < MAX_URLS and recovered is None:
        url = queue.pop(0)
        if url in seen or not _allowed(url):
            continue
        seen.add(url)
        try:
            result = fetch(url)
        except Exception as error:
            attempts.append({"url": url, "status": "fetch_failed", "error": f"{type(error).__name__}: {error}"})
            continue

        attempts.append({
            "url": url,
            "status": result.status,
            "final_url": result.final_url,
            "content_type": result.content_type,
            "bytes": len(result.payload),
        })
        if result.status >= 400:
            continue

        if _is_pdf(result):
            if not (_looks_supplementary(url) or _looks_supplementary(result.final_url)):
                continue
            extraction = _extract_target_text(result.payload)
            recovered = {
                "source_url": result.final_url,
                "sha256": hashlib.sha256(result.payload).hexdigest(),
                "pdf_bytes": len(result.payload),
                **extraction,
            }
            break

        if "html" in result.content_type.lower() or result.payload.lstrip().startswith(b"<"):
            text = result.payload.decode("utf-8", errors="replace")
            for candidate in discover_candidate_links(result.final_url, text):
                if candidate not in seen and candidate not in queue:
                    queue.append(candidate)

    if recovered is None:
        return {
            "analysis_id": "kessler_2008_supplement_probe_v1",
            "doi": DOI,
            "supplement_status": "NOT_RECOVERED_FROM_REGISTERED_PUBLIC_ROUTES",
            "figure_s8a_text_status": "NOT_EVALUABLE",
            "attempts": attempts,
            "claim_boundary": "Do not infer a formal A:D interaction SE/CI from rounded genotype means when the day-level supplement is unavailable.",
        }

    matched = recovered.get("matched_pages") or []
    return {
        "analysis_id": "kessler_2008_supplement_probe_v1",
        "doi": DOI,
        "supplement_status": "SUPPLEMENT_PDF_RECOVERED",
        "figure_s8a_text_status": "TARGET_TEXT_RECOVERED" if matched else "PDF_RECOVERED_TARGET_NOT_TEXT_EXTRACTABLE",
        "supplement": recovered,
        "attempts": attempts,
        "claim_boundary": "A recovered supplement is an access result. A formal A:D interaction uncertainty still requires exact day/cell values or a source-reported factorial uncertainty.",
    }


def render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Kessler 2008 supplement recovery probe v1",
        "",
        f"DOI: `{report['doi']}`",
        "",
        f"Supplement status: **{report['supplement_status']}**",
        f"Fig. S8A text status: **{report['figure_s8a_text_status']}**",
        "",
        "## Identification boundary",
        "",
        str(report["claim_boundary"]),
        "",
    ]
    supplement = report.get("supplement")
    if isinstance(supplement, dict):
        lines += [
            "## Recovered supplement receipt",
            "",
            f"- source URL: `{supplement.get('source_url', '')}`",
            f"- SHA-256: `{supplement.get('sha256', '')}`",
            f"- bytes: {supplement.get('pdf_bytes', '')}",
            f"- pages: {supplement.get('page_count', 'not extracted')}",
            "",
        ]
        pages = supplement.get("matched_pages") or []
        if pages:
            lines += ["## Targeted text hits", ""]
            for hit in pages:
                lines += [f"### PDF page index {hit['page_index_zero_based']}", "", "```text", str(hit.get("excerpt", "")), "```", ""]
    lines += ["## Access attempts", ""]
    for attempt in report.get("attempts", []):
        lines.append(f"- `{attempt.get('url')}` → {attempt.get('status')}")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_json", type=Path)
    parser.add_argument("out_md", type=Path)
    args = parser.parse_args(argv)
    report = probe()
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    args.out_md.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({
        "supplement_status": report["supplement_status"],
        "figure_s8a_text_status": report["figure_s8a_text_status"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
