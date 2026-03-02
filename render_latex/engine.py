"""LaTeX compilation engine using latexmk."""

import subprocess
from pathlib import Path

from render_latex.config import ENGINES, get_latexmk_args, get_output_path


def compile_tex(
    input_path: Path,
    output_dir: Path | None = None,
    engine: str = "pdflatex",
    clean: bool = False,
) -> Path:
    """
    Compile a LaTeX file to PDF using latexmk.

    Args:
        input_path: Path to the .tex file.
        output_dir: Optional directory for output PDF. Defaults to input directory.
        engine: LaTeX engine: "pdflatex" or "xelatex".
        clean: If True, run latexmk -c after successful compile to remove aux files.

    Returns:
        Path to the generated PDF.

    Raises:
        FileNotFoundError: If input_path does not exist.
        ValueError: If engine is not pdflatex or xelatex.
        RuntimeError: If latexmk returns non-zero exit code.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if engine not in ENGINES:
        raise ValueError(f"Engine must be one of {ENGINES}, got {engine!r}")

    args = ["latexmk"] + get_latexmk_args(engine) + [str(input_path)]

    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        args.insert(-1, f"-outdir={output_dir}")

    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        cwd=input_path.parent,
    )

    if result.returncode != 0:
        stderr = result.stderr or result.stdout or "(no output)"
        raise RuntimeError(
            f"LaTeX compilation failed (exit code {result.returncode}): {stderr}"
        )

    if clean:
        clean_args = ["latexmk", "-c", str(input_path)]
        if output_dir is not None:
            clean_args.insert(-1, f"-outdir={output_dir}")
        subprocess.run(clean_args, capture_output=True, cwd=input_path.parent)

    return get_output_path(input_path, output_dir)
