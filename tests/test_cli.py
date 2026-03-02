"""Tests for the CLI."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from render_latex.cli import app

runner = CliRunner()


class TestCLI:
    """Tests for render-latex CLI."""

    def test_help(self) -> None:
        """--help prints usage."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Compile" in result.output
        assert "input_file" in result.output

    def test_rejects_non_tex_extension(self) -> None:
        """Rejects input without .tex extension."""
        result = runner.invoke(app, ["doc.txt"])
        assert result.exit_code == 1
        assert ".tex" in result.output

    def test_file_not_found_in_input(self, tmp_path: Path) -> None:
        """Exits when file not found in input/."""
        (tmp_path / "input").mkdir(parents=True)
        (tmp_path / "output").mkdir()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(app, ["nonexistent.tex"])
        assert result.exit_code == 1
        assert "not found" in result.output.lower()

    def test_rejects_invalid_engine(self, tmp_path: Path) -> None:
        """Rejects invalid engine."""
        (tmp_path / "input").mkdir(parents=True)
        (tmp_path / "output").mkdir()
        (tmp_path / "input" / "doc.tex").write_text(
            r"\documentclass{article}\begin{document}x\end{document}"
        )
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(app, ["doc.tex", "--engine", "invalid"])
        assert result.exit_code == 1
        assert "engine" in result.output.lower()
