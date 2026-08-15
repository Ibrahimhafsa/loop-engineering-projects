"""
Checker: Reviews the Maker's result against success conditions.
The Checker's job is to validate if the result meets requirements.
"""

from datetime import datetime


class SuccessCondition:
    """Defines a single success condition."""

    def __init__(self, name: str, check_func, description: str):
        """
        Initialize a success condition.

        Args:
            name: Name of the condition
            check_func: Function that returns True if condition is met
            description: Human-readable description
        """
        self.name = name
        check_func_actual = check_func
        self.description = description

    def validate(self, result: dict) -> bool:
        """Validate if this condition is met."""
        summary = result.get("summary", "")

        # Define conditions based on condition name
        if self.name == "min_length":
            return len(summary) >= 20  # At least 20 characters
        elif self.name == "word_count":
            words = summary.split()
            return len(words) >= 5  # At least 5 words
        elif self.name == "has_action":
            action_verbs = ["performs", "provides", "creates", "extracts", "extraction", "extracting", "includes", "handles"]
            return any(verb in summary.lower() for verb in action_verbs)
        else:
            return True

    def __repr__(self) -> str:
        return f"{self.name}: {self.description}"


class Checker:
    """Reviews Maker results against success conditions."""

    def __init__(self):
        """Initialize the Checker with default success conditions."""
        self.name = "Checker"
        self.conditions = [
            SuccessCondition(
                "min_length",
                None,
                "Summary must be at least 20 characters long",
            ),
            SuccessCondition(
                "word_count", None, "Summary must have at least 5 words"
            ),
            SuccessCondition(
                "has_action",
                None,
                "Summary must contain an action verb (performs, provides, creates, etc.)",
            ),
        ]

    def check(self, result: dict) -> dict:
        """
        Check the Maker's result against all success conditions.

        Args:
            result: dict from Maker with 'summary' key

        Returns:
            dict with:
                - verdict: "PASS" or "FAIL"
                - conditions_checked: list of condition names
                - passed_conditions: list of passed condition names
                - failed_conditions: list of failed condition names
                - summary: human-readable summary
                - timestamp: when check was performed
        """
        summary = result.get("summary", "")
        passed = []
        failed = []

        # Check each condition
        for condition in self.conditions:
            if condition.validate(result):
                passed.append(condition.name)
            else:
                failed.append(condition.name)

        # Determine verdict
        verdict = "PASS" if len(failed) == 0 else "FAIL"

        # Generate feedback for failed conditions
        feedback_lines = []
        for condition in self.conditions:
            if condition.name in failed:
                feedback_lines.append(f"- {condition.description}")

        feedback = "\n".join(feedback_lines) if feedback_lines else ""

        check_result = {
            "verdict": verdict,
            "conditions_checked": [c.name for c in self.conditions],
            "passed_conditions": passed,
            "failed_conditions": failed,
            "feedback": feedback,
            "summary": summary,
            "timestamp": datetime.now().isoformat(),
        }

        return check_result

    def display_check(self, check_result: dict, attempt_num: int) -> str:
        """Display the checker's result in a readable format."""
        output = []
        output.append("=" * 60)
        output.append(f"CHECKER REVIEW (Attempt #{attempt_num})")
        output.append("=" * 60)
        output.append(f"Summary Reviewed: {check_result['summary']}")
        output.append("")
        output.append(f"Verdict: {check_result['verdict']}")
        output.append("")
        output.append("Conditions Checked:")
        for condition in self.conditions:
            status = "[PASS]" if condition.name in check_result["passed_conditions"] else "[FAIL]"
            output.append(f"  {status} - {condition.description}")
        output.append("")

        if check_result["feedback"]:
            output.append("Feedback for Improvement:")
            output.append(check_result["feedback"])
            output.append("")

        output.append("=" * 60)
        return "\n".join(output)
