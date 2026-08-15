"""
Project 5: Maker-Checker Loop
Main entry point that demonstrates the Maker-Checker pattern.

This script runs two scenarios:
1. A PASS flow: Successful creation on first attempt
2. A FAIL → FIX → RECHECK flow: Failed on attempt 1, fixed on attempt 2
"""

from loop import MakerCheckerLoop


def main():
    """Main function to demonstrate Maker-Checker pattern."""

    print("\n")
    print("+" + "=" * 58 + "+")
    print("|" + " " * 58 + "|")
    print("|" + "  PROJECT 5: MAKER-CHECKER LOOP DEMONSTRATION".center(58) + "|")
    print("|" + "  Learning the Maker-Checker Pattern".center(58) + "|")
    print("|" + " " * 58 + "|")
    print("+" + "=" * 58 + "+")

    # Initialize the loop
    loop = MakerCheckerLoop(progress_file="progress.md", max_attempts=3)

    # Scenario 1: PASS flow (succeeds on first attempt)
    print("\n")
    print("#" * 60)
    print("#  SCENARIO 1: PASS FLOW (Succeeds Immediately)".ljust(59) + "#")
    print("#" * 60)
    print(
        "\nIn this scenario, the Maker creates a good summary that passes\n"
        "the Checker's validation on the first attempt."
    )

    task1_request = "Create a Python calculator that can add, subtract, multiply, and divide"
    result1 = loop.run_task("Task 1: Write Project Summary", task1_request)

    print("\n" + "-" * 60)
    print("SCENARIO 1 RESULT:")
    print(f"  Status: {result1['status']}")
    print(f"  Total Attempts: {result1['total_attempts']}")
    print(f"  Verdict: {result1['verdict']}")
    print("-" * 60)

    # Scenario 2: FAIL → FIX → RECHECK flow
    print("\n\n")
    print("#" * 60)
    print("#  SCENARIO 2: FAIL -> FIX -> RECHECK FLOW".ljust(59) + "#")
    print("#" * 60)
    print(
        "\nIn this scenario, the Maker creates a brief summary that fails\n"
        "the Checker's validation. The Maker then improves it (using feedback\n"
        "from the Checker) and it passes on the second attempt."
    )

    # This request is designed to fail initially but pass after improvement
    # The Maker will create "Web scraper for extracting data" initially (FAIL)
    # Then create improved version with feedback (PASS)
    task2_request = "List features for a web scraper tool"
    result2 = loop.run_task("Task 2: Write Feature List", task2_request)

    print("\n" + "-" * 60)
    print("SCENARIO 2 RESULT:")
    print(f"  Status: {result2['status']}")
    print(f"  Total Attempts: {result2['total_attempts']}")
    print(f"  Verdict: {result2['verdict']}")
    print("-" * 60)

    # Display summary
    loop.display_summary()

    # Print final summary
    print("\n" + "=" * 60)
    print("PROJECT EXECUTION COMPLETE")
    print("=" * 60)
    print(f"\nTask 1 (Calculator): {result1['status']} in {result1['total_attempts']} attempt(s)")
    print(f"Task 2 (Scraper): {result2['status']} in {result2['total_attempts']} attempt(s)")
    print(f"\nAll results saved to: progress.md")
    print("=" * 60)
    print("\nKey Observations:")
    print("  [OK] Maker creates summaries")
    print("  [OK] Checker validates against success conditions")
    print("  [OK] If FAIL, loop allows Maker to improve and retry")
    print("  [OK] Progress is saved to progress.md (the spine)")
    print("  [OK] Loop continues until PASS or max attempts reached")
    print("=" * 60)


if __name__ == "__main__":
    main()
