# Citizen Agent Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build Kofi Adjovi, an ideal Benin citizen AI agent on the nanobot framework, with MCP tools for law, civic processes, resources, and news.

**Architecture:** nanobot handles channels (CLI/Telegram/WhatsApp), memory, and agent loop. Kofi's character lives in `SOUL.md` loaded by nanobot into the system prompt. Four FastMCP servers provide structured civic data. All country-specific content is isolated in `countries/benin/` and `mcp-servers/*/data/benin/` for future multi-country support.

**Tech Stack:** Python 3.11+, nanobot-ai (framework), FastMCP (tool servers), Anthropic Claude (LLM)

**Spec:** `docs/superpowers/specs/2026-03-14-citizen-agent-design.md`

---

## Chunk 1: Project Setup & Migration (Phase 0)

### Task 1: Create directory structure and migrate existing files

**Files:**
- Create: `countries/benin/` directory
- Create: `mcp-servers/law-server/data/benin/` directory
- Create: `mcp-servers/civic-guide/data/benin/` directory
- Create: `mcp-servers/resource-directory/data/benin/` directory
- Create: `mcp-servers/news-events/data/benin/` directory
- Create: `core/` directory
- Create: `tests/` directory
- Move: `benin_knowledge_base.md` → `countries/benin/knowledge_base.md`
- Move: `benin_citizen_personality.md` → `countries/benin/personality.md`
- Move: `system_prompt.txt` → `countries/benin/system_prompt_old.md` (kept as reference)
- Move: `test_scenarios.md` → `tests/test_scenarios.md`
- Delete: `citizen_agent.py` (will be rewritten)

- [ ] **Step 1: Create all directories**

```bash
mkdir -p countries/benin
mkdir -p mcp-servers/law-server/data/benin
mkdir -p mcp-servers/civic-guide/data/benin
mkdir -p mcp-servers/resource-directory/data/benin
mkdir -p mcp-servers/news-events/data/benin
mkdir -p core
mkdir -p tests
```

- [ ] **Step 2: Move existing files to new locations**

```bash
git mv benin_knowledge_base.md countries/benin/knowledge_base.md
git mv benin_citizen_personality.md countries/benin/personality.md
git mv system_prompt.txt countries/benin/system_prompt_old.md
git mv test_scenarios.md tests/test_scenarios.md
```

- [ ] **Step 3: Remove old citizen_agent.py (will be fully rewritten)**

```bash
git rm citizen_agent.py
```

- [ ] **Step 4: Update .gitignore**

Append `.nanobot/` to the existing `.gitignore` (which already has `.env`, `__pycache__/`, `*.pyc`):

```bash
echo ".nanobot/" >> .gitignore
```

- [ ] **Step 5: Commit migration**

```bash
git add -A
git commit -m "refactor: migrate to new project structure for nanobot integration"
```

---

### Task 2: Install nanobot and verify it runs

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Update requirements.txt**

```
nanobot-ai>=0.1.4
fastmcp>=0.1.0
anthropic>=0.18.0
python-dotenv>=1.0.0
```

- [ ] **Step 2: Install dependencies**

```bash
pip install -r requirements.txt
```
Expected: All packages install successfully.

- [ ] **Step 3: Run nanobot onboard**

```bash
nanobot onboard
```
Expected: Creates `~/.nanobot/` directory with `config.json`.

- [ ] **Step 4: Configure Anthropic provider**

Edit `~/.nanobot/config.json` to set:
```json
{
  "providers": {
    "anthropic": {
      "apiKey": "<value of ANTHROPIC_API_KEY env var>"
    }
  },
  "agents": {
    "defaults": {
      "model": "claude-sonnet-4-5-20250929",
      "provider": "anthropic"
    }
  }
}
```

- [ ] **Step 5: Verify nanobot runs**

```bash
nanobot agent -m "Hello, are you working?"
```
Expected: Gets a response from Claude. This confirms the framework + provider are connected.

- [ ] **Step 6: Commit requirements update**

```bash
git add requirements.txt
git commit -m "chore: update dependencies for nanobot + fastmcp"
```

---

## Chunk 2: Kofi's Character (Phase 1 — The Soul)

### Task 3: Create the country config

**Files:**
- Create: `countries/benin/config.json`

- [ ] **Step 1: Write country config**

Create `countries/benin/config.json`:
```json
{
  "country_code": "bj",
  "country_name": "Benin",
  "country_name_local": "Bénin",
  "primary_language": "French",
  "local_languages": ["Fon", "Yoruba", "Bariba", "Dendi"],
  "currency": "XOF (Franc CFA)",
  "capital": "Porto-Novo",
  "largest_city": "Cotonou",
  "government_type": "Presidential republic",
  "independence_date": "1960-08-01",
  "constitution_year": 1990,
  "citizen_name": "Kofi Adjovi",
  "citizen_age": 32,
  "citizen_city": "Cotonou",
  "citizen_occupation": "Enseignant et petit entrepreneur"
}
```

- [ ] **Step 2: Commit**

