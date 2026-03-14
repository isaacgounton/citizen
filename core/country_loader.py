#!/usr/bin/env python3
"""Country loader — loads country-specific configuration and content."""

import json
import os
from pathlib import Path


class CountryLoader:
    """Load country-specific files for the citizen agent."""

    def __init__(self, country: str = None):
        self.country = country or os.environ.get("CITIZEN_COUNTRY", "benin")
        self.project_root = Path(__file__).parent.parent
        self.country_dir = self.project_root / "countries" / self.country

        if not self.country_dir.exists():
            raise FileNotFoundError(
                f"Country '{self.country}' not found at {self.country_dir}"
            )

    def get_config(self) -> dict:
        """Load country config.json."""
        with open(self.country_dir / "config.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def get_knowledge_base(self) -> str:
        """Load country knowledge base markdown."""
        return (self.country_dir / "knowledge_base.md").read_text(encoding="utf-8")

    def get_personality(self) -> str:
        """Load country personality definition."""
        return (self.country_dir / "personality.md").read_text(encoding="utf-8")
