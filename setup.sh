#!/bin/zsh
set -e

# AI : assert MacTeX is installed — full distro, no extra packages needed
if ! command -v pdflatex &>/dev/null; then
  echo "pdflatex not found. Install MacTeX: brew install --cask mactex" >&2
  exit 1
fi

python3 build_resume.py
