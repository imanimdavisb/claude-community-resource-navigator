"""
Community Resource Navigator
------------------------------
Run this file with:

    python community_resource_navigator.py

This version does NOT require an API key or paid API credits.

IMPORTANT: This tool does not replace a caseworker, therapist,
attorney, healthcare provider, or emergency service.
"""

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

STAFF_ROLES = {
    "1": "caseworker",
    "2": "intake worker",
    "3": "volunteer",
    "4": "supervisor",
}

URGENCY_LABELS = {
    "High": "(!!) HIGH",
    "Medium": "( ! ) MEDIUM",
    "Low": "(  ) LOW",
}

CATEGORY_KEYWORDS = {
    "Housing / Rent Assistance": [
        "rent", "eviction", "landlord", "behind on rent", "housing",
        "shelter", "homeless", "no place to stay", "lease"
    ],
    "Employment / Income Support": [
        "job", "lost job", "unemployed", "employment", "income",
        "laid off", "work", "paycheck", "hours cut"
    ],
    "Food Assistance": [
        "food", "groceries", "hungry", "snap", "ebt", "meal",
        "feeding", "pantry"
    ],
    "Utility Assistance": [
        "utility", "electric", "gas bill", "water bill", "heat",
        "lights", "power", "shut off"
    ],
    "Healthcare Needs": [
        "doctor", "medical", "healthcare", "medicine", "medication",
        "insurance", "hospital", "clinic"
    ],
    "Mental Health Support": [
        "stress", "anxiety", "depression", "grief", "mental health",
        "overwhelmed", "therapy", "counseling"
    ],
    "Legal Aid": [
        "legal", "court", "lawyer", "attorney", "rights",
        "eviction notice", "custody"
    ],
}

FOLLOW_UP_QUESTIONS = {
    "Housing / Rent Assistance": [
        "How many months behind is the client on rent?",
        "Has the client received an eviction notice or court date?",
        "What is the total amount owed?",
        "Does the client have a current lease or landlord contact?"
    ],
    "Employment / Income Support": [
        "When did the client lose their job or income?",
        "Has the client applied for unemployment benefits?",
        "Is the client currently looking for work?",
        "Does the client have transportation or childcare barriers?"
    ],
    "Food Assistance": [
        "Does the client currently receive SNAP or EBT?",
        "How many people are in the household?",
        "Does the client need food today?",
        "Are there children, seniors, or people with medical needs in the home?"
    ],
    "Utility Assistance": [
        "Is there a shutoff notice or past-due balance?",
        "Which utility bill needs support?",
        "What is the amount owed?",
        "Has the client applied for utility assistance before?"
    ],
    "Healthcare Needs": [
        "Does the client have health insurance?",
        "Is this an urgent medical need?",
        "Does the client need help finding a clinic or provider?",
        "Is the client able to afford medication?"
    ],
    "Mental Health Support": [
        "Is the client currently safe?",
        "Does the client have a counselor or support person?",
        "Is the client experiencing a crisis right now?",
        "Would the client like help finding counseling or support groups?"
    ],
    "Legal Aid": [
        "Does the client have any upcoming court dates?",
        "Has the client received legal documents?",
        "Does the client already have legal representation?",
        "What legal issue does the client need help with?"
    ],
}

NEXT_STEPS = {
    "Housing / Rent Assistance": [
        "Gather rent balance, lease details, and landlord contact information.",
        "Check eligibility for emergency rental assistance programs.",
        "Connect the client with a housing support agency.",
        "If eviction is involved, refer the client to legal aid quickly."
    ],
    "Employment / Income Support": [
        "Review the client’s employment history and recent income loss.",
        "Encourage the client to apply for unemployment or income support.",
        "Share local workforce development or job placement resources.",
        "Identify barriers such as childcare, transportation, or documentation."
    ],
    "Food Assistance": [
        "Ask whether the client needs food immediately.",
        "Refer the client to SNAP, EBT, or food pantry resources.",
        "Identify household size and any urgent nutrition needs.",
        "Provide local food assistance options when available."
    ],
    "Utility Assistance": [
        "Review the shutoff notice or utility balance.",
        "Help the client gather account numbers and billing documents.",
        "Refer the client to utility assistance programs.",
        "Prioritize urgent shutoff or no-heat situations."
    ],
    "Healthcare Needs": [
        "Clarify the client’s medical concern and urgency.",
        "Refer the client to a community clinic or healthcare provider.",
        "Check whether the client has insurance or medication needs.",
        "Encourage emergency care if symptoms are urgent or severe."
    ],
    "Mental Health Support": [
        "Confirm whether the client is safe right now.",
        "Share crisis resources if there is immediate risk.",
        "Refer the client to counseling or mental health support.",
        "Encourage follow-up with a trusted provider or support person."
    ],
    "Legal Aid": [
        "Ask for copies of court notices or legal documents.",
        "Identify any upcoming deadlines or court dates.",
        "Refer the client to legal aid or tenant rights support.",
        "Document the legal issue clearly for follow-up."
    ],
}


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
    lower = text.lower()
    return any(keyword in lower for keyword in CRISIS_KEYWORDS)


