# Project 9: Rehearse a Routine for Free

## Project Goal

Create and test a small, checkable routine before putting it on any repeating schedule. This project teaches you how to safely validate that a routine works as intended through one-off runs and full transcript inspection.

**Key Learning:** Before automating something, test it manually to ensure both infrastructure and business logic succeed.

---

## What is Routine Rehearsal?

Routine rehearsal is the practice of:

1. **Creating** a small routine with one clear task
2. **Testing** it with one-off/manual runs (not on a schedule)
3. **Inspecting** the FULL transcript of each run
4. **Verifying** that the task succeeded (not just that the script ran)
5. **Only then** putting it on a repeating schedule

Think of it like a dress rehearsal for a play:
- Actors don't schedule performances until they've rehearsed
- Musicians don't tour until they've done dry runs
- Developers don't deploy to production without testing

Similarly, **routines shouldn't be scheduled until they've been rehearsed and verified**.

---

## Why Test Before Scheduling?

### Problem: Status Column is Misleading

When you schedule a routine, you often see a "status" column:

```
Routine      Status    Last Run
commit-sum   SUCCESS   2 hours ago
cleanup      SUCCESS   1 hour ago
backup       FAILED    30 mins ago
```

**Green/SUCCESS means:** "The process ended without an infrastructure error"  
**Red/FAILED means:** "The process crashed or exited with an error"

**Green does NOT mean:** "The task actually succeeded or produced the right result"

### Real Problems Green Status Misses

Your routine can be GREEN but:
- ❌ Produce wrong output
- ❌ Process corrupted data
- ❌ Skip critical steps silently
- ❌ Generate empty files
- ❌ Write to the wrong location
- ❌ Process only partial data
- ❌ Have permission issues on second run
- ❌ Depend on external state that's now changed

**Testing before scheduling catches these problems.**

---

## What is a One-Off Run?

A one-off run is:
- A single, manual execution of a routine
- Not on a repeating schedule
- Done specifically to test and validate
- The place where you inspect the FULL transcript

### One-Off vs. Scheduled

| Aspect | One-Off Run | Scheduled Run |
|--------|------------|---------------|
| **Trigger** | Manual ("run now") | Automatic (cron/timer) |
| **Frequency** | Once | Repeating |
| **Purpose** | Testing/validation | Production execution |
| **Inspection** | Full transcript review | Status column only |
| **When to use** | Before scheduling | After validation |

### How to Do a One-Off Run

In this project, one-off runs are done by:
```bash
python routine.py
```

In production with Claude Agents, you would use:
- Claude Code: "Run now" button
- CLI: `/schedule --run-now`
- API: One-time execution call

---

## Why the Full Transcript Matters

### Status Column Shows

```
Status: SUCCESS ✓
Exit Code: 0
Duration: 2.3 seconds
```

**This tells you:** The infrastructure worked.

### Full Transcript Shows

```
[ROUTINE] Starting commit summary generation...
[ROUTINE] Summary saved to: /path/to/summary.md
[ROUTINE] Routine completed successfully

[SUCCESS] Routine execution completed successfully
```

**This tells you:** Every step of the task.

### What to Check in Full Transcript

When you review a transcript, verify:

1. **Did it start?** Look for initialization messages
2. **Did it do the work?** Look for status messages from each step
3. **Did it finish?** Look for completion messages
4. **What did it produce?** Look for output file creation messages
5. **Are there warnings?** Look for `[WARN]` or `[ERROR]` prefixes
6. **What's the actual data?** When possible, check the files created

Example: If your routine says "saved to summary.md", the full transcript lets you:
- Verify the file was created
- Check the file path
- See any errors during creation
- Read what was actually written

---

## The Critical Lesson

### Green Status is Not Task Success

```
Run 1: Status = SUCCESS (Green)
       Transcript = Commits saved to summary.md
       Reality = Task succeeded ✓

Run 2: Status = SUCCESS (Green)  
       Transcript = "Skipped processing due to missing config"
       Reality = Task failed silently ✗
```

**Headline:** "Green means the session ended without an infrastructure error;  
it does not necessarily mean the task itself succeeded."

### Before You Schedule

Ask yourself:
- [ ] Did I run it manually at least once?
- [ ] Did I read the FULL transcript, not just check green/red?
- [ ] Did I verify the output files were created?
- [ ] Did I check that the output data is correct?
- [ ] Did I test edge cases or error conditions?
- [ ] Am I confident this won't silently fail in production?

If you answer "no" to any of these, **do not schedule it yet**. Run it one-off again and review the transcript.

---

## Understanding A1, A3, A5

In the Loop Engineering crash course:

