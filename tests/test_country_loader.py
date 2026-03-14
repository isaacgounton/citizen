"""Tests for the country loader module."""
import os
import pytest

from country_loader import CountryLoader


def test_load_benin_config():
    loader = CountryLoader("benin")
    config = loader.get_config()
    assert config["country_code"] == "bj"
    assert config["country_name"] == "Benin"


def test_load_benin_knowledge_base():
    loader = CountryLoader("benin")
    kb = loader.get_knowledge_base()
    assert "Cotonou" in kb
    assert "Dahomey" in kb


def test_load_benin_personality():
    loader = CountryLoader("benin")
    personality = loader.get_personality()
    assert "Kofi" in personality


def test_default_country_from_env():
    os.environ["CITIZEN_COUNTRY"] = "benin"
    loader = CountryLoader()
    assert loader.country == "benin"
    del os.environ["CITIZEN_COUNTRY"]


def test_unknown_country_raises():
    with pytest.raises(FileNotFoundError):
        CountryLoader("atlantis")
