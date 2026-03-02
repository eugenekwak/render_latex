"""CLI for render-latex."""

from pathlib import Path

import typer

from render_latex.config import ENGINES, INPUT_DIR, OUTPUT_DIR
from render_latex.engine import compile_tex

app = typer.Typer(
    name="render-latex",
    help="Compile LaTeX files to PDF using latexmk.",
)


def _find_input_file(filename: str) -> Path:
    """Search input folder for the named file. Raise FileNotFoundError if not found."""
    if not filename.lower().endswith(".tex"):
        filename = filename + ".tex"
    d = Path.cwd() / INPUT_DIR if not INPUT_DIR.is_absolute() else INPUT_DIR
    candidate = d / filename
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"File '{filename}' not found in {INPUT_DIR}/")


@app.command()
def main(
    input_file: str = typer.Argument(
        ...,
        help="Name of the .tex file (e.g. input.tex). Searched in input/.",
    ),
    engine: str = typer.Option(
        "pdflatex",
        "--engine",
        "-e",
        help="LaTeX engine: pdflatex or xelatex.",
    ),
    clean: bool = typer.Option(
        False,
        "--clean",
        "-c",
        help="Remove auxiliary files (.aux, .log, etc.) after successful compile.",
    ),
) -> None:
    """Compile a LaTeX file to PDF. Input from input/, output to output/."""
    if not input_file.lower().endswith(".tex"):
        if "." in input_file:
            typer.echo(f"Error: Input file must have .tex extension, got {input_file}", err=True)
            raise typer.Exit(1)
        input_file = input_file + ".tex"

    if engine not in ENGINES:
        typer.echo(f"Error: Engine must be one of {ENGINES}, got {engine!r}", err=True)
        raise typer.Exit(1)

    try:
        tex_path = _find_input_file(input_file)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    output_dir = Path.cwd() / OUTPUT_DIR if not OUTPUT_DIR.is_absolute() else OUTPUT_DIR

    try:
        pdf_path = compile_tex(
            input_path=tex_path,
            output_dir=output_dir,
            engine=engine,
            clean=clean,
        )
        typer.echo(f"PDF written to {pdf_path}")
    except RuntimeError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
