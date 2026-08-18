#!/usr/bin/env python3
"""
Project 10: The Secrets Drill
Demonstrates safe handling of secrets using environment variables.
"""

import os
import sys


def main():
    """
    Routine that attempts to obtain a secret from environment variables.

    IMPORTANT: This routine is instructed to:
    - Look for DEMO_TOKEN in environment variables only
    - Do NOT attempt to load from .env file
    - Never print the actual token value
    """

    print("=" * 60)
    print("SECRETS DRILL - Attempting to obtain secret")
    print("=" * 60)

    # Check if DEMO_TOKEN is available in environment variables
    demo_token = os.environ.get("DEMO_TOKEN")

    if demo_token:
        print("\n[SUCCESS] Secret found successfully from environment variable.")
        print(f"  Token length: {len(demo_token)} characters")
        print(f"  Token starts with: {demo_token[:4]}...")
        print("\nThe secret is now available for use in your application.")
        return True
    else:
        print("\n[FAILED] Secret 'DEMO_TOKEN' not found in environment variables.")
        print("\nPossible reasons:")
        print("  1. DEMO_TOKEN is not set in the execution environment")
        print("  2. This is a fresh/cloud environment without pre-loaded secrets")
        print("  3. The .env file is gitignored and not available here")
        print("\nSolution:")
        print("  Set DEMO_TOKEN as an environment variable before running this routine.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
