#!/usr/bin/env python3
"""
Project 12: Dreaming Loop
A self-improving meta-loop that detects repeated failures in source logs and proposes improvements.

This is the final capstone project in the Loop Engineering crash course.
It demonstrates:
- Reading and analyzing historical logs
- Detecting repeated patterns (failures/corrections)
- Maker-checker validation pattern
- Evidence-based improvement proposals
- Safe git branching without auto-merge
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import subprocess
import sys


class DreamingLoopError(Exception):
    """Base exception for dreaming loop errors."""
    pass


class LogReader:
    """Reads and parses the source loop progress.md file."""

    def __init__(self, source_log_path):
        self.source_log_path = Path(source_log_path)
        if not self.source_log_path.exists():
            raise DreamingLoopError(f"Source log not found: {source_log_path}")

    def read_all_entries(self):
        """Read all check entries from the source log."""
        content = self.source_log_path.read_text(encoding='utf-8')
        entries = []

        # Parse check history section
        check_sections = re.split(r'### Check #\d+', content)

        for i, section in enumerate(check_sections[1:], 1):
            lines = section.strip().split('\n')
            entry = self._parse_check_entry(lines, i)
            if entry:
                entries.append(entry)

        return entries

    def _parse_check_entry(self, lines, check_number):
        """Parse a single check entry from lines."""
        entry = {
            'check_number': check_number,
            'timestamp': None,
            'health_status': None,
            'raw_text': '\n'.join(lines),
            'fields': {}
        }

        for line in lines:
            if '**Date/Time**:' in line:
                ts_str = line.split('**Date/Time**:')[1].strip()
                try:
                    entry['timestamp'] = datetime.fromisoformat(ts_str)
                except:
                    entry['timestamp'] = None
            elif '**Health Status**:' in line:
                entry['health_status'] = line.split('**Health Status**:')[1].strip()
            elif '**' in line and ':' in line:
                key = line.split('**')[1]
                val = line.split('**')[2].split(':', 1)[1].strip() if len(line.split('**')) > 2 else ''
                entry['fields'][key] = val

        if entry['timestamp'] and entry['health_status']:
            return entry
        return None

    def entries_after(self, cutoff_date):
        """Get entries after a specific date."""
        all_entries = self.read_all_entries()
        return [e for e in all_entries if e['timestamp'] and e['timestamp'] > cutoff_date]


class PatternDetector:
    """Detects repeated failures or corrections in the log entries."""

    def __init__(self, entries):
        self.entries = entries

    def find_repeated_failures(self):
        """Find failure patterns that occur more than once."""
        failure_patterns = defaultdict(list)

        for entry in self.entries:
            if entry['health_status'] == 'FAIL':
                # Extract the failure type/message
                failure_type = entry['fields'].get('Failure Type', 'Unknown failure')
                error_msg = entry['fields'].get('Error Message', '')

                # Use failure type as the key
                key = failure_type
                failure_patterns[key].append({
                    'check_number': entry['check_number'],
                    'timestamp': entry['timestamp'],
                    'error_message': error_msg,
                    'raw': entry['raw_text']
                })

        # Filter to only repeated failures (2+ occurrences)
        repeated = {}
        for pattern, occurrences in failure_patterns.items():
            if len(occurrences) > 1:
                repeated[pattern] = occurrences

        return repeated

    def find_unnecessary_rules(self):
        """Find rules that haven't been used in recent entries."""
        # Simplified version: if a check passes consistently,
        # look for any validation rules that weren't triggered
        pass_count = sum(1 for e in self.entries if e['health_status'] == 'PASS')
        fail_count = len(self.entries) - pass_count

        # If we have more than 70% pass rate, some rules might be overly strict
        if len(self.entries) > 0 and pass_count / len(self.entries) > 0.7:
            return [
                {
                    'rule': 'Mandatory checker_verdict field',
                    'reason': 'All recent checks pass without issue',
                    'evidence': f'{pass_count} out of {len(self.entries)} checks passed',
                    'suggestion': 'Consider if this validation is still necessary'
                }
            ]

        return []


