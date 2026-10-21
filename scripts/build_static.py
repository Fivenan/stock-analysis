"""Build a public-safe, dependency-free HTML companion from an explicit allowlist."""
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DOCS = ("TRADING_GUIDE", "USER_GUIDE", "LEARNING_PLAN_90_DAYS", "DATA_PROVIDER_MATRIX",
        "API_OPTIMIZATION", "BROKER_INTEGRATION", "GERMANY_TAX_AND_REGULATION",
        "MARKET_ACCESS", "SOURCES", "STRATEGIES", "BACKTEST_METHODOLOGY", "ROADMAP",
        "VERIFICATION")
STYLE = """body{font:17px/1.6 system-ui;max-width:1100px;margin:auto;padding:2rem;color:#16283b;background:#f6f8fb}a{color:#075aa5}nav{display:flex;gap:1rem;flex-wrap:wrap}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:white;padding:1.4rem;border:1px solid #ccd6e0}aside{background:#fff0b9;padding:1rem}input{font:inherit;padding:.7rem;width:90%}table{border-collapse:collapse}td,th{padding:.6rem;border:1px solid #ccd6e0}h1{line-height:1.2}"""


def page(title: str, body: str) -> str:
    return ("<!doctype html><html lang='en'><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            f"<title>{escape(title)} · Global Market Research Lab</title>"
            "<link rel='stylesheet' href='assets/style.css'><body>"
            "<nav><a href='index.html'>Research home</a><a href='learning.html'>Learning library</a>"
            "<a href='reports.html'>Synthetic reports</a><a href='DATA_PROVIDER_MATRIX.html'>Providers</a>"
            "<a href='MARKET_ACCESS.html'>Market access</a><a href='SOURCES.html'>Sources</a></nav>"
            "<aside>SIMULATION ONLY · SYNTHETIC SAMPLE · Static companion. "
            "The full research app runs locally; this site cannot place orders or run Python.</aside>"
            f"<h1>{escape(title)}</h1>{body}</body></html>")


def document_text(text: str) -> str:
    """Escape all content, linking only allowlisted relative guides and https URLs."""
    pieces = []
    cursor = 0
    for match in re.finditer(r"\[([^\]\n]+)\]\(([^\s)]+)\)", text):
        pieces.append(escape(text[cursor:match.start()]))
        label, url = match.groups()
        parsed = urlparse(url)
        destination = None
        if parsed.scheme == "https" and parsed.netloc and not parsed.username and not parsed.password:
            destination = url
        elif url.endswith(".md") and "/" not in url and url[:-3] in DOCS:
            destination = url[:-3] + ".html"
        pieces.append((f"<a href='{escape(destination, quote=True)}'>{escape(label)}</a>"
                       if destination else escape(match.group())))
        cursor = match.end()
    pieces.append(escape(text[cursor:]))
    return "<pre>" + "".join(pieces) + "</pre>"


