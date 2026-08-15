#!/usr/bin/env python3
"""
Human-on-the-Loop Approval Loop
Demonstrates the human-on-the-loop pattern where the system proposes actions
and humans approve or reject them before execution.
"""

import json
import os
from datetime import datetime
from pathlib import Path


class ApprovalLoop:
    def __init__(self, progress_file="progress.md"):
        self.progress_file = Path(progress_file)
        self.beats = []
        self.load_history()

    def load_history(self):
        """Load previous beats from progress.md (the spine)."""
        if self.progress_file.exists():
            content = self.progress_file.read_text(encoding="utf-8")
            # Extract JSON blocks from progress.md
            import re
            json_blocks = re.findall(r'```json\n(.*?)\n```', content, re.DOTALL)
            for block in json_blocks:
                try:
                    beat = json.loads(block)
                    self.beats.append(beat)
                except json.JSONDecodeError:
                    pass
        print(f"Loaded {len(self.beats)} previous beats from memory")

    def propose_action(self, task):
        """Generate a proposed action based on the task."""
        proposals = {
            "send email": f"Proposal: Send an email with subject 'Task Completed' to recipient@example.com",
            "create file": f"Proposal: Create a new file named 'task_output.txt' with content '{task}'",
            "update database": f"Proposal: Update database table 'tasks' with status='completed' and timestamp=now()",
            "generate report": f"Proposal: Generate a report document summarizing '{task}' and save as 'report.pdf'",
            "notify team": f"Proposal: Send notification to the team about '{task}' completion",
            "archive data": f"Proposal: Archive data related to '{task}' to archive_storage",
            "process payment": f"Proposal: Process payment of $100 for '{task}'",
            "schedule meeting": f"Proposal: Schedule a meeting to discuss '{task}' at 2 PM tomorrow",
        }

        # Simple matching: check if task contains key words
        task_lower = task.lower()
        for key, proposal in proposals.items():
            if key in task_lower:
                return proposal

        # Default proposal
        return f"Proposal: Execute task '{task}' and record completion"

    def execute_action(self, task, proposal):
        """Execute the proposed action (simulated)."""
        # Simulate different actions
        if "email" in proposal.lower():
            return f"✓ Email sent successfully to recipient@example.com"
        elif "file" in proposal.lower():
            return f"✓ File 'task_output.txt' created with task data"
        elif "database" in proposal.lower():
            return f"✓ Database updated: tasks table record modified"
        elif "report" in proposal.lower():
            return f"✓ Report generated and saved as 'report.pdf'"
        elif "notification" in proposal.lower():
            return f"✓ Notification sent to team"
        elif "archive" in proposal.lower():
            return f"✓ Data archived successfully"
        elif "payment" in proposal.lower():
            return f"✓ Payment processed successfully"
        elif "meeting" in proposal.lower():
            return f"✓ Meeting scheduled for tomorrow at 2 PM"
        else:
            return f"✓ Task executed and recorded as complete"

    def get_approval(self, proposal):
        """Ask human for approval."""
        print(f"\n{proposal}")
        print("\nDo you approve this action? (yes/no): ", end="")
        response = input().strip().lower()
        return response in ["yes", "y"]

    def save_beat(self, task, proposal, approved, result=None):
        """Save beat to progress.md."""
        beat = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "proposal": proposal,
            "decision": "APPROVED" if approved else "REJECTED",
            "result": result if approved else "Not executed (rejected)",
            "beat_number": len(self.beats) + 1
        }
        self.beats.append(beat)
        self._write_progress()
        return beat

    def _write_progress(self):
        """Write all beats to progress.md."""
        header = """# Progress: Human-on-the-Loop Approval Loop

This file is the spine - persistent memory that carries state between beats.

## Overview
- Total beats: {total_beats}
- Approved: {approved}
- Rejected: {rejected}

## Beat History
""".format(
            total_beats=len(self.beats),
            approved=sum(1 for b in self.beats if b["decision"] == "APPROVED"),
            rejected=sum(1 for b in self.beats if b["decision"] == "REJECTED")
        )

        beats_section = ""
        for beat in self.beats:
            beats_section += f"\n### Beat {beat['beat_number']}: {beat['timestamp']}\n"
            beats_section += f"- **Task**: {beat['task']}\n"
            beats_section += f"- **Decision**: {beat['decision']}\n"
            beats_section += f"- **Result**: {beat['result']}\n"

        json_section = "\n## Raw Data\n\n"
        for beat in self.beats:
            json_section += "```json\n"
            json_section += json.dumps(beat, indent=2)
            json_section += "\n```\n\n"

        content = header + beats_section + json_section
        self.progress_file.write_text(content, encoding="utf-8")

    def run_beat(self):
        """Run a single beat of the loop."""
        print("\n" + "="*60)
        print("BEAT", len(self.beats) + 1)
        print("="*60)

        # Step 1: Get task from user
        print("\nWhat task should the loop process?")
        print("Examples: 'send email', 'create file', 'update database'")
        print("Your task: ", end="")
        task = input().strip()

        if not task:
            print("❌ No task provided. Skipping beat.")
            return False

        # Step 2: Propose action
        print("\n[LOOP] Analyzing task...")
        proposal = self.propose_action(task)

        # Step 3: Show proposal and get approval
        print("[LOOP] Proposing action:")
        approved = self.get_approval(proposal)

        # Step 4: Execute or reject
        if approved:
            print("\n✓ APPROVED by human")
            print("[LOOP] Executing action...")
            result = self.execute_action(task, proposal)
            print(result)
            self.save_beat(task, proposal, approved=True, result=result)
        else:
            print("\n✗ REJECTED by human")
            print("[LOOP] Action not executed (as requested)")
            self.save_beat(task, proposal, approved=False)

        return True

    def show_history(self):
        """Display all previous beats."""
        if not self.beats:
            print("\nNo beats recorded yet.")
            return

        print("\n" + "="*60)
        print("BEAT HISTORY")
        print("="*60)

        for beat in self.beats:
            print(f"\nBeat {beat['beat_number']} ({beat['timestamp']})")
            print(f"  Task: {beat['task']}")
            print(f"  Proposal: {beat['proposal']}")
            print(f"  Decision: {beat['decision']}")
            print(f"  Result: {beat['result']}")

        print(f"\nTotal Beats: {len(self.beats)}")
        print(f"Approved: {sum(1 for b in self.beats if b['decision'] == 'APPROVED')}")
        print(f"Rejected: {sum(1 for b in self.beats if b['decision'] == 'REJECTED')}")


def main():
    loop = ApprovalLoop("progress.md")

    print("="*60)
    print("HUMAN-ON-THE-LOOP APPROVAL LOOP")
    print("="*60)
    print("\nThis loop demonstrates human-on-the-loop pattern:")
    print("1. Loop proposes an action")
    print("2. Human reviews and approves/rejects")
    print("3. Loop executes only if approved")
    print("4. Progress is saved in progress.md (the spine)")

    while True:
        print("\n" + "-"*60)
        print("Options:")
        print("  [1] Run a new beat")
        print("  [2] Show beat history")
        print("  [3] Exit")
        print("Choice: ", end="")

        choice = input().strip()

        if choice == "1":
            loop.run_beat()
        elif choice == "2":
            loop.show_history()
        elif choice == "3":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
