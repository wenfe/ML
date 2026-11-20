"""Prompt-building helpers for agent tasks."""


def task_prompt(task: str, context: str | None = None) -> str:
    """Format a task with optional supporting context."""
    if not task.strip():
        raise ValueError("Task cannot be empty.")
    if context:
        return f"Context:\n{context}\n\nTask:\n{task}"
    return task
