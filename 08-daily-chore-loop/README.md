# Project 8: Daily Project Health Check Loop (Capstone)

The **capstone project** that demonstrates all six components of Loop Engineering in one integrated system.

This is a beginner-friendly project that shows how a real daily task can use all six Loop Engineering principles working together.

---

## What Does This Loop Do?

Every day, this loop:
1. **Scans a project directory** to understand its current state
2. **Collects health metrics** (file count, code lines, documentation status)
3. **Creates a health report** with findings
4. **Validates the report** against quality standards
5. **Improves the report** if validation fails
6. **Saves the report** to a file for teams to see
7. **Records everything** so future runs remember the history

Think of it like a doctor's daily report on a patient's health - taking measurements, writing up findings, validating they're complete, and keeping records.

---

## The Six Loop Engineering Components

### 1. HEARTBEAT - Regular Interval-Based Execution

The **heartbeat** is the regular pulse of the loop. It runs on a schedule.

**In this project:**
- Each run is one "heartbeat"
- Heartbeats are numbered sequentially (Check #1, Check #2, etc.)
- Each heartbeat checks the project's health at a point in time

**Analogy:** Like a doctor checking a patient's vital signs every morning at 9 AM.

**In the code:**
```python
run_number = progress["total_checks"] + 1
print(f"[HEARTBEAT] Daily check cycle #{run_number}")
```

**Why it matters:** Regular intervals create predictable health data. You can track trends ("Is the project getting healthier or less healthy?").

---

### 2. WORKTREE/ISOLATION - Isolated Working Environment

**Worktree/Isolation** means each run gets its own isolated workspace and output files.

**In this project:**
- Each run creates a separate report file: `health_report_run1_TIMESTAMP.md`, `health_report_run2_TIMESTAMP.md`, etc.
- Each report is independent - changes in one run don't affect others
- Historical reports stay intact for comparison

**Analogy:** Like a doctor keeping separate patient charts for each visit - March checkup, April checkup, May checkup - instead of overwriting the same file.

**In the code:**
```python
timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
report_file = Path(f"health_report_run{run_number}_{timestamp_str}.md")
```

**Why it matters:** Isolation prevents runs from interfering with each other. You can compare reports over time and see exactly what changed between runs.

---

### 3. SKILL/PROJECT KNOWLEDGE - Using Domain Knowledge

**Skill** means the loop understands the domain it's operating in. It knows what makes a project "healthy."

**In this project:**
- The loop knows how to analyze Python projects
- It counts files, measures code lines, checks for documentation
- It understands that README.md and progress.md are important
- It collects metrics that matter for project health

**Analogy:** A good doctor has medical knowledge - they know which vital signs matter (pulse, blood pressure), how to interpret them, and what's normal.

**In the code:**
```python
def maker_collect_metrics(project_dir: str = ".") -> dict:
    """Collect health metrics from the project."""
    # Skill: Know how to count files, read Python, check documentation
    file_count = ...
    python_files = ...
    python_lines = ...
    has_readme = (project_path / "README.md").exists()
    # ... more project knowledge
```

**Why it matters:** A loop that understands its domain makes better decisions. Generic loops are weak; domain-aware loops are powerful.

---

### 4. MAKER-CHECKER - Dual-Step Validation

**Maker-Checker** is a two-role validation pattern:
- **MAKER**: Creates something (collects metrics, writes report)
- **CHECKER**: Validates it against success conditions

**In this project:**

**The Maker Step:**
1. Collects project metrics (how many files? how much code?)
2. Creates a health report based on those metrics
3. If previous attempts failed, improves the report based on feedback

**The Checker Step:**
1. Validates the report against 4 success conditions:
   - Condition 1: Project must have files
   - Condition 2: Summary must be descriptive (>15 chars)
   - Condition 3: Larger projects should document themselves
   - Condition 4: Projects should track progress
2. Returns PASS or FAIL
3. If FAIL, provides feedback

**The Loop:**
```
[MAKER] Collect metrics → Create report
    ↓
[CHECKER] Validate report
    ↓
    ├─→ PASS? → Done!
    │
    └─→ FAIL? → Retry with feedback (up to max_attempts)
```

**In the code:**
```python
# MAKER STEP
metrics = maker_collect_metrics()
report = maker_create_health_report(metrics, previous_feedback)

# CHECKER STEP
checker_result = checker_validate_report(report)

if checker_result["verdict"] == "FAIL":
    # Provide feedback and try again
    previous_feedback = checker_result["feedback"]
```

**Why it matters:** Separating creation from validation ensures quality. The Maker can focus on generation; the Checker can focus on standards. If validation fails, we improve instead of just failing.

---

### 5. CONNECTOR/ACTION - Taking Action in the External World

**Connector/Action** means the loop actually does something - it affects the outside world.

**In this project:**
- The loop writes health reports to actual files
- These files can be read by humans or systems
- The reports appear in the project directory
- They trigger awareness (team sees project is healthy or needs work)

**Analogy:** Like a doctor actually writing the report and sending it to the patient or their insurance company - not just thinking about it.

**In the code:**
```python
def connector_write_report(report: dict, checker_result: dict, run_number: int) -> str:
    """Write the health report to a file."""
    report_file = Path(f"health_report_run{run_number}_{timestamp_str}.md")
    report_file.write_text(content)  # ← ACTION: Actually wrote a file
    return str(report_file)
```

**Why it matters:** A loop that only thinks is useless. A loop that acts changes the world. The connector is how the loop affects reality.

---

### 6. SPINE/PERSISTENT MEMORY - Recording History

The **spine** is memory that survives between runs. It's not just RAM - it's permanent storage.

**In this project:**
- All health checks are recorded in `progress.md`
- Even after the program stops, the spine remembers what happened
- Next run reads the spine and remembers previous checks
- This creates a continuous memory across time

**In the code:**
```python
def read_progress() -> dict:
    """Read the spine from progress.md"""
    # Returns history of all previous checks

def write_progress(progress: dict) -> None:
    """Write the spine to progress.md"""
    # Records this run's check for future runs to remember
```

**Why it matters:** Without spine, each run starts from zero. With spine, the system has continuity. It learns. It remembers. It can track trends.

---

## How progress.md Provides Memory

The `progress.md` file is the **spine** - the system's persistent memory.

**What it stores:**
```
- Total checks completed (cumulative)
- Latest status (PASS or FAIL)
- Each run's:
  - Timestamp (when it ran)
  - Metrics (files, code lines, etc.)
  - Health score (0-100)
  - Checker verdict (PASS or FAIL)
  - Feedback provided
```

**Example memory growth:**
```
Run 1: Check #1 - Health Score: 75/100 - PASS
Run 2: Check #2 - Health Score: 80/100 - PASS
Run 3: Check #3 - Health Score: 82/100 - PASS
```

The spine shows **trends** - is the project getting healthier? Are issues being fixed?

---

## What is a Beat?

A **beat** is one complete cycle of the loop's work.

**Timeline:**
```
Beat 1: Collect metrics → Create report → Validate → Result: FAIL
Beat 2: (using feedback) → Create improved report → Validate → Result: PASS
```

Each beat is one pulse of activity. A single run might have multiple beats if validation fails and we retry.

**In the code:**
```python
while attempt <= max_attempts:
    print(f"[BEAT {attempt}] Starting health check cycle")
    # ... Maker step, Checker step ...
    attempt += 1
```

---

## What is the Safety Limit?

The **safety limit** is the maximum number of beats (retries) before giving up.

**In this project:**
- Default maximum: 2 attempts
- If Checker fails on attempt 1, Maker tries again with feedback
- If Checker fails on attempt 2, loop stops (graceful failure)

**Why it matters:** Prevents infinite loops. If something is broken, we don't retry forever - we give up gracefully.

**In the code:**
```python
def run_daily_health_check(project_dir: str = ".", max_attempts: int = 2):
    # Loop stops after max_attempts, even if not successful
    while attempt <= max_attempts:
        # ...
        attempt += 1
```

---

## The Stopping Condition

The loop stops when **ANY** of these is true:

1. **Success**: Checker returns PASS (success condition met)
2. **Limit Reached**: Attempts == max_attempts (safety limit)

**In the code:**
```python
if checker_result["verdict"] == "PASS":
    success = True
    print(f"[SUCCESS] Checker approved the health report!")
    break
else:
    attempt += 1
    if attempt > max_attempts:
        break  # ← Stopped by limit
```

---

## Project Structure

```
08-daily-chore-loop/
├── health_check_loop.py      # Main loop implementation
├── progress.md               # Spine (persistent memory)
├── README.md                 # This file
├── health_report_run1_*.md   # First check's report
├── health_report_run2_*.md   # Second check's report
└── COMPLETION_REPORT.md      # Test results
```

---

## How to Run the Project

### Run 1: First Daily Health Check
```bash
python health_check_loop.py
```

**What happens:**
1. Loop checks the project directory
2. Maker collects metrics
3. Checker validates the report
4. Creates `health_report_run1_TIMESTAMP.md`
5. Saves memory in `progress.md`

### Run 2: Second Daily Health Check
```bash
python health_check_loop.py
```

**What happens:**
1. Loop reads `progress.md` - remembers Run 1
2. Checks project again (same directory)
3. Creates `health_report_run2_TIMESTAMP.md`
4. Updates `progress.md` with new check
5. **Memory is preserved!** - Shows both Run 1 and Run 2

### Run 3+ (Optional)
```bash
python health_check_loop.py
```

**What happens:**
- Each new run adds to the spine
- `progress.md` grows with history
- Can analyze trends ("Is health improving?")

---

## Key Concepts Summary

| Concept | What It Is | Why It Matters | In This Project |
|---------|-----------|----------------|-----------------|
| **Heartbeat** | Regular pulse / iteration | Creates predictable timing | Check cycle #N |
| **Beat** | One cycle of the loop | Measures progress in small steps | Each attempt is one beat |
| **Worktree/Isolation** | Independent workspaces | Prevents interference between runs | Separate report files |
| **Skill/Knowledge** | Domain understanding | Makes better decisions | Knows how to analyze projects |
| **Maker-Checker** | Two-role validation | Quality control through separation | Collect→Validate→Improve |
| **Connector/Action** | External impact | Loop affects the world | Writes report files |
| **Spine/Memory** | Persistent storage | Enables learning | progress.md remembers |
| **Safety Limit** | Maximum attempts | Prevents infinite loops | max_attempts = 2 |
| **Success Condition** | Goal definition | Defines when to stop | Checker returns PASS |

---

## Understanding the Full System

**A complete heartbeat cycle:**

```
Start: progress.md exists (spine has memory)
   ↓
Read progress.md (remember previous checks)
   ↓
Loop starts (Beat 1)
   ├─ [SKILL] Analyze project files
   ├─ [MAKER] Create health report
   ├─ [CHECKER] Validate report
   └─ [VERDICT] PASS or FAIL?
        ├─ PASS → write report file [CONNECTOR]
        │
        └─ FAIL → Try again (Beat 2) with feedback
              ├─ [MAKER] Improve report
              ├─ [CHECKER] Validate again
              └─ Write report file [CONNECTOR]
   ↓
Update progress.md (spine remembers this run)
   ↓
End: Files exist, spine updated (ready for next heartbeat)
```

**Next heartbeat (next run):**
```
Start: progress.md exists (spine has memory from last run!)
   ↓
Read progress.md (remember Run 1)
   ↓
Run Check #2
   └─ Same process, but now memory shows the trend
   ↓
End: progress.md updated with Run 2 (spine grows)
```

---

## Loop Engineering Principles Demonstrated

✓ **Heartbeat**: Regular daily check cycles (numbered #1, #2, #3...)
✓ **Worktree/Isolation**: Each report is isolated (separate files per run)
✓ **Skill/Project Knowledge**: Knows how to analyze projects (counts files, lines)
✓ **Maker-Checker**: Two-step validation (collect → validate → improve)
✓ **Connector/Action**: Writes actual report files (affects the world)
✓ **Spine/Persistent Memory**: progress.md remembers all previous checks
✓ **Safety Limits**: Max attempts prevent doom loops
✓ **Success Conditions**: Clear criteria for pass/fail
✓ **Beginner-Friendly**: Uses Python standard library only

---

## Why This is the Capstone

Project 8 integrates everything from Projects 1-7:

- **Project 1** (ISS Loop): Basic looping concept
- **Project 2** (Portfolio Loop): Conditional execution
- **Project 3** (Morning Brief): Reading project data
- **Project 4** (Event-Driven): Responding to events
- **Project 5** (Maker-Checker): Dual validation
- **Project 6** (Human-on-the-Loop): User interaction
- **Project 7** (Safe Loop): Limits and memory
- **Project 8** (Daily Health Check): **ALL six components together**

This project shows how a real-world automation task combines all the principles.

---

## Key Takeaways

1. **Loops are predictable**: Heartbeats create rhythm
2. **Isolation prevents chaos**: Separate workspaces keep runs clean
3. **Skill matters**: Domain knowledge makes loops smarter
4. **Dual validation works**: Maker-Checker catches problems
5. **Action creates impact**: Connectors write files, send alerts, etc.
6. **Memory is power**: Spine enables learning and trending
7. **Limits are safety**: Prevent runaway loops
8. **Simple beats complex**: No frameworks needed - just logic

---

## Explaining This in an Interview

**Elevator Pitch (30 seconds):**
> "This is a daily health check loop. It runs daily, analyzes a project's files and code, creates a health report, validates that report meets quality standards, and saves everything to memory. It demonstrates heartbeat, isolation, skill, maker-checker, connector, and spine - the six foundations of Loop Engineering."

**Slightly Longer (2 minutes):**
> "The loop has six components. First, heartbeat - it runs on a schedule as check #1, #2, etc. Second, isolation - each check gets its own report file. Third, skill - it knows how to analyze Python projects. Fourth, maker-checker - it creates a report (maker) then validates it (checker), improving if needed. Fifth, connector - it writes the report to an actual file. Sixth, spine - it remembers all previous checks in progress.md so the next run sees the history. If something fails, it retries with feedback (up to 2 times). Once successful or out of attempts, it updates memory and stops - no infinite loops."

