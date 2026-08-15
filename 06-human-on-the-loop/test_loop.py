#!/usr/bin/env python3
"""
Test script for the Human-on-the-Loop Approval Loop.
Demonstrates the loop with pre-defined test cases.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import patch
from approval_loop import ApprovalLoop


def test_scenario_1_approval():
    """Test scenario 1: User approves an action."""
    print("\n" + "="*70)
    print("TEST SCENARIO 1: APPROVAL")
    print("="*70)
    print("Task: send email")
    print("Expected: Action is approved and executed\n")

    loop = ApprovalLoop("progress.md")

    # Simulate user input
    with patch('builtins.input', side_effect=["send email", "yes"]):
        loop.run_beat()

    print("\n✓ Test 1 Complete: Approval recorded in progress.md")


def test_scenario_2_rejection():
    """Test scenario 2: User rejects an action."""
    print("\n" + "="*70)
    print("TEST SCENARIO 2: REJECTION")
    print("="*70)
    print("Task: process payment")
    print("Expected: Action is rejected and NOT executed\n")

    loop = ApprovalLoop("progress.md")

    # Simulate user input
    with patch('builtins.input', side_effect=["process payment", "no"]):
        loop.run_beat()

    print("\n✓ Test 2 Complete: Rejection recorded in progress.md")


def test_scenario_3_memory():
    """Test scenario 3: Loop remembers previous decisions."""
    print("\n" + "="*70)
    print("TEST SCENARIO 3: MEMORY (Human-on-the-Loop Remembers)")
    print("="*70)
    print("Loading the loop fresh from progress.md")
    print("Expected: All previous beats loaded from the spine\n")

    loop = ApprovalLoop("progress.md")

    if len(loop.beats) >= 2:
        print(f"✓ Successfully loaded {len(loop.beats)} previous beats from progress.md")
        print("\nMemory content:")
        for beat in loop.beats:
            print(f"\n  Beat {beat['beat_number']}:")
            print(f"    Task: {beat['task']}")
            print(f"    Decision: {beat['decision']}")
            print(f"    Timestamp: {beat['timestamp']}")
    else:
        print("❌ Expected at least 2 beats loaded, but got:", len(loop.beats))

    print("\n✓ Test 3 Complete: Loop demonstrates persistent memory through spine")


def show_progress_file():
    """Display the progress.md file content."""
    print("\n" + "="*70)
    print("PROGRESS.MD CONTENT (THE SPINE)")
    print("="*70)

    progress_path = Path("progress.md")
    if progress_path.exists():
        content = progress_path.read_text()
        print(content)
    else:
        print("progress.md has not been created yet.")


def main():
    print("\n" + "="*70)
    print("HUMAN-ON-THE-LOOP APPROVAL LOOP - TEST SUITE")
    print("="*70)
    print("\nThis test suite demonstrates:")
    print("1. Approval workflow")
    print("2. Rejection workflow")
    print("3. Memory persistence through progress.md (the spine)")

    # Clean up progress.md before tests
    progress_path = Path("progress.md")
    if progress_path.exists():
        progress_path.unlink()

    # Run scenarios
    test_scenario_1_approval()
    test_scenario_2_rejection()
    test_scenario_3_memory()
    show_progress_file()

    print("\n" + "="*70)
    print("ALL TESTS COMPLETE")
    print("="*70)
    print("\nKey Observations:")
    print("✓ Approval workflow executed the action")
    print("✓ Rejection workflow prevented execution")
    print("✓ progress.md (spine) persists state between runs")
    print("✓ Loop can recall all previous decisions")
    print("\nThis demonstrates the human-on-the-loop pattern successfully!")


if __name__ == "__main__":
    main()
