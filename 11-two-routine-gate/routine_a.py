#!/usr/bin/env python3
"""
Routine A: Draft Creator
Runs as a manual, one-off trigger.
Creates a draft for human review and saves it to a local file.
Does NOT automatically trigger Routine B.
"""
import json
import datetime
from pathlib import Path


def load_state():
    """Load the current state from state.json."""
    if Path("state.json").exists():
        with open("state.json", "r") as f:
            return json.load(f)
    return {"routine_a_runs": 0, "drafts": [], "approvals": [], "routine_b_results": []}


def save_state(state):
    """Save state to state.json."""
    with open("state.json", "w") as f:
        json.dump(state, f, indent=2)


def generate_draft():
    """Generate a sample draft for human review."""
    draft_content = """# Project Proposal Draft

**Project Name:** Quarterly Report Generation System
**Proposed By:** Routine A (Automated Draft Creator)
**Date:** {date}

## Summary
This proposal suggests implementing an automated quarterly report generation system
that will collect key metrics and generate a summary document.

## Proposed Changes
1. Add data collection module
2. Implement report formatting
3. Generate PDF output

## Implementation Plan
- Phase 1: Data collection (Week 1-2)
- Phase 2: Report formatting (Week 3)
- Phase 3: Testing and deployment (Week 4)

## Risk Assessment
- Low risk implementation
- Uses existing infrastructure
- Minimal external dependencies

## Next Steps
This draft requires human review and approval before proceeding.
Approval will trigger the final implementation in Routine B.

---
*Draft created by Routine A for human review*
*Do NOT proceed to Routine B without explicit approval*
""".format(date=datetime.datetime.now().isoformat())

    return draft_content


def run_routine_a():
    """Execute Routine A: create and save a draft."""
    print("\n" + "="*60)
    print("ROUTINE A: Draft Creator (Manual Trigger)")
    print("="*60 + "\n")
    # Set UTF-8 encoding for this script
    import sys
    if sys.stdout.encoding != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    state = load_state()

    # Generate draft
    draft = generate_draft()
    timestamp = datetime.datetime.now().isoformat()

    # Save draft to file with UTF-8 encoding
    draft_filename = "draft_latest.md"
    with open(draft_filename, "w", encoding="utf-8") as f:
        f.write(draft)

    print(f"[DONE] Draft created: {draft_filename}")
    print(f"[DONE] Timestamp: {timestamp}")
    print(f"\n--- DRAFT CONTENT ---\n{draft}\n--- END DRAFT ---\n")

    # Update state
    state["routine_a_runs"] += 1
    state["drafts"].append({
        "timestamp": timestamp,
        "filename": draft_filename,
        "status": "created",
        "approved": False
    })
    save_state(state)

    print("State updated in state.json")
    print("\n⚠️  IMPORTANT: HUMAN REVIEW REQUIRED")
    print("1. Read the draft above")
    print("2. Review the content in", draft_filename)
    print("3. Decide: approve or reject")
    print("4. Only after approval, trigger Routine B")
    print("\nRoutine B will NOT run without your explicit approval.")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_routine_a()
