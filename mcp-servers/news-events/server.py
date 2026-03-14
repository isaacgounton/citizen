#!/usr/bin/env python3
"""News & Events — MCP server for current affairs, events, and laws."""
import json
from datetime import datetime
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("news-events", instructions="Get upcoming events, recent laws, and current civic issues.")
DATA_DIR = Path(__file__).parent / "data"

def load_events(country: str) -> list:
    path = DATA_DIR / country / "events.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_laws(country: str) -> list:
    path = DATA_DIR / country / "laws.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_issues(country: str) -> list:
    path = DATA_DIR / country / "issues.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def upcoming_events(events: list) -> list:
    today = datetime.now().strftime("%Y-%m-%d")
    return [e for e in events if e.get("date", "") >= today or e.get("recurring", False)]

def recent_laws(laws: list) -> list:
    return sorted(laws, key=lambda l: l.get("year", 0), reverse=True)

def current_issues(issues: list) -> list:
    return [i for i in issues if i.get("status") == "ongoing"]

COUNTRY = "benin"
_events = load_events(COUNTRY)
_laws = load_laws(COUNTRY)
_issues = load_issues(COUNTRY)

@mcp.tool()
def get_upcoming_events() -> str:
    """Get upcoming national events, elections, and holidays."""
    results = upcoming_events(_events)
    if not results:
        return "Aucun événement à venir."
    return json.dumps(results, ensure_ascii=False, indent=2)

@mcp.tool()
def get_recent_laws() -> str:
    """Get recently passed or notable laws."""
    results = recent_laws(_laws)
    if not results:
        return "Aucune loi récente."
    return json.dumps(results, ensure_ascii=False, indent=2)

@mcp.tool()
def get_current_issues() -> str:
    """Get ongoing civic issues (unemployment, infrastructure, governance)."""
    results = current_issues(_issues)
    if not results:
        return "Aucun problème en cours."
    return json.dumps(results, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    mcp.run()
