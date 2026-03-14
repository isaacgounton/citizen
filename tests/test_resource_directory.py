"""Tests for the resource directory MCP tools."""
import pytest
from conftest import load_mcp_server

server = load_mcp_server("resource-directory")
load_resources = server.load_resources
find_resource = server.find_resource
get_contact = server.get_contact
find_help = server.find_help


@pytest.fixture
def benin_resources():
    return load_resources("benin")


def test_load_resources_returns_list(benin_resources):
    assert isinstance(benin_resources, list)
    assert len(benin_resources) > 0


def test_find_resource_by_type(benin_resources):
    results = find_resource(benin_resources, "police", "Cotonou")
    assert len(results) > 0


def test_get_contact_returns_info(benin_resources):
    result = get_contact(benin_resources, "Commissariat Central")
    assert result is not None
    assert "phone" in result or "address" in result


def test_find_help_matches_problem(benin_resources):
    results = find_help(benin_resources, "corruption")
    assert len(results) > 0
