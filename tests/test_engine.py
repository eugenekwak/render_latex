"""Unit tests for the LaTeX compilation engine."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from render_latex.engine import compile_tex


class TestCompileTex:
    """Tests for compile_tex function."""

    @patch("render_latex.engine.subprocess.run")
    def test_calls_latexmk_with_pdflatex_default(
        self, mock_run: MagicMock, tmp_path: Path
    ) -> None:
        """compile_tex invokes latexmk -pdf -interaction=nonstopmode for pdflatex."""
        tex_file = tmp_path / "doc.tex"
        tex_file.write_text(r"\documentclass{article}\begin{document}x\end{document}")
        mock_run.return_value = MagicMock(returncode=0)

        result = compile_tex(tex_file, output_dir=None, engine="pdflatex", clean=False)

        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert call_args[0] == "latexmk"
        assert "-pdf" in call_args
        assert "-interaction=nonstopmode" in call_args
        assert "-xelatex" not in call_args
        assert str(tex_file) in call_args
        assert result == tmp_path / "doc.pdf"

    @patch("render_latex.engine.subprocess.run")
    def test_calls_latexmk_with_xelatex(
        self, mock_run: MagicMock, tmp_path: Path
    ) -> None:
        """compile_tex passes -xelatex when engine is xelatex."""
        tex_file = tmp_path / "doc.tex"
        tex_file.write_text(r"\documentclass{article}\begin{document}x\end{document}")
        mock_run.return_value = MagicMock(returncode=0)

        compile_tex(tex_file, output_dir=None, engine="xelatex", clean=False)

        call_args = mock_run.call_args[0][0]
        assert "-xelatex" in call_args
        assert "-pdf" in call_args

    @patch("render_latex.engine.subprocess.run")
    def test_output_dir_used_when_provided(
        self, mock_run: MagicMock, tmp_path: Path
    ) -> None:
        """When output_dir is set, PDF is written there."""
        tex_file = tmp_path / "doc.tex"
        tex_file.write_text(r"\documentclass{article}\begin{document}x\end{document}")
        out_dir = tmp_path / "out"
        out_dir.mkdir()
        mock_run.return_value = MagicMock(returncode=0)

        result = compile_tex(tex_file, output_dir=out_dir, engine="pdflatex", clean=False)

        assert result == out_dir / "doc.pdf"
        call_args = mock_run.call_args[0][0]
        assert "-outdir=" in " ".join(call_args) or any(
            "-outdir" in str(a) for a in call_args
        )

    @patch("render_latex.engine.subprocess.run")
    def test_raises_on_compilation_failure(
        self, mock_run: MagicMock, tmp_path: Path
    ) -> None:
        """compile_tex raises when latexmk returns non-zero."""
        tex_file = tmp_path / "doc.tex"
        tex_file.write_text(r"\documentclass{article}\begin{document}x\end{document}")
        mock_run.return_value = MagicMock(returncode=1, stderr=b"Error")

        with pytest.raises(RuntimeError) as exc_info:
            compile_tex(tex_file, output_dir=None, engine="pdflatex", clean=False)

        assert "compilation failed" in str(exc_info.value).lower()

    @patch("render_latex.engine.subprocess.run")
    def test_clean_runs_latexmk_c_after_success(
        self, mock_run: MagicMock, tmp_path: Path
    ) -> None:
        """When clean=True, latexmk -c is called after successful compile."""
        tex_file = tmp_path / "doc.tex"
        tex_file.write_text(r"\documentclass{article}\begin{document}x\end{document}")
        mock_run.return_value = MagicMock(returncode=0)

        compile_tex(tex_file, output_dir=None, engine="pdflatex", clean=True)

        assert mock_run.call_count == 2
        first_call = mock_run.call_args_list[0][0][0]
        second_call = mock_run.call_args_list[1][0][0]
        assert "-pdf" in first_call
        assert second_call[0] == "latexmk"
        assert "-c" in second_call

    def test_raises_on_missing_input_file(self) -> None:
        """compile_tex raises when input file does not exist."""
        with pytest.raises(FileNotFoundError):
            compile_tex(
                Path("/nonexistent/doc.tex"),
                output_dir=None,
                engine="pdflatex",
                clean=False,
            )

    def test_raises_on_invalid_engine(self, tmp_path: Path) -> None:
        """compile_tex raises when engine is not pdflatex or xelatex."""
        tex_file = tmp_path / "doc.tex"
        tex_file.write_text(r"\documentclass{article}\begin{document}x\end{document}")

        with pytest.raises(ValueError) as exc_info:
            compile_tex(tex_file, output_dir=None, engine="invalid", clean=False)

        assert "engine" in str(exc_info.value).lower()
