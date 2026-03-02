"""Configuration for LaTeX engine selection and paths."""

from pathlib import Path

ENGINES = ("pdflatex", "xelatex")

# Static paths relative to current working directory
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")


def get_latexmk_args(engine: str) -> list[str]:
    """Return latexmk arguments for the given engine."""
    if engine not in ENGINES:
        raise ValueError(f"Engine must be one of {ENGINES}, got {engine!r}")
    base = ["-pdf", "-interaction=nonstopmode"]
    if engine == "xelatex":
        base.insert(1, "-xelatex")
    return base


def get_output_path(input_path: Path, output_dir: Path | None) -> Path:
    """Compute output PDF path from input .tex and optional output directory."""
    pdf_name = input_path.stem + ".pdf"
    if output_dir is not None:
        return output_dir / pdf_name
    return input_path.parent / pdf_name
