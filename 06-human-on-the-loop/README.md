# Project 6: Human-on-the-Loop Approval Loop

A beginner-friendly implementation of the **human-on-the-loop** pattern from the Loop Engineering crash course. This project demonstrates how systems can propose actions while keeping humans in control of critical decisions.

## Table of Contents

1. [What is Human-on-the-Loop?](#what-is-human-on-the-loop)
2. [Human-in-the-Loop vs Human-on-the-Loop](#human-in-the-loop-vs-human-on-the-loop)
3. [Key Concepts](#key-concepts)
   - [Beat](#beat)
   - [Spine](#spine)
4. [How Progress.md Provides Memory](#how-progressmd-provides-memory)
5. [How Approval/Rejection Works](#how-approvalrejection-works)
6. [Project Structure](#project-structure)
7. [How to Run](#how-to-run)
8. [Example Walkthrough](#example-walkthrough)

## What is Human-on-the-Loop?

**Human-on-the-loop** is an AI/automation pattern where:

- **The system proposes actions autonomously**
- **Humans review proposals before execution**
- **Humans maintain veto power** - they can reject any proposal
- **Actions only execute if approved** by the human
- **System learns from feedback** through the spine (persistent memory)

This pattern is ideal for:
- High-stakes decisions (financial transactions, personnel actions)
- Compliance-heavy workflows (legal approvals, regulatory requirements)
- Building trust in automated systems (users see proposals before execution)
- Gradually automating processes (humans stay informed of changes)

### Real-World Examples

- **Email automation**: Loop drafts replies, human approves before sending
- **Financial systems**: Loop proposes transactions, manager approves before posting
- **Content moderation**: Loop flags potentially harmful content, human makes final decision
- **Scheduling**: Loop proposes meeting times, human confirms
- **Data processing**: Loop identifies records for deletion, admin approves

## Human-in-the-Loop vs Human-on-the-Loop

| Aspect | Human-in-the-Loop | Human-on-the-Loop |
|--------|-------------------|-------------------|
| **Timing** | Human involved DURING process | Human reviews AFTER proposal |
| **Automation** | Limited; humans drive execution | High; system drives execution |
| **Decision Point** | Human makes the decision | System proposes, human approves/rejects |
| **Workflow** | Slower, requires constant input | Faster, human only intervenes on proposals |
| **Latency** | Higher (waiting for human input) | Lower (system acts independently) |
| **Trust** | Human directly controls outcome | Human controls through approval gates |
| **Example** | Human fills form → system validates → human submits | System generates form → human reviews → human approves submission |

**Summary**: 
- **Human-in-the-loop** = Human actively guiding each step
- **Human-on-the-loop** = Human monitoring and approving proposed steps

## Key Concepts

### Beat

A **beat** is a single cycle or iteration of the loop. Each beat represents one complete workflow:

1. **Input**: Receive a task
2. **Proposal**: Generate a proposed action
3. **Review**: Show proposal to human
4. **Decision**: Human approves or rejects
5. **Execution**: Execute if approved, skip if rejected
6. **Memory**: Save everything to the spine

In this project, one beat = one task processing cycle with human approval.

### Spine

The **spine** is persistent memory that carries state between beats. It's the project's source of truth.

In this project, the spine is `progress.md` - a markdown file that:
- Records all beats sequentially
- Saves task details, proposals, and decisions
- Tracks timestamps for each action
- Allows the loop to remember previous decisions
- Serves as an audit trail

**Why is it called "spine"?** Because it's the backbone that holds the loop's continuity - without it, each beat would be isolated and the loop would have no memory.

## How Progress.md Provides Memory

The `progress.md` file works as follows:

```
# Progress: Human-on-the-Loop Approval Loop

## Overview
- Total beats: 2
- Approved: 1
- Rejected: 1

## Beat History
### Beat 1: 2026-08-15T10:30:45.123456
- **Task**: send email
- **Decision**: APPROVED
- **Result**: ✓ Email sent successfully

### Beat 2: 2026-08-15T10:35:20.654321
- **Task**: process payment
- **Decision**: REJECTED
- **Result**: Not executed (rejected)

## Raw Data
```json
{
  "timestamp": "2026-08-15T10:30:45.123456",
  "task": "send email",
  "proposal": "Proposal: Send an email with subject...",
  "decision": "APPROVED",
  "result": "✓ Email sent successfully",
  "beat_number": 1
}
```
```

**Memory capabilities**:
1. Loop reads progress.md at startup
2. Extracts all JSON blocks to reconstruct beat history
3. Displays previous decisions to remind human
4. Allows system to make context-aware proposals
5. Creates an audit trail for compliance/review

## How Approval/Rejection Works

The approval flow in this project:

```
┌─────────────────────┐
│   Input: Task       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────┐
│  Proposal: Generate Action      │
│  (System-driven)                │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  Show Proposal to Human         │
│  Ask: "Do you approve? (Y/N)"   │
└──────────┬──────────────────────┘
           │
      ┌────┴────┐
      │          │
   YES│          │NO
      │          │
      ▼          ▼
   APPROVED    REJECTED
      │          │
      ▼          ▼
  EXECUTE    DO NOT EXECUTE
  RECORD     RECORD
```

**Key Points**:
- Proposal is shown BEFORE execution
- Human has veto power
- Decision is recorded regardless of approval/rejection
- Only APPROVED actions execute
- REJECTED actions are logged but not executed

## Project Structure

```
06-human-on-the-loop/
├── approval_loop.py       # Main loop implementation
├── progress.md            # Spine: persistent memory (created on first run)
├── README.md              # This file - documentation
└── .gitignore            # Git ignore file
```

**Files explained**:

- **approval_loop.py**: The main script containing the ApprovalLoop class
  - `load_history()`: Read previous beats from progress.md
  - `propose_action()`: Generate action based on task
  - `get_approval()`: Ask human for approval
  - `execute_action()`: Execute the approved action
  - `save_beat()`: Record beat to progress.md
  - `run_beat()`: Run a single loop iteration

- **progress.md**: Created automatically on first run
  - Human-readable beat history
  - JSON data blocks for parsing
  - Statistics (total beats, approved, rejected)

## How to Run

### Requirements
- Python 3.6+ (standard library only, no external dependencies)
- Terminal/command prompt

### Steps

1. **Navigate to project directory**:
   ```bash
   cd 06-human-on-the-loop
   ```

2. **Run the loop**:
   ```bash
   python approval_loop.py
   ```

3. **Choose option at menu**:
   ```
   Options:
     [1] Run a new beat
     [2] Show beat history
     [3] Exit
   ```

4. **For a new beat**:
   - Enter a task (e.g., "send email", "create file")
   - Review the proposed action
   - Type "yes" or "no" to approve/reject
   - Loop executes (if approved) and saves to progress.md

### Example Commands

```bash
# Run the loop
python approval_loop.py

# On first run, you'll see:
# ✓ Loaded 0 previous beats from memory

# Choose option 1 to run a new beat
# Enter task: send email
# Review proposal: Proposal: Send an email with subject 'Task Completed'...
# Approve? (yes/no): yes
# ✓ APPROVED by human
# ✓ Email sent successfully to recipient@example.com

# Choose option 2 to see history
# Shows all beats with timestamps and decisions

# On second run, you'll see:
# ✓ Loaded 1 previous beats from memory
# (Shows your previous beat)
```

## Example Walkthrough

### First Run - Approval

```
$ python approval_loop.py
============================================================
HUMAN-ON-THE-LOOP APPROVAL LOOP
============================================================

This loop demonstrates human-on-the-loop pattern:
1. Loop proposes an action
2. Human reviews and approves/rejects
3. Loop executes only if approved
4. Progress is saved in progress.md (the spine)

✓ Loaded 0 previous beats from memory

------------------------------------------------------------
Options:
  [1] Run a new beat
  [2] Show beat history
  [3] Exit
Choice: 1

============================================================
BEAT 1
============================================================

What task should the loop process?
Examples: 'send email', 'create file', 'update database'
Your task: send email

[LOOP] Analyzing task...
[LOOP] Proposing action:

Proposal: Send an email with subject 'Task Completed' to recipient@example.com

Do you approve this action? (yes/no): yes

✓ APPROVED by human
[LOOP] Executing action...
✓ Email sent successfully to recipient@example.com

Beat saved to progress.md
```

### First Run - Rejection

```
Options:
  [1] Run a new beat
  [2] Show beat history
  [3] Exit
Choice: 1

============================================================
BEAT 2
============================================================

What task should the loop process?
Your task: process payment

[LOOP] Analyzing task...
[LOOP] Proposing action:

Proposal: Process payment of $100 for 'process payment'

Do you approve this action? (yes/no): no

✗ REJECTED by human
[LOOP] Action not executed (as requested)

Beat saved to progress.md
```

### Second Run - Memory Demonstration

```
$ python approval_loop.py
============================================================
HUMAN-ON-THE-LOOP APPROVAL LOOP
============================================================

✓ Loaded 2 previous beats from memory

------------------------------------------------------------
Options:
  [1] Run a new beat
  [2] Show beat history
  [3] Exit
Choice: 2

============================================================
BEAT HISTORY
============================================================

Beat 1 (2026-08-15T10:30:45.123456)
  Task: send email
  Proposal: Proposal: Send an email with subject...
  Decision: APPROVED
  Result: ✓ Email sent successfully to recipient@example.com

Beat 2 (2026-08-15T10:35:20.654321)
  Task: process payment
  Proposal: Proposal: Process payment of $100...
  Decision: REJECTED
  Result: Not executed (rejected)

Total Beats: 2
Approved: 1
Rejected: 1
```

## Key Takeaways

1. **Human-on-the-loop keeps humans in control** while allowing automation
2. **The spine (progress.md) is essential** for memory and audit trails
3. **Each beat follows a pattern**: input → propose → review → execute/skip → record
4. **Rejection is just as important as approval** - it shows humans maintain veto power
5. **Loop learns from history** by reading progress.md on startup

## For Interview Explanation

**Short version** (30 seconds):
> "This is a human-on-the-loop pattern. The system analyzes tasks and proposes actions, but humans must approve them before execution. All decisions are saved in progress.md, which acts as persistent memory. On the next run, the loop loads previous decisions and can learn from them."

**Longer version** (2 minutes):
> "The project demonstrates human-on-the-loop, which balances automation with human control. Here's how it works: First, the user provides a task. The loop analyzes it and generates a proposal. It shows the proposal to the human and asks for approval. If approved, the action executes and the result is recorded. If rejected, it's noted but not executed. All decisions get saved to progress.md with timestamps, creating a permanent record. On the next run, progress.md is loaded first, allowing the loop to remember previous decisions and build context. This pattern is useful in high-stakes situations—like financial transactions or compliance workflows—where you want automation but need human oversight."

## Next Steps

- Try different task types (email, file creation, database updates)
- Run multiple times to see how progress.md accumulates history
- Modify the `propose_action()` method to add more task types
- Add timestamps to understand beat sequencing
- Review progress.md to see the audit trail

---

**Created as part of Loop Engineering Crash Course - Project 6**
