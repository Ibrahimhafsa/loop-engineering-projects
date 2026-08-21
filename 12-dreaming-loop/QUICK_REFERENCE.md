# Quick Reference Card - Project 12 Dreaming Loop

**Print this or keep it open during your interview!**

---

## 60-Second Pitch (MEMORIZE THIS)

> "The dreaming loop is a self-improving meta-loop that watches another loop's logs and detects repeated failures. It uses a maker-checker pattern to validate improvement proposals and creates them on a safe git branch—never auto-merging. The human always stays in control. This demonstrates safe AI automation: proposing fixes based on evidence without automatic execution."

---

## The Flow (Draw this if asked)

```
Source Log (Project 8)
       ↓
   LogReader (reads progress.md)
       ↓
PatternDetector (finds 2+ occurrences)
       ↓
   Maker (drafts proposal)
       ↓
  Checker (validates evidence)
       ↓
DreamingLoop (orchestrates)
       ↓
Git Branch (claude/...) ← STOPS HERE
       ↓
Human Review (human decides)
```

---

## What It Detects

**Repeated Failure Example**:
- Check #3 (2026-08-17): "Missing validation check"
- Check #5 (2026-08-19): "Missing validation check" (SAME ERROR)
- **Action**: Propose adding validation

---

## Key Concepts (Know These)

| Term | Meaning |
|------|---------|
| **Spine** | State file (dreaming-state.md) that remembers what was processed |
| **Maker** | Role that identifies patterns and drafts proposals |
| **Checker** | Role that validates evidence before accepting proposals |
| **claude/ branch** | Safe branch where proposals sit (never auto-merged) |
| **Evidence** | Real log entries cited in every proposal |
| **Human Gate** | Point where human must decide to merge or reject |

---

## When Asked "Why Not Auto-Merge?"

**Answer**: "Because we can't trust that every fix is correct. The dreaming loop identifies patterns, but a human should verify the fix makes sense. This keeps humans in control—the loop proposes, but humans decide."

---

## When Asked "How Does It Prevent Bad Proposals?"

**Answer**: 
1. **Evidence requirement** - Problem must appear 2+ times in real logs
2. **Minimal approach** - Only proposes smallest necessary fix
3. **Maker-checker pattern** - Separate roles for proposing and validating
4. **Human gate** - Human reviews before any merge

---

## When Asked "How Is This Different From Auto-Fix Tools?"

**Answer**: "Auto-fix tools typically apply changes automatically and hope for the best. The dreaming loop identifies patterns, proposes fixes, and STOPS. Humans then review the evidence and decide whether to apply it. This is safer and more transparent."

---

## Test Results (You Tested This)

- ✅ Detects planted failures (2 occurrences found)
- ✅ Creates evidence-based proposals
- ✅ Validates with maker-checker
- ✅ Creates safe git branch
- ✅ Does NOT auto-merge
- ✅ All 15 tests pass

---

## File Purposes

| File | Purpose | Read If... |
|------|---------|-----------|
| `dreaming_loop.py` | Main code | You want to see implementation |
| `README.md` | Full explanation | You want detailed understanding |
| `INTERVIEW_SUMMARY.md` | Interview prep | You're preparing for interview |
| `A6_CHECKLIST.md` | Safety verification | Asked about safety measures |
| `COMPLETION_REPORT.md` | Test results | You want proof it works |
| `dreaming-state.md` | State persistence | Understand how it remembers |

---

## Common Questions

**Q: Why is it called a "dreaming loop"?**
A: Because a loop that runs and forgets is "asleep." A loop that runs, remembers, and reflects is "dreaming." A loop that improves is "learning."

**Q: Who decides whether to apply changes?**
A: Always the human. The loop only proposes.

**Q: Why separate maker and checker roles?**
A: To prevent bad ideas. The maker is creative, the checker is skeptical.

**Q: What happens if the checker rejects a proposal?**
A: The loop doesn't create it. No branch, no proposal—just moves to next analysis.

**Q: Can the loop modify the rules file automatically?**
A: No. It only creates .md proposal files on branches.

---

## Files to Review (In Order)

1. **First**: This file (QUICK_REFERENCE.md) ← You're here
2. **Second**: INTERVIEW_SUMMARY.md (60-sec pitch, 2-min explanation)
3. **Third**: dreaming_loop.py (understand the code)
4. **Fourth**: README.md (full beginner explanation)
5. **Fifth**: COMPLETION_REPORT.md (see proof of testing)

---

## The Evidence (Know This by Heart)

```
Issue: Missing validation check
Frequency: 2 occurrences

Occurrence #1:
  Check #3, 2026-08-17T09:30:15
  Error: "Validation step skipped - checker_feedback field was empty"

Occurrence #2:
  Check #5, 2026-08-19T08:20:30
  Error: "Validation step skipped - checker_feedback field was empty"

Proposed Fix:
  Add mandatory validation check for checker_feedback field
```

---

## Git Commands You Ran

```bash
# Run the loop
python dreaming_loop.py

# See the branch created
git branch

# Check proposal files
git checkout claude/dreaming-loop-2026-08-22
cat IMPROVEMENT_PROPOSAL.md

# Go back to main (don't merge)
git checkout main
```

---

## Why This Matters for Your Career

- Shows you understand **safe automation**
- Demonstrates **evidence-based thinking**
- Proves you can **keep humans in control**
- Exhibits **defensive design** (preventing bad proposals)
- Shows **transparency** and **audit trails**

Companies want engineers who can build intelligent systems that don't overreach. This project shows you can.

---

## One More Thing

The dreaming loop is the capstone of Loop Engineering because it synthesizes everything:
- **Projects 1-7**: Built different loop architectures
- **Project 8**: Loops that remember (spine)
- **Projects 9-11**: Added complexity and safety
- **Project 12**: Meta-loops that improve other loops

You went from "building loops" to "building systems of loops."

---

**Good luck! You've got this.** 🚀
