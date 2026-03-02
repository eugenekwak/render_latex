# render-latex

CLI to compile LaTeX files to PDF using latexmk. 

## System Requirements

- **LaTeX backend** (see below) — required to compile .tex files to PDF
- **Python 3.10+**
- **uv** (recommended) or pip for dependency management

## LaTeX Backend

This tool invokes external programs (`latexmk`, `pdflatex`, `xelatex`) to turn `.tex` source files into PDFs. You must install a LaTeX distribution first; it is not a Python package.

**Recommended: TeX Live** — the standard distribution used in academia and industry. It includes all engines and packages needed for LaTeX documents.

### macOS (Homebrew)

```bash
# Full TeX Live (~4GB)
brew install --cask mactex

# Or smaller BasicTeX (~100MB)
brew install basictex
```

**MacTeX vs BasicTeX**

| | MacTeX | BasicTeX |
|---|--------|----------|
| **Size** | ~4 GB | ~100 MB |
| **Pros** | All packages included; compiles most documents without extra setup | Fast install; small disk footprint |
| **Cons** | Long download; large install | May need `tlmgr install <package>` for fonts (e.g. cmbright), bibliography, or layout packages |
| **Best for** | Documents with custom fonts, academic papers, zero-fuss workflow | Simple documents; users comfortable running `tlmgr` when needed |

Choose **MacTeX** if you want everything to work out of the box. Choose **BasicTeX** if you prefer a smaller install and can run `tlmgr install geometry cmbright enumitem` (or similar) when you hit missing packages.

After install, restart your terminal or run `eval "$(/usr/libexec/path_helper -s)"` so `latexmk` is on your PATH.

### Linux

```bash
# Ubuntu / Debian
sudo apt install texlive-full    # full (~5GB), or:
sudo apt install texlive-latex-base texlive-latex-extra   # smaller

# Fedora
sudo dnf install texlive-scheme-full
```

### Windows

Install [MiKTeX](https://miktex.org/download) (installer or portable). MiKTeX can auto-install missing packages on first use.

### Verify

```bash
latexmk --version
```

If that prints a version, you're ready to use render-latex.

## Installation

### With uv (recommended)

```bash
# Install uv: https://docs.astral.sh/uv/getting-started/installation/
uv sync
# Optional: run `uv lock` and commit uv.lock for reproducible installs
```

### With pip

```bash
pip install -e .
```

## Project Folders

| Folder | Purpose |
|--------|---------|
| `input/` | LaTeX source files (.tex) |
| `output/` | Generated PDF files |

## Usage

Run from the project root. The CLI looks for the named file in `input/` and writes the PDF to `output/`.

```bash
# Compile input.tex from input/
uv run python run.py input.tex
# or: uv run python -m render_latex input.tex

# Use XeLaTeX (Unicode, OpenType fonts)
uv run python run.py paper.tex --engine xelatex

# Clean auxiliary files after compile
uv run python run.py paper.tex --clean
```

> **Note:** Use `uv run python run.py` or `uv run python -m render_latex` rather than `uv run render-latex`, which can fail with editable installs.

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `input_file` | Yes | Name of the .tex file (e.g. `input.tex`). Searched in `input/`. |

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--engine` | `-e` | `pdflatex` | LaTeX engine: `pdflatex` or `xelatex` |
| `--clean` | `-c` | `False` | Remove .aux, .log, etc. after successful compile |

## Examples

**Compile a document:**
```bash
# Put yourfile.tex in input/, run from project root
uv run python run.py yourfile.tex
# Output: output/yourfile.pdf
```

**XeLaTeX with custom fonts:**
```bash
uv run python run.py document.tex --engine xelatex --clean
```

## Development

```bash
uv sync                    # Install dependencies
uv run pytest              # Run tests
uv run ruff check render_latex/ tests/     # Lint
```