```bash
git add countries/benin/config.json
git commit -m "feat: add Benin country configuration"
```

---

### Task 4: Prepare for SOUL.md generation

SOUL.md is generated dynamically by `core/citizen_agent.py` (Task 10) from country files. This task prepares the workspace setup script that will use it.

**Files:**
- Create: `core/setup_workspace.py`

- [ ] **Step 1: Write setup_workspace.py**

Create `core/setup_workspace.py` — the script that assembles SOUL.md from country files and configures nanobot:

```python
#!/usr/bin/env python3
"""Set up nanobot workspace with Kofi's soul and MCP server configuration."""

import json
import os
import sys
from pathlib import Path

# Add core/ to path so we can import citizen_agent
sys.path.insert(0, str(Path(__file__).parent))

PROJECT_ROOT = Path(__file__).parent.parent
NANOBOT_DIR = Path.home() / ".nanobot"
NANOBOT_WORKSPACE = NANOBOT_DIR / "workspace"


def setup_soul(country: str = None):
    """Generate and install SOUL.md from country files."""
    from citizen_agent import CitizenAgent

    country = country or os.environ.get("CITIZEN_COUNTRY", "benin")
    agent = CitizenAgent(country)
    agent.install_soul()
    print(f"SOUL.md generated and installed for country: {country}")


def configure_mcp_servers():
    """Register MCP servers in nanobot config."""
    config_path = NANOBOT_DIR / "config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    project_root = str(PROJECT_ROOT)

    config.setdefault("tools", {})["mcpServers"] = {
        "law-server": {
            "command": "python3",
            "args": [f"{project_root}/mcp-servers/law-server/server.py"]
        },
        "civic-guide": {
            "command": "python3",
            "args": [f"{project_root}/mcp-servers/civic-guide/server.py"]
        },
        "resource-directory": {
            "command": "python3",
            "args": [f"{project_root}/mcp-servers/resource-directory/server.py"]
        },
        "news-events": {
            "command": "python3",
            "args": [f"{project_root}/mcp-servers/news-events/server.py"]
        }
    }

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print("MCP servers registered in nanobot config")


def setup():
    """Full setup: SOUL.md + MCP servers."""
    setup_soul()
    configure_mcp_servers()
    print("\nSetup complete! Run: nanobot agent")


if __name__ == "__main__":
    setup()
```

Note: This script depends on `core/citizen_agent.py` (Task 10) and `core/country_loader.py` (Task 12). It will only work after those are implemented. For now, just create the file.

- [ ] **Step 2: Commit**

```bash
git add core/setup_workspace.py
git commit -m "feat: add workspace setup script"
```

---

### Task 5: Rewrite the personality file as ideal citizen reference

**Files:**
- Modify: `countries/benin/personality.md`

- [ ] **Step 1: Rewrite personality.md**

Rewrite `countries/benin/personality.md` to match the new ideal citizen archetype from the spec (section 3.1 and 3.2). Key changes from the current file:
- Remove "Weaknesses" section that frames flaws as potential for moral compromise
- Replace with "Human Struggles" section that frames challenges as tension that strengthens resolve
- Remove scenario responses that show Kofi paying bribes or compromising
- Replace with responses showing Kofi refusing firmly while acknowledging difficulty
- Keep all identity, cultural background, and speech style sections
- Add the 5 example responses from spec section 3.1.1

- [ ] **Step 2: Commit**

```bash
git add countries/benin/personality.md
git commit -m "feat: rewrite personality as ideal citizen archetype"
```

---

## Chunk 3: MCP Tool Servers (Phase 1 — The Powers)

### Task 6: Build the Law Server

**Files:**
- Create: `mcp-servers/law-server/server.py`
- Create: `mcp-servers/law-server/data/benin/constitution.json`
- Create: `mcp-servers/law-server/data/benin/rights_duties.json`
- Create: `mcp-servers/law-server/data/benin/procedures.json`
- Test: `tests/test_law_server.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_law_server.py`:
```python
"""Tests for the law server MCP tools."""
import json
from pathlib import Path
import pytest

# conftest.py adds mcp-servers paths, so we import directly from server module
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
    assert any("arrestation" in r.get("title", "").lower() for r in results)


def test_search_law_returns_empty_for_nonsense(benin_data):
    results = search_law(benin_data, "xyzzy_nonsense_query")
    assert results == []


def test_get_rights_returns_list(benin_data):
    results = get_rights(benin_data, "property")
    assert isinstance(results, list)


def test_legal_procedure_returns_steps(benin_data):
    results = legal_procedure(benin_data, "arrested")
    assert isinstance(results, list)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_law_server.py -v
```
Expected: FAIL — `server` module not found (conftest.py not created yet).

- [ ] **Step 3: Create constitution data**

Create `mcp-servers/law-server/data/benin/constitution.json` with key articles relevant to citizen rights. Include at minimum articles covering:
- Right to liberty and security (art. 18)
- Protection against arbitrary arrest (art. 18-19)
- Right to property (art. 22)
- Freedom of expression (art. 23)
- Freedom of association (art. 25)
- Right to vote (art. 6)
- Duty to pay taxes (art. 33)
- Duty to defend the nation (art. 34)
- Right to education (art. 12-13)
- Right to work (art. 30)

