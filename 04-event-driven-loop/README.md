# Project 4: Event-Driven Loop

A beginner-friendly implementation of an event-driven loop architecture with persistent memory. This project demonstrates how loops can wait for user input (events) instead of running on fixed schedules.

## Project Structure

```
04-event-driven-loop/
├── event_loop.py      # Main event-driven loop implementation
├── progress.md        # Spine (persistent memory)
└── README.md          # This file
```

## Core Concepts

### What is an Event-Driven Loop?

An event-driven loop is a program that waits for events to trigger processing, rather than checking for work on a fixed schedule. Think of it like:
- **Doorbell approach** (event-driven): Wait for someone to ring the bell, then respond
- **Repeated knocking** (scheduled loop): Knock on the door every 5 seconds to check if anyone answered

Event-driven loops are more efficient because they don't waste resources checking constantly.

### Scheduled Loop vs. Event-Driven Loop

**Scheduled Loop (Fixed Interval):**
```
While True:
  Wait 5 seconds
  Do work (whether or not anything needs doing)
  Repeat
```
- Runs work on a timer
- Wastes resources checking for work that might not exist
- Example: Checking email every 30 seconds

**Event-Driven Loop (Reactive):**
```
While True:
  Wait for an event
  Do work (only when event arrives)
  Repeat
```
- Runs work only when something happens
- More efficient (no wasted cycles)
- Example: Processing a task when a user submits it

### What is a Beat?

A **beat** is one complete iteration of the loop triggered by a single event. In this project, one beat consists of:

1. **Read the spine** - Load state from progress.md
2. **Wait for event** - Get user input (the event)
3. **Process event** - Do work based on the input
4. **Update state** - Record what happened
5. **Save the spine** - Write back to progress.md

Each time you run the program and enter a task, that's one beat.

### What is the Spine?

The **spine** is the persistent memory of the loop - the file that keeps information alive between beats. In this project, it's `progress.md`.

Without a spine:
- Each beat would be isolated
- The loop would forget previous events
- No history would be preserved

With a spine:
- Each beat can remember what came before
- Events are accumulated in a history
- The loop has continuity and context

### How progress.md Provides Memory

The `progress.md` file stores:
- **Event count**: How many events have been processed
- **Event history**: Timestamp, input, and result of each event
- **Loop state**: Last event time and current status

When the loop starts (beats 1, 2, 3, ...), it reads progress.md first. This means:
1. It knows how many events have already been processed
2. It can show you previous events
3. It maintains a complete audit trail

Example flow:
```
Run 1: Enter "greet" → Saved to progress.md (1 event)
Run 2: Enter "time"  → progress.md remembers "greet" + adds "time" (2 events)
Run 3: Enter "help"  → progress.md remembers both + adds "help" (3 events)
```

## How to Run the Project

### First Run

```bash
python event_loop.py
```

When prompted, enter an event (task). Examples:
- `greet` - The loop will greet you
- `time` - Get the current time
- `count` - Count total events processed
- `echo hello` - Echo back what you said
- `help` - Show available commands

**What happens:**
1. The loop reads progress.md (finds no previous events)
2. Waits for your input
3. Processes your event
4. Saves result to progress.md

### Second Run

```bash
python event_loop.py
```

Enter a different event (e.g., `time`).

**What happens:**
1. The loop reads progress.md
2. Shows you the previous event from Run 1 ✓ (Proof of memory!)
3. Waits for your input
4. Processes your new event
5. Saves both events to progress.md

### Run Multiple Times

Run the program again with different events:
- `python event_loop.py` → Enter: `greet`
- `python event_loop.py` → Enter: `count`
- `python event_loop.py` → Enter: `echo Event-Driven Loop`

Each run adds another event to the history in progress.md.

## Key Differences from Project 3 (Scheduled Loop)

**Project 3 (Scheduled Loop):**
- Loop runs every N seconds automatically
- No waiting for user input
- Processes on a timer, whether or not there's work

**Project 4 (Event-Driven Loop):**
- Loop waits for user input (event)
- One beat = one user task
- Only processes when you enter something

## Technical Implementation

The event loop follows a simple pattern:

```python
1. Read progress.md (spine)           # Load previous state
2. Wait for user input (event)         # Block until user enters task
3. Process the event                   # Do work based on input
4. Update internal state               # Record what happened
5. Save to progress.md (spine)         # Persist memory
```

The implementation uses:
- **pathlib.Path** - File handling
- **json** - Storing structured state
- **datetime** - Timestamps
- **Python standard library only** - No external dependencies

## What You Learned

✅ Event-driven vs. scheduled loops
✅ How beats represent single iterations triggered by events
✅ Using progress.md as a spine for persistent memory
✅ How loops maintain state across multiple runs
✅ Reading and writing structured data to files
✅ Building beginner-friendly CLI applications

## Next Steps

Once you understand this project:
- Modify `process_event()` to handle different event types
- Add more commands (custom event handlers)
- Extend progress.md with additional metadata
- Combine with other Loop Engineering concepts
