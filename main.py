"""Entry point for the HR Agent CLI."""

from hr_agent import HRAgent


def main() -> None:
    agent = HRAgent()
    print(agent.welcome())
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye! Have a great day. 👋")
            break

        if user_input.lower() in ("quit", "exit", "bye", "goodbye"):
            print("HR Agent: Goodbye! Have a great day. 👋")
            break

        if not user_input:
            continue

        response = agent.respond(user_input)
        print(f"\nHR Agent: {response}\n")


if __name__ == "__main__":
    main()
