import argparse
import sys
from textwrap import fill


from .workflow import run_research


def print_item(text: str) -> None:
    print(fill(
        text,
        width=88,
        initial_indent="- ",
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    ))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Research a question and produce a sourced answer."
    )
    parser.add_argument("question", help="The question to research")
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Show planning, search, and page reads while research runs",
    )
    parser.add_argument(
        "--demo",
        choices=("first-timeout", "no-pages"),
        help="Simulate page-fetch timeouts",
    )
    args = parser.parse_args()

    question = args.question.strip()
    if not question:
        parser.error("question cannot be empty")

    def report(message: str) -> None:
        if args.trace:
            print(message, file=sys.stderr, flush=True)

    print("Researching...", file=sys.stderr, flush=True)
    if args.demo:
        print(f"Demo mode: {args.demo}", file=sys.stderr, flush=True)

    try:
        answer = run_research(question, report=report, demo=args.demo)
    except RuntimeError as error:
        parser.exit(1, f"Error: {error}\n")

    print(f"\nResearch report | Confidence: {answer.confidence}")
    print(fill(answer.question, width=88))

    print("\nShort answer")
    print(fill(answer.short_answer, width=88))

    if answer.key_findings:
        print("\nKey findings")
        for finding in answer.key_findings:
            citations = ", ".join(finding.source_ids)
            print_item(f"{finding.claim} [{citations}]")

    if answer.limitations:
        print("\nLimitations")
        for limitation in answer.limitations:
            print_item(limitation)

    if answer.suggested_next_steps:
        print("\nSuggested next steps")
        for step in answer.suggested_next_steps:
            print_item(step)

    print("\nSources")
    if not answer.sources:
        print("None cited.")
    for source in answer.sources:
        print(f"[{source.source_id}] {source.title}")
        print(f"     {source.url}")


if __name__ == "__main__":
    main()