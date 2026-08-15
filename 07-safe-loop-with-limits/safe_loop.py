#!/usr/bin/env python3
"""
Safe Loop with Limits - Loop Engineering Project 7

Demonstrates safe autonomous looping with:
- Success condition (target reached)
- Limits (max attempts)
- Spine (persistent memory in progress.md)
- Beats (iterations)
- Doom loop prevention
"""

import json
import time
from datetime import datetime
from pathlib import Path


def read_progress() -> dict:
    """Read the spine (persistent memory) from progress.md"""
    progress_file = Path("progress.md")

    if not progress_file.exists():
        # First time running - initialize progress
        return {
            "attempts": [],
            "current_value": 0,
            "target": None,
            "status": "not_started"
        }

    # Parse the markdown file to extract JSON
    content = progress_file.read_text()

    # Extract JSON from markdown code block
    if "```json" in content:
        start = content.find("```json") + len("```json")
        end = content.find("```", start)
        json_str = content[start:end].strip()
        return json.loads(json_str)

    return {
        "attempts": [],
        "current_value": 0,
        "target": None,
        "status": "not_started"
    }


def write_progress(progress: dict) -> None:
    """Write the spine (persistent memory) to progress.md"""
    progress_file = Path("progress.md")

    markdown = f"""# Safe Loop Progress - Spine (Persistent Memory)

This file is the **spine** - it persists across runs and remembers what happened.

## Current State
- **Status**: {progress['status']}
- **Current Value**: {progress['current_value']}
- **Target**: {progress['target']}
- **Total Attempts**: {len(progress['attempts'])}

## All Attempts (Memory of the Loop)

```json
{json.dumps(progress, indent=2)}
```

## Attempt Details

"""

    for i, attempt in enumerate(progress["attempts"], 1):
        markdown += f"\n### Attempt {i}\n"
        markdown += f"- **Timestamp**: {attempt['timestamp']}\n"
        markdown += f"- **Action**: {attempt['action']}\n"
        markdown += f"- **Value After Action**: {attempt['value_after']}\n"
        markdown += f"- **Success Condition Met**: {attempt['success_met']}\n"
        markdown += f"- **Result**: {attempt['result']}\n"

    progress_file.write_text(markdown)


def perform_beat(progress: dict) -> dict:
    """
    Perform one beat (iteration) of the loop.

    A beat is one unit of work in the loop.
    Returns updated progress dict.
    """
    attempt_num = len(progress["attempts"]) + 1
    timestamp = datetime.now().isoformat()

    # Action: increment the counter by 1
    progress["current_value"] += 1
    action = f"Incremented value by 1"

    # Check success condition: did we reach the target?
    success_met = progress["current_value"] >= progress["target"]

    if success_met:
        result = "[SUCCESS] CONDITION MET!"
        progress["status"] = "success"
    else:
        result = f"Not yet at target ({progress['current_value']}/{progress['target']})"
        progress["status"] = "running"

    # Record this attempt in the spine
    attempt_record = {
        "attempt_number": attempt_num,
        "timestamp": timestamp,
        "action": action,
        "value_after": progress["current_value"],
        "success_met": success_met,
        "result": result
    }

    progress["attempts"].append(attempt_record)

    return progress


def run_safe_loop(target: int, max_attempts: int = 5) -> None:
    """
    Run a safe autonomous loop that:
    1. Has a success condition (reach target)
    2. Has limits (max attempts)
    3. Uses spine for persistent memory
    4. Performs beats (iterations)
    5. Prevents doom loops
    """

    print("\n" + "="*70)
    print("SAFE LOOP WITH LIMITS - Loop Engineering Project 7")
    print("="*70)

    # Read the spine (persistent memory)
    progress = read_progress()

    # Check if this is a new run or continuing
    if progress["status"] != "not_started":
        print(f"\n[SPINE] Reading persistent memory...")
        print(f"   Previous attempts: {len(progress['attempts'])}")
        print(f"   Last known value: {progress['current_value']}")
        print()

    # Set target for this run
    progress["target"] = target

    print(f"[SUCCESS CONDITION] Reach value {target}")
    print(f"[LIMIT] Maximum {max_attempts} attempts (Doom Loop Prevention)")
    print(f"[SPINE] Persistent memory stored in progress.md")
    print(f"[BEAT] Each iteration of the loop\n")

    attempt_count = len(progress["attempts"])

    print(f"Starting from value: {progress['current_value']}")
    print(f"Previous attempts on record: {attempt_count}\n")

    # Check if success condition is already met (from previous runs)
    if progress["current_value"] >= progress["target"]:
        print(f"[SPINE] Success condition already met from previous run!")
        progress["status"] = "success"
    else:
        # The main loop - this is the safe autonomous loop
        while True:
            # Check if we've hit the limit (prevent doom loop)
            if len(progress["attempts"]) >= max_attempts:
                progress["status"] = "limit_reached"
                print(f"\n[LIMIT REACHED] {max_attempts} attempts completed")
                print(f"   Success condition was NOT met")
                print(f"   This prevents infinite loops (doom loop prevention)")
                break

            # Perform one beat (iteration)
            beat_num = len(progress["attempts"]) + 1
            print(f"[BEAT {beat_num}]")

            progress = perform_beat(progress)

            # Get the last attempt record
            last_attempt = progress["attempts"][-1]
            print(f"   Action: {last_attempt['action']}")
            print(f"   Value now: {last_attempt['value_after']}")
            print(f"   Result: {last_attempt['result']}")

            # Write spine after each beat
            write_progress(progress)
            print(f"   Spine updated (progress.md)")

            # Check success condition
            if last_attempt["success_met"]:
                print(f"\n[SUCCESS] Loop stops because success condition met")
                break

            # Brief pause to show iteration (not required, just for visibility)
            time.sleep(0.5)

    # Write spine after the loop completes
    write_progress(progress)

    # Final summary
    print("\n" + "="*70)
    print("LOOP COMPLETE")
    print("="*70)
    print(f"Status: {progress['status'].upper()}")
    print(f"Final Value: {progress['current_value']}")
    print(f"Target: {progress['target']}")
    print(f"Total Attempts: {len(progress['attempts'])}")
    print(f"Spine saved to: progress.md")
    print("="*70 + "\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        target = int(sys.argv[1])
    else:
        target = 3

    run_safe_loop(target=target, max_attempts=5)
