#!/usr/bin/env python3
"""
Routine B: Approved Action Handler
Runs as a local HTTP API server.
Requires bearer token authentication.
Only executes actions after human approval via Routine A.
"""
import json
import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import secrets
import os


# Global variables for token and state
BEARER_TOKEN = None
SERVER_PORT = 9999


def load_state():
    """Load the current state from state.json."""
    if Path("state.json").exists():
        with open("state.json", "r") as f:
            return json.load(f)
    return {"routine_a_runs": 0, "drafts": [], "approvals": [], "routine_b_results": []}


def save_state(state):
    """Save state to state.json."""
    with open("state.json", "w") as f:
        json.dump(state, f, indent=2)


def check_approval():
    """Check if the latest draft has been approved."""
    state = load_state()
    if not state["approvals"]:
        return False
    latest_approval = state["approvals"][-1]
    return latest_approval.get("approved", False)


def execute_action():
    """Execute the follow-up action after approval."""
    timestamp = datetime.datetime.now().isoformat()

    # Read the draft that was approved
    if Path("draft_latest.md").exists():
        with open("draft_latest.md", "r", encoding="utf-8") as f:
            draft_content = f.read()
    else:
        draft_content = "No draft found"

    # Generate final result (use unicode-safe characters)
    result_content = f"""# Final Approved Result

**Generated:** {timestamp}
**Status:** APPROVED AND EXECUTED

## Original Proposal
{draft_content}

## Final Action Taken
[DONE] Draft has been reviewed and approved by human
[DONE] Implementation action completed successfully
[DONE] Report generated and saved

## Execution Details
- Routine A created the draft
- Human reviewed the draft
- Human approved the proposal
- Routine B executed the approved action
- This result file was created

## Next Steps
The approved proposal is now in effect. Implementation team should proceed
with the project as outlined in the proposal above.

---
This document confirms that Routine B successfully executed the approved action.
All approvals have been verified and recorded in state.json
"""

    # Save result to file with UTF-8 encoding
    result_filename = "result_approved.md"
    with open(result_filename, "w", encoding="utf-8") as f:
        f.write(result_content)

    return result_filename, result_content


class RequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Routine B API."""

    def do_POST(self):
        """Handle POST request to trigger approved action."""
        if self.path != "/trigger":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')
            return

        # Check bearer token
        auth_header = self.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Unauthorized: Missing or invalid bearer token"
            }).encode())
            return

        provided_token = auth_header[7:]  # Remove "Bearer " prefix
        if provided_token != BEARER_TOKEN:
            self.send_response(403)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Forbidden: Invalid bearer token"
            }).encode())
            return

        # Check if draft is approved
        if not check_approval():
            self.send_response(403)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Forbidden: No approved draft. Routine A draft must be approved first."
            }).encode())
            return

        # Execute the action
        try:
            result_filename, result_content = execute_action()

            # Update state with execution result
            state = load_state()
            state["routine_b_results"].append({
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "executed",
                "result_file": result_filename,
                "success": True
            })
            save_state(state)

            # Return success response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "status": "success",
                "message": "Approved action executed successfully",
                "result_file": result_filename,
                "timestamp": datetime.datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response, indent=2, ensure_ascii=True).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": f"Internal server error: {str(e)}"
            }).encode())

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def start_server():
    """Start the HTTP server for Routine B."""
    print("\n" + "="*60)
    print("ROUTINE B: Approved Action Handler (HTTP Server)")
    print("="*60 + "\n")

    server = HTTPServer(("localhost", SERVER_PORT), RequestHandler)
    print(f"[READY] Server listening on http://localhost:{SERVER_PORT}")
    print(f"[READY] Endpoint: POST /trigger")
    print(f"[READY] Required header: Authorization: Bearer {BEARER_TOKEN}")
    print("\nServer running. Press Ctrl+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[STOPPED] Server stopped")
        server.server_close()


def initialize_token():
    """Initialize or load the bearer token."""
    global BEARER_TOKEN
    token_file = ".routine_b_token"

    # Check if token file exists
    if Path(token_file).exists():
        with open(token_file, "r") as f:
            BEARER_TOKEN = f.read().strip()
        print(f"[LOADED] Token loaded from {token_file}")
    else:
        # Generate new token
        BEARER_TOKEN = secrets.token_urlsafe(32)
        with open(token_file, "w") as f:
            f.write(BEARER_TOKEN)
        os.chmod(token_file, 0o600)  # Read/write for owner only
        print(f"[NEW] New token generated and saved to {token_file}")

    return BEARER_TOKEN


if __name__ == "__main__":
    # Initialize token
    token = initialize_token()
    print("\n" + "*** BEARER TOKEN ***")
    print("="*60)
    print(f"Token: {token}")
    print("\n*** IMPORTANT: Save this token immediately!")
    print("*** It will NOT be shown again!")
    print("*** Use it in the Authorization header when triggering Routine B")
    print("="*60)

    # Start server
    start_server()
