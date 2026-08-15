#!/usr/bin/env python3
"""
Morning Brief Generator with Memory
A simple scheduled loop project that demonstrates persistent memory between runs.
"""

from datetime import datetime
import os
import json

PROGRESS_FILE = "progress.md"

def read_spine():
    """Read the spine (progress.md) to understand previous runs."""
    if not os.path.exists(PROGRESS_FILE):
        return {"runs": [], "last_brief": None}

    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            # Try to extract JSON from the file (between markers)
            if "<!-- SPINE_DATA:" in content and ":SPINE_DATA -->" in content:
                start = content.find("<!-- SPINE_DATA:") + len("<!-- SPINE_DATA:")
                end = content.find(":SPINE_DATA -->")
                json_str = content[start:end].strip()
                return json.loads(json_str)
    except Exception as e:
        print(f"Note: Could not read previous state: {e}")

    return {"runs": [], "last_brief": None}

def generate_brief(spine_data):
    """Generate today's morning brief."""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    date_str = now.strftime("%A, %B %d, %Y")

    brief = {
        "timestamp": timestamp,
        "date": date_str,
        "run_number": len(spine_data["runs"]) + 1,
        "status": "✓ Morning brief generated successfully",
        "message": f"Good morning! Today is {date_str}."
    }

    return brief

def save_spine(spine_data):
    """Save the spine (progress.md) with updated state."""
    spine_json = json.dumps(spine_data, indent=2)

    content = f"""# Morning Brief - Loop Memory

## What is this?
This file serves as the **spine** (persistent memory) for the Morning Brief project.
Each time the loop runs, it reads this file first, then updates it with the new brief.

## How does it work?
1. The loop reads this file to understand what happened in previous runs
2. It generates a new morning brief
3. It saves the brief and current state back to this file
4. On the next run, it reads all this information again

This demonstrates **memory** in a scheduled loop.

---

## Run History

"""

    # Add each previous run
    for i, brief in enumerate(spine_data["runs"], 1):
        content += f"### Run #{brief['run_number']} - {brief['timestamp']}\n"
        content += f"**Date:** {brief['date']}\n"
        content += f"**Status:** {brief['status']}\n"
        content += f"**Message:** {brief['message']}\n\n"

    # Add the metadata as a comment (so it's not visible but can be read by the script)
    content += f"""---

<!-- SPINE_DATA:{spine_json}:SPINE_DATA -->
"""

    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def display_brief(brief):
    """Display the morning brief nicely."""
    print("\n" + "="*60)
    print("✓ MORNING BRIEF GENERATED")
    print("="*60)
    print(f"📅 Date: {brief['date']}")
    print(f"🕐 Time: {brief['timestamp']}")
    print(f"🔢 Run #{brief['run_number']}")
    print(f"📊 Status: {brief['status']}")
    print(f"💬 Message: {brief['message']}")
    print("="*60 + "\n")

def main():
    """Main loop function."""
    print("\n[LOOP] Starting morning brief generation...")

    # SPINE: Read previous state
    print("[SPINE] Reading previous runs from progress.md...")
    spine_data = read_spine()
    previous_runs = len(spine_data["runs"])
    print(f"[SPINE] Found {previous_runs} previous run(s)")

    # BEAT: Generate new brief
    print("[BEAT] Generating new morning brief...")
    brief = generate_brief(spine_data)

    # BEAT: Update spine
    print("[BEAT] Saving state to progress.md...")
    spine_data["runs"].append(brief)
    spine_data["last_brief"] = brief
    save_spine(spine_data)

    # Display the brief
    display_brief(brief)

    # Show memory
    if previous_runs > 0:
        print(f"💾 MEMORY CHECK: This run knows about {previous_runs} previous brief(s)!")
        print(f"   Last brief was at: {spine_data['runs'][-2]['timestamp']}")
    else:
        print("💾 MEMORY CHECK: This is the first run - memory is empty")

    print("✓ Morning brief complete!\n")

if __name__ == "__main__":
    main()
