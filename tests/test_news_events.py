"""Tests for the news & events MCP tools."""
import pytest
from conftest import load_mcp_server

server = load_mcp_server("news-events")
load_events = server.load_events
load_laws = server.load_laws
load_issues = server.load_issues
upcoming_events = server.upcoming_events
recent_laws = server.recent_laws
current_issues = server.current_issues


@pytest.fixture
def benin_events():
    return load_events("benin")


@pytest.fixture
def benin_laws():
    return load_laws("benin")


@pytest.fixture
def benin_issues():
    return load_issues("benin")


def test_load_events_with_content(benin_events):
    assert isinstance(benin_events, list)
    assert len(benin_events) > 0
    assert all("name" in e and "date" in e for e in benin_events)


def test_load_laws_with_content(benin_laws):
    assert isinstance(benin_laws, list)
    assert len(benin_laws) > 0
    assert all("title" in l for l in benin_laws)


def test_upcoming_events_have_dates(benin_events):
    results = upcoming_events(benin_events)
    assert isinstance(results, list)
    assert all("date" in e for e in results)


def test_recent_laws_have_titles(benin_laws):
    results = recent_laws(benin_laws)
    assert all("title" in l for l in results)


def test_current_issues_returns_ongoing(benin_issues):
    results = current_issues(benin_issues)
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(i["status"] == "ongoing" for i in results)
