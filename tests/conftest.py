import sys
import importlib.util
from pathlib import Path

# Add core/ to path for country_loader and citizen_agent imports
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

# MCP servers all have server.py — use importlib to load each by unique name
MCP_ROOT = Path(__file__).parent.parent / "mcp-servers"


def _load_server(name: str):
    """Load an MCP server module by its directory name, avoiding import collisions."""
    spec = importlib.util.spec_from_file_location(
        f"mcp_{name.replace('-', '_')}",
        MCP_ROOT / name / "server.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f"mcp_{name.replace('-', '_')}"] = mod
    spec.loader.exec_module(mod)
    return mod


def load_mcp_server(name: str):
    """Get or load an MCP server module."""
    key = f"mcp_{name.replace('-', '_')}"
    if key not in sys.modules:
        return _load_server(name)
    return sys.modules[key]
