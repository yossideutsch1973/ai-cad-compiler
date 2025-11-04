from __future__ import annotations

from pathlib import Path


def test_web_app_files_exist() -> None:
    """Verify that the web app files exist in the docs directory."""
    docs_dir = Path(__file__).resolve().parents[1] / "docs"
    
    assert docs_dir.exists(), "docs directory should exist"
    assert (docs_dir / "index.html").exists(), "index.html should exist"
    assert (docs_dir / "style.css").exists(), "style.css should exist"
    assert (docs_dir / "app.js").exists(), "app.js should exist"


def test_index_html_contains_title() -> None:
    """Verify that index.html contains the expected title."""
    docs_dir = Path(__file__).resolve().parents[1] / "docs"
    index_html = (docs_dir / "index.html").read_text()
    
    assert "AI-CAD Compiler Demo" in index_html
    assert "Pyodide" in index_html or "pyodide" in index_html


def test_app_js_contains_compile_function() -> None:
    """Verify that app.js contains the compile function."""
    docs_dir = Path(__file__).resolve().parents[1] / "docs"
    app_js = (docs_dir / "app.js").read_text()
    
    assert "compileIntent" in app_js
    assert "compile_all" in app_js
