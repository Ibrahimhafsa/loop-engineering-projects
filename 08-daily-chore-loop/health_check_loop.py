#!/usr/bin/env python3
"""
Daily Project Health Check Loop - Loop Engineering Project 8 (Capstone)

Demonstrates all six components of Loop Engineering:
1. HEARTBEAT: Runs daily check cycle
2. WORKTREE/ISOLATION: Each run gets isolated report files
3. SKILL/PROJECT KNOWLEDGE: Analyzes project metrics
4. MAKER-CHECKER: Maker collects health data, Checker validates it
5. CONNECTOR/ACTION: Writes health reports to local files
6. SPINE/PERSISTENT MEMORY: progress.md remembers previous checks
"""

import json
import time
from datetime import datetime
from pathlib import Path


def read_progress() -> dict:
    """Read the spine (persistent memory) from progress.md"""
    progress_file = Path("progress.md")

    if not progress_file.exists():
        return {
            "runs": [],
            "latest_status": "never_run",
            "total_checks": 0
        }

    content = progress_file.read_text()

    if "```json" in content:
        start = content.find("```json") + len("```json")
        end = content.find("```", start)
        json_str = content[start:end].strip()
        return json.loads(json_str)

    return {
        "runs": [],
        "latest_status": "never_run",
        "total_checks": 0
    }


def write_progress(progress: dict) -> None:
    """Write the spine (persistent memory) to progress.md"""
    progress_file = Path("progress.md")

    markdown = f"""# Daily Health Check Loop - Spine (Persistent Memory)

This file is the **spine** - it remembers all health checks across runs.

## Summary
- **Latest Status**: {progress['latest_status']}
- **Total Checks Completed**: {progress['total_checks']}
- **Last Check**: {progress['runs'][-1]['timestamp'] if progress['runs'] else 'Never'}

## All Health Checks (Heartbeat Memory)

```json
{json.dumps(progress, indent=2)}
```

## Check History

"""

    for i, run in enumerate(progress["runs"], 1):
        markdown += f"\n### Check #{i}\n"
        markdown += f"- **Date/Time**: {run['timestamp']}\n"
        markdown += f"- **Health Status**: {run['health_status']}\n"
        markdown += f"- **Files Count**: {run['maker_metrics']['file_count']}\n"
        markdown += f"- **Python Lines**: {run['maker_metrics']['python_lines']}\n"
        markdown += f"- **Overall Score**: {run['health_score']}/100\n"
        markdown += f"- **Checker Verdict**: {run['checker_verdict']}\n"
        if run.get('checker_feedback'):
            markdown += f"- **Checker Feedback**: {run['checker_feedback']}\n"

    progress_file.write_text(markdown)


def maker_collect_metrics(project_dir: str = ".") -> dict:
    """
    MAKER STEP: Collect health metrics from the project.
    This demonstrates SKILL/PROJECT KNOWLEDGE - analyzing a project.
    """
    project_path = Path(project_dir)

    file_count = 0
    python_lines = 0
    python_files = 0

    for file in project_path.rglob("*"):
        if file.is_file():
            file_count += 1
            if file.suffix == ".py":
                python_files += 1
                try:
                    lines = len(file.read_text(errors='ignore').splitlines())
                    python_lines += lines
                except:
                    pass

    metrics = {
        "timestamp": datetime.now().isoformat(),
        "file_count": file_count,
        "python_files": python_files,
        "python_lines": python_lines,
        "has_readme": (project_path / "README.md").exists(),
        "has_progress": (project_path / "progress.md").exists(),
    }

    return metrics


def maker_create_health_report(metrics: dict, previous_feedback: str = None) -> dict:
    """
    MAKER STEP: Create a health report based on metrics.
    If previous_feedback is provided, improve the report.
    """
    report = {
        "timestamp": metrics["timestamp"],
        "metrics": metrics,
        "summary": "",
        "details": [],
    }

    has_readme = metrics["has_readme"]
    has_progress = metrics["has_progress"]
    file_count = metrics["file_count"]
    python_files = metrics["python_files"]

    if previous_feedback:
        report["summary"] = "Improved health report with enhanced metrics and analysis"
        report["details"] = [
            f"Project contains {file_count} files total",
            f"Python files identified: {python_files}",
            f"Total Python lines of code: {metrics['python_lines']}",
            f"Documentation: README.md {'present' if has_readme else 'missing'}",
            f"Memory/Spine: progress.md {'present' if has_progress else 'missing'}",
            "Enhanced analysis with detailed breakdown",
        ]
    else:
        report["summary"] = f"Health check for project with {file_count} files"
        report["details"] = [
            f"Total files in project: {file_count}",
            f"Python files found: {python_files}",
            f"Documentation status: {'Has README' if has_readme else 'No README'}",
            f"Spine/memory status: {'Has progress.md' if has_progress else 'No progress.md'}",
        ]

    return report


