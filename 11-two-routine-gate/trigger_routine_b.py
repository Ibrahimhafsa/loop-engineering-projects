#!/usr/bin/env python3
"""
Helper script to trigger Routine B after approval.
Reads the bearer token from .routine_b_token and sends the trigger request.
"""
import urllib.request
import json
from pathlib import Path
import sys


def read_token():
    """Read bearer token from .routine_b_token file."""
    token_file = ".routine_b_token"
    if not Path(token_file).exists():
        print(f"❌ Token file not found: {token_file}")
        print("Please start Routine B first to generate the token.")
        return None

    with open(token_file, "r") as f:
        token = f.read().strip()

    if not token:
        print("❌ Token file is empty")
        return None

    return token


def trigger_routine_b(token):
    """Send trigger request to Routine B."""
    url = "http://localhost:9999/trigger"

    print("\n" + "="*60)
    print("TRIGGERING ROUTINE B")
    print("="*60 + "\n")

    print(f"Target: {url}")
    print(f"Token: {token[:20]}... (truncated for safety)")
    print("\nSending POST request...")

    try:
        # Create request
        request = urllib.request.Request(
            url,
            method="POST",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        # Send request
        with urllib.request.urlopen(request, timeout=5) as response:
            data = response.read().decode()
            result = json.loads(data)

            print("\n✓ Response received (Status: 200)\n")
            print("Response:")
            print(json.dumps(result, indent=2))

            if result.get("success") or result.get("status") == "success":
                print("\n✓ ROUTINE B EXECUTED SUCCESSFULLY!")
                print(f"✓ Result file: {result.get('result_file', 'unknown')}")
            else:
                print("\n⚠️  Unexpected response")

    except urllib.error.HTTPError as e:
        error_data = e.read().decode()
        try:
            error_json = json.loads(error_data)
            error_msg = error_json.get("error", error_data)
        except:
            error_msg = error_data

        print(f"\n❌ Error (Status: {e.code})")
        print(f"Message: {error_msg}")

        if e.code == 401:
            print("\n⚠️  UNAUTHORIZED: Missing or invalid bearer token")
        elif e.code == 403:
            print("\n⚠️  FORBIDDEN: Either invalid token or draft not approved")
            print("Check that:")
            print("1. Draft from Routine A has been created")
            print("2. Draft has been approved using approve_draft.py")
        elif e.code == 404:
            print("\n❌ Server not found. Is Routine B running?")
            print("Start Routine B: python routine_b.py")

    except urllib.error.URLError as e:
        print(f"\n❌ Connection error: {e}")
        print("Is Routine B running on http://localhost:9999 ?")
        print("Start Routine B: python routine_b.py")

    except Exception as e:
        print(f"\n❌ Error: {e}")

    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    token = read_token()
    if token:
        trigger_routine_b(token)
    else:
        sys.exit(1)
