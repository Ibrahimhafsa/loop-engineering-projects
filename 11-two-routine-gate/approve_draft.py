#!/usr/bin/env python3
"""
Human Approval Gate
Allows human to review and approve/reject the draft from Routine A.
Only after approval can Routine B be triggered.
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


def show_draft():
    """Display the latest draft for review."""
    if not Path("draft_latest.md").exists():
        print("❌ No draft found. Please run Routine A first.")
        return False

    print("\n" + "="*60)
    print("DRAFT FOR REVIEW")
    print("="*60 + "\n")

    with open("draft_latest.md", "r") as f:
        content = f.read()
        print(content)

    return True


def get_approval_decision():
    """Get approval/rejection decision from human."""
    while True:
        print("\n" + "="*60)
        print("HUMAN APPROVAL GATE")
        print("="*60)
        print("\nDo you approve this draft?")
        print("1. Approve (will allow Routine B to run)")
        print("2. Reject (draft will be discarded)")
        print("3. Cancel (no change)")

        choice = input("\nEnter your choice (1/2/3): ").strip()

        if choice == "1":
            return "approved"
        elif choice == "2":
            return "rejected"
        elif choice == "3":
            return "cancelled"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def approve_draft():
    """Process the human approval."""
    print("\n" + "="*60)
    print("HUMAN APPROVAL GATE")
    print("="*60 + "\n")

    # Show draft
    if not show_draft():
        return

    # Get decision
    decision = get_approval_decision()

    if decision == "cancelled":
        print("\n✓ No changes made. Exiting.")
        return

    # Update state
    state = load_state()
    approval_record = {
        "timestamp": datetime.datetime.now().isoformat(),
        "decision": decision,
        "approved": (decision == "approved")
    }
    state["approvals"].append(approval_record)
    save_state(state)

    # Display result
    print("\n" + "="*60)
    if decision == "approved":
        print("✓ DRAFT APPROVED!")
        print("="*60)
        print("\nThe draft has been approved and Routine B can now be triggered.")
        print("\nTo trigger Routine B, follow these steps:")
        print("1. Start Routine B server: python routine_b.py")
        print("2. In another terminal, read the token from .routine_b_token")
        print("3. Trigger with: curl -X POST http://localhost:9999/trigger \\")
        print('     -H "Authorization: Bearer <YOUR_TOKEN>"')
        print("\nOr use: python trigger_routine_b.py")
    else:
        print("✗ DRAFT REJECTED")
        print("="*60)
        print("\nThe draft has been rejected.")
        print("Routine B will NOT run.")
        print("Please create a new draft with Routine A if you want to try again.")

    print("="*60 + "\n")


if __name__ == "__main__":
    approve_draft()
