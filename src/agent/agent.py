"""Core conversational agent."""

from collections.abc import Sequence
from typing import Protocol

from src.agent.memory import ConversationMemory
from src.models.llm_client import ChatMessage, LLMClient
from src.prompts.system_prompts import SYSTEM_PROMPT


class CompletionClient(Protocol):
    def complete(self, messages: Sequence[ChatMessage]) -> str: ...


class Agent:
    """Run conversations using a configured language model."""

    def __init__(self, client: CompletionClient | None = None) -> None:
        self.client = client or LLMClient()
        self.memory = ConversationMemory(system_prompt=SYSTEM_PROMPT)

    def run(self, message: str) -> str:
        """Send a user message to the model and retain the conversation."""
        if not message.strip():
            raise ValueError("Message cannot be empty.")

        self.memory.add("user", message)
        try:
            response = self.client.complete(self.memory.messages)
        except Exception:
            self.memory.remove_last()
            raise
        self.memory.add("assistant", response)
        return response
