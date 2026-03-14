#!/usr/bin/env python3
"""Law Server — MCP server for constitutional and legal information."""

import json
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("law-server", instructions="Search Benin constitutional law and citizen rights.")

DATA_DIR = Path(__file__).parent / "data"


def load_data(country: str) -> dict:
    """Load all legal data for a country."""
    country_dir = DATA_DIR / country
    data = {}
    for f in country_dir.glob("*.json"):
        with open(f, "r", encoding="utf-8") as fh:
            data[f.stem] = json.load(fh)
    return data


def search_law(data: dict, query: str) -> list:
    """Search constitution articles by topic keywords."""
    query_terms = query.lower().split()
    results = []
    for article in data.get("constitution", []):
        topics = [t.lower() for t in article.get("topics", [])]
        title = article.get("title", "").lower()
        text = article.get("text", "").lower()
        if any(term in topics or term in title or term in text for term in query_terms):
            results.append(article)
    return results


def get_rights(data: dict, topic: str) -> list:
    """Get citizen rights/duties for a topic category."""
    topic_lower = topic.lower()
    return [
        r for r in data.get("rights_duties", [])
        if topic_lower in [t.lower() for t in r.get("topics", [])]
        or topic_lower == r.get("category", "").lower()
    ]


def legal_procedure(data: dict, situation: str) -> list:
    """Get legal procedure for a specific situation."""
    situation_lower = situation.lower()
    return [
        p for p in data.get("procedures", [])
        if situation_lower in p.get("situation", "").lower()
        or any(situation_lower in t for t in p.get("topics", []))
    ]


COUNTRY = "benin"
_data = load_data(COUNTRY)


@mcp.tool()
def search_constitution(query: str) -> str:
    """Search the constitution for articles related to a topic. Use this before citing any law."""
    results = search_law(_data, query)
    if not results:
        return "Aucun article trouvé pour cette recherche. Consultez un juriste pour plus d'informations."
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def get_citizen_rights(topic: str) -> str:
    """Get citizen rights and duties for a category (property, labor, criminal, family, civic, education, health)."""
    results = get_rights(_data, topic)
    if not results:
        return f"Aucune information trouvée pour le sujet '{topic}'."
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def get_legal_procedure(situation: str) -> str:
    """Get step-by-step legal procedure for a situation (arrested, eviction, labor dispute, property dispute, domestic violence, business fraud)."""
    results = legal_procedure(_data, situation)
    if not results:
        return f"Aucune procédure trouvée pour '{situation}'. Consultez un avocat ou le Médiateur de la République."
    return json.dumps(results, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
