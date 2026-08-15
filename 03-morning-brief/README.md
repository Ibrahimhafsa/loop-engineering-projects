# Morning Brief with a Memory 🌅

## What This Project Does

This is a **scheduled loop** that runs periodically (like a cron job) and generates a "morning brief" — a simple status update for each run. The key feature is **memory**: the loop remembers what happened in previous runs and can reference that information.

Think of it like a daily journal that remembers all your past entries. Each time you open your journal, you can see everything you've written before.

---

## Core Concepts from Loop Engineering

### 1. **Scheduled Loop**
A scheduled loop is a program that runs automatically on a repeating schedule. Instead of manually running something over and over, the scheduler handles it for you.

**In this project:**
- You can run `python morning_brief.py` manually to test
- In production, you'd use a scheduler like `cron` (Linux/Mac) or Task Scheduler (Windows) to run it automatically every morning
- Each run is independent, but they share memory (see below)

### 2. **Heartbeat**
The heartbeat is the **overall clock** or **schedule** that controls when your loop runs. It's the "pulse" of your system.

**In this project:**
- The heartbeat would be "run this every morning at 6:00 AM"
- Each heartbeat triggers one run

### 3. **Beat**
A beat is a single **execution** or **iteration** of the loop. Every time the heartbeat pulse fires, one beat happens.

**In this project:**
- Each run of `python morning_brief.py` is one beat
- Each beat:
  - Reads the previous state
  - Generates a new brief
  - Saves the state
  - Displays results

### 4. **Spine (Persistent Memory)**
The spine is the **persistent data store** that survives between runs. It's the "memory" that connects one beat to the next.

**In this project:**
- The spine is `progress.md` — a simple markdown file
- Between runs, the spine stores:
  - The timestamp of each previous run
  - The brief that was generated
  - The status of each beat
  - How many times the loop has run
- Each new beat **reads the spine first** to understand the history
- Then it **writes to the spine** to save its results

---

## How Memory Works in This Project

### Run #1 (First Time)
```
[SPINE] Read progress.md
  → No previous runs found (memory is empty)
[BEAT] Generate morning brief for today
[BEAT] Save to progress.md
  → progress.md now contains: Run #1, timestamp, message
[DISPLAY] Show the brief
```

### Run #2 (Second Time)
```
[SPINE] Read progress.md
  → Found Run #1 from previous execution ✓
  → Load that information into memory
[BEAT] Generate morning brief for today
[BEAT] Save to progress.md
  → progress.md now contains: Run #1, Run #2, both timestamps, all messages
[DISPLAY] Show the brief
💾 MEMORY CHECK: This run knows about 1 previous run!
```

The magic is that the **spine (progress.md) connects the runs across time**. Without it, each run would start from zero. With it, each run is part of a continuous story.

---

## Project Structure

```
03-morning-brief/
├── morning_brief.py          # The main loop script
├── progress.md               # The spine (memory between runs)
├── README.md                 # This file
└── .claude/                  # Claude Code configuration
```

---

## How to Run the Project

### Prerequisites
- Python 3.6+ (just the standard library, no external packages needed)

### Run Once (Manual)
```bash
python morning_brief.py
```

This will:
1. Read `progress.md` to check for previous runs
2. Generate a new morning brief
3. Save the brief to `progress.md`
4. Display the brief in the terminal

### Run Twice to See Memory in Action
```bash
# First run
python morning_brief.py

# Wait a moment (or just run immediately)
# Second run - it will show "MEMORY CHECK: This run knows about 1 previous run!"
python morning_brief.py
```

### Set Up Real Scheduling (Optional)

#### On Linux/Mac (using cron)
```bash
# Edit your crontab
crontab -e

# Add this line to run the brief every morning at 6 AM
0 6 * * * cd /path/to/03-morning-brief && python morning_brief.py
```

#### On Windows (using Task Scheduler)
1. Open Task Scheduler
2. Create a Basic Task
3. Set trigger to "Daily" at your preferred time
4. Set action to "Start a program"
5. Program: `python.exe`
6. Arguments: `morning_brief.py`
7. Start in: `/path/to/03-morning-brief`

---

## Understanding the Code

### Main Functions

**`read_spine()`**
- Reads the `progress.md` file
- Extracts the JSON data embedded in comments
- Returns a dictionary with all previous runs
- If no previous runs exist, returns an empty structure

**`generate_brief(spine_data)`**
- Creates a new brief with the current timestamp and date
- Increments the run number based on how many previous runs exist
- Returns a dictionary containing the brief data

**`save_spine(spine_data)`**
- Takes all the run history
- Writes it to `progress.md` in a readable format
- Stores the raw JSON in an HTML comment for the script to read
- This is the critical step that creates memory

**`display_brief(brief)`**
- Pretty-prints the morning brief to the terminal
- Shows date, time, run number, status, and message

**`main()`**
- Orchestrates the entire beat:
  1. [SPINE] Read previous state
  2. [BEAT] Generate new brief
  3. [BEAT] Save new state
  4. Display results
  5. Verify memory is working

---

## What Happens to progress.md?

### After Run #1
```markdown
# Morning Brief - Loop Memory

## What is this?
This file serves as the **spine** (persistent memory)...

## Run History

### Run #1 - 2026-08-15 10:30:45
**Date:** Thursday, August 15, 2026
**Status:** ✓ Morning brief generated successfully
**Message:** Good morning! Today is Thursday, August 15, 2026.

<!-- SPINE_DATA:{"runs": [{...}], "last_brief": {...}}:SPINE_DATA -->
```

### After Run #2
The file now contains both Run #1 and Run #2, showing the complete history of all executions.

---

## Key Takeaways

1. **Spine = Persistence** — The spine file stores state between runs
2. **Memory = Intelligence** — By reading the spine first, each beat knows about previous beats
3. **Simple = Effective** — No databases or complex systems needed, just a markdown file
4. **Scheduled = Automation** — The heartbeat (scheduler) runs the loop automatically
5. **Beats = Individual Runs** — Each execution is one beat that reads, processes, and writes

---

## Next Steps (Learning Path)

- ✅ **Project 3 (This One):** Learn the basics of loops, beats, and simple memory
- 📖 **Project 4:** Add more complex state (TODO list, counter, etc.)
- 📖 **Project 5:** Multiple spines for different types of data
- 📖 **Project 6:** Real scheduled heartbeat with proper cron setup

---

## Troubleshooting

**Progress.md looks weird or corrupted**
- Delete `progress.md`
- Run the script again
- It will create a fresh `progress.md` on the first beat

**The script doesn't find previous runs**
- Check that `progress.md` exists in the same folder as `morning_brief.py`
- Look for the `<!-- SPINE_DATA:` marker in the file
- If it's not there, the script couldn't save the state properly

**I want to reset and start over**
- Just delete `progress.md` and run the script again
- Each new beat will create fresh state

---

## Summary

This project demonstrates the core idea of Loop Engineering: **a scheduled loop that maintains persistent memory between runs**. The spine (`progress.md`) is what makes it work — without it, each run is isolated. With it, each run is part of a continuous, growing story.

The morning brief is just the example. You could use this pattern for:
- Daily health tracking
- Monitoring task status
- Aggregating logs
- Building a time-series history of anything
- Creating an audit trail

The pattern is the same: read spine → do work → write spine → display results.
