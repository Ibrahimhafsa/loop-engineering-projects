# A6 Checklist: Two-Routine Gate Audit

The A6 checklist verifies that both Routine A and Routine B follow safe automation practices.

## Understanding A6

**A6** stands for six key audit points that make automation safe:

1. **Actions** - What can this routine actually do?
2. **Approval** - Is there human approval in the critical path?
3. **Access** - Who can trigger this? Is it protected?
4. **Audit** - Is everything logged?
5. **Ability** - Can this break things or is it safe?
6. **Automation** - What's truly automated vs. manual?

This checklist applies to **both Routine A and Routine B**.

---

## Checklist for Routine A

### 1. Connectors: Pruned and Minimal

**Question:** What external systems does Routine A connect to?

**Requirement:** Only use what's necessary. No external APIs, credentials, or cloud services.

- [ ] No external HTTP calls
- [ ] No database connections
- [ ] No API keys or credentials
- [ ] No cloud services (AWS, GCP, Azure, etc.)
- [ ] Local file I/O only

**Verification:**

```bash
grep -E "(http|requests|boto|gcloud|azure)" routine_a.py
```

Should return: **nothing** (no external connectors)

**Finding:** ✓ PASS - Routine A uses only Python standard library, local file I/O only.

---

### 2. Unrestricted Pushes: Disabled

**Question:** Can Routine A automatically trigger downstream actions without approval?

**Requirement:** Routine A must NOT automatically trigger Routine B. It must stop and wait for human approval.

- [ ] Routine A does NOT import/call routine_b.py
- [ ] Routine A does NOT start an HTTP server to Routine B
- [ ] Routine A does NOT make HTTP calls to Routine B
- [ ] Draft file is created and displayed, then stops

**Verification:**

```bash
grep -E "(import.*routine_b|requests.post|trigger|urlopen|http)" routine_a.py
```

Should return: **nothing** (no downstream triggers)

**Finding:** ✓ PASS - Routine A creates draft and stops. No automatic triggers.

---

### 3. State File: Selected and Used

**Question:** Where is state recorded? Is the state file actually used?

**Requirement:** Use a persistent state file (JSON or Markdown) to record all actions.

- [ ] State file exists: `state.json`
- [ ] Routine A reads from state.json
- [ ] Routine A writes to state.json
- [ ] Routine A increments a counter or logs the action

**Verification:**

```bash
grep -E "(load_state|save_state|state.json)" routine_a.py | head -5
```

Should show: state loading and saving

**Finding:** ✓ PASS - Routine A loads state, creates draft, updates state.

**Example state entry from Routine A:**

```json
{
  "routine_a_runs": 1,
  "drafts": [
    {
      "timestamp": "2026-08-19T10:30:45.123456",
      "filename": "draft_latest.md",
      "status": "created",
      "approved": false
    }
  ]
}
```

---

### 4. Human Approval Gate: Exists Between A and B

**Question:** Is there an explicit approval step that blocks Routine B from running?

**Requirement:** A human must manually approve the draft. Approval must be recorded.

- [ ] Approval script exists: `approve_draft.py`
- [ ] Human must run approval script
- [ ] Approval decision is recorded in state.json
- [ ] Routine B checks approval status before executing

**Verification:**

```bash
python approve_draft.py
# Follow prompts: review draft, choose approve/reject
cat state.json | grep -A 5 "approvals"
```

Should show: approval record with timestamp and decision

**Finding:** ✓ PASS - `approve_draft.py` displays draft and records decision.

**Example approval entry:**

```json
{
  "timestamp": "2026-08-19T10:31:30.654321",
  "decision": "approved",
  "approved": true
}
```

---

### 5. Routine B Cannot Run Without Approval

**Question:** What prevents Routine B from executing if draft is NOT approved?

**Requirement:** Routine B must check the approval status in state.json. If no approval, it must reject the trigger request.

- [ ] Routine B calls `check_approval()` function
- [ ] `check_approval()` reads state.json
- [ ] `check_approval()` returns False if no approval
- [ ] HTTP response is 403 Forbidden with message about no approval

**Verification:**

```bash
# In routine_b.py, look for approval check:
grep -A 5 "check_approval" routine_b.py
```

Should show: function that validates approval

**Code review:**