def checker_validate_report(report: dict) -> dict:
    """
    CHECKER STEP: Validate the health report against success conditions.
    This demonstrates MAKER-CHECKER pattern.
    """
    verdict = "PASS"
    feedback = []
    failed_conditions = []

    metrics = report["metrics"]
    summary_text = report["summary"]

    conditions_passed = 0
    conditions_total = 0

    conditions_total += 1
    if metrics["file_count"] > 0:
        conditions_passed += 1
    else:
        verdict = "FAIL"
        failed_conditions.append("no_files")
        feedback.append("Project has no files")

    conditions_total += 1
    if len(summary_text) > 15:
        conditions_passed += 1
    else:
        verdict = "FAIL"
        failed_conditions.append("summary_too_short")
        feedback.append("Summary must be descriptive (>15 chars)")

    conditions_total += 1
    if metrics["has_readme"] or metrics["file_count"] < 5:
        conditions_passed += 1
    else:
        feedback.append("Larger projects should have README.md")

    conditions_total += 1
    if metrics["has_progress"] or metrics["python_files"] == 0:
        conditions_passed += 1
    else:
        feedback.append("Consider adding progress.md for tracking")

    health_score = int((conditions_passed / conditions_total) * 100)

    return {
        "verdict": verdict,
        "health_score": health_score,
        "conditions_total": conditions_total,
        "conditions_passed": conditions_passed,
        "failed_conditions": failed_conditions,
        "feedback": " | ".join(feedback) if feedback else "All conditions met",
    }


def connector_write_report(report: dict, checker_result: dict, run_number: int) -> str:
    """
    CONNECTOR/ACTION STEP: Write the health report to a file.
    This demonstrates the CONNECTOR concept - taking action in the external world.
    """
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = Path(f"health_report_run{run_number}_{timestamp_str}.md")

    content = f"""# Daily Project Health Check - Run {run_number}

**Timestamp**: {report['timestamp']}
**Verdict**: {checker_result['verdict']}
**Health Score**: {checker_result['health_score']}/100

## Health Summary
{report['summary']}

## Metrics Collected (Skill/Project Knowledge)
- **Total Files**: {report['metrics']['file_count']}
- **Python Files**: {report['metrics']['python_files']}
- **Python Lines of Code**: {report['metrics']['python_lines']}
- **Has README.md**: {report['metrics']['has_readme']}
- **Has progress.md (Spine)**: {report['metrics']['has_progress']}

## Detailed Findings
"""

    for detail in report["details"]:
        content += f"\n- {detail}"

    content += f"\n\n## Checker Validation\n"
    content += f"- **Conditions Passed**: {checker_result['conditions_passed']}/{checker_result['conditions_total']}\n"
    content += f"- **Verdict**: {checker_result['verdict']}\n"
    content += f"- **Feedback**: {checker_result['feedback']}\n"

    content += f"\n## Loop Engineering Components Demonstrated\n"
    content += f"1. **Heartbeat**: Daily check cycle (run #{run_number})\n"
    content += f"2. **Worktree/Isolation**: Isolated report file created\n"
    content += f"3. **Skill/Project Knowledge**: Analyzed {report['metrics']['file_count']} files\n"
    content += f"4. **Maker-Checker**: Maker collected metrics, Checker validated (verdict: {checker_result['verdict']})\n"
    content += f"5. **Connector/Action**: Report saved to {report_file}\n"
    content += f"6. **Spine/Memory**: Progress tracked in progress.md\n"

    report_file.write_text(content)
    return str(report_file)


