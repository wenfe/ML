"""In-memory conversation history."""

from typing import TypedDict


class Message(TypedDict):
    role: str
    content: str


class ConversationMemory:
    def __init__(self, system_prompt: str) -> None:
        self.messages: list[Message] = [
            {"role": "system", "content": system_prompt}
        ]

    def add(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})

    def remove_last(self) -> None:
        if len(self.messages) > 1:
            self.messages.pop()

    def clear(self, system_prompt: str) -> None:
        self.messages = [{"role": "system", "content": system_prompt}]
