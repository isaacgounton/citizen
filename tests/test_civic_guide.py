"""Tests for the civic guide MCP tools."""
import pytest
from conftest import load_mcp_server

server = load_mcp_server("civic-guide")
load_processes = server.load_processes
get_process = server.get_process
list_processes = server.list_processes
check_requirements = server.check_requirements


@pytest.fixture
def benin_processes():
    return load_processes("benin")


def test_load_processes_returns_list(benin_processes):
    assert isinstance(benin_processes, list)
    assert len(benin_processes) >= 8


def test_get_process_voter_registration(benin_processes):
    result = get_process(benin_processes, "voter-registration")
    assert result is not None
    assert "steps" in result
    assert len(result["steps"]) > 0


def test_get_process_unknown_returns_none(benin_processes):
    assert get_process(benin_processes, "nonexistent") is None


def test_list_processes_by_category(benin_processes):
    results = list_processes(benin_processes, "voting")
    assert len(results) > 0
    assert all(r["category"] == "voting" for r in results)


def test_check_requirements_returns_dict(benin_processes):
    reqs = check_requirements(benin_processes, "voter-registration")
    assert isinstance(reqs, dict)
    assert "requirements" in reqs
