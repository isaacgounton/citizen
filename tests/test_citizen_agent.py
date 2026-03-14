"""Tests for the citizen agent prompt assembler."""
import pytest

from citizen_agent import CitizenAgent


def test_build_soul_contains_identity():
    agent = CitizenAgent("benin")
    soul = agent.build_soul()
    assert "Kofi Adjovi" in soul
    assert "Cotonou" in soul


def test_build_soul_contains_knowledge():
    agent = CitizenAgent("benin")
    soul = agent.build_soul()
    assert "Dahomey" in soul
    assert "Constitution" in soul or "constitution" in soul


def test_build_soul_contains_tool_instructions():
    agent = CitizenAgent("benin")
    soul = agent.build_soul()
    assert "search_constitution" in soul
    assert "JAMAIS" in soul


def test_build_soul_contains_error_handling():
    agent = CitizenAgent("benin")
    soul = agent.build_soul()
    assert "ne suis pas sûr" in soul


def test_install_soul_creates_file(tmp_path):
    agent = CitizenAgent("benin")
    agent.install_soul(tmp_path / "SOUL.md")
    assert (tmp_path / "SOUL.md").exists()
    content = (tmp_path / "SOUL.md").read_text()
    assert "Kofi" in content