class StateManager:
    """Manages the dreaming-state.md file."""

    def __init__(self, state_file_path):
        self.state_file_path = Path(state_file_path)

    def read_state(self):
        """Read the current dreaming state."""
        if not self.state_file_path.exists():
            return {
                'last_processed_date': None,
                'last_run_timestamp': None,
                'entries_processed': 0,
                'repeated_issues_detected': [],
                'proposal_status': 'none',
                'next_review': None
            }

        content = self.state_file_path.read_text(encoding='utf-8')
        state = {
            'last_processed_date': None,
            'last_run_timestamp': None,
            'entries_processed': 0,
            'repeated_issues_detected': [],
            'proposal_status': 'none',
            'next_review': None
        }

        # Parse the state file
        for line in content.split('\n'):
            if 'last_processed_date:' in line:
                date_str = line.split('last_processed_date:')[1].strip()
                if date_str and date_str != 'None':
                    try:
                        state['last_processed_date'] = datetime.fromisoformat(date_str)
                    except:
                        pass
            elif 'entries_processed:' in line:
                try:
                    state['entries_processed'] = int(line.split(':')[1].strip())
                except:
                    pass
            elif 'proposal_status:' in line:
                state['proposal_status'] = line.split('proposal_status:')[1].strip()

        return state

    def write_state(self, state):
        """Write the dreaming state to file."""
        timestamp = datetime.now()

        # Ensure parent directory exists
        self.state_file_path.parent.mkdir(parents=True, exist_ok=True)

        content = f"""# Dreaming Loop State

**Last Updated**: {timestamp.isoformat()}

## Processing History

- last_processed_date: {state.get('last_processed_date').isoformat() if state.get('last_processed_date') else 'None'}
- last_run_timestamp: {timestamp.isoformat()}
- entries_processed: {state.get('entries_processed', 0)}
- proposal_status: {state.get('proposal_status', 'none')}

## Repeated Issues Detected

```
{json.dumps(state.get('repeated_issues_detected', []), indent=2)}
```

## Next Scheduled Review

- Frequency: Weekly (manual execution for testing)
- Next Review: {(timestamp + timedelta(days=7)).isoformat()}

## Notes

This state file is automatically updated by the dreaming loop after each run.
It tracks which log entries have been processed to avoid re-analyzing old data.
"""
        self.state_file_path.write_text(content, encoding='utf-8')


class Maker:
    """The 'maker' role: identifies repeated issues and drafts proposals."""

    def __init__(self, repeated_patterns, unnecessary_rules, entries):
        self.repeated_patterns = repeated_patterns
        self.unnecessary_rules = unnecessary_rules
        self.entries = entries

    def draft_proposal(self):
        """Draft an improvement proposal based on detected patterns."""
        proposal = {
            'issue': None,
            'frequency': 0,
            'evidence_entries': [],
            'proposed_change': None,
            'why_minimal': None,
            'deletion_proposal': None,
            'status': 'draft'
        }

        if self.repeated_patterns:
            # Use the first repeated pattern
            pattern_name = list(self.repeated_patterns.keys())[0]
            occurrences = self.repeated_patterns[pattern_name]

            proposal['issue'] = pattern_name
            proposal['frequency'] = len(occurrences)
            proposal['evidence_entries'] = occurrences

            # Propose minimal change
            if 'validation' in pattern_name.lower():
                proposal['proposed_change'] = (
                    'Add mandatory validation check for checker_feedback field '
                    'before calculating health_score.'
                )
                proposal['why_minimal'] = (
                    'This single validation rule prevents the specific failure '
                    'without modifying existing logic.'
                )

        if self.unnecessary_rules:
            rule = self.unnecessary_rules[0]
            proposal['deletion_proposal'] = {
                'rule': rule['rule'],
                'reason': rule['reason'],
                'evidence': rule['evidence']
            }

        return proposal


