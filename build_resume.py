#!/usr/bin/env python3

import subprocess
import shutil
import sys
from datetime import date
from pathlib import Path

TEX_FILE = Path("henry_routson_resume.tex")
OUTPUT_PDF = Path(f"henry_routson_resume_{date.today().isoformat()}.pdf")
AUX_EXTENSIONS = [".aux", ".log", ".out"]

def find_pdflatex() -> str | None:
    for candidate in [
        "pdflatex",
        "/Library/TeX/texbin/pdflatex",
        "/usr/local/texlive/2026/bin/universal-darwin/pdflatex",
        "/usr/local/texlive/2026basic/bin/universal-darwin/pdflatex",
    ]:
        if shutil.which(candidate) or Path(candidate).exists():
            return candidate
    return None

def build(pdflatex: str) -> None:
    job_name = TEX_FILE.stem
    # AI : run twice so cross-references resolve correctly
    for _ in range(2):
        result = subprocess.run(
            [pdflatex, "-interaction=nonstopmode", f"-jobname={job_name}", str(TEX_FILE)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(result.stdout[-3000:])
            sys.exit(f"pdflatex failed (exit {result.returncode})")

    generated = TEX_FILE.with_suffix(".pdf")
    generated.rename(OUTPUT_PDF)
    print(f"Built: {OUTPUT_PDF}")

def cleanup() -> None:
    for ext in AUX_EXTENSIONS:
        p = TEX_FILE.with_suffix(ext)
        if p.exists():
            p.unlink()

if __name__ == "__main__":
    pdflatex = find_pdflatex()
    if not pdflatex:
        sys.exit(
            "pdflatex not found.\n"
            "Install with:  brew install --cask mactex\n"
            "Then restart your terminal."
        )
    build(pdflatex)
    cleanup()