### A1: Agent Level 1 (Basic Agentic Loops)
- **Projects:** 01, 02
- **Complexity:** Simple loops with basic control flow
- **Autonomy:** Low - you control most decisions
- **Example:** "Run this command when this happens"
- **Focus:** Understanding loop basics

### A3: Agent Level 3 (Intermediate Agentic Loops)
- **Projects:** 03, 04, 05, 06, 07
- **Complexity:** Loops with decision-making and feedback
- **Autonomy:** Medium - agent makes some decisions
- **Example:** "Ask for approval, then execute based on response"
- **Focus:** Adding intelligence and interaction

### A5: Agent Level 5 (Advanced Agentic Loops)
- **Projects:** 08, 09
- **Complexity:** Production-ready with safety and validation
- **Autonomy:** High - agent handles complex scenarios
- **Example:** "Run safely with limits, validate before scheduling"
- **Focus:** Safety, validation, and production readiness

**Project 9 (this project) teaches A5 concepts:** You learn that even advanced routines need validation before they're trusted on a schedule.

---

## Project Structure

```
09-rehearse-routine/
├── README.md                 # This file - project guide
├── TEST_RESULTS.md          # Actual test runs and transcripts
├── routine.py               # The working routine
├── routine_failing.py       # The intentionally failing routine (for learning)
└── summary.md              # Output from successful routine run
```

---

## This Project's Routines

### routine.py (Working Routine)
**Purpose:** Summarize recent git commits and save to a file

**What it does:**
1. Runs `git log` to get recent commits
2. Generates a summary with timestamp
3. Saves to `summary.md`
4. Reports success

**Run it:**
```bash
python routine.py
```

**What to check in transcript:**
- Does it say "Summary saved to:"?
- Is the file path correct?
- Does it say "Routine completed successfully"?

**What to check in output:**
```bash
cat summary.md
```
- Is there a timestamp?
- Are commits listed?
- Is the file readable?

### routine_failing.py (Intentionally Failing Routine)
**Purpose:** Demonstrate how routines can fail silently or report infrastructure success when the task actually fails

**What it does:**
1. Starts successfully (infrastructure works)
2. Tries to read `config.json` (which doesn't exist)
3. Fails with an error
4. Reports the error

**Run it:**
```bash
python routine_failing.py
```

**What to observe:**
- It starts normally
- But fails when it can't find the config file
- The transcript shows the actual error
- Exit code is 1 (failure)

**The lesson:** If this routine didn't have proper error handling, it could have returned exit code 0 while silently skipping the configuration step. Always ensure error handling is visible in transcripts.

---

## How to Use This Project

### For Learning

1. Read this README
2. Run `python routine.py` manually
3. Read the full output above
4. Check the `summary.md` file
5. Run `python routine_failing.py` and see the difference
6. Read `TEST_RESULTS.md` for analysis

### The Key Experiment

Compare two scenarios:

**Scenario A: Just check the status**
```
Run 1: GREEN ✓
Run 2: GREEN ✓
Conclusion: Both work!
```

**Scenario B: Read the transcripts**
```
Run 1 Transcript: "Commits saved to summary.md" → Works ✓
Run 2 Transcript: "Commits saved to summary.md" → Works ✓
Conclusion: Both work! (same as scenario A)
```

**But what if...**
```
Run 1: GREEN ✓
Run 2: GREEN ✓
Run 1 Transcript: "Commits saved to summary.md" → Works ✓
Run 2 Transcript: "Skipped due to network error" → FAILED silently! ✗
```

**Lesson:** Always read transcripts, never trust status alone.

---

## Key Takeaways

1. **Rehearse before scheduling** - One-off runs catch problems
2. **Read full transcripts** - Status column is incomplete
3. **Verify outputs** - Check files, data, and side effects
4. **Test edge cases** - What if resources are missing?
5. **Green status ≠ task success** - Green means process didn't crash
6. **Silent failures exist** - A routine can succeed in infrastructure but fail its task
7. **Production readiness requires validation** - Not just working code, but proven execution

---

## For Interviews (Beginner Explanation)

> "In this project, I learned that scheduling a routine is dangerous without testing it first. I created a simple routine that summarizes git commits, then tested it manually with a one-off run. I inspected the full transcript to verify not just that the script ran, but that it actually completed its task correctly. Then I created a failing version to show how a routine can have a green status but still fail its real task. This taught me that before automating anything, I need to rehearse it first and check the full transcript, not just the status column. This is called routine rehearsal, and it's a best practice for production automation."

---

## Next Steps

After this project:
- ✅ You understand routine rehearsal
- ✅ You know why transcripts matter
- ✅ You understand the status column limitation
- ✅ You know what A1, A3, A5 mean
- ✅ You're ready to build more complex routines with confidence

**Do not move directly from routine.py to scheduling.** Always rehearse first.
