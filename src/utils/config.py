"""Environment-backed application configuration."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_openai_api_key() -> str:
    value = os.getenv("OPENAI_API_KEY", "").strip()
    if not value:
        raise RuntimeError("Set OPENAI_API_KEY in your .env file.")
    return value


def get_openai_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()


def get_openweather_api_key() -> str:
    value = os.getenv("OPENWEATHER_API_KEY", "").strip()
    if not value:
        raise RuntimeError("Set OPENWEATHER_API_KEY in your .env file.")
    return value
