#!/usr/bin/env python3
"""Set up nanobot workspace with Kofi's soul and MCP server configuration."""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

PROJECT_ROOT = Path(__file__).parent.parent
NANOBOT_DIR = Path.home() / ".nanobot"
NANOBOT_WORKSPACE = NANOBOT_DIR / "workspace"


def setup_soul(country: str = None):
    """Generate and install SOUL.md from country files."""
    from citizen_agent import CitizenAgent

    country = country or os.environ.get("CITIZEN_COUNTRY", "benin")
    agent = CitizenAgent(country)
    agent.install_soul()
    print(f"SOUL.md generated and installed for country: {country}")


def configure_mcp_servers():
    """Register MCP servers in nanobot config."""
    config_path = NANOBOT_DIR / "config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    project_root = str(PROJECT_ROOT)

    config.setdefault("tools", {})["mcpServers"] = {
        "law-server": {
            "command": "python3",
            "args": [f"{project_root}/mcp-servers/law-server/server.py"]
        },
        "civic-guide": {
            "command": "python3",
            "args": [f"{project_root}/mcp-servers/civic-guide/server.py"]
        },
        "resource-directory": {
            "command": "python3",
            "args": [f"{project_root}/mcp-servers/resource-directory/server.py"]
        },
        "news-events": {
            "command": "python3",
            "args": [f"{project_root}/mcp-servers/news-events/server.py"]
        }
    }

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print("MCP servers registered in nanobot config")


def setup():
    """Full setup: SOUL.md + MCP servers."""
    setup_soul()
    configure_mcp_servers()
    print("\nSetup complete! Run: nanobot agent")


if __name__ == "__main__":
    setup()
