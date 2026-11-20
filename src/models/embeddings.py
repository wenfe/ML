"""OpenAI text-embedding helper."""

from openai import OpenAI

from src.utils.config import get_openai_api_key


def create_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """Create an embedding vector for the supplied text."""
    if not text.strip():
        raise ValueError("Text cannot be empty.")
    client = OpenAI(api_key=get_openai_api_key())
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
