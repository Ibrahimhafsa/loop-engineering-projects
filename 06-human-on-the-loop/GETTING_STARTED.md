# Getting Started: Human-on-the-Loop Approval Loop

## Quick Start (2 minutes)

```bash
# Navigate to project
cd 06-human-on-the-loop

# Run the test suite (automated demonstration)
python test_loop.py

# Run the interactive loop
python approval_loop.py
```

## What You'll See

### Running the Test Suite

The test suite automatically demonstrates the entire pattern:

```
HUMAN-ON-THE-LOOP APPROVAL LOOP - TEST SUITE
┌─────────────────────────────────────────────┐
│ TEST 1: APPROVAL                            │
├─────────────────────────────────────────────┤
│ Task: send email                            │
│ Proposal: Send email with subject...        │
│ Decision: APPROVED                          │
│ Execution: ✓ Email sent successfully        │
│ Result: PASSED ✓                            │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ TEST 2: REJECTION                           │
├─────────────────────────────────────────────┤
│ Task: process payment                       │
│ Proposal: Process payment of $100...        │
│ Decision: REJECTED                          │
│ Execution: Skipped (not executed)           │
│ Result: PASSED ✓                            │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ TEST 3: MEMORY PERSISTENCE                  │
├─────────────────────────────────────────────┤
│ Loaded 2 previous beats from progress.md    │
│ Loop remembers: approval + rejection        │
│ Result: PASSED ✓                            │
└─────────────────────────────────────────────┘
```

### Running Interactive Mode

```
HUMAN-ON-THE-LOOP APPROVAL LOOP
────────────────────────────────────────
Loaded 0 previous beats from memory

Options:
  [1] Run a new beat
  [2] Show beat history
  [3] Exit

Choice: 1

What task should the loop process?
Your task: send email

[LOOP] Analyzing task...
[LOOP] Proposing action:

Proposal: Send an email with subject 'Task Completed'

Do you approve this action? (yes/no): yes

✓ APPROVED by human
[LOOP] Executing action...
✓ Email sent successfully to recipient@example.com
```

## Understanding the Flow

### The Beat Cycle

```
┌──────────────────────────────────────────────┐
│ BEAT: One Complete Loop Iteration            │
└──────────────────────────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │ INPUT: User provides    │
        │ task description        │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │ PROPOSE: Loop analyzes  │
        │ task and generates      │
        │ proposed action         │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │ SHOW: Display proposal  │
        │ to human for review     │
        └────────────┬────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼────┐            ┌────▼────┐
    │ APPROVE │            │ REJECT  │
    │   YES   │            │   NO    │
    └────┬────┘            └────┬────┘
         │                      │
    ┌────▼──────┐          ┌────▼──────┐
    │ EXECUTE   │          │ SKIP      │
    │ Action    │          │ Execution │
    └────┬──────┘          └────┬──────┘
         │                      │
         └──────────┬───────────┘
                    │
         ┌──────────▼──────────┐
         │ RECORD: Save beat   │
         │ to progress.md      │
         │ (the spine)         │
         └─────────────────────┘
```

### The Memory (Spine)

After running beats, `progress.md` contains:

```markdown
# Progress: Human-on-the-Loop Approval Loop

## Overview
- Total beats: N
- Approved: X
- Rejected: Y

## Beat History
### Beat 1: [timestamp]
- **Task**: your task description
- **Decision**: APPROVED or REJECTED
- **Result**: what happened

### Beat 2: [timestamp]
...
```

**Key insight**: `progress.md` is the "spine" - it carries state between runs.

## Example Workflow

### Run 1: Test Approval

```
$ python approval_loop.py
Loaded 0 previous beats from memory

[1] Run a new beat
Choice: 1

Your task: send email
Proposal: Send an email with subject...
Approve? (yes/no): yes

✓ APPROVED
✓ Email sent successfully
```

**Result**: progress.md now contains 1 approved beat

### Run 2: Test Rejection

```
$ python approval_loop.py
Loaded 1 previous beats from memory  ← Loop remembers from progress.md

[1] Run a new beat
Choice: 1

Your task: process payment
Proposal: Process payment of $100...
Approve? (yes/no): no

✗ REJECTED
[LOOP] Action not executed (as requested)
```

**Result**: progress.md now contains 2 beats (1 approved, 1 rejected)

### Run 3: See Full History

```
$ python approval_loop.py
Loaded 2 previous beats from memory  ← All previous beats remembered

[2] Show beat history

Beat 1 (2026-08-15T23:45:49.126665)
  Task: send email
  Decision: APPROVED
  Result: ✓ Email sent successfully...

Beat 2 (2026-08-15T23:45:49.140763)
  Task: process payment
  Decision: REJECTED
  Result: Not executed (rejected)

Total Beats: 2
Approved: 1
Rejected: 1
```

## Key Files

| File | Purpose |
|------|---------|
| `approval_loop.py` | Main ApprovalLoop class and CLI interface |
| `test_loop.py` | Automated test suite demonstrating all features |
| `progress.md` | Persistent memory (spine) - created automatically |
| `README.md` | Complete documentation and concepts |
| `PROJECT_SUMMARY.md` | Project completion summary |
| `GETTING_STARTED.md` | This file |

## What This Demonstrates

✓ **Human-on-the-Loop Pattern**
- System proposes, human decides, system executes (or not)
- Differs from human-in-the-loop where human guides each step

✓ **Persistent Memory (Spine)**
- progress.md carries state between program runs
- Loop learns from previous decisions
- Provides audit trail

✓ **Beat Concept**
- Each task processing cycle = one beat
- Beats accumulate and build history
- Each beat is recorded with timestamp

✓ **Approval/Rejection**
- Both paths are equally important
- Rejections show human veto power
- No results are fabricated

## For Interviews

**Short answer**: "The loop proposes actions and humans approve/reject before execution. All decisions save to progress.md, so the loop learns from history."

**Longer answer**: "This demonstrates human-on-the-loop. The system analyzes tasks and generates proposals, but humans maintain veto power. When a human approves, the action executes; when they reject, it's logged but not executed. All decisions—timestamps, tasks, proposals—save to progress.md, which acts as persistent memory. On the next run, progress.md loads first, allowing the loop to remember previous decisions and build context over time."

## Learning Resources

- See `README.md` for detailed concept explanations
- Review `PROJECT_SUMMARY.md` for test results and requirements
- Read `approval_loop.py` to understand the implementation
- Run `test_loop.py` to see the pattern in action

---

**Ready to explore?** Start with `python test_loop.py` to see everything working automatically.
