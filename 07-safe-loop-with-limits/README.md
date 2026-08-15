# Project 7: Safe Loop with Limits

A beginner-friendly demonstration of **safe autonomous loops** - the foundation of loop engineering.

## What is a Loop?

A loop is a process that repeats a sequence of actions over and over until something tells it to stop.

**In everyday life**: A person trying to find their keys might:
1. Check the bedroom
2. Check the kitchen
3. Check the living room
4. (repeat until found)

**In this project**: A loop that keeps trying to reach a target value by incrementing a counter.

## What is a Beat?

A **beat** is one complete iteration of the loop - one cycle of the repeated action.

**Timeline:**
```
Beat 1: Increment counter from 0 to 1 → Check if success
Beat 2: Increment counter from 1 to 2 → Check if success
Beat 3: Increment counter from 2 to 3 → Check if success [SUCCESS!]
```

Each beat is a heartbeat of the system - one pulse of activity.

## What is a Success Condition?

A **success condition** is the goal that tells the loop when to stop working.

**In this project**: "Stop when value reaches the target"

**Examples in real life:**
- "Stop searching when you find your keys"
- "Stop cooking when the food is done"
- "Stop retrying when the service is online"

## Why Are Limits Necessary?

Without limits, a loop can run forever. This is dangerous.

**Problems without limits:**
- If the success condition can never be met, the loop runs infinitely
- The system wastes all resources
- The system becomes unresponsive
- It's a **doom loop** (infinite bad cycle)

**With limits:**
- Loop stops after a maximum number of attempts
- System remains responsive
- Resources are protected
- Graceful failure instead of crash

## What is a Doom Loop?

A **doom loop** is an infinite loop - a cycle that repeats forever because:
1. The success condition is never met
2. There are no limits to stop the loop
3. The system keeps trying forever with no progress

**Example:**
```
Try to connect to server
  → Server is offline
  → Try again immediately
  → Server is still offline
  → Try again immediately
  → (repeats forever...)
```

**Consequences:**
- 100% CPU usage
- System freeze
- Resource exhaustion
- Unable to recover

## How Limits Prevent Doom Loops

Limits are the safety mechanism.

**Limit**: "After 5 attempts, STOP. Even if not successful."

**What happens:**
```
Attempt 1: Failed (1/5 attempts used)
Attempt 2: Failed (2/5 attempts used)
Attempt 3: Failed (3/5 attempts used)
Attempt 4: Failed (4/5 attempts used)
Attempt 5: Failed (5/5 attempts used)
→ STOP. Loop terminates. System gracefully handles failure.
```

The loop **cannot** run forever - it's mechanically impossible.

## What is the Spine?

The **spine** is persistent memory - data that survives across runs.

**Without spine**: Each time you run the program, it starts from scratch
- Loses all history
- Can't learn from previous attempts
- Can't resume work

**With spine**: Each run remembers previous runs
- History is preserved
- Can resume where you left off
- System has continuous memory

**In this project**: The spine is `progress.md`
- Stores all previous attempts
- Records timestamps and results
- Persists between runs
- Acts as the "long-term memory" of the loop

## How progress.md Provides Memory

`progress.md` is a markdown file that contains:

1. **Current state**: What's the loop working on right now?
2. **All attempts**: What happened in every beat?
3. **Timestamps**: When did each attempt happen?
4. **Results**: Did each attempt succeed or fail?

**Timeline example:**
```
Run 1 (target=3):
  Beat 1: 0→1 (not success)
  Beat 2: 1→2 (not success)
  Beat 3: 2→3 (✓ success) → STOP

Run 2 (target=3, read progress.md):
  "Oh, we already reached the target in Run 1!"
  → Remember the history
  → Know we succeeded
```

## Difference: Normal Loop vs. Safe Autonomous Loop

### UNSAFE: Normal Loop
```python
while True:              # No limit - can run forever!
    try_something()
    if success:
        break
    # What if success never happens?
    # This is a doom loop!
```

**Problems:**
- No limit → infinite loop possible
- No memory → can't learn from past
- Not autonomous → needs constant watching
- Not safe → can crash the system

### SAFE: Safe Autonomous Loop (This Project)
```python
while attempt_count < MAX_ATTEMPTS:  # ✓ Has a limit
    read_spine()                      # ✓ Remembers the past
    try_something()
    write_spine()                     # ✓ Records progress
    if success:                       # ✓ Clear success condition
        break
```

**Features:**
- [OK] Limit prevents doom loops
- [OK] Spine provides memory
- [OK] Success condition is explicit
- [OK] Can run autonomously without supervision
- [OK] Safe - cannot run infinitely

## Project Structure

```
07-safe-loop-with-limits/
├── safe_loop.py          # Main loop implementation
├── progress.md           # Spine (persistent memory)
├── README.md             # This file
└── test_results/         # Example runs (created during testing)
    ├── run_1_success.md  # Example: Success before limit
    └── run_2_limit.md    # Example: Limit reached
```

## Running the Project

### Run 1: Success Before Limit (target = 3)
```bash
python safe_loop.py 3
```
Expected: Loop stops because success condition is met (value reaches 3)

### Run 2: Limit Reached (target = 10)
```bash
python safe_loop.py 10
```
Expected: Loop stops after 5 attempts because limit is reached (value never reaches 10)

### Run 3: Read Spine (target = 3 again)
```bash
python safe_loop.py 3
```
Expected: Reads progress.md, sees we already succeeded, and remembers previous attempts

## Key Takeaways

| Concept | Why It Matters | How It Works |
|---------|---|---|
| **Beat** | Breaks work into small steps | One cycle = one iteration |
| **Success Condition** | Defines the goal | Loop stops when condition is true |
| **Limit** | Prevents infinite loops | Loop stops after max attempts |
| **Spine** | Provides memory | progress.md survives between runs |
| **Safe Loop** | Autonomous yet safe | Can run without supervision |

## Loop Engineering Principles Demonstrated

[OK] **Success Condition**: Explicitly defined (reach target value)
[OK] **Limits**: Maximum 5 attempts prevent doom loops
[OK] **Safe Autonomous Loop**: Runs without intervention, with safeguards
[OK] **Doom Loop Prevention**: Limit mechanically prevents infinite loops
[OK] **Beat**: Clear iteration structure
[OK] **Spine/Persistent Memory**: progress.md remembers across runs
