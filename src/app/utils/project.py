import tomllib
from typing import Any

def get_version_from_pyproject() -> str:
    """Extract the project version from pyproject.toml."""
    with open("pyproject.toml", "rb") as f:
        data: dict[str, Any] = tomllib.load(f)
    return data["tool"]["poetry"]["version"]
