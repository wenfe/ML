"""Search JSON documents in the local knowledge base."""

import json
from pathlib import Path
from typing import Any

KNOWLEDGE_BASE = Path(__file__).resolve().parents[2] / "data" / "knowledge_base"


def search(query: str, directory: Path = KNOWLEDGE_BASE) -> list[dict[str, Any]]:
    """Return JSON documents whose serialized content contains every query term."""
    terms = query.casefold().split()
    if not terms:
        return []

    results: list[dict[str, Any]] = []
    if not directory.exists():
        return results

    for path in sorted(directory.glob("*.json")):
        with path.open(encoding="utf-8") as file:
            document = json.load(file)
        text = json.dumps(document, ensure_ascii=False).casefold()
        if all(term in text for term in terms):
            results.append({"file": path.name, "document": document})
    return results
