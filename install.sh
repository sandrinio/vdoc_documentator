#!/bin/bash

# VDoc Installer
# Installs/Updates vdoc from the main branch using pipx with --force

REPO_URL="git+https://github.com/sandrinio/vdoc_documentator.git"

if ! command -v pipx &> /dev/null; then
    echo "Error: pipx is not installed. Please install pipx first."
    exit 1
fi

# Check if vdoc is already installed
if pipx list | grep -q "package vdoc"; then
    echo "Found existing vdoc installation. Removing..."
    pipx uninstall vdoc
fi

echo "Installing vdoc from ${REPO_URL}..."
pipx install "$REPO_URL"

if [ $? -eq 0 ]; then
    echo "✅ vdoc installed successfully!"
    vdoc --version
else
    echo "❌ Installation failed."
    exit 1
fi