def build(target: Path | None = None) -> Path:
    if ((ROOT / "build").is_symlink() or (ROOT / "build").is_junction()
            or not (ROOT / "build").resolve().is_relative_to(ROOT)):
        raise ValueError("Project build directory must not escape the project")
    lexical = ROOT / "build" / "site"
    if (lexical.is_symlink() or lexical.is_junction()
            or not lexical.resolve().is_relative_to(ROOT / "build")):
        raise ValueError("Static build/site must not escape project build")
    expected = lexical.resolve()
    if target is not None and (target.is_symlink() or target.is_junction()):
        raise ValueError("Static output must be the project build/site directory")
    target = expected if target is None else target.resolve()
    if target != expected or target.is_symlink() or target.is_junction():
        raise ValueError("Static output must be the project build/site directory")
    target.mkdir(parents=True, exist_ok=True)
    # Never recursively delete or copy a tree. Refuse unexpected pre-existing artifacts.
    allowed = {"index.html", "learning.html", "reports.html", ".nojekyll", "manifest.json"}
    allowed.update(name + ".html" for name in DOCS)
    allowed.update({"assets/style.css", "assets/search.js"})
    report_root = ROOT / "tests/fixtures/financial_reports"
    if report_root.is_symlink() or report_root.is_junction():
        raise ValueError("Report input path escape")
    reports = sorted(report_root.glob("*"))
    if any(p.is_symlink() or p.is_junction() or not p.resolve().is_relative_to(report_root)
           for p in reports):
        raise ValueError("Report input path escape")
    report_names = {p.name for p in reports if p.suffix in (".json", ".csv")}
    allowed.update("downloads/" + name for name in report_names)
    for prior in target.rglob("*"):
        if (prior.is_symlink() or prior.is_junction()
                or (prior.is_file() and prior.relative_to(target).as_posix() not in allowed)):
            raise ValueError("Unexpected output artifact; inspect build/site before rebuilding")

    def write(name: str, content: str) -> None:
        destination = target / name
        if not destination.resolve().is_relative_to(target):
            raise ValueError("Output path escape")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8", newline="\n")

    write("assets/style.css", STYLE)
    write("assets/search.js", "document.querySelector('input').addEventListener('input',e=>{for(const x of document.querySelectorAll('article'))x.hidden=!x.textContent.toLowerCase().includes(e.target.value.toLowerCase())});")
    library = "<label>Search all guide text <input type='search' aria-label='Search guides'></label>"
    if (ROOT / "docs").is_symlink() or (ROOT / "docs").is_junction():
        raise ValueError("Document input path escape")
    for name in DOCS:
        source = ROOT / "docs" / (name + ".md")
        if (source.is_symlink() or source.is_junction()
                or not source.resolve().is_relative_to(ROOT / "docs")):
            raise ValueError("Document input path escape")
        text = source.read_text(encoding="utf-8")
        # Escaped source text preserves every research citation without interpreting HTML or scripts.
        content = document_text(text)
        write(name + ".html", page(name.replace("_", " "), content))
        library += f"<article><h2><a href='{name}.html'>{escape(name.replace('_', ' '))}</a></h2>{content}</article>"
    write("learning.html", page("Searchable learning library", library + "<script src='assets/search.js'></script>"))
    report_body = "<p>Computed by the verified daily event engine from deterministic 2024–2025 fixtures. These are not observed market results, profitability evidence, or personal recommendations. Includes rejected orders and costs; reports preserve warnings and conventions. Source: arithmetic generator v1, CC0, retrieved 2026-01-01 UTC.</p>"
    summary = json.loads((ROOT / "tests/fixtures/financial_reports/summary.json").read_text())
    report_body += "<pre>" + escape(json.dumps(summary, indent=2)) + "</pre><ul>"
    for source in reports:
        if source.name in report_names:
            write("downloads/" + source.name, source.read_text(encoding="utf-8"))
            report_body += f"<li><a href='downloads/{source.name}' download>{escape(source.name)}</a></li>"
    write("reports.html", page("Computed synthetic experiments", report_body + "</ul>"))
    write("index.html", page("Global Market Research Lab",
        "<p>An English EUR-based learning and experimentation workspace. Explore the research library, "
        "compare synthetic reports and follow the 90-day paper-only learning plan.</p>"
        "<p>Local app: twelve pages, three active strategies, same-cost benchmark, durable paper account "
        "and append-only journal. No credentials needed. Real feeds, contributions, advanced strategy "
        "validation and full tax accounting remain deferred.</p>"
        "<p><a href='USER_GUIDE.html'>Local setup and user guide</a> · "
        "<a href='LEARNING_PLAN_90_DAYS.html'>90-day plan</a> · "
        "<a href='VERIFICATION.html'>Verification and limits</a></p>"
        "<p><a href='https://github.com/Fivenan/stock-analysis'>Source repository (access required)</a>. "
        "Market data coverage does not establish Trade Republic instrument access.</p>"))
    write(".nojekyll", "")
    hashes = {p.relative_to(target).as_posix(): sha256(p.read_bytes()).hexdigest()
              for p in sorted(target.rglob("*")) if p.is_file() and p.name != "manifest.json"}
    fingerprint = sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
    write("manifest.json", json.dumps({"schema": 1, "synthetic_only": True,
          "content_fingerprint": fingerprint, "files": hashes}, indent=2, sort_keys=True))
    return target


if __name__ == "__main__":
    print(build())
