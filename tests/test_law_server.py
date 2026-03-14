"""Tests for the law server MCP tools."""
import sys
from pathlib import Path

# Ensure law-server is resolved first (conftest inserts multiple servers)
_law_server_path = str(Path(__file__).parent.parent / "mcp-servers" / "law-server")
if _law_server_path not in sys.path:
    sys.path.insert(0, _law_server_path)
else:
    sys.path.remove(_law_server_path)
    sys.path.insert(0, _law_server_path)

import pytest

from server import load_data, search_law, get_rights, legal_procedure


@pytest.fixture
def benin_data():
    return load_data("benin")


def test_load_data_returns_dict(benin_data):
    assert isinstance(benin_data, dict)
    assert "constitution" in benin_data
    assert "rights_duties" in benin_data
    assert "procedures" in benin_data


def test_search_law_finds_arrest_article(benin_data):
    results = search_law(benin_data, "arrestation")
    assert len(results) > 0
    assert any("arrest" in r.get("topics", []) or "arrestation" in r.get("title", "").lower() for r in results)


def test_search_law_returns_empty_for_nonsense(benin_data):
    results = search_law(benin_data, "xyzzy_nonsense_query")
    assert results == []


def test_get_rights_returns_list(benin_data):
    results = get_rights(benin_data, "property")
    assert isinstance(results, list)
    assert len(results) > 0


def test_legal_procedure_returns_steps(benin_data):
    results = legal_procedure(benin_data, "arrested")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "steps" in results[0]
