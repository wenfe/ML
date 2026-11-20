"""Common small helpers."""


def require_non_empty(value: str, name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{name} cannot be empty.")
    return cleaned
