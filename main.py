"""Command-line entry point for the AI agent."""

from src.agent.agent import Agent


def main() -> None:
    agent = Agent()
    print("AI Agent ready. Type 'exit' to quit.")
    while True:
        message = input("You: ").strip()
        if message.casefold() in {"exit", "quit"}:
            break
        if not message:
            continue
        print(f"Agent: {agent.run(message)}")


if __name__ == "__main__":
    main()
