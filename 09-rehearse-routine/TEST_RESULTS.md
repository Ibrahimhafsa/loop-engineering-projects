# Test Results: Project 9 - Rehearse a Routine for Free

## Overview
This document contains the actual observed results from running Project 9's routine both successfully and with intentional failure. These results demonstrate the critical lesson: **status indicators show infrastructure success, not task success**.

---

## Run 1: Successful Execution

**File:** `routine.py`  
**Date:** 2026-08-18  
**Time:** 01:54:02  
**Status:** SUCCESS (Exit Code: 0)

### Full Transcript

```
[ROUTINE] Starting commit summary generation...
[ROUTINE] Summary saved to: F:\agentic-ai-projects\loop-engineering-1\loop-engineering-projects\09-rehearse-routine\summary.md
[ROUTINE] Routine completed successfully

[SUCCESS] Routine execution completed successfully
```

### Output File Generated
**File:** `summary.md`

```markdown
# Commit Summary
Generated at: 2026-08-18T01:54:02.933280

## Recent Commits (Last 10)

```
e63f74a Add Project 8 daily health check loop
90fbe86 Add Project 7 safe loop with limits
3a81eb9 Add documentation: Getting Started guide and Completion Report
175fb54 Add Project 6: Human-on-the-Loop Approval Loop
dcf2c7f Add Project 5 loop engineering project
600951a Add Project 4 event-driven loop
50801cf Add Project 3 morning brief memory loop
ff6cda2 Add Loop Engineering projects 1 and 2
```

## Routine Status
[OK] Successfully generated commit summary
[OK] Total commits captured: 8
```

### What Happened
1. Routine started successfully
2. Git command executed and fetched recent commits
3. Summary file was created with commit data
4. Routine exited with code 0 (success)

### Verification
- [x] summary.md file created
- [x] Contains recent git commits
- [x] Contains timestamp
- [x] Exit code: 0 (successful)

---

## Run 2: Intentional Failure

**File:** `routine_failing.py`  
**Date:** 2026-08-18  
**Time:** 01:55:30  
**Status:** FAILED (Exit Code: 1)

### Full Transcript

```
[ROUTINE] Starting commit summary generation...
[ROUTINE] Loading configuration...

[ERROR] Routine failed: [Errno 2] No such file or directory: 'F:\agentic-ai-projects\loop-engineering-1\loop-engineering-projects\09-rehearse-routine\config.json'
```

### What Happened
1. Routine started successfully (initial infrastructure worked)
2. Attempted to read `config.json` file
3. File does not exist - task failed at this point
4. Routine exited with code 1 (failure)

### Verification
- [x] config.json file does NOT exist (intentional)
- [x] Routine detected the missing file
- [x] Routine reported the error
- [x] Exit code: 1 (failed)

---

## The Critical Lesson

### Problem: Status Column Can Be Misleading

If you only look at the "status" of each run:

| Run | Status | Appears | Actually |
|-----|--------|---------|----------|
| Run 1 | SUCCESS (Green) | Task succeeded | Task succeeded ✓ |
| Run 2 | FAILED (Red) | Task failed | Task failed (as intended) ✓ |

**This example makes the status column look reliable.**

However, consider this alternative scenario:

| Run | Status | Appears | Actually |
|-----|--------|---------|----------|
| Run 1 | SUCCESS (Green) | Task succeeded | Task succeeded ✓ |
| Run 2 | SUCCESS (Green) | Task succeeded | Task FAILED silently (data corrupted, wrong output, etc.) ✗ |

### The Real Lesson

**"Green means the session ended without an infrastructure error; it does not necessarily mean the task itself succeeded."**

A routine can:
- Return exit code 0 (infrastructure success) but produce wrong output
- Return exit code 0 but skip critical steps silently
- Return exit code 0 but corrupt data
- Return exit code 0 but fail to meet actual requirements

### Why Full Transcripts Matter

The **full transcript** shows:
- Exactly what happened at each step
- What files were created or modified
- What data was processed
- Any warnings or anomalies
- The actual success of the business logic, not just the infrastructure

The **status column only shows**:
- Whether the session exited cleanly
- The exit code
- Nothing about what actually happened inside

---

## Conclusion

Before putting a routine on a repeating schedule, you must:

1. Run it once manually (one-off)
2. **Read the full transcript** from start to finish
3. **Verify the output files** were created correctly
4. **Check the data** that was generated or processed
5. Only then decide if the routine is ready for scheduling

This is why Project 9 teaches routine rehearsal: to catch problems that the status column alone cannot reveal.
