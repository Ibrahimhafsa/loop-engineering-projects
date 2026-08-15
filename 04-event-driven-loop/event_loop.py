"""
Event-Driven Loop: A simple event-driven architecture with persistent memory.

This script demonstrates:
- An event-driven loop that waits for user input
- Reading from progress.md (the spine) before processing each event
- Recording events, results, and timestamps in persistent memory
- The concept of a "beat" - one iteration of the loop triggered by an event
"""

import json
from datetime import datetime
from pathlib import Path


def read_progress():
    """Read the spine (progress.md) to get current state."""
    progress_file = Path("progress.md")

    if not progress_file.exists():
        return {
            "event_count": 0,
            "events": [],
            "last_event_time": None
        }

    content = progress_file.read_text()
    # For simplicity, we'll parse the JSON data at the end of the file
    # or create a new state if it doesn't exist

    try:
        # Try to extract JSON from the file
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('```json'):
                json_start = i + 1
                for j in range(json_start, len(lines)):
                    if lines[j].strip() == '```':
                        json_content = '\n'.join(lines[json_start:j])
                        return json.loads(json_content)
    except (json.JSONDecodeError, IndexError):
        pass

    # If no JSON found, return default state
    return {
        "event_count": 0,
        "events": [],
        "last_event_time": None
    }


def process_event(event_text, state):
    """Process a single event (one beat of the loop)."""
    # Simple event processing: analyze the event
    event_lower = event_text.lower()

    # Determine result based on event
    if "greet" in event_lower or "hello" in event_lower:
        result = "Greeted the user with a warm welcome!"
    elif "count" in event_lower:
        result = f"Counted {len(state['events']) + 1} total events processed."
    elif "time" in event_lower:
        result = f"Current time is {datetime.now().strftime('%H:%M:%S')}."
    elif "help" in event_lower:
        result = "Available commands: 'greet', 'count', 'time', 'echo <text>', 'quit'"
    elif "echo" in event_lower:
        parts = event_text.split(maxsplit=1)
        if len(parts) > 1:
            result = f"Echo: {parts[1]}"
        else:
            result = "Echo: (no text provided)"
    else:
        result = f"Processed event: '{event_text}'"

    return result


def save_progress(state):
    """Save the spine (progress.md) with updated state."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create markdown content
    markdown = "# Event-Driven Loop Progress\n\n"
    markdown += "## Loop State\n"
    markdown += f"- Status: Ready\n"
    markdown += f"- Event Count: {state['event_count']}\n"
    markdown += f"- Last Event: {state['last_event_time'] if state['last_event_time'] else 'None'}\n\n"

    markdown += "## Events Processed\n\n"

    for i, event in enumerate(state['events'], 1):
        markdown += f"### Event {i}\n"
        markdown += f"- **Time**: {event['timestamp']}\n"
        markdown += f"- **Input**: {event['input']}\n"
        markdown += f"- **Result**: {event['result']}\n\n"

    markdown += "## Raw State (JSON)\n"
    markdown += "```json\n"
    markdown += json.dumps(state, indent=2)
    markdown += "\n```\n\n"
    markdown += "## Notes\n"
    markdown += "This file serves as the spine - the persistent memory of the event-driven loop.\n"
    markdown += "Each event and its result are recorded here.\n"

    Path("progress.md").write_text(markdown)


def run_event_loop():
    """Main event-driven loop."""
    print("\n" + "="*60)
    print("EVENT-DRIVEN LOOP")
    print("="*60)
    print("\nWelcome to the Event-Driven Loop!")
    print("Type 'help' for available commands, or 'quit' to exit.\n")

    # BEAT 0: Read the spine before processing
    state = read_progress()
    print(f"[READ] Spine loaded. Previous events: {state['event_count']}")

    if state['events']:
        print("\n[HISTORY] Previous events:")
        for event in state['events'][-3:]:  # Show last 3 events
            print(f"   - [{event['timestamp']}] {event['input']}")

    # Wait for user input (event)
    print("\n[WAIT] Waiting for event...\n")
    event_input = input("Enter an event (task): ").strip()

    if not event_input or event_input.lower() == 'quit':
        print("\nGoodbye!")
        return

    # BEAT 1: Process the event
    print("\n[PROCESS] Processing event...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = process_event(event_input, state)

    print(f"[OK] Result: {result}")

    # BEAT 2: Update state
    state['event_count'] += 1
    state['last_event_time'] = timestamp
    state['events'].append({
        "timestamp": timestamp,
        "input": event_input,
        "result": result
    })

    # BEAT 3: Save the spine (persistent memory)
    print("\n[SAVE] Saving to spine (progress.md)...")
    save_progress(state)
    print("[OK] Spine updated!\n")

    print("="*60)
    print(f"[DONE] Beat completed! Total events: {state['event_count']}")
    print("Run the loop again to see your event history.\n")


if __name__ == "__main__":
    run_event_loop()
