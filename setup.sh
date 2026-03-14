#!/bin/bash
set -e

echo "=== Citizen Agent Setup ==="

# Check Python 3.11+
if ! python3 -c "import sys; assert sys.version_info >= (3, 11)" 2>/dev/null; then
    # Try python3.12 explicitly
    if command -v python3.12 &>/dev/null; then
        echo "Using python3.12 for venv..."
        PYTHON=python3.12
    else
        echo "Error: Python 3.11+ required. Found: $(python3 --version)"
        exit 1
    fi
else
    PYTHON=python3
fi

# Check for API key (OpenAI or Anthropic)
if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "Warning: No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY"
    echo "Continuing setup anyway..."
fi

# Create venv if needed
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    $PYTHON -m venv .venv
fi

source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Initialize nanobot if needed
if [ ! -f "$HOME/.nanobot/config.json" ]; then
    echo "Initializing nanobot..."
    nanobot onboard
fi

# Set up workspace (SOUL.md + MCP servers)
echo "Setting up Kofi's workspace..."
python3 core/setup_workspace.py

# Run tests
echo "Running tests..."
pytest tests/ -v

echo ""
echo "=== Setup complete! ==="
echo "Run: source .venv/bin/activate && nanobot agent"
echo "Then talk to Kofi in French!"
