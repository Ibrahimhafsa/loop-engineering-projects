#!/usr/bin/env python3
"""
Routine: Commit Summary Generator
A simple routine that summarizes recent git commits into a file.
This routine is designed for rehearsal and testing with one-off runs.
"""

import subprocess
import os
from datetime import datetime

def get_git_commits(count=10):
    """Fetch recent git commits."""
    try:
        result = subprocess.run(
            ["git", "log", f"-{count}", "--oneline"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise Exception(f"Git error: {result.stderr}")
    except Exception as e:
        raise Exception(f"Failed to get commits: {e}")

def generate_summary():
    """Generate and save a summary of recent commits."""
    print("[ROUTINE] Starting commit summary generation...")

    commits = get_git_commits(10)

    summary_content = f"""# Commit Summary
Generated at: {datetime.now().isoformat()}

## Recent Commits (Last 10)

```
{commits}
```

## Routine Status
[OK] Successfully generated commit summary
[OK] Total commits captured: {len(commits.split(chr(10)))}
"""

    output_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "summary.md"
    )

    with open(output_file, "w") as f:
        f.write(summary_content)

    print(f"[ROUTINE] Summary saved to: {output_file}")
    print("[ROUTINE] Routine completed successfully")

if __name__ == "__main__":
    try:
        generate_summary()
        print("\n[SUCCESS] Routine execution completed successfully")
    except Exception as e:
        print(f"\n[ERROR] Routine failed: {e}")
        exit(1)
