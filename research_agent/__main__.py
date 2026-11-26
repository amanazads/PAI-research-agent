import argparse

from .workflow import run_research


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Research a question and produce a sourced answer."
    )
    parser.add_argument("question", help="The question to research")
    parser.add_argument(
        "--demo",
        choices=("first-timeout", "no-pages"),
        help="Simulate a timeout on the first page or on every selected page",
    )
    args = parser.parse_args()

    question = args.question.strip()
    if not question:
        parser.error("question cannot be empty")

    if args.demo:
        print(f"Demo mode: {args.demo}")

    try:
        answer = run_research(question, demo=args.demo)
    except RuntimeError as error:
        parser.exit(1, f"Error: {error}\n")

    print(f"\nQuestion: {answer.question}")
    print(f"\nShort answer: {answer.short_answer}")
    print(f"\nConfidence: {answer.confidence}")

    print("\nKey findings:")
    if not answer.key_findings:
        print("None verified.")
    for finding in answer.key_findings:
        print(f"- {finding.claim} [{', '.join(finding.source_ids)}]")

    print("\nSources:")
    if not answer.sources:
        print("None cited.")
    for source in answer.sources:
        print(f"- [{source.source_id}] {source.title}: {source.url}")

    print("\nLimitations:")
    for limitation in answer.limitations:
        print(f"- {limitation}")

    print("\nSuggested next steps:")
    for step in answer.suggested_next_steps:
        print(f"- {step}")


if __name__ == "__main__":
    main()