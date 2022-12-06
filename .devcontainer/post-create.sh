#!/usr/bin/env bash

# Install poetry and dependencies
echo "Installing poetry..."
poetry install
poetry run pre-commit install --install-hook
poetry run mypy --install-types --non-interactive . || true

# Copy workspace settings to .vscode/settings.json
echo "Copying workspace settings..."
mkdir -p .vscode
cp .devcontainer/settings.json.template .vscode/settings.json

# Replace variables in settings.json
echo "Replacing variables in settings.json..."
export PYTHON_VENV="$(poetry show -v 2> /dev/null | head -n1 | cut -d ' ' -f 3)"
export PYTHON_VENV_BIN="$PYTHON_VENV/bin/python"
sed -i "s|{{PYTHON_VENV_BIN}}|$PYTHON_VENV_BIN|g" .vscode/settings.json

echo "Done!"
