# Project 11: Build the Two-Routine Gate

## What is Project 11?

Project 11 demonstrates how to build a **human approval gate** between two automated routines. This is a real-world pattern used in many automated systems: you want automation to *propose* changes, but require a human to *approve* them before anything destructive happens.

Think of it like:
- Routine A writes a proposal and puts it on your desk
- You (the human) read it and decide: "yes" or "no"
- Only if you say "yes" does Routine B execute the approved action

This prevents mistakes where automation runs the wrong action without human oversight.

---

## Project Structure

```
11-two-routine-gate/
├── routine_a.py              # Creates a draft for human review
├── routine_b.py              # HTTP server, executes approved action
├── approve_draft.py          # Human approval gate interface
├── trigger_routine_b.py      # Helper to trigger Routine B with token
├── state.json               # Persistent state file (created at runtime)
├── .routine_b_token         # Bearer token (created at runtime, NOT in Git)
├── draft_latest.md          # Latest draft (created by Routine A)
├── result_approved.md       # Final result (created by Routine B)
├── README.md                # This file
├── A6_CHECKLIST.md          # Audit checklist for both routines
├── COMPLETION_REPORT.md     # Test results and final status
└── .gitignore               # Prevents secrets from being committed
```

---

## What is Routine A?

**Routine A** is a manual, one-off trigger that:
1. Creates a **draft** (a proposed change or summary)
2. Saves the draft to `draft_latest.md`
3. Displays the draft for you to read
4. Records the action in `state.json`
5. **Does NOT** automatically trigger Routine B

**Key point:** Routine A stops after creating the draft. It waits for human approval.

### Run Routine A

```bash
python routine_a.py
```

This will:
- Generate a sample project proposal
- Save it to `draft_latest.md`
- Print the draft to your terminal
- Update `state.json` with a record of this run

---

## What is the Human Gate?

The **human gate** is YOU. After Routine A creates a draft, you must:

1. **Read** the draft in `draft_latest.md`
2. **Review** it carefully
3. **Decide:** Do you approve this, or should it be rejected?
4. **Approve or reject** using the approval script

**Key point:** Without explicit human approval, Routine B will NOT run. This is the gate.

### Approve the Draft

```bash
python approve_draft.py
```

This will:
- Display the draft again
- Ask you: "Do you approve? (1=yes, 2=no, 3=cancel)"
- Record your decision in `state.json`
- Explain what to do next

---

## What is Routine B?

**Routine B** is a local HTTP server that:
1. Listens on `http://localhost:9999`
2. Requires a **bearer token** for authentication
3. Checks that a draft has been **approved**
4. Executes the approved action (creates `result_approved.md`)
5. Records the result in `state.json`

**Key point:** Routine B is an API that only runs after you approve. It cannot run without both:
- The correct bearer token
- An approved draft from Routine A

### What is an API Trigger?

An **API** is a way for programs to talk to each other. Instead of one program running another directly, it sends a message (HTTP request) to an endpoint (URL).

Routine B exposes an **endpoint** at `http://localhost:9999/trigger`. When you send a message to this endpoint with the right token, Routine B runs the approved action.

This is how modern systems work: automations don't talk to each other directly; they talk via HTTP APIs.

### What is a Bearer Token?

A **bearer token** is like a password for an API. It proves you are authorized to trigger an action.

When Routine B first runs, it:
1. Generates a random token (like `K8x9_zA...`)
2. Saves it to `.routine_b_token`
3. Displays it **once** to you
4. Tells you to save it

**IMPORTANT:** If you lose the token, you cannot trigger Routine B. Save it.

The token is NOT committed to Git (see `.gitignore`). This keeps secrets out of version control.

### Why Shouldn't Secrets Be Committed to Git?

Secrets (tokens, passwords, API keys) should never be in Git because:

1. **Anyone with repo access gets the secret** - If you push a secret to GitHub, anyone with access to the repo can see it
2. **Git history is permanent** - Even if you delete a secret later, it stays in Git history
3. **Public repos are global** - If you accidentally push to a public repo, the whole internet can see it
4. **Revocation is hard** - You have to rotate the secret everywhere it's used

**Best practice:** Store secrets in environment variables, `.env` files (in `.gitignore`), or secure vaults. Never commit them.

### Start Routine B

```bash
python routine_b.py
```

This will:
- Generate a bearer token (or load the existing one)
- Display the token once: **SAVE THIS**
- Start listening on `http://localhost:9999/trigger`
- Wait for incoming requests

**Keep this terminal running** while you trigger Routine B.

---

## How to Trigger Routine B

After Routine B is running and you've approved the draft, you can trigger it in two ways:

### Option 1: Use the Helper Script (Easier)

```bash
python trigger_routine_b.py
```

This reads the token from `.routine_b_token` and sends the request for you.

### Option 2: Use curl Directly

```bash
curl -X POST http://localhost:9999/trigger \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Replace `YOUR_TOKEN_HERE` with the actual token from `.routine_b_token`.

### What is curl?

**curl** is a command-line tool that sends HTTP requests. It's like pressing a button that tells a server "do something".

The parts:
- `-X POST` = send a POST request (not GET)
- `http://localhost:9999/trigger` = the URL (the endpoint)
- `-H "Authorization: Bearer ..."` = add a header with the token

---

## How to Check What's Approved

The **state file** (`state.json`) records everything:
- When Routine A ran
- What drafts were created
- Whether each draft was approved or rejected
- When Routine B was triggered
- Whether Routine B succeeded

Look at `state.json` to see the full timeline:

```bash
cat state.json
```

Or format it nicely:

```bash
python -m json.tool state.json
```

---

## What is a State File?

A **state file** is a local file that records what happened. Instead of programs only living in memory (lost when they close), you write the state to disk.

`state.json` tracks:
- `routine_a_runs`: How many times Routine A ran
- `drafts`: All drafts created (with timestamps and filenames)
- `approvals`: All approval decisions (with timestamp and yes/no)
- `routine_b_results`: All times Routine B was triggered (with success status)

This makes the sequence **auditable** - you can see exactly what happened and when.

---

## What is the A6 Checklist?

The **A6 checklist** is an audit tool to verify that your two-routine system is safe and follows best practices:

1. **Connectors are pruned/minimal** - Only use what's needed (no external APIs, just local)
2. **Unrestricted pushes are disabled** - Nothing automatically runs without approval
3. **A state file is selected and used** - `state.json` tracks everything
4. **Human approval gate exists** - You must explicitly approve between A and B
5. **Routine B cannot run without approval** - It checks the approval status
6. **Results are recorded clearly** - Both file results and state.json log

See `A6_CHECKLIST.md` for the full checklist.

---

## Complete Workflow

### 1. Create the Draft (Routine A)

```bash
python routine_a.py
```

Output: `draft_latest.md` created, state.json updated, draft displayed.

### 2. Review the Draft

Read `draft_latest.md` carefully. Is the proposal good?

### 3. Approve or Reject (Human Gate)

```bash
python approve_draft.py
```

Choose "Approve" (1) if you like it. This records approval in state.json.

### 4. Start Routine B Server

Open a **new terminal** and run:

```bash
python routine_b.py
```

Save the token displayed. Keep this terminal running.

### 5. Trigger Routine B

In your original terminal, run:

```bash
python trigger_routine_b.py
```

Or use curl:

