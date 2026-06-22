"""
Community Resource Navigator
------------------------------
Paste this file into your GitHub repo and run it with:

    python community_resource_navigator.py

Requirements:
    pip install anthropic

You'll need an Anthropic API key. Get one at https://console.anthropic.com
Set it as an environment variable before running:

    On Mac/Linux:  export ANTHROPIC_API_KEY="sk-ant-..."
    On Windows:    set ANTHROPIC_API_KEY=sk-ant-...

Or the script will prompt you to enter it manually.

IMPORTANT: This tool does not replace a caseworker, therapist,
attorney, or emergency service.
"""

import os
import sys
import json

try:
    import anthropic
except ImportError:
    print("The 'anthropic' package is not installed.")
    print("Run: pip install anthropic")
    sys.exit(1)


# ---------------------------------------------------------
# CRISIS KEYWORDS
# If any appear in the situation text, crisis resources are
# shown FIRST before any other output.
# ---------------------------------------------------------
CRISIS_KEYWORDS = [
    "kill myself", "suicide", "hurt myself", "self harm", "self-harm",
    "abuse", "hitting me", "hit me", "afraid for my safety", "unsafe",
    "emergency", "no place to stay tonight", "homeless tonight",
    "nowhere to sleep tonight", "domestic violence", "threatened",
]

# ---------------------------------------------------------
# STAFF ROLES
# Shown in the menu; passed to the AI for context.
# ---------------------------------------------------------
STAFF_ROLES = {
    "1": "caseworker",
    "2": "intake worker",
    "3": "volunteer",
    "4": "supervisor",
}

# ---------------------------------------------------------
# RESOURCE CATEGORIES
# Used only to display the urgency color in the terminal.
# The AI determines the actual category from the situation.
# ---------------------------------------------------------
URGENCY_LABELS = {
    "High":   "(!!) HIGH",
    "Medium": "( ! ) MEDIUM",
    "Low":    "(  ) LOW",
}


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def divider(char="=", width=60):
    print(char * width)

def section(title):
    print()
    print(title)
    print("-" * len(title))

def print_list(items, prefix="  - "):
    for item in items:
        print(f"{prefix}{item}")

def check_for_crisis(text):
    """Returns True if any crisis keyword is found in the text."""
    lower = text.lower()
    return any(keyword in lower for keyword in CRISIS_KEYWORDS)

def show_crisis_message():
    """Prints crisis/emergency resources prominently."""
    print()
    divider("!")
    print("!! POTENTIAL CRISIS DETECTED")
    divider("!")
    print("  If someone is in immediate danger:  call 911")
    print("  Mental health crisis (24/7):         call or text 988")
    print("  Crisis Text Line:                    text HOME to 741741")
    print("  This program is NOT a substitute for emergency services.")
    divider("!")
    print()

def get_api_key():
    """Gets the API key from the environment or prompts the user."""
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if key:
        return key
    print("\nNo ANTHROPIC_API_KEY environment variable found.")
    key = input("Enter your Anthropic API key: ").strip()
    if not key:
        print("No API key provided. Exiting.")
        sys.exit(1)
    return key

def choose_role():
    """Lets the user pick their staff role."""
    print("\nSelect your staff role:")
    for num, role in STAFF_ROLES.items():
        print(f"  {num}. {role.title()}")
    choice = input("Enter number (or press Enter for caseworker): ").strip()
    return STAFF_ROLES.get(choice, "caseworker")


# ---------------------------------------------------------
# AI ANALYSIS
# Sends the situation to Claude and returns structured JSON.
# ---------------------------------------------------------

SYSTEM_PROMPT_TEMPLATE = """You are a community resource navigator assistant helping a {role} at a social services agency.
Analyze the described client situation and respond ONLY with a valid JSON object (no markdown, no backticks, no extra text).

Return this exact structure:
{{
  "primary_category": "<one of: Housing / Rent Assistance, Employment / Income Support, Food Assistance, Utility Assistance, Healthcare Needs, Mental Health Support, Legal Aid, Multiple Needs, Unclear>",
  "urgency": "<one of: High, Medium, Low>",
  "urgency_reason": "<1 sentence explaining the urgency level>",
  "identified_needs": [
    {{"name": "<need name>", "description": "<max 10 words>"}}
  ],
  "follow_up_questions": [
    "<specific, practical question tailored to this exact situation>"
  ],
  "next_steps": [
    "<concrete, actionable step ordered by priority>"
  ],
  "staff_summary": "<2-3 sentence professional summary for case notes, written in third person>",
  "referral_note": "<1 sentence about any important referral or coordination needed>"
}}

Include 2-4 identified_needs, 4-6 follow_up_questions, and 4-6 next_steps."""


def analyze_situation(client, situation, role):
    """Calls the Anthropic API and returns a parsed result dict."""
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(role=role)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": f'Client situation: "{situation}"'}
        ]
    )

    raw = message.content[0].text.strip()
    # Strip accidental markdown fences just in case
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

def display_results(result, situation, role):
    """Prints all sections of the analysis to the terminal."""

    divider()
    print(f"RESOURCE CATEGORY:  {result['primary_category']}")
    urgency_label = URGENCY_LABELS.get(result['urgency'], result['urgency'])
    print(f"URGENCY:            {urgency_label}")
    print(f"REASON:             {result['urgency_reason']}")
    divider()

    section("IDENTIFIED NEEDS")
    for need in result.get("identified_needs", []):
        print(f"  • {need['name']}: {need['description']}")

    section("FOLLOW-UP QUESTIONS TO ASK")
    print_list(result.get("follow_up_questions", []))

    section("SUGGESTED NEXT STEPS")
    for i, step in enumerate(result.get("next_steps", []), 1):
        print(f"  {i}. {step}")

    section("STAFF SUMMARY  (for case notes)")
    print(f"  {result.get('staff_summary', '')}")
    referral = result.get("referral_note", "")
    if referral:
        print()
        print(f"  Referral note: {referral}")

    divider()
    print(f"  Client situation: \"{situation}\"")
    print(f"  Staff role:       {role.title()}")
    divider()
    print()


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():
    divider()
    print("  COMMUNITY RESOURCE NAVIGATOR")
    divider()
    print("  This tool helps staff get a starting point.")
    print("  It does NOT replace a caseworker, therapist,")
    print("  attorney, or emergency service.")
    divider()

    api_key = get_api_key()
    client = anthropic.Anthropic(api_key=api_key)
    role = choose_role()

    while True:
        print()
        situation = input("Describe the client's situation (or 'quit' to exit):\n> ").strip()

        if situation.lower() in ("quit", "exit", "q"):
            print("\nGoodbye.\n")
            break

        if not situation:
            print("Please enter a description.")
            continue

        # Always check for crisis keywords first
        if check_for_crisis(situation):
            show_crisis_message()

        print("\nAnalyzing situation...\n")

        try:
            result = analyze_situation(client, situation, role)
            display_results(result, situation, role)
        except json.JSONDecodeError:
            print("Error: Could not parse the AI response. Please try again.")
        except anthropic.APIConnectionError:
            print("Error: Could not connect to the Anthropic API.")
            print("Check your internet connection and try again.")
        except anthropic.AuthenticationError:
            print("Error: Invalid API key. Check your ANTHROPIC_API_KEY and try again.")
        except anthropic.RateLimitError:
            print("Error: Rate limit reached. Wait a moment and try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")

        again = input("Analyze another situation? (y/n): ").strip().lower()
        if again != "y":
            print("\nGoodbye.\n")
            break


if __name__ == "__main__":
    main()