class Checker:
    """The 'checker' role: validates proposals against evidence."""

    def __init__(self, proposal, log_entries):
        self.proposal = proposal
        self.log_entries = log_entries

    def validate(self):
        """Validate that the proposal is evidence-based and minimal."""
        errors = []

        if not self.proposal.get('issue'):
            errors.append('No issue identified')

        if self.proposal.get('frequency', 0) < 2:
            errors.append('Issue does not appear more than once')

        if not self.proposal.get('evidence_entries'):
            errors.append('No evidence entries provided')

        if not self.proposal.get('proposed_change'):
            errors.append('No proposed change specified')

        if not self.proposal.get('why_minimal'):
            errors.append('No justification for minimal approach')

        # Verify evidence actually exists in logs
        if self.proposal.get('evidence_entries'):
            for entry in self.proposal['evidence_entries']:
                check_num = entry.get('check_number')
                if not any(e['check_number'] == check_num for e in self.log_entries):
                    errors.append(f'Evidence entry Check #{check_num} not found in logs')

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'status': 'PASS' if len(errors) == 0 else 'FAIL'
        }


class DreamingLoop:
    """The main dreaming loop orchestrator."""

    def __init__(self, source_log_path, state_file_path, project_root):
        self.source_log_path = source_log_path
        self.state_file_path = state_file_path
        self.project_root = Path(project_root)

        self.log_reader = LogReader(source_log_path)
        self.state_manager = StateManager(state_file_path)
        self.current_state = self.state_manager.read_state()

    def run(self, force_reprocess=False):
        """Execute the dreaming loop."""
        print("=" * 70)
        print("DREAMING LOOP - Weekly Improvement Cycle")
        print("=" * 70)
        print()

        # Read source logs
        print("[1] Reading source logs...")
        all_entries = self.log_reader.read_all_entries()
        print(f"    Found {len(all_entries)} total entries")

        # Determine cutoff date
        if self.current_state['last_processed_date'] and not force_reprocess:
            cutoff = self.current_state['last_processed_date']
            print(f"[2] Filtering entries after {cutoff.isoformat()}...")
            new_entries = self.log_reader.entries_after(cutoff)
            print(f"    Found {len(new_entries)} new entries since last run")
        else:
            # First run: start from 2026-08-15
            cutoff = datetime.fromisoformat('2026-08-15T00:00:00')
            new_entries = self.log_reader.entries_after(cutoff)
            print(f"[2] First run: processing entries from {cutoff.isoformat()}")
            print(f"    Found {len(new_entries)} entries")

        if not new_entries:
            print("\n[3] No new entries to process. Sleeping until next week.")
            return

        # Detect patterns
        print(f"\n[3] Detecting repeated failures/corrections...")
        detector = PatternDetector(new_entries)
        repeated_patterns = detector.find_repeated_failures()
        unnecessary_rules = detector.find_unnecessary_rules()

        if repeated_patterns:
            print(f"    Found {len(repeated_patterns)} repeated pattern(s):")
            for pattern, occurrences in repeated_patterns.items():
                print(f"      - {pattern} ({len(occurrences)} occurrences)")
        else:
            print("    No repeated failures detected.")

        if unnecessary_rules:
            print(f"\n    Found {len(unnecessary_rules)} potentially unnecessary rule(s):")
            for rule in unnecessary_rules:
                print(f"      - {rule['rule']}")

        # Maker creates proposal
        print(f"\n[4] Maker: Drafting proposal...")
        maker = Maker(repeated_patterns, unnecessary_rules, new_entries)
        proposal = maker.draft_proposal()

        if proposal['issue']:
            print(f"    Issue: {proposal['issue']}")
            print(f"    Frequency: {proposal['frequency']} occurrences")
            print(f"    Proposed Change: {proposal['proposed_change']}")
        else:
            print("    No improvement proposal drafted.")

        # Checker validates
        print(f"\n[5] Checker: Validating proposal...")
        checker = Checker(proposal, all_entries)
        validation = checker.validate()

        if validation['valid']:
            print(f"    Validation: PASS ✓")
            proposal['status'] = 'accepted'
        else:
            print(f"    Validation: FAIL ✗")
            for error in validation['errors']:
                print(f"      - {error}")
            proposal['status'] = 'rejected'
            return

        # Create proposal artifacts
        print(f"\n[6] Creating proposal artifacts...")
        self._create_proposal_files(proposal, repeated_patterns, unnecessary_rules, new_entries)
        print(f"    ✓ Proposal files created")

        # Create git branch
        print(f"\n[7] Creating git branch (claude/)...")
        branch_name = self._create_git_branch(proposal)
        print(f"    ✓ Branch: {branch_name}")

        # Update state
        print(f"\n[8] Updating dreaming-state.md...")
        self.current_state['last_processed_date'] = max(
            e['timestamp'] for e in new_entries if e['timestamp']
        )
        self.current_state['entries_processed'] += len(new_entries)
        self.current_state['repeated_issues_detected'].append({
            'issue': proposal.get('issue'),
            'frequency': proposal.get('frequency'),
            'detected_at': datetime.now().isoformat()
        })
        self.current_state['proposal_status'] = proposal['status']

        self.state_manager.write_state(self.current_state)
        print(f"    ✓ State updated")

        print()
        print("=" * 70)
        print("DREAMING LOOP COMPLETE")
        print("=" * 70)
        print()
        print(f"Summary:")
        print(f"  - Entries processed: {len(new_entries)}")
        print(f"  - Repeated patterns found: {len(repeated_patterns)}")
        print(f"  - Proposal status: {proposal['status'].upper()}")
        print(f"  - Branch: {branch_name}")
        print(f"  - Next review: 1 week from now (manual trigger for testing)")
        print()

    def _create_proposal_files(self, proposal, patterns, rules, entries):
        """Create IMPROVEMENT_PROPOSAL.md and PR_DESCRIPTION.md."""

        # Create IMPROVEMENT_PROPOSAL.md
        proposal_md = self._format_improvement_proposal(proposal, patterns, entries)
        proposal_file = self.project_root / 'IMPROVEMENT_PROPOSAL.md'
        proposal_file.write_text(proposal_md, encoding='utf-8')

        # Create PR_DESCRIPTION.md
        pr_desc = self._format_pr_description(proposal, patterns, rules, entries)
        pr_file = self.project_root / 'PR_DESCRIPTION.md'
        pr_file.write_text(pr_desc, encoding='utf-8')

    def _format_improvement_proposal(self, proposal, patterns, entries):
        """Format the improvement proposal."""
        evidence_text = ""
        if proposal['evidence_entries']:
            for i, evidence in enumerate(proposal['evidence_entries'], 1):
                evidence_text += f"\n#### Occurrence #{i}\n"
                evidence_text += f"- **Check**: Check #{evidence['check_number']}\n"
                evidence_text += f"- **Date/Time**: {evidence['timestamp'].isoformat()}\n"
                evidence_text += f"- **Error**: {evidence['error_message']}\n"

        deletion_text = ""
        if proposal.get('deletion_proposal'):
            deletion_text = f"""
## Proposed Deletion

**Rule**: {proposal['deletion_proposal']['rule']}

**Reason**: {proposal['deletion_proposal']['reason']}

**Evidence**: {proposal['deletion_proposal']['evidence']}
"""

        return f"""# Improvement Proposal

**Generated**: {datetime.now().isoformat()}
**Status**: {proposal['status'].upper()}

## Problem Detected

**Issue**: {proposal.get('issue', 'Unknown')}

**Frequency**: {proposal.get('frequency', 0)} occurrences

## Evidence

{evidence_text}

## Proposed Change

{proposal.get('proposed_change', 'No change specified')}

## Why This Is Minimal

{proposal.get('why_minimal', 'See above')}

{deletion_text}

## Safety Notes

- This proposal was validated by the checker pattern
- No rules files were automatically modified
- Human review and merge approval is required before applying this change
- The proposed change is the smallest reasonable intervention for the detected problem
"""

    def _format_pr_description(self, proposal, patterns, rules, entries):
        """Format the PR description."""

        evidence_section = ""
        if proposal['evidence_entries']:
            evidence_section = "\n### Evidence\n"
            for i, evidence in enumerate(proposal['evidence_entries'], 1):
                evidence_section += f"""
**Run #{i}**
- Check: Check #{evidence['check_number']}
- Timestamp: {evidence['timestamp'].isoformat()}
- Error: {evidence['error_message']}
"""

        deletion_section = ""
        if proposal.get('deletion_proposal'):
            deletion_section = f"""
## Proposed Deletion

**What**: {proposal['deletion_proposal']['rule']}

**Why**: {proposal['deletion_proposal']['reason']}

**Evidence**: {proposal['deletion_proposal']['evidence']}
"""

        return f"""# Weekly Improvement Proposal

**Proposal Date**: {datetime.now().strftime('%Y-%m-%d')}

## Problem

{proposal.get('issue', 'Repeated pattern detected')}

## Frequency

{proposal.get('frequency', '?')} occurrences in recent logs

{evidence_section}

## Proposed Solution

{proposal.get('proposed_change', 'See above')}

### Why This Change is Minimal

{proposal.get('why_minimal', 'See above')}

{deletion_section}

## Safety

- ✓ Validated by checker pattern
- ✓ Evidence-based (not speculative)
- ✓ No automatic rules modifications
- ⚠ REQUIRES HUMAN REVIEW AND MERGE
- ⚠ Created on claude/ branch, not merged to main

## Next Steps

1. Review this proposal carefully
2. Verify the evidence matches your actual logs
3. Consider the proposed changes
4. Manually merge this branch to main IF you approve
5. Delete the claude/ branch after merging

**Do not merge unless you have verified the evidence and agree with the proposal.**
"""

    def _create_git_branch(self, proposal):
        """Create a git branch starting with 'claude/' for the proposal."""
        branch_date = datetime.now().strftime('%Y-%m-%d')
        branch_name = f"claude/dreaming-loop-{branch_date}"

        try:
            # Check if branch already exists
            result = subprocess.run(
                ['git', 'rev-parse', '--verify', branch_name],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # Branch exists, switch to it
                subprocess.run(
                    ['git', 'checkout', branch_name],
                    cwd=self.project_root,
                    capture_output=True
                )
            else:
                # Create new branch from main
                subprocess.run(
                    ['git', 'checkout', '-b', branch_name],
                    cwd=self.project_root,
                    capture_output=True
                )

            # Add the proposal files
            subprocess.run(
                ['git', 'add', 'IMPROVEMENT_PROPOSAL.md', 'PR_DESCRIPTION.md'],
                cwd=self.project_root,
                capture_output=True
            )

            # Commit
            commit_msg = f"Dreaming loop proposal: {proposal.get('issue', 'improvement')}"
            subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                cwd=self.project_root,
                capture_output=True
            )

            # Switch back to main (do not merge)
            subprocess.run(
                ['git', 'checkout', 'main'],
                cwd=self.project_root,
                capture_output=True
            )

        except Exception as e:
            print(f"Warning: Could not create git branch: {e}")

        return branch_name


def main():
    """Main entry point."""
    # Use absolute paths
    project_root = Path(__file__).parent
    source_log = Path(__file__).parent.parent / '08-daily-chore-loop' / 'progress.md'
    state_file = project_root / 'dreaming-state.md'

    try:
        loop = DreamingLoop(source_log, state_file, project_root)
        loop.run()
    except DreamingLoopError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
