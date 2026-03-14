import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-servers" / "law-server"))
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-servers" / "civic-guide"))
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-servers" / "resource-directory"))
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-servers" / "news-events"))
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