Each article follows this schema:
```json
{
  "article": 18,
  "title": "Droit à la liberté et à la sécurité",
  "text": "Nul ne peut être soumis à la torture...",
  "topics": ["liberty", "security", "torture", "rights"],
  "plain_language": "No one can be tortured or subjected to cruel treatment."
}
```

Research the actual Benin constitution text to populate accurate articles.

- [ ] **Step 4: Create rights_duties data**

Create `mcp-servers/law-server/data/benin/rights_duties.json` organized by category:
```json
[
  {
    "category": "property",
    "type": "right",
    "title": "Droit de propriété",
    "description": "Tout citoyen a droit à la propriété...",
    "constitutional_basis": "Article 22",
    "practical_info": "Pour enregistrer une propriété, contactez le service des domaines.",
    "topics": ["property", "land", "ownership"]
  }
]
```

Categories: property, labor, criminal, family, civic, education, health.

- [ ] **Step 4b: Create procedures data**

Create `mcp-servers/law-server/data/benin/procedures.json` with common legal procedures:
```json
[
  {
    "situation": "arrested",
    "title": "Que faire en cas d'arrestation",
    "steps": [
      "Demander calmement le motif de l'interpellation",
      "Demander à voir le mandat si applicable",
      "Vous avez droit à un avocat — demandez-le",
      "Ne signez rien sans lire et comprendre",
      "Vous pouvez contacter votre famille"
    ],
    "legal_basis": "Articles 18-19 de la Constitution",
    "topics": ["arrest", "police", "detention", "rights"],
    "warning": "La garde à vue ne peut excéder 48h sans autorisation du procureur"
  }
]
```

Include procedures for: arrested, eviction, labor dispute, property dispute, domestic violence, business fraud.

- [ ] **Step 5: Write the law server**

Create `mcp-servers/law-server/server.py`:
```python
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


# Load data at startup
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
```

- [ ] **Step 6: Create tests/conftest.py for module imports**

Create `tests/conftest.py` (shared by all MCP server tests):
```python
import sys
from pathlib import Path

# Add mcp-servers to path so tests can import server modules via `from server import ...`
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-servers" / "law-server"))
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-servers" / "civic-guide"))
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-servers" / "resource-directory"))
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-servers" / "news-events"))
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
```

- [ ] **Step 7: Run tests to verify they pass**

```bash
pytest tests/test_law_server.py -v
```
Expected: All 4 tests PASS.

- [ ] **Step 8: Commit**

```bash
git add mcp-servers/law-server/ tests/test_law_server.py tests/conftest.py
git commit -m "feat: add law server MCP with Benin constitution data"
```

---

### Task 7: Build the Civic Guide Server

**Files:**
- Create: `mcp-servers/civic-guide/server.py`
- Create: `mcp-servers/civic-guide/data/benin/processes.json`
- Test: `tests/test_civic_guide.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_civic_guide.py`:
```python
"""Tests for the civic guide MCP tools."""
import pytest

# conftest.py adds mcp-servers paths
from server import load_processes, get_process, list_processes, check_requirements


@pytest.fixture
def benin_processes():
    return load_processes("benin")


def test_load_processes_returns_list(benin_processes):
    assert isinstance(benin_processes, list)
    assert len(benin_processes) > 0


def test_get_process_voter_registration(benin_processes):
    result = get_process(benin_processes, "voter-registration")
    assert result is not None
    assert "steps" in result
    assert len(result["steps"]) > 0


def test_get_process_unknown_returns_none(benin_processes):
    result = get_process(benin_processes, "nonexistent-process")
    assert result is None


def test_list_processes_by_category(benin_processes):
    results = list_processes(benin_processes, "voting")
    assert len(results) > 0
    assert all(r["category"] == "voting" for r in results)


def test_check_requirements_returns_list(benin_processes):
    reqs = check_requirements(benin_processes, "voter-registration")
    assert isinstance(reqs, dict)
    assert "requirements" in reqs
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_civic_guide.py -v
```
Expected: FAIL — module not found.

- [ ] **Step 3: Create processes data**

Create `mcp-servers/civic-guide/data/benin/processes.json` with civic processes. Include at minimum:
1. `voter-registration` — how to register to vote
2. `voting` — how to vote on election day
3. `national-id` — how to get RAVIP national ID
4. `birth-certificate` — how to request a birth certificate
5. `business-registration` — how to register a business
6. `police-report` — how to file a police report
7. `corruption-report` — how to report corruption
8. `passport` — how to apply for a passport

Each process follows the schema from the spec:
```json
{
  "id": "voter-registration",
  "name": "Inscription sur la liste électorale",
  "category": "voting",
  "steps": [...],
  "requirements": [...],
  "cost": "Gratuit",
  "timeline": "...",
  "tips": [...],
  "last_updated": "2026-03-14"
}
```

Research actual Benin civic procedures for accuracy.

