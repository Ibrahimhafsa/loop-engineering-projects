# Project 12: Building a Dreaming Loop

**The Final Capstone Project in Loop Engineering**

## What Is a Dreaming Loop?

A **dreaming loop** is a meta-loop that watches another loop and **dreams of improvements**.

Just like humans learn from past mistakes by reflecting on them, the dreaming loop:
1. Reads the history/logs of another loop
2. Looks for repeated problems
3. Proposes small, evidence-based fixes
4. Lets a human decide whether to apply the fix

**Key idea**: It doesn't fix things automatically. It *proposes* fixes and waits for human approval.

---

## Why Run It Weekly?

Most loops run on **their own schedule** (daily, hourly, per-request, etc.).

The dreaming loop runs on a **different schedule** — typically weekly — to:
- Let time pass so patterns emerge (you can't see a repeated problem after just one run)
- Batch multiple observations together
- Propose one thoughtful change per week instead of constant small tweaks

**For this learning project**: We'll run it manually whenever we want to test it, but the code is structured for weekly execution.

---

## The Source Loop

This dreaming loop watches **Project 8: Daily Health Check Loop**.

**Source log file**:
```
../08-daily-chore-loop/progress.md
```

This file contains a history of every time the health check ran, what it checked, whether it passed or failed, and what it learned.

---

## Understanding progress.md

The source loop's `progress.md` is its **spine** — its persistent memory.

Each entry in progress.md looks like:

```
### Check #3 (TEST DATA)
- **Date/Time**: 2026-08-17T09:30:15.123456
- **Health Status**: FAIL
- **Failure Type**: Missing validation check
- **Error Message**: Validation step skipped - checker_feedback field was empty
```

The dreaming loop reads entries like this, looking for patterns.

---

## Understanding dreaming-state.md

The dreaming loop also has its own **spine**: `dreaming-state.md`.

It remembers:
- When it last processed entries (so it doesn't re-analyze old data)
- How many entries it has processed overall
- What repeated issues it has found
- When the next review is scheduled

On the first run, it starts from an initial date and processes forward.

On subsequent runs, it only looks at entries that came after `last_processed_date`.

**This prevents duplicate work.**

---

## The Spine Concept

A **spine** is the loop's persistent memory file. It survives between runs.

In this crash course:
- **Project 1-8**: Each loop has a spine (progress.md, health-check state, etc.)
- **Project 12**: The dreaming loop has its own spine (dreaming-state.md)

The spine is how loops remember what happened and continue intelligently from where they left off.

---

## How the Loop Detects Repeated Failures

The dreaming loop looks at the source logs and counts:
- How many times did this specific problem occur?
- When did it happen?
- What was the error message?

If the **same problem appears more than once**, it's a repeated failure.

For example:
- **Test data in this project**: A validation step is skipped on 2026-08-17 and again on 2026-08-19.
- The dreaming loop detects both occurrences.
- It proposes: "Add a mandatory validation check to prevent this."

---

## Maker-Checker Pattern

The dreaming loop uses a **maker-checker** pattern (common in software and finance):

### Maker
The maker's job:
- Find repeated problems in the logs
- Draft a proposal to fix the problem
- Prepare the evidence

The maker is trying to **identify and propose**.

### Checker
The checker's job:
- Verify the problem actually appears in the logs
- Verify it appears more than once
- Verify the proposed fix is minimal and reasonable
- Verify the proposal is evidence-based (not speculative)
- Reject proposals without solid evidence

The checker is trying to **prevent bad proposals**.

**Example**:

**Maker proposes**: "Add extra logging everywhere"
**Checker rejects**: "This isn't minimal. Where's the evidence that extra logging would help?"

**Maker proposes**: "Add validation for checker_feedback (appears to cause failures on 2026-08-17 and 2026-08-19)"
**Checker accepts**: "Both failures are documented, validation would prevent both. This is minimal."

---

## Why Evidence Is Required

A proposal without evidence is just a guess.

The dreaming loop **only proposes changes that are backed by real log entries**.

Each proposal must include:
- **Issue**: What is the problem?
- **Frequency**: How many times did it occur?
- **Evidence**: Here are the exact log entries showing it happened
- **Proposed Change**: Here is the specific fix
- **Why Minimal**: This is the smallest change that would prevent the problem

If the dreaming loop can't point to real entries in the log, **it doesn't propose anything**.

---

## The Improvement Proposal

When the dreaming loop finds a repeated issue:
1. Maker drafts a proposal
2. Checker validates it
3. If valid, files are created:
   - `IMPROVEMENT_PROPOSAL.md`: Detailed proposal with evidence
   - `PR_DESCRIPTION.md`: Ready for human review

These files are **not** automatically applied to the rules. They sit on a git branch waiting for human approval.

---

## Why Use a claude/ Branch?

The proposal is created on a **separate git branch** with a name like:
```
claude/dreaming-loop-2026-08-22
```

This keeps the proposal **isolated** from main.

**Important**: The proposal branch is **never automatically merged**.

A human must:
1. Read the proposal
2. Review the evidence
3. Decide whether to merge it to main

This is the **human gate** — the dreaming loop proposes, but the human decides.

---

## Why Not Directly Modify main?

It's not safe for an automated loop to directly change rules.

What if the proposal is wrong?
What if the evidence is misinterpreted?
What if there's a better way to fix the problem?

By using a branch + human approval:
- The loop can propose
- The human can review
- The human can modify or reject
- The human remains in control

---

## The Human Gate

**The human gate** is the point where a human must decide to merge.

Before merging:
- Review the proposal
- Check the evidence
- Decide whether the change makes sense
- Merge manually if you approve

This is why the dreaming loop **never auto-merges**.

---

## Rule Deletion Proposals

The dreaming loop also looks for rules that **might no longer be needed**.

For example:
- If the last 20 checks all passed without triggering a validation rule
- Maybe that validation rule is overly strict?
- Maybe it should be removed?

The dreaming loop proposes: "Consider removing this rule."

**Important**: It doesn't actually delete the rule. It just proposes deletion.

The human reviews it and decides.

---

## How to Run the Project

### First Run

```bash
cd 12-dreaming-loop
python dreaming_loop.py
```

This will:
1. Read the source logs (Project 8)
2. Detect the planted repeated failures
3. Create a proposal
4. Create a git branch
5. Update dreaming-state.md

### Check the Results

After running:
- Look at `IMPROVEMENT_PROPOSAL.md` (the detailed evidence)
- Look at `PR_DESCRIPTION.md` (ready for GitHub PR)
- Look at `dreaming-state.md` (updated processing history)
- Check the new branch:
  ```bash
  git branch
  ```

### How to Test It

Because we can't wait a real week:
- Add test data to the source log (already done)
- Run the loop manually
- Verify it detects the test failures
- Review the proposal
- Delete the branch if you want:
  ```bash
  git branch -D claude/dreaming-loop-2026-08-22
  ```

---

## Key Files

```
12-dreaming-loop/
├── dreaming_loop.py          Main loop implementation
├── README.md                 This file
├── dreaming-state.md         State persistence (updated after each run)
├── IMPROVEMENT_PROPOSAL.md   Generated proposal with evidence
├── PR_DESCRIPTION.md         Generated PR ready for review
├── A6_CHECKLIST.md          Safety checklist
├── COMPLETION_REPORT.md     Test results
└── .gitignore              Git ignore rules
```

---

## What Makes This Beginner-Friendly?

1. **No external dependencies**: Only Python standard library
2. **Clear structure**: Separate Maker and Checker classes
3. **Evidence-based**: Every proposal includes real log entries
4. **Safe**: Proposals sit on a branch, never auto-merge
5. **Documented**: Every file explains what it does and why
6. **Testable**: You can run it manually and see the results immediately

---

## The Complete Flow

```
HEARTBEAT / WEEKLY TRIGGER
          ↓
READ SOURCE LOGS (progress.md)
          ↓
READ dreaming-state.md (remember last processed date)
          ↓
FILTER NEW ENTRIES (only entries after last processed date)
          ↓
DETECT REPEATED FAILURES
          ↓
MAKER: DRAFT PROPOSAL
          ↓
CHECKER: VALIDATE EVIDENCE
          ↓
CREATE claude/ BRANCH
          ↓
CREATE PROPOSAL FILES
          ↓
UPDATE dreaming-state.md
          ↓
WAIT FOR HUMAN REVIEW (do not auto-merge)
```

---

## What the Dreaming Loop Learns

By running repeatedly:
- The loop learns which problems keep happening
- The loop learns which fixes work (if humans accept proposals)
- The loop learns which rules are important and which are noise
- Over time, the source loop gets better

This is **self-improvement through reflection**.

---

## Important Notes

1. **Do not fabricate evidence**: Every proposal must cite real log entries
2. **Do not auto-merge**: The human must review and decide
3. **Do not modify rules automatically**: Only propose, never apply
4. **Do track state**: dreaming-state.md lets the loop pick up where it left off
5. **Do create branches**: Always use `claude/` branches for proposals

---

## For the Interview

In a GIAIC interview, you might explain:

> "The dreaming loop is a meta-loop that watches another loop and proposes improvements. It reads logs, finds repeated problems, validates them with a maker-checker pattern, and creates a branch with evidence-based proposals. The human always stays in control — the loop never auto-merges. This teaches self-improvement through reflection while keeping safety and human oversight."

---

## Questions?

- What is a spine? → A file that remembers state between runs
- Why weekly? → Time for patterns to emerge
- Why maker-checker? → To validate proposals before creating them
- Why evidence? → To prevent guesses and speculation
- Why branches? → To keep proposals safe and reversible
- Why human approval? → To stay safe and in control

---

**This is the capstone project. Everything you learned in Projects 1-11 comes together here.**

Good luck! 🚀