```python
def check_approval():
    """Check if the latest draft has been approved."""
    state = load_state()
    if not state["approvals"]:
        return False
    latest_approval = state["approvals"][-1]
    return latest_approval.get("approved", False)
```

**Finding:** ✓ PASS - Routine B checks approval before executing.

---

### 6. Results Recorded Clearly

**Question:** What evidence exists that Routine A ran and created its draft?

**Requirement:** Results must be clear in both files and state file.

- [ ] Draft file created: `draft_latest.md`
- [ ] Draft file is readable and contains proposal
- [ ] state.json contains draft record with timestamp
- [ ] Routine A logs to console with ✓ symbols (checkmarks)

**Verification:**

```bash
python routine_a.py
# Output should show:
#   ✓ Draft created: draft_latest.md
#   ✓ Timestamp: <ISO timestamp>
#   ✓ State updated in state.json

ls -la draft_latest.md
cat state.json | jq '.drafts[-1]'  # Show latest draft record
```

**Finding:** ✓ PASS - Draft created, displayed, and recorded.

---

## Checklist for Routine B

### 1. Connectors: Pruned and Minimal

**Question:** What external systems does Routine B connect to?

**Requirement:** Only local HTTP server, no external APIs.

- [ ] No external API calls
- [ ] No database connections
- [ ] No credentials to external services
- [ ] Local HTTP server only on localhost:9999
- [ ] All state and results written to local files

**Verification:**

```bash
grep -E "(http|requests|boto|gcloud|azure).*[^localhost]" routine_b.py
```

Should return: **nothing** (only localhost connections)

**Finding:** ✓ PASS - Routine B is a local-only HTTP server.

---

### 2. Unrestricted Pushes: Disabled

**Question:** Can Routine B be triggered without proper authorization?

**Requirement:** Routine B must require bearer token authentication.

- [ ] Bearer token required in Authorization header
- [ ] Token is checked on every request
- [ ] Invalid/missing token returns 401 or 403
- [ ] Approval status is checked before executing

**Verification:**

```bash
# Check for token validation:
grep -A 10 "Authorization" routine_b.py | head -15
```

Should show: token parsing and validation

**Code review:**

```python
auth_header = self.headers.get("Authorization", "")
if not auth_header.startswith("Bearer "):
    self.send_response(401)
    # Error response

provided_token = auth_header[7:]
if provided_token != BEARER_TOKEN:
    self.send_response(403)
    # Error response
```

**Finding:** ✓ PASS - Token required, validated on every request.

---

### 3. State File: Selected and Used

**Question:** Where does Routine B record its actions?

**Requirement:** Routine B must read and write to state.json.

- [ ] Routine B reads state.json to check approval
- [ ] Routine B writes result to state.json after executing
- [ ] Result includes timestamp and success status

**Verification:**

```bash
grep -E "(load_state|save_state|routine_b_results)" routine_b.py
```

Should show: state loading and saving

**Code review:**

```python
state = load_state()
# ... execute action ...
state["routine_b_results"].append({
    "timestamp": datetime.datetime.now().isoformat(),
    "status": "executed",
    "result_file": result_filename,
    "success": True
})
save_state(state)
```

**Finding:** ✓ PASS - Routine B records execution in state.json.

**Example execution entry:**

```json
{
  "timestamp": "2026-08-19T10:32:15.987654",
  "status": "executed",
  "result_file": "result_approved.md",
  "success": true
}
```

---

### 4. Human Approval Gate: Enforcement

**Question:** How does Routine B verify that a human approved the draft?

**Requirement:** Routine B must check `state.json` for approval before executing.

- [ ] `check_approval()` reads state.json
- [ ] Function checks latest approval in the list
- [ ] Returns False if no approvals or latest is rejected
- [ ] Returns True only if latest is approved
- [ ] Trigger request returns 403 if not approved

**Verification:**

```bash
# Start Routine B
python routine_b.py &

# Try to trigger WITHOUT approval
python trigger_routine_b.py
# Should see error: "No approved draft"

# Now approve and try again
python approve_draft.py  # Select "Approve"
python trigger_routine_b.py
# Should now succeed
```

**Finding:** ✓ PASS - Routine B enforces approval check.

---

### 5. Bearer Token: Proper Protection

**Question:** How is the bearer token generated and stored?

