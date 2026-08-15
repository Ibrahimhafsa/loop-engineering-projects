# Project 5: Maker-Checker Loop

A beginner-friendly learning project that demonstrates the **Maker-Checker pattern**, a simple agentic loop architecture.

## What is Maker-Checker?

The Maker-Checker pattern is a quality control loop with two distinct roles:

- **MAKER**: Creates a result based on a task or user request
- **CHECKER**: Reviews the result against predefined success conditions
  - Returns **PASS** if all conditions are met
  - Returns **FAIL** if any conditions are not met

If the Checker returns FAIL, the loop allows the Maker to try again with feedback, creating a continuous improvement cycle.

---

## Why Separate Maker and Checker?

Separating these roles creates **quality control through diversity**:

1. **Specialization**: Each component has a single, clear responsibility
   - Maker focuses on *creation*
   - Checker focuses on *validation*

2. **Auditability**: You can trace exactly what was created and why it passed/failed

3. **Iterability**: The loop can retry until conditions are met, improving the result

4. **Testing**: Each component can be tested independently

---

## Key Concepts

### PASS vs FAIL

- **PASS**: All success conditions are met. The result is acceptable.
- **FAIL**: One or more success conditions are not met. The Maker needs to improve.

### Success Conditions

Success conditions are **predefined rules** that the Checker uses to validate results. In this project:

1. **Min Length**: Summary must be at least 20 characters
2. **Word Count**: Summary must have at least 5 words
3. **Has Action Verb**: Summary must contain an action verb (performs, provides, creates, extracts, etc.)

Success conditions are customizable per use case.

### RECHECK

A **RECHECK** happens when:
1. Checker returns FAIL
2. Maker receives feedback
3. Maker creates an improved result
4. Checker reviews the new result

This cycle repeats until PASS or max attempts is reached.

### The Spine (progress.md)

The **spine** is persistent memory stored in `progress.md`. It tracks:

- The original user request
- Each attempt's Maker output
- Each attempt's Checker verdict
- Passed and failed conditions
- Feedback for improvement
- Timestamp of each step

The spine allows the system to "remember" what happened and why, creating an **auditable record** of the entire loop.

### Maximum Attempts

A **maximum attempts limit** (default: 3) prevents infinite loops:

- **Prevents wasted computation**: If the Maker can't meet conditions, we stop retrying
- **Clear failure states**: If max attempts is reached and still FAIL, we know to escalate or investigate
- **Bounds the system**: Gives clear guarantees about resource usage

---

## How the Loop Works

```
User Request
    ↓
[MAKER] Creates result
    ↓
[CHECKER] Validates against success conditions
    ↓
    ├─→ PASS? → Loop Complete
    │
    └─→ FAIL? → Still attempts left?
        ├─→ Yes → Provide feedback to Maker → Back to MAKER
        └─→ No → Loop Failed
```

---

## Project Structure

```
05-maker-checker-loop/
├── main.py                 # Entry point - runs demonstrations
├── loop.py                 # MakerCheckerLoop orchestrator
├── maker.py                # Maker: creates summaries
├── checker.py              # Checker: validates results
├── progress.md             # Spine: persistent memory of all attempts
├── README.md               # This file
└── COMPLETION_REPORT.md    # Test results and observations
```

---

## Running the Project

```bash
python main.py
```

This runs two scenarios:
1. **Scenario 1**: FAIL → FIX → PASS on first task
2. **Scenario 2**: FAIL → FIX → PASS on second task

Both demonstrate the core loop functionality.

---

## Code Overview

### Maker (maker.py)

The Maker creates a summary based on a user request. If it receives feedback from a previous failed attempt, it uses that feedback to create an improved version.

```python
maker = Maker()
result = maker.create_summary(
    user_request="Create a Python calculator",
    previous_feedback="Make it more detailed"
)
# Returns: { "summary": "...", "original_request": "...", ... }
```

### Checker (checker.py)

The Checker validates a result against success conditions. It returns a verdict (PASS or FAIL) and identifies which conditions failed.

```python
checker = Checker()
check_result = checker.check(maker_result)
# Returns: { "verdict": "PASS/FAIL", "passed_conditions": [...], "failed_conditions": [...] }
```

### Loop (loop.py)

The MakerCheckerLoop orchestrates the entire flow, handling retries and saving progress to the spine.

```python
loop = MakerCheckerLoop(progress_file="progress.md", max_attempts=3)
result = loop.run_task("Task 1", "User request here")
# Returns: final result with status, total attempts, and verdict
```

---

## Success Conditions in Detail

### Condition 1: Minimum Length
- **Description**: Summary must be at least 20 characters long
- **Why**: Ensures the summary has enough substance to be useful
- **Example**: "Python calculator tool" (21 chars) → PASS

### Condition 2: Word Count
- **Description**: Summary must have at least 5 words
- **Why**: Forces more complete descriptions than single words
- **Example**: "A Python tool that performs..." (5+ words) → PASS

### Condition 3: Action Verb
- **Description**: Summary must contain an action verb
- **Why**: Ensures the summary describes what the tool DOES, not just what it is
- **Valid verbs**: performs, provides, creates, extracts, includes, handles, etc.
- **Example**: "Tool that extracts data" (contains "extracts") → PASS

---

## Adding Custom Tasks

To add your own task:

1. Add a user request in `main.py`
2. The Maker will automatically generate a summary based on the keywords
3. Run the loop with `loop.run_task("Task Name", "Your request here")`

To customize success conditions, modify the `conditions` list in `checker.py`.

---

## Key Takeaways

1. **Separation of Concerns**: Maker and Checker are independent
2. **Iteration**: Failed attempts lead to improvement, not failure
3. **Memory**: The spine preserves the full history
4. **Validation**: Clear success conditions ensure quality
5. **Safety**: Maximum attempts prevent runaway loops
6. **Simplicity**: Python standard library only - no external dependencies

---

## Learning Objectives Demonstrated

✓ Maker-Checker pattern fundamentals
✓ PASS/FAIL verification workflows  
✓ Iterative improvement through feedback
✓ Persistent memory (the spine)
✓ Success condition validation
✓ Safe loop termination
✓ Beginner-friendly agentic loop design
