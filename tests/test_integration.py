"""Integration tests (require latexmk installed)."""

import shutil
from pathlib import Path

import pytest

from render_latex.engine import compile_tex

LATEXMK_AVAILABLE = shutil.which("latexmk") is not None


@pytest.mark.skipif(not LATEXMK_AVAILABLE, reason="latexmk not installed")
class TestIntegration:
    """Integration tests with real latexmk."""

    def test_compiles_minimal_tex(self, tmp_path: Path) -> None:
        """Compiles minimal.tex to PDF."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        tex_file = tmp_path / "minimal.tex"
        tex_file.write_text((fixtures_dir / "minimal.tex").read_text())

        pdf_path = compile_tex(tex_file, output_dir=None, engine="pdflatex", clean=True)

        assert pdf_path.exists()
        assert pdf_path.suffix == ".pdf"
        assert pdf_path.stat().st_size > 0
