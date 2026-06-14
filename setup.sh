 
 #!/bin/zsh
# Installs system dependencies and builds the resume PDF.

set -e

if ! command -v pdflatex &>/dev/null; then
  echo "Installing basictex..."
  brew install --cask basictex
  eval "$(/usr/libexec/path_helper)"
fi

# AI : install packages that BasicTeX omits but our .tex requires
sudo tlmgr install enumitem titlesec parskip

python3 build_resume.py
