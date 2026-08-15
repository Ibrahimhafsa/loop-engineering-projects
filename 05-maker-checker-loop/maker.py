"""
Maker: Creates a summary from user input.
The Maker's job is to take a user request and produce a result.
"""

import json
from datetime import datetime


class Maker:
    """Creates a summary from user input."""

    def __init__(self):
        """Initialize the Maker."""
        self.name = "Maker"

    def create_summary(self, user_request: str, previous_feedback: str = None) -> dict:
        """
        Create a summary from a user request.

        Args:
            user_request: The original user request
            previous_feedback: Optional feedback from checker for improvement

        Returns:
            dict with keys: summary, request, feedback_considered, timestamp
        """
        # If there's previous feedback, enhance the summary
        if previous_feedback:
            enhanced_request = f"{user_request}. (Feedback received: {previous_feedback})"
        else:
            enhanced_request = user_request

        # Simple summary creation logic
        # For "Create a Python calculator", summary = "A Python tool that performs arithmetic operations"
        # For "List features for web scraper", summary might include features

        summary = self._generate_summary(user_request, has_feedback=bool(previous_feedback))

        result = {
            "summary": summary,
            "original_request": user_request,
            "feedback_considered": previous_feedback is not None,
            "timestamp": datetime.now().isoformat(),
        }

        return result

    def _generate_summary(self, user_request: str, has_feedback: bool = False) -> str:
        """
        Generate a summary based on the user request.
        This is intentionally simple for beginners to understand.
        """
        request_lower = user_request.lower()

        # Extract key topic from request
        if "calculator" in request_lower:
            if has_feedback:
                # Improved version based on feedback
                return (
                    "A Python tool that performs basic arithmetic operations including "
                    "addition, subtraction, multiplication, and division with clear input/output."
                )
            else:
                # Initial version (intentionally brief to demonstrate failure)
                return "Python calculator tool"

        elif "scraper" in request_lower:
            if has_feedback:
                # Improved version that passes validation
                return (
                    "A web scraper that extracts and parses data from websites "
                    "with support for multiple formats and storage options."
                )
            else:
                # Initial brief version that fails (no action verb in the list)
                return "Web scraper data tool"

        else:
            # Generic fallback
            if has_feedback:
                return f"An enhanced solution for: {user_request}"
            else:
                return f"A solution for: {user_request}"

    def display_result(self, result: dict) -> str:
        """Display the maker's result in a readable format."""
        output = []
        output.append("=" * 60)
        output.append("MAKER RESULT")
        output.append("=" * 60)
        output.append(f"Original Request: {result['original_request']}")
        output.append(f"Summary Created: {result['summary']}")
        output.append(f"Feedback Considered: {result['feedback_considered']}")
        output.append(f"Timestamp: {result['timestamp']}")
        output.append("=" * 60)
        return "\n".join(output)