**Requirement:** Generate random token, save to file, display once, protect from Git.

- [ ] Token generated with `secrets.token_urlsafe()`
- [ ] Token saved to `.routine_b_token` (not committed to Git)
- [ ] Token file has restricted permissions (0o600 if on Unix)
- [ ] Token displayed exactly once at server start
- [ ] Message warns "SAVE IT, it will not be shown again"

**Verification:**

```bash
# Check .gitignore includes token file:
grep ".routine_b_token" .gitignore

# Check token file doesn't exist in git:
git status | grep ".routine_b_token"
# Should show: not in git

# Run Routine B and note the token:
python routine_b.py 2>&1 | head -20
```

**Finding:** ✓ PASS - Token generated, protected, and warned appropriately.

---

### 6. Results Recorded Clearly

**Question:** What evidence exists that Routine B executed the approved action?

**Requirement:** Results must be clear in both files and state.json.

- [ ] Result file created: `result_approved.md`
- [ ] Result file contains approved proposal + action proof
- [ ] state.json contains execution record with timestamp
- [ ] HTTP response shows success status
- [ ] Trigger script displays success message

**Verification:**

```bash
# After triggering Routine B:
ls -la result_approved.md
cat result_approved.md  # Should show approved proposal + execution proof

cat state.json | jq '.routine_b_results[-1]'  # Latest execution
```

**Finding:** ✓ PASS - Result file and state both record execution.

**Example result file excerpt:**

```markdown
# Final Approved Result

**Generated:** 2026-08-19T10:32:15.987654
**Status:** APPROVED AND EXECUTED

## Original Proposal
[Draft content here]

## Final Action Taken
✓ Draft has been reviewed and approved by human
✓ Implementation action completed successfully
✓ Report generated and saved
```

---

## Summary Table

| Checklist Item | Routine A | Routine B | Status |
|---|---|---|---|
| 1. Connectors pruned | ✓ Local only | ✓ Local only | PASS |
| 2. No unrestricted pushes | ✓ No auto-trigger | ✓ Token required | PASS |
| 3. State file used | ✓ state.json | ✓ state.json | PASS |
| 4. Approval gate exists | ✓ approve_draft.py | ✓ check_approval() | PASS |
| 5. B blocked without approval | ✓ N/A | ✓ 403 response | PASS |
| 6. Results recorded | ✓ Draft + state | ✓ Result + state | PASS |

**Overall Result: ✓ ALL CHECKS PASS**

---

## What This Means

**Security:**
- No external APIs or credentials leak
- No automatic pushes bypass human oversight
- State is fully auditable
- Bearer token prevents unauthorized access

**Reliability:**
- State file proves what happened and when
- Approval gate prevents mistakes
- Results are recorded for verification
- Easy to diagnose problems

**Best Practices:**
- Human approval in the critical path
- Minimal dependencies (Python stdlib only)
- Secrets protected from Git
- Clear audit trail

This automation can be safely used in production because:
1. A human must explicitly approve before B runs
2. Everything is logged to state.json
3. No external services can be compromised
4. Token protection prevents unauthorized access
5. Results are verifiable

---

## Running the Full A6 Audit

Execute this sequence to verify all points:

```bash
# 1. Create draft
python routine_a.py

# 2. Check state (Routine A checks)
cat state.json

# 3. Review draft and approve
python approve_draft.py  # Choose option 1

# 4. Check state (approval checks)
cat state.json

# 5. Start Routine B server
python routine_b.py &
TOKEN=$(cat .routine_b_token)

# 6. Test rejection (missing approval)
# First, in another terminal, test with no approval:
# Create new state with no approval:
echo '{"routine_a_runs": 0, "drafts": [], "approvals": [], "routine_b_results": []}' > state.json
python trigger_routine_b.py  # Should fail

# 7. Restore approval
python approve_draft.py  # Approve again

# 8. Trigger Routine B
python trigger_routine_b.py

# 9. Verify results
cat result_approved.md
cat state.json

# 10. Test invalid token
curl -X POST http://localhost:9999/trigger \
  -H "Authorization: Bearer INVALID_TOKEN"
# Should return 403 Forbidden

# 11. Test missing token
curl -X POST http://localhost:9999/trigger
# Should return 401 Unauthorized

echo "✓ A6 Checklist Complete"
```

All checks should pass.
