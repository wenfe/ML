"""FastAPI routes for the conversational agent."""

from functools import lru_cache

from fastapi import FastAPI, HTTPException

from src.agent.agent import Agent
from src.api.schemas import ChatRequest, ChatResponse

app = FastAPI(title="AI Agent API", version="0.1.0")


@lru_cache(maxsize=1)
def _get_agent() -> Agent:
    return Agent()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        response = _get_agent().run(request.message)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ChatResponse(response=response)
