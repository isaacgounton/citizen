#!/usr/bin/env python3
"""Resource Directory — MCP server for finding offices, contacts, and help resources."""
import json
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("resource-directory", instructions="Find government offices, NGOs, and help resources.")
DATA_DIR = Path(__file__).parent / "data"

def load_resources(country: str) -> list:
    path = DATA_DIR / country / "resources.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_resource(resources: list, resource_type: str, location: str = None) -> list:
    results = [r for r in resources if r.get("type", "").lower() == resource_type.lower()]
    if location:
        results = [r for r in results if location.lower() in r.get("location", "").lower()]
    return results

def get_contact(resources: list, name: str) -> dict | None:
    for r in resources:
        if name.lower() in r.get("name", "").lower():
            return r
    return None

def find_help(resources: list, problem: str) -> list:
    problem_lower = problem.lower()
    return [
        r for r in resources
        if any(problem_lower in p.lower() for p in r.get("problems", []))
        or problem_lower in r.get("type", "").lower()
    ]

COUNTRY = "benin"
_resources = load_resources(COUNTRY)

@mcp.tool()
def find_nearby_resource(resource_type: str, location: str = "Cotonou") -> str:
    """Find offices by type (police, hospital, government, ngo, legal-aid) near a location."""
    results = find_resource(_resources, resource_type, location)
    if not results:
        return f"Aucune ressource de type '{resource_type}' trouvée à {location}."
    return json.dumps(results, ensure_ascii=False, indent=2)

@mcp.tool()
def get_contact_info(organization_name: str) -> str:
    """Get address, phone, hours for a specific organization."""
    result = get_contact(_resources, organization_name)
    if not result:
        return f"Organisation '{organization_name}' non trouvée."
    return json.dumps(result, ensure_ascii=False, indent=2)

@mcp.tool()
def find_help_for_problem(problem: str) -> str:
    """Find resources for a problem (corruption, theft, domestic-violence, health, emergency)."""
    results = find_help(_resources, problem)
    if not results:
        return f"Aucune ressource pour '{problem}'. Urgence: 117 (police), 118 (pompiers)."
    return json.dumps(results, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    mcp.run()
