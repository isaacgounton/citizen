"""Tests for the civic guide MCP tools."""
import sys
from pathlib import Path

# Ensure civic-guide is resolved first (conftest inserts multiple servers)
_civic_guide_path = str(Path(__file__).parent.parent / "mcp-servers" / "civic-guide")
if _civic_guide_path not in sys.path:
    sys.path.insert(0, _civic_guide_path)
else:
    sys.path.remove(_civic_guide_path)
    sys.path.insert(0, _civic_guide_path)

import pytest
from server import load_processes, get_process, list_processes, check_requirements

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