```bash
curl -X POST http://localhost:9999/trigger \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 6. Check Results

```bash
cat result_approved.md  # See the final approved result
cat state.json          # See the full audit trail
```

---

## Testing

### Test 1: Create Draft and Review

```bash
python routine_a.py
cat draft_latest.md  # Read the draft
```

**Verify:** Draft was created and displayed.

### Test 2: Reject Draft

```bash
python approve_draft.py
# Choose option 2 (Reject)
cat state.json  # Check that approval shows "rejected"
```

**Verify:** Rejection is recorded.

### Test 3: Routine B Without Approval

Start Routine B:

```bash
python routine_b.py
```

(In another terminal) Try to trigger without approval:

```bash
python trigger_routine_b.py
```

**Verify:** Error message says "No approved draft" or similar.

### Test 4: Invalid Token

Get a wrong token and try:

```bash
curl -X POST http://localhost:9999/trigger \
  -H "Authorization: Bearer WRONG_TOKEN"
```

**Verify:** Error 403 Forbidden (invalid token).

### Test 5: Missing Token

Try without any token:

```bash
curl -X POST http://localhost:9999/trigger
```

**Verify:** Error 401 Unauthorized (missing token).

### Test 6: Full Approval Flow

```bash
# Create draft
python routine_a.py

# Approve
python approve_draft.py  # Choose option 1 (Approve)

# Start server (new terminal)
python routine_b.py

# Trigger (original terminal)
python trigger_routine_b.py

# Check result
cat result_approved.md
cat state.json
```

**Verify:** Draft created, approved, Routine B executed, result file created, state.json shows full timeline.

---

## Troubleshooting

### "Connection refused" when triggering Routine B

**Problem:** Routine B server is not running.

**Solution:** Start Routine B in another terminal:
```bash
python routine_b.py
```

### "Token file not found"

**Problem:** `.routine_b_token` doesn't exist.

**Solution:** Start Routine B at least once to generate it:
```bash
python routine_b.py
```

### "No approved draft" error

**Problem:** You tried to trigger Routine B without approving first.

**Solution:** 
1. Run Routine A: `python routine_a.py`
2. Approve: `python approve_draft.py` (choose option 1)
3. Then trigger Routine B

### State file is missing

**Problem:** `state.json` doesn't exist.

**Solution:** Run Routine A to create it:
```bash
python routine_a.py
```

---

## Security Summary

**Secrets Protection:**
- Bearer token saved in `.routine_b_token` (not in Git)
- No external APIs or credentials needed
- Token is generated locally
- All state stored locally

**Access Control:**
- Routine B requires bearer token
- Routine B checks approval status
- No automatic pushes or external triggers
- Human must explicitly approve between A and B

**Audit Trail:**
- `state.json` records every action with timestamps
- Approval decisions are logged
- Routine B execution is logged
- Files create clear artifacts (drafts, results)

---

## Interview Explanation

For a GIAIC interview, explain this project like this:

> "I built two routines connected by a human approval gate. Routine A creates a draft—like a proposal. Instead of automatically proceeding, the system stops and waits for me, the human, to review the draft. If I approve it, then Routine B runs—it's an HTTP server that executes the approved action. The key security features are: (1) a bearer token that proves you're authorized, (2) checking that the draft was actually approved before allowing Routine B to run, (3) a state file that logs every action for audit purposes, and (4) no secrets in Git. This pattern prevents automation from running the wrong thing without human oversight."

---

## Files Summary

| File | Purpose |
|------|---------|
| `routine_a.py` | Generate draft for human review |
| `routine_b.py` | HTTP server with bearer token, executes approved action |
| `approve_draft.py` | Human approval interface |
| `trigger_routine_b.py` | Helper to trigger Routine B |
| `state.json` | Persistent audit log (created at runtime) |
| `.routine_b_token` | Bearer token (created at runtime, not in Git) |
| `draft_latest.md` | Latest draft from Routine A |
| `result_approved.md` | Final result from Routine B |
| `.gitignore` | Prevents secrets from being committed |
| `README.md` | This documentation |
| `A6_CHECKLIST.md` | Security and design audit |
| `COMPLETION_REPORT.md` | Test results and verification |

---

**Ready to start?** Run `python routine_a.py` and follow the instructions!
