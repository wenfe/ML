"""Tests for agent conversation handling."""

import unittest
from collections.abc import Sequence

from src.agent.agent import Agent
from src.models.llm_client import ChatMessage


class FakeClient:
    def complete(self, messages: Sequence[ChatMessage]) -> str:
        return "Test response"


class AgentTests(unittest.TestCase):
    def test_run_retains_user_and_assistant_messages(self) -> None:
        agent = Agent(client=FakeClient())

        self.assertEqual(agent.run("Hello"), "Test response")
        self.assertEqual(agent.memory.messages[-2]["content"], "Hello")
        self.assertEqual(agent.memory.messages[-1]["content"], "Test response")

    def test_run_rejects_blank_messages(self) -> None:
        agent = Agent(client=FakeClient())

        with self.assertRaises(ValueError):
            agent.run("   ")


if __name__ == "__main__":
    unittest.main()