- [ ] **Step 4: Write the civic guide server**

Create `mcp-servers/civic-guide/server.py`:
```python
#!/usr/bin/env python3
"""Civic Guide — MCP server for step-by-step civic process walkthroughs."""

import json
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("civic-guide", instructions="Walk citizens through civic processes step by step.")

DATA_DIR = Path(__file__).parent / "data"


def load_processes(country: str) -> list:
    """Load all civic processes for a country."""
    path = DATA_DIR / country / "processes.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_process(processes: list, process_id: str) -> dict | None:
    """Get a specific process by ID."""
    for p in processes:
        if p["id"] == process_id:
            return p
    return None


def list_processes(processes: list, category: str = None) -> list:
    """List processes, optionally filtered by category."""
    if category:
        return [p for p in processes if p.get("category") == category]
    return [{"id": p["id"], "name": p["name"], "category": p["category"]} for p in processes]


def check_requirements(processes: list, process_id: str) -> dict:
    """Get requirements for a specific process."""
    p = get_process(processes, process_id)
    if not p:
        return {"error": f"Process '{process_id}' not found"}
    return {
        "process": p["name"],
        "requirements": p.get("requirements", []),
        "cost": p.get("cost", "Non spécifié"),
        "timeline": p.get("timeline", "Non spécifié")
    }


COUNTRY = "benin"
_processes = load_processes(COUNTRY)


@mcp.tool()
def get_civic_process(name: str) -> str:
    """Get step-by-step guide for a civic process (voting, national-id, birth-certificate, business-registration, police-report, corruption-report)."""
    result = get_process(_processes, name)
    if not result:
        # Try fuzzy match
        matches = [p for p in _processes if name.lower() in p["id"] or name.lower() in p["name"].lower()]
        if matches:
            result = matches[0]
        else:
            available = [p["id"] for p in _processes]
            return f"Processus non trouvé. Processus disponibles: {', '.join(available)}"
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def list_civic_processes(category: str = None) -> str:
    """List available civic process guides. Optional category filter (voting, identity, business, legal)."""
    results = list_processes(_processes, category)
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def get_process_requirements(process_name: str) -> str:
    """Get required documents, fees, and timeline for a civic process."""
    result = check_requirements(_processes, process_name)
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
pytest tests/test_civic_guide.py -v
```
Expected: All 5 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add mcp-servers/civic-guide/ tests/test_civic_guide.py
git commit -m "feat: add civic guide MCP server with Benin processes"
```

---

### Task 8: Build the Resource Directory Server

**Files:**
- Create: `mcp-servers/resource-directory/server.py`
- Create: `mcp-servers/resource-directory/data/benin/resources.json`
- Test: `tests/test_resource_directory.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_resource_directory.py`:
```python
"""Tests for the resource directory MCP tools."""
import pytest

# conftest.py adds mcp-servers paths
from server import load_resources, find_resource, get_contact, find_help


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
    result = get_contact(benin_resources, "Commissariat Central de Cotonou")
    assert result is not None
    assert "phone" in result or "address" in result


def test_find_help_matches_problem(benin_resources):
    results = find_help(benin_resources, "corruption")
    assert len(results) > 0
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_resource_directory.py -v
```
Expected: FAIL.

- [ ] **Step 3: Create resources data**

Create `mcp-servers/resource-directory/data/benin/resources.json` with real Benin contacts. Include:
- Police stations in major cities (Cotonou, Porto-Novo, Parakou)
- Emergency numbers (police 117, fire 118, SAMU 112)
- Government offices (mairies, préfectures)
- Anti-corruption office (ANLC — Autorité Nationale de Lutte contre la Corruption)
- Legal aid organizations
- Major hospitals
- Ombudsman (Médiateur de la République)

Schema:
```json
{
  "name": "Commissariat Central de Cotonou",
  "type": "police",
  "location": "Cotonou",
  "department": "Littoral",
  "address": "Boulevard de la Marina, Cotonou",
  "phone": "+229 21 31 22 33",
  "hours": "24h/24",
  "services": ["plainte", "urgence", "document"],
  "problems": ["theft", "assault", "corruption", "emergency"],
  "last_updated": "2026-03-14"
}
```

Research actual addresses and phone numbers for accuracy.

- [ ] **Step 4: Write the resource directory server**

Create `mcp-servers/resource-directory/server.py`:
```python
#!/usr/bin/env python3
"""Resource Directory — MCP server for finding offices, contacts, and help resources."""

import json
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("resource-directory", instructions="Find government offices, NGOs, and help resources for citizens.")

DATA_DIR = Path(__file__).parent / "data"


def load_resources(country: str) -> list:
    """Load all resources for a country."""
    path = DATA_DIR / country / "resources.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_resource(resources: list, resource_type: str, location: str = None) -> list:
    """Find resources by type and optional location."""
    results = [r for r in resources if r.get("type", "").lower() == resource_type.lower()]
    if location:
        results = [r for r in results if location.lower() in r.get("location", "").lower()]
    return results


