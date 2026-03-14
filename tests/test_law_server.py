"""Tests for the law server MCP tools."""
import pytest
from conftest import load_mcp_server

server = load_mcp_server("law-server")
load_data = server.load_data
search_law = server.search_law
get_rights = server.get_rights
legal_procedure = server.legal_procedure


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
