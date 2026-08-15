"""
Maker-Checker Loop: Orchestrates the Maker-Checker pattern.
This is the main loop that coordinates Maker, Checker, and progress tracking.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from maker import Maker
from checker import Checker


class MakerCheckerLoop:
    """Orchestrates the Maker-Checker pattern with persistent memory."""

    def __init__(self, progress_file: str = "progress.md", max_attempts: int = 3):
        """
        Initialize the Maker-Checker loop.

        Args:
            progress_file: Path to progress.md (the spine)
            max_attempts: Maximum retry attempts before giving up
        """
        self.progress_file = Path(progress_file)
        self.max_attempts = max_attempts
        self.maker = Maker()
        self.checker = Checker()

    def run_task(self, task_id: str, user_request: str) -> dict:
        """
        Run a complete task through the Maker-Checker loop.

        Args:
            task_id: Identifier for this task (e.g., "Task 1")
            user_request: The user's request to be processed

        Returns:
            dict with final result, verdict, and attempt count
        """
        print("\n" + "=" * 60)
        print(f"STARTING {task_id}")
        print("=" * 60)
        print(f"User Request: {user_request}\n")

        attempt = 0
        current_feedback = None
        final_result = None

        while attempt < self.max_attempts:
            attempt += 1
            print(f"\n--- Attempt #{attempt} ---")

            # STEP 1: Maker creates result
            print("Step 1: Maker is creating result...")
            maker_result = self.maker.create_summary(user_request, current_feedback)
            print(self.maker.display_result(maker_result))

            # STEP 2: Checker reviews result
            print("\nStep 2: Checker is reviewing result...")
            check_result = self.checker.check(maker_result)
            print(self.checker.display_check(check_result, attempt))

            final_result = {
                "task_id": task_id,
                "user_request": user_request,
                "attempt": attempt,
                "maker_output": maker_result["summary"],
                "verdict": check_result["verdict"],
                "passed_conditions": check_result["passed_conditions"],
                "failed_conditions": check_result["failed_conditions"],
                "feedback": check_result["feedback"],
            }

            # STEP 3: Check if we passed
            if check_result["verdict"] == "PASS":
                print(f"\n[SUCCESS] on attempt #{attempt}!")
                final_result["status"] = "PASSED"
                final_result["total_attempts"] = attempt
                self._save_progress(task_id, final_result)
                return final_result

            # STEP 4: If failed and attempts remain, prepare for retry
            if attempt < self.max_attempts:
                print(f"\n[FAILED] on attempt #{attempt}")
                print(f"Maker will try to improve (attempt #{attempt + 1} of {self.max_attempts})")
                # Prepare feedback for next iteration
                current_feedback = "Make it more detailed and descriptive"
                self._save_progress(task_id, final_result, intermediate=True)
            else:
                # Max attempts reached
                print(f"\n[FAILED] - Max attempts ({self.max_attempts}) reached")
                final_result["status"] = "FAILED_MAX_ATTEMPTS"
                final_result["total_attempts"] = attempt
                self._save_progress(task_id, final_result)
                return final_result

        return final_result

    def _save_progress(self, task_id: str, result: dict, intermediate: bool = False):
        """
        Save progress to progress.md (the spine).

        Args:
            task_id: Identifier for this task
            result: Result dict from the loop
            intermediate: If True, this is an intermediate save (not final)
        """
        # Read current progress
        if self.progress_file.exists():
            content = self.progress_file.read_text()
        else:
            content = ""

        # Prepare update text
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        attempt_num = result["attempt"]

        attempt_section = f"""### Attempt {attempt_num}
- **Status**: {"CHECKING" if intermediate else result.get("status", "COMPLETE")}
- **Maker Output**: {result["maker_output"]}
- **Checker Verdict**: {result["verdict"]}
- **Attempt Number**: {attempt_num}
- **Timestamp**: {timestamp}
- **Passed Conditions**: {", ".join(result.get("passed_conditions", []))}
- **Failed Conditions**: {", ".join(result.get("failed_conditions", []))}"""

        if result.get("feedback"):
            attempt_section += f"\n- **Feedback**: {result['feedback']}"

        # Find and update the task section
        if task_id in content:
            # Task already exists, append attempt
            # Find the attempt section
            pattern = rf"(## {task_id}.*?)(?=## |$)"
            match = re.search(pattern, content, re.DOTALL)
            if match:
                task_section = match.group(1)
                # Find last attempt marker
                if "### Attempt" in task_section:
                    # Insert new attempt before Final Status
                    final_status_pos = task_section.rfind("### Final Status")
                    if final_status_pos != -1:
                        before = content[: match.start(1) + final_status_pos]
                        after = content[match.start(1) + final_status_pos :]
                        content = before + attempt_section + "\n\n" + after
                    else:
                        content = content.replace(task_section, task_section + "\n\n" + attempt_section)
                else:
                    content = content.replace(task_section, task_section + "\n\n" + attempt_section)

        # Update final status if this is the final attempt
        if not intermediate:
            final_status = f"""### Final Status
- **Overall Result**: {result.get("status", "UNKNOWN")}
- **Total Attempts**: {result.get("total_attempts", attempt_num)}"""

            if "### Final Status" in content:
                # Replace existing final status
                pattern = rf"(## {task_id}.*?)### Final Status\n- \*\*Overall Result\*\*:.*?\n- \*\*Total Attempts\*\*:.*?(?=\n\n|## |$)"
                content = re.sub(
                    pattern,
                    rf"\1" + final_status,
                    content,
                    flags=re.DOTALL,
                )
            else:
                # Add final status
                pattern = rf"(## {task_id}.*?)(?=## |$)"
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    insertion_point = match.end(1) - 1
                    content = (
                        content[:insertion_point]
                        + "\n\n"
                        + final_status
                        + content[insertion_point :]
                    )

        self.progress_file.write_text(content)
        print(f"\n[Progress saved to {self.progress_file}]")

    def display_summary(self):
        """Display a summary of all completed tasks."""
        print("\n" + "=" * 60)
        print("LOOP SUMMARY")
        print("=" * 60)
        print(f"Max Attempts per Task: {self.max_attempts}")
        print("=" * 60)