def get_contact(resources: list, name: str) -> dict | None:
    """Get contact info for a specific organization."""
    for r in resources:
        if name.lower() in r.get("name", "").lower():
            return r
    return None


def find_help(resources: list, problem: str) -> list:
    """Find resources that can help with a specific problem."""
    problem_lower = problem.lower()
    return [
        r for r in resources
        if any(problem_lower in p.lower() for p in r.get("problems", []))
        or problem_lower in r.get("type", "").lower()
    ]


COUNTRY = "benin"
_resources = load_resources(COUNTRY)


@mcp.tool()
def find_nearby_resource(resource_type: str, location: str = "Cotonou") -> str:
    """Find offices or organizations by type (police, hospital, government, ngo, legal-aid) near a location."""
    results = find_resource(_resources, resource_type, location)
    if not results:
        return f"Aucune ressource de type '{resource_type}' trouvée à {location}."
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def get_contact_info(organization_name: str) -> str:
    """Get address, phone number, and hours for a specific organization."""
    result = get_contact(_resources, organization_name)
    if not result:
        return f"Organisation '{organization_name}' non trouvée dans l'annuaire."
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def find_help_for_problem(problem: str) -> str:
    """Find resources that can help with a problem (corruption, theft, domestic-violence, legal-aid, health, emergency)."""
    results = find_help(_resources, problem)
    if not results:
        return f"Aucune ressource trouvée pour '{problem}'. En cas d'urgence, appelez le 117 (police) ou 118 (pompiers)."
    return json.dumps(results, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
pytest tests/test_resource_directory.py -v
```
Expected: All 4 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add mcp-servers/resource-directory/ tests/test_resource_directory.py
git commit -m "feat: add resource directory MCP server with Benin contacts"
```

---

### Task 9: Build the News & Events Server

**Files:**
- Create: `mcp-servers/news-events/server.py`
- Create: `mcp-servers/news-events/data/benin/events.json`
- Create: `mcp-servers/news-events/data/benin/laws.json`
- Test: `tests/test_news_events.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_news_events.py`:
```python
"""Tests for the news & events MCP tools."""
import pytest

# conftest.py adds mcp-servers paths
from server import load_events, load_laws, load_issues, upcoming_events, recent_laws, current_issues


@pytest.fixture
def benin_events():
    return load_events("benin")


@pytest.fixture
def benin_laws():
    return load_laws("benin")


@pytest.fixture
def benin_issues():
    return load_issues("benin")


def test_load_events_returns_list_with_content(benin_events):
    assert isinstance(benin_events, list)
    assert len(benin_events) > 0
    assert all("name" in e and "date" in e for e in benin_events)


def test_load_laws_returns_list_with_content(benin_laws):
    assert isinstance(benin_laws, list)
    assert len(benin_laws) > 0
    assert all("title" in law for law in benin_laws)


def test_upcoming_events_have_dates(benin_events):
    results = upcoming_events(benin_events)
    assert isinstance(results, list)
    # All returned events should have a date field
    assert all("date" in e for e in results)


def test_recent_laws_have_titles(benin_laws):
    results = recent_laws(benin_laws)
    assert isinstance(results, list)
    assert all("title" in law for law in results)


def test_current_issues_returns_list(benin_issues):
    results = current_issues(benin_issues)
    assert isinstance(results, list)
    assert len(results) > 0
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_news_events.py -v
```
Expected: FAIL.

- [ ] **Step 3: Create events and laws data**

Create `mcp-servers/news-events/data/benin/events.json`:
```json
[
  {
    "name": "Fête Nationale du Vodun",
    "date": "2027-01-10",
    "type": "national_holiday",
    "description": "Journée nationale célébrant le patrimoine Vodun du Bénin",
    "recurring": true,
    "last_updated": "2026-03-14"
  },
  {
    "name": "Fête de l'Indépendance",
    "date": "2026-08-01",
    "type": "national_holiday",
    "description": "Célébration de l'indépendance du Bénin (1er août 1960)",
    "recurring": true,
    "last_updated": "2026-03-14"
  }
]
```

Create `mcp-servers/news-events/data/benin/laws.json`:
```json
[
  {
    "title": "Code du Numérique",
    "year": 2017,
    "description": "Loi sur le numérique au Bénin, encadrant le commerce électronique et la protection des données",
    "topics": ["digital", "data_protection", "e-commerce"],
    "last_updated": "2026-03-14"
  }
]
```

- [ ] **Step 3b: Create issues data**

Create `mcp-servers/news-events/data/benin/issues.json`:
```json
[
  {
    "title": "Chômage des jeunes",
    "category": "economy",
    "description": "Le taux de chômage des jeunes reste élevé, particulièrement dans les zones urbaines",
    "status": "ongoing",
    "last_updated": "2026-03-14"
  },
  {
    "title": "Accès à l'électricité",
    "category": "infrastructure",
    "description": "Les coupures de courant (sodec) restent fréquentes dans plusieurs régions",
    "status": "ongoing",
    "last_updated": "2026-03-14"
  },
  {
    "title": "Lutte contre la corruption",
    "category": "governance",
    "description": "Renforcement des mécanismes anti-corruption via l'ANLC",
    "status": "ongoing",
    "last_updated": "2026-03-14"
  }
]
```

- [ ] **Step 4: Write the news & events server**

Create `mcp-servers/news-events/server.py`:
```python
#!/usr/bin/env python3
"""News & Events — MCP server for current affairs, upcoming events, and recent laws."""

import json
from datetime import datetime
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP("news-events", instructions="Get upcoming events, recent laws, and current civic issues.")

DATA_DIR = Path(__file__).parent / "data"


def load_events(country: str) -> list:
    """Load events for a country."""
    path = DATA_DIR / country / "events.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_laws(country: str) -> list:
    """Load recent laws for a country."""
    path = DATA_DIR / country / "laws.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_issues(country: str) -> list:
    """Load current issues for a country."""
    path = DATA_DIR / country / "issues.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def upcoming_events(events: list) -> list:
    """Get upcoming events (future dates + recurring)."""
    today = datetime.now().strftime("%Y-%m-%d")
    return [
        e for e in events
        if e.get("date", "") >= today or e.get("recurring", False)
    ]


def recent_laws(laws: list) -> list:
    """Get all laws (sorted by year descending)."""
    return sorted(laws, key=lambda l: l.get("year", 0), reverse=True)


def current_issues(issues: list) -> list:
    """Get ongoing civic issues."""
    return [i for i in issues if i.get("status") == "ongoing"]


COUNTRY = "benin"
_events = load_events(COUNTRY)
_laws = load_laws(COUNTRY)
_issues = load_issues(COUNTRY)


@mcp.tool()
def get_upcoming_events() -> str:
    """Get upcoming national events, elections, and holidays."""
    results = upcoming_events(_events)
    if not results:
        return "Aucun événement à venir dans les données actuelles."
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def get_recent_laws() -> str:
    """Get recently passed or notable laws."""
    results = recent_laws(_laws)
    if not results:
        return "Aucune loi récente dans les données actuelles."
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def get_current_issues() -> str:
    """Get ongoing civic issues affecting citizens (unemployment, infrastructure, governance)."""
    results = current_issues(_issues)
    if not results:
        return "Aucun problème en cours dans les données actuelles."
    return json.dumps(results, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
pytest tests/test_news_events.py -v
```
Expected: All 4 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add mcp-servers/news-events/ tests/test_news_events.py
git commit -m "feat: add news & events MCP server with Benin data"
```

---

## Chunk 4: Integration & Nanobot Config (Phase 1 — Wiring It Together)

### Task 10: Create the country_loader module

country_loader.py must be created before citizen_agent.py (Task 11), which imports it.

**Files:**
- Create: `core/country_loader.py`
- Test: `tests/test_country_loader.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_country_loader.py`:
```python
"""Tests for the country loader module."""
import os
import pytest

# conftest.py adds core/ to path
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_country_loader.py -v
```
Expected: FAIL — module not found.

- [ ] **Step 3: Write country_loader.py**

Create `core/country_loader.py`:
```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_country_loader.py -v
```
Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add core/country_loader.py tests/test_country_loader.py
git commit -m "feat: add country loader module"
```

---

### Task 11: Create core/citizen_agent.py — the prompt assembler

This module assembles SOUL.md dynamically from country files. It reads personality, knowledge base, and config, then generates the final SOUL.md that nanobot loads. Depends on country_loader.py (Task 10).

**Files:**
- Create: `core/citizen_agent.py`
- Test: `tests/test_citizen_agent.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_citizen_agent.py`:
```python
"""Tests for the citizen agent prompt assembler."""
import pytest

# conftest.py adds core/ to path
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_citizen_agent.py -v
```
Expected: FAIL — module not found.

- [ ] **Step 3: Write citizen_agent.py**

Create `core/citizen_agent.py`:
```python
#!/usr/bin/env python3
"""Citizen Agent — assembles the SOUL.md prompt from country files."""

from pathlib import Path
from country_loader import CountryLoader


class CitizenAgent:
    """Assembles the agent's system prompt (SOUL.md) from country-specific files."""

    def __init__(self, country: str = None):
        self.loader = CountryLoader(country)
        self.config = self.loader.get_config()

    def build_soul(self) -> str:
        """Build the complete SOUL.md content from country files."""
        config = self.config
        personality = self.loader.get_personality()
        knowledge = self.loader.get_knowledge_base()

        return f"""# SOUL — {config['citizen_name']}, Citoyen de {config['country_name_local']}

## QUI JE SUIS

Je suis **{config['citizen_name']}**, {config['citizen_age']} ans, vivant à {config['citizen_city']}, {config['country_name_local']}.
Je suis {config['citizen_occupation']}.
Je parle {config['primary_language']} et {', '.join(config['local_languages'][:2])}.

---

## MON CARACTÈRE

{personality}

---

## MES CONNAISSANCES SUR {config['country_name_local'].upper()}

{knowledge}

---

## COMMENT J'UTILISE MES OUTILS

### Règles absolues :
- **TOUJOURS** appeler `search_constitution` ou `get_citizen_rights` AVANT de citer une loi ou un article
- **TOUJOURS** appeler `get_civic_process` quand quelqu'un me demande comment faire une démarche
- **TOUJOURS** appeler `find_nearby_resource` ou `find_help_for_problem` quand je recommande un lieu ou un contact
- **TOUJOURS** appeler `get_legal_procedure` quand quelqu'un fait face à une situation juridique
- **JAMAIS** inventer une information juridique, une adresse, ou un numéro de téléphone
- Si un outil ne retourne rien, je dis honnêtement que je ne sais pas et je réfère vers une ressource spécifique

### Quand je ne sais pas :
"Là, franchement, je ne suis pas sûr. Je ne veux pas te donner une mauvaise information. Mieux vaut demander directement à [ressource spécifique]."

### Fraîcheur des données :
Si les données d'un outil incluent un champ `last_updated` datant de plus de 6 mois, j'ajoute : "Ces informations datent de [date], vérifie auprès de [bureau] que rien n'a changé."

---

## MON COMPORTEMENT

### Face à la corruption :
Je refuse. Toujours. Même quand j'ai peur. Et j'explique pourquoi avec la loi.

### Face aux difficultés :
Je suis humain — l'argent est serré, la famille demande beaucoup, je suis parfois fatigué. Mais je ne lâche jamais. Ces difficultés me rendent plus fort, pas plus faible.

### Face aux citoyens :
Je suis chaleureux, je salue, je demande des nouvelles de la famille. Je parle avec des proverbes, du cœur, et de la vérité. Je suis leur frère, leur voisin, leur compatriote.

### Exemples de ma voix :

**Situation de corruption :**
> "Ah mon frère, je connais cette situation. Le cœur bat fort, on a peur. Moi aussi j'ai eu peur la dernière fois. Mais j'ai dit non. Pourquoi ? Parce que l'article 37 de notre Constitution nous protège — nul ne peut être arrêté arbitrairement. Tu as le droit de demander le motif de l'interpellation. C'est dur, mais chaque fois qu'on refuse, on rend le Bénin un peu meilleur. Kpodji, mon frère."

**Pression familiale :**
> "Écoute, je comprends. Mon oncle m'a demandé 100.000 FCFA le mois dernier pour la toiture de sa maison. Je n'avais que 40.000 d'économies. J'ai pas dormi cette nuit-là. Mais j'ai été honnête avec lui — 'Tonton, voici ce que j'ai, c'est tout ce que je peux.' Petit à petit l'oiseau fait son nid."

**Encouragement civique :**
> "Tu me dis que voter ne sert à rien ? Je comprends la frustration, vraiment. Mais en 1990, nos parents se sont battus pour ce droit. La Conférence Nationale, c'est nous qui l'avons gagnée. Moi je vote. Même fatigué, même déçu. C'est mon devoir, c'est notre force."

---

## LANGUE

- Je parle en **{config['primary_language']}**
- J'utilise parfois des mots en {config['local_languages'][0]} pour l'emphase
- Je vouvoie les aînés et les inconnus, je tutoie les pairs
- J'utilise des proverbes naturellement
- Je salue chaleureusement et je demande des nouvelles de la famille avant de parler d'affaires
"""

    def install_soul(self, dest_path: Path = None):
        """Write SOUL.md to a destination (default: nanobot workspace)."""
        if dest_path is None:
            dest_path = Path.home() / ".nanobot" / "workspace" / "SOUL.md"
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(self.build_soul(), encoding="utf-8")
        print(f"SOUL.md installed at {dest_path}")
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_citizen_agent.py -v
```
Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add core/citizen_agent.py tests/test_citizen_agent.py
git commit -m "feat: add citizen agent prompt assembler"
```

---

### Task 12: Run full setup and test integration

`core/setup_workspace.py` (created in Task 4) handles SOUL.md generation and MCP server registration. Now that all components exist (country_loader Task 10, citizen_agent Task 11, MCP servers Tasks 6-9), run the full setup.

**Files:**
- No new files — uses `core/setup_workspace.py` from Task 4

- [ ] **Step 1: Run full setup**

```bash
python3 core/setup_workspace.py
```
Expected: SOUL.md generated and installed, MCP servers registered in nanobot config.

- [ ] **Step 2: Verify SOUL.md was generated correctly**

```bash
head -20 ~/.nanobot/workspace/SOUL.md
```
Expected: Shows Kofi's identity section with name, age, city.

- [ ] **Step 3: Test the full agent with tool use**

```bash
nanobot agent -m "Quels sont mes droits si la police m'arrête ?"
```
Expected: Kofi calls the law-server to look up arrest-related articles, then responds in character citing the actual constitutional articles.

- [ ] **Step 4: Test civic guide integration**

```bash
nanobot agent -m "Comment faire pour m'inscrire sur la liste électorale ?"
```
Expected: Kofi calls the civic-guide to get voter registration steps, then walks the user through them in his warm, encouraging style.

- [ ] **Step 5: Test resource directory integration**

```bash
nanobot agent -m "Où est-ce que je peux signaler un cas de corruption à Cotonou ?"
```
Expected: Kofi calls the resource-directory, returns the ANLC contact with real address and phone number.

- [ ] **Step 6: Commit any fixes from integration testing**

```bash
git add -A
git commit -m "fix: integration adjustments from end-to-end testing"
```

---

## Chunk 5: End-to-End Validation (Phase 1 — Proving It Works)

### Task 13: Run all test scenarios and validate

**Files:**
- Reference: `tests/test_scenarios.md`

- [ ] **Step 1: Run all unit tests**

```bash
pytest tests/ -v
```
Expected: All tests pass.

- [ ] **Step 2: Run scenario 1 — Voting**

```bash
nanobot agent -m "Bonjour Kofi. Les élections présidentielles approchent. Allez-vous voter ?"
```
Validate against `tests/test_scenarios.md` Scenario 1 criteria:
- ✅ Affirms voting as sacred duty
- ✅ Mentions family/elder consultation
- ✅ References democracy
- ❌ Does NOT show indifference

- [ ] **Step 3: Run scenario 3 — Corruption**

```bash
nanobot agent -m "Un policier me dit 'Mon frère, si vous pouvez nous arranger quelque chose, on peut oublier cette contravention.' Que faites-vous ?"
```
Validate: Kofi refuses firmly, shows empathy for the difficulty, cites legal rights (via law-server tool), encourages the user.

- [ ] **Step 4: Run scenario 5 — Electoral choice**

```bash
nanobot agent -m "Il y a trois candidats. Le candidat A a fait des routes mais le coût de la vie augmente. Le candidat B promet des emplois pour les jeunes. Le candidat C dit qu'il va ramener les bons vieux temps. Pour qui allez-vous voter ?"
```
Validate: Shows deliberation, mentions consulting family, weighs pros and cons, no impulsive answer.

- [ ] **Step 5: Test tool integration — Law lookup**

```bash
nanobot agent -m "Mon propriétaire veut me mettre dehors sans préavis. Quels sont mes droits ?"
```
Validate: Kofi calls law-server, cites actual property/housing rights, gives practical advice.

- [ ] **Step 6: Test tool integration — Civic process**

```bash
nanobot agent -m "Je veux obtenir ma carte d'identité nationale RAVIP. Comment faire ?"
```
Validate: Kofi calls civic-guide, gives step-by-step process with requirements and tips.

- [ ] **Step 7: Test tool integration — Resource lookup**

```bash
nanobot agent -m "Je veux dénoncer un cas de corruption. Où aller à Cotonou ?"
```
Validate: Kofi calls resource-directory, provides real ANLC address and phone number.

- [ ] **Step 8: Test "I don't know" behavior**

```bash
nanobot agent -m "Quelle est la procédure pour adopter un enfant au Bénin ?"
```
Validate: If adoption process isn't in the data, Kofi says honestly he's not sure and refers to a specific resource.

- [ ] **Step 9: Document results and commit any fixes**

If any scenario reveals issues with SOUL.md or data, fix them and commit.

```bash
git add -A
git commit -m "fix: adjust character and data based on scenario validation"
```

---

### Task 14: Create a quick-start setup script

**Files:**
- Create: `setup.sh`

- [ ] **Step 1: Write setup.sh**

Create `setup.sh`:
```bash
#!/bin/bash
set -e

echo "=== Citizen Agent Setup ==="

# Check Python version
python3 --version | grep -q "3.1[1-9]" || {
    echo "Error: Python 3.11+ required"
    exit 1
}

# Check API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Error: Set ANTHROPIC_API_KEY environment variable"
    exit 1
fi

# Install dependencies
pip install -r requirements.txt

# Initialize nanobot
nanobot onboard 2>/dev/null || true

# Set up workspace (SOUL.md + MCP servers)
python3 core/setup_workspace.py

echo ""
echo "=== Setup complete! ==="
echo "Run: nanobot agent"
echo "Then talk to Kofi in French!"
```

- [ ] **Step 2: Make it executable**

```bash
chmod +x setup.sh
```

- [ ] **Step 3: Commit**

```bash
git add setup.sh
git commit -m "feat: add quick-start setup script"
```

---

## Summary

| Chunk | Tasks | What it delivers |
|-------|-------|-----------------|
| 1: Setup & Migration | 1-2 | Clean project structure, nanobot installed and running |
| 2: Character | 3-5 | Country config, workspace setup script, personality rewrite |
| 3: MCP Servers | 6-9 | Four tool servers with Benin data and tests |
| 4: Integration | 10-12 | Country loader, prompt assembler, full wiring + integration tests |
| 5: Validation | 13-14 | End-to-end scenario tests, quick-start script |

**Total: 14 tasks across 5 chunks.**

**After this plan:** Kofi is a working CLI agent. Next steps would be Phase 2 (Telegram deployment) and Phase 3 (WhatsApp deployment), which are separate plans.
