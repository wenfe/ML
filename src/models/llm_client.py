"""OpenAI chat-completions client."""

from collections.abc import Sequence
from typing import TypedDict

from openai import OpenAI

from src.utils.config import get_openai_api_key, get_openai_model


class ChatMessage(TypedDict):
    role: str
    content: str


class LLMClient:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=get_openai_api_key())
        self.model = get_openai_model()

    def complete(self, messages: Sequence[ChatMessage]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=list(messages),  # type: ignore[arg-type]
        )
        content = response.choices[0].message.content
        if content is None:
            raise RuntimeError("The language model returned an empty response.")
        return content
