#!/usr/bin/env python3
"""Civic Guide — MCP server for step-by-step civic process walkthroughs."""
import json
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("civic-guide", instructions="Walk citizens through civic processes step by step.")
DATA_DIR = Path(__file__).parent / "data"

def load_processes(country: str) -> list:
    path = DATA_DIR / country / "processes.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_process(processes: list, process_id: str) -> dict | None:
    for p in processes:
        if p["id"] == process_id:
            return p
    return None

def list_processes(processes: list, category: str = None) -> list:
    if category:
        return [p for p in processes if p.get("category") == category]
    return [{"id": p["id"], "name": p["name"], "category": p["category"]} for p in processes]

def check_requirements(processes: list, process_id: str) -> dict:
    p = get_process(processes, process_id)
    if not p:
        return {"error": f"Process '{process_id}' not found"}
    return {
        "process": p["name"],
        "requirements": p.get("requirements", []),
        "cost": p.get("cost", "Non spécifié"),
        "timeline": p.get("timeline", "Non spécifié")
    }

COUNTRY = "benin"
_processes = load_processes(COUNTRY)

@mcp.tool()
def get_civic_process(name: str) -> str:
    """Get step-by-step guide for a civic process."""
    result = get_process(_processes, name)
    if not result:
        matches = [p for p in _processes if name.lower() in p["id"] or name.lower() in p["name"].lower()]
        if matches:
            result = matches[0]
        else:
            available = [p["id"] for p in _processes]
            return f"Processus non trouvé. Disponibles: {', '.join(available)}"
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
def list_civic_processes(category: str = None) -> str:
    """List available civic process guides."""
    results = list_processes(_processes, category)
    return json.dumps(results, ensure_ascii=False, indent=2)

@mcp.tool()
def get_process_requirements(process_name: str) -> str:
    """Get required documents, fees, and timeline for a civic process."""
    result = check_requirements(_processes, process_name)
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    mcp.run()
