from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse

import pytest

SPEC = importlib.util.spec_from_file_location("build_static", "scripts/build_static.py")
assert SPEC and SPEC.loader
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_static_safe_reproducible_relative_links(tmp_path):
    target = builder.build()
    first = (target / "manifest.json").read_bytes()
    builder.build()
    assert first == (target / "manifest.json").read_bytes()
    manifest = json.loads(first)
    for name, digest in manifest["files"].items():
        assert sha256((target / name).read_bytes()).hexdigest() == digest
        assert all(part not in name for part in (".runtime", ".office", ".env", "journal", "sqlite"))
    for file in target.glob("*.html"):
        text = file.read_text(encoding="utf-8")
        for link in re.findall(r'(?:href|src)=\x27([^\x27]+)\x27', text):
            if link.startswith("https:"):
                continue
            assert not link.startswith("/")
            assert (file.parent / link).is_file()
            assert urlparse(urljoin("https://example.test/stock-analysis/" + file.name, link)).path.startswith("/stock-analysis/")
        assert "SIMULATION ONLY" in text
    with pytest.raises(ValueError, match="build/site"):
        builder.build(tmp_path / "escape")


def test_markdown_is_escaped():
    assert "&lt;script&gt;" in builder.page("<script>", "safe")
    rendered = builder.document_text("<script> [bad](javascript:alert) [safe](https://example.test/a) [guide](USER_GUIDE.md)")
    assert "&lt;script&gt;" in rendered and "href='javascript" not in rendered
    assert "href='https://example.test/a'" in rendered
    assert "href='USER_GUIDE.html'" in rendered


def test_static_rejects_lexical_site_link_before_write(monkeypatch):
    original = Path.is_symlink
    lexical = builder.ROOT / "build" / "site"
    monkeypatch.setattr(Path, "is_symlink", lambda path: path == lexical or original(path))
    with pytest.raises(ValueError, match="build/site"):
        builder.build()
