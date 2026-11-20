"""Dispatch requests to the agent's available local tools."""

from collections.abc import Callable
from typing import Any

from src.tools.calculator import calculate
from src.tools.search import search
from src.tools.weather import get_weather

Tool = Callable[..., Any]
TOOLS: dict[str, Tool] = {
    "calculator": calculate,
    "search": search,
    "weather": get_weather,
}


def execute_tool(name: str, arguments: dict[str, Any]) -> Any:
    """Execute a registered tool, rejecting unknown tool names."""
    try:
        tool = TOOLS[name]
    except KeyError as exc:
        raise ValueError(f"Unknown tool: {name}") from exc
    return tool(**arguments)