def run_daily_health_check(project_dir: str = ".", max_attempts: int = 2) -> None:
    """
    Run the Daily Project Health Check Loop.

    Demonstrates all six Loop Engineering components:
    1. HEARTBEAT: Regular check cycle
    2. WORKTREE/ISOLATION: Isolated report files per run
    3. SKILL/PROJECT KNOWLEDGE: Analyzes project metrics
    4. MAKER-CHECKER: Maker→Checker→Feedback loop
    5. CONNECTOR/ACTION: Writes health reports to files
    6. SPINE/PERSISTENT MEMORY: progress.md remembers checks
    """

    print("\n" + "="*70)
    print("DAILY PROJECT HEALTH CHECK LOOP - Loop Engineering Project 8")
    print("="*70)
    print("\nDemonstrating all 6 Loop Engineering components:")
    print("  1. [HEARTBEAT] Daily check cycle")
    print("  2. [WORKTREE/ISOLATION] Isolated report files")
    print("  3. [SKILL/PROJECT KNOWLEDGE] Analyzing project")
    print("  4. [MAKER-CHECKER] Dual-step validation")
    print("  5. [CONNECTOR/ACTION] Writing report files")
    print("  6. [SPINE/PERSISTENT MEMORY] Tracking in progress.md")
    print()

    progress = read_progress()
    run_number = progress["total_checks"] + 1

    print(f"[HEARTBEAT] Daily check cycle #{run_number}")
    print(f"[SPINE] Reading persistent memory... {len(progress['runs'])} previous checks")
    print()

    attempt = 1
    checker_result = None
    report = None
    success = False

    while attempt <= max_attempts:
        print(f"[BEAT {attempt}] Starting health check cycle")
        print()

        print(f"  [MAKER] Collecting project metrics...")
        metrics = maker_collect_metrics(project_dir)
        print(f"    - Files found: {metrics['file_count']}")
        print(f"    - Python files: {metrics['python_files']}")
        print(f"    - Python lines: {metrics['python_lines']}")
        print()

        previous_feedback = None
        if attempt > 1 and checker_result:
            previous_feedback = checker_result["feedback"]
            print(f"  [MAKER] Creating improved report based on feedback:")
            print(f"    - {previous_feedback}")
            print()

        print(f"  [MAKER] Creating health report...")
        report = maker_create_health_report(metrics, previous_feedback)
        print(f"    - Summary: {report['summary']}")
        print(f"    - Details collected: {len(report['details'])}")
        print()

        print(f"  [CHECKER] Validating report...")
        checker_result = checker_validate_report(report)
        print(f"    - Health Score: {checker_result['health_score']}/100")
        print(f"    - Verdict: {checker_result['verdict']}")
        print(f"    - Conditions: {checker_result['conditions_passed']}/{checker_result['conditions_total']}")
        if checker_result["feedback"]:
            print(f"    - Feedback: {checker_result['feedback']}")
        print()

        if checker_result["verdict"] == "PASS":
            success = True
            print(f"  [SUCCESS] Checker approved the health report!")
            break
        else:
            print(f"  [FAIL] Checker rejected report, attempting improvement...")
            if attempt < max_attempts:
                print(f"    Attempt {attempt + 1} will use feedback to improve")
            print()

        attempt += 1

    print(f"\n[CONNECTOR/ACTION] Writing health report to file...")
    report_file = connector_write_report(report, checker_result, run_number)
    print(f"  Report saved: {report_file}")
    print()

    run_record = {
        "run_number": run_number,
        "timestamp": datetime.now().isoformat(),
        "health_status": checker_result["verdict"],
        "health_score": checker_result["health_score"],
        "maker_metrics": {
            "file_count": metrics["file_count"],
            "python_files": metrics["python_files"],
            "python_lines": metrics["python_lines"],
            "has_readme": metrics["has_readme"],
            "has_progress": metrics["has_progress"],
        },
        "checker_verdict": checker_result["verdict"],
        "checker_feedback": checker_result["feedback"],
        "attempts": attempt,
        "report_file": report_file,
    }

    progress["runs"].append(run_record)
    progress["total_checks"] = len(progress["runs"])
    progress["latest_status"] = checker_result["verdict"]

    print(f"[SPINE] Updating persistent memory in progress.md...")
    write_progress(progress)
    print(f"  Progress saved - Total checks: {progress['total_checks']}")
    print()

    print("="*70)
    print("DAILY HEALTH CHECK COMPLETE")
    print("="*70)
    print(f"Status: {checker_result['verdict']}")
    print(f"Health Score: {checker_result['health_score']}/100")
    print(f"Project Files Analyzed: {metrics['file_count']}")
    print(f"Attempts Used: {attempt}/{max_attempts}")
    print(f"Report File: {report_file}")
    print(f"Spine Location: progress.md")
    print(f"Total Checks in Memory: {progress['total_checks']}")
    print("="*70 + "\n")


if __name__ == "__main__":
    import sys

    project_dir = sys.argv[1] if len(sys.argv) > 1 else "."

    run_daily_health_check(project_dir=project_dir, max_attempts=2)