def show_crisis_message():
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


def choose_role():
    print("\nSelect your staff role:")
    for num, role in STAFF_ROLES.items():
        print(f"  {num}. {role.title()}")
    choice = input("Enter number (or press Enter for caseworker): ").strip()
    return STAFF_ROLES.get(choice, "caseworker")


def identify_categories(situation):
    lower = situation.lower()
    matched = []

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in lower for keyword in keywords):
            matched.append(category)

    if len(matched) == 0:
        return ["Unclear"]

    return matched


def determine_urgency(situation, categories):
    lower = situation.lower()

    high_keywords = [
        "eviction notice", "court date", "shut off", "no food today",
        "homeless tonight", "no place to stay tonight", "emergency",
        "unsafe", "abuse", "domestic violence"
    ]

    medium_keywords = [
        "behind on rent", "lost job", "needs food", "past due",
        "overwhelmed", "hours cut", "unemployed"
    ]

    if any(keyword in lower for keyword in high_keywords):
        return "High", "The situation may involve immediate safety, housing, utility, or crisis concerns."

    if any(keyword in lower for keyword in medium_keywords) or len(categories) > 1:
        return "Medium", "The client has multiple needs or a time-sensitive support issue."

    return "Low", "The situation appears important but does not show immediate crisis indicators."


def build_identified_needs(categories):
    needs = []

    descriptions = {
        "Housing / Rent Assistance": "Rent, housing, or eviction support",
        "Employment / Income Support": "Job loss or income support",
        "Food Assistance": "Food or grocery support",
        "Utility Assistance": "Help with utility bills",
        "Healthcare Needs": "Medical or insurance support",
        "Mental Health Support": "Stress, counseling, or emotional support",
        "Legal Aid": "Legal guidance or rights support",
        "Unclear": "More information is needed"
    }

    for category in categories:
        needs.append({
            "name": category,
            "description": descriptions.get(category, "Support need identified")
        })

    return needs


def build_follow_up_questions(categories):
    questions = []

    for category in categories:
        questions.extend(FOLLOW_UP_QUESTIONS.get(category, []))

    if not questions:
        questions = [
            "What is the client's most urgent concern right now?",
            "What support has the client already tried to access?",
            "Does the client have any deadlines or immediate risks?",
            "What documents or information does the client have available?"
        ]

    return questions[:6]


def build_next_steps(categories):
    steps = []

    for category in categories:
        steps.extend(NEXT_STEPS.get(category, []))

    if not steps:
        steps = [
            "Clarify the client's main concern.",
            "Ask about urgency, deadlines, and safety.",
            "Identify the most appropriate resource category.",
            "Refer the client to a caseworker or community support agency."
        ]

    return steps[:6]


def build_staff_summary(situation, categories, urgency):
    category_text = ", ".join(categories)

    return (
        f"The client reported the following situation: {situation} "
        f"The identified support area is {category_text}, with an urgency level of {urgency}. "
        "Staff should gather more details, confirm immediate needs, and connect the client with appropriate resources."
    )


def analyze_situation(situation, role):
    categories = identify_categories(situation)

    if len(categories) > 1:
        primary_category = "Multiple Needs"
    else:
        primary_category = categories[0]

    urgency, urgency_reason = determine_urgency(situation, categories)

    result = {
        "primary_category": primary_category,
        "urgency": urgency,
        "urgency_reason": urgency_reason,
        "identified_needs": build_identified_needs(categories),
        "follow_up_questions": build_follow_up_questions(categories),
        "next_steps": build_next_steps(categories),
        "staff_summary": build_staff_summary(situation, categories, urgency),
        "referral_note": "Coordinate with the appropriate community resource or support agency based on the identified needs."
    }

    return result


def display_results(result, situation, role):
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


def main():
    divider()
    print("  COMMUNITY RESOURCE NAVIGATOR")
    divider()
    print("  This tool helps staff get a starting point.")
    print("  It does NOT replace a caseworker, therapist,")
    print("  attorney, healthcare provider, or emergency service.")
    print("  No API key or paid credits required.")
    divider()

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

        if check_for_crisis(situation):
            show_crisis_message()

        print("\nAnalyzing situation...\n")

        result = analyze_situation(situation, role)
        display_results(result, situation, role)

        again = input("Analyze another situation? (y/n): ").strip().lower()
        if again != "y":
            print("\nGoodbye.\n")
            break


if __name__ == "__main__":
    main()
