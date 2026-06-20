"""
Community Resource Navigator (Beginner Python Project)
--------------------------------------------------------
This program asks a user to describe their situation in plain language,
then it:
  1. Checks for any crisis/safety keywords first
  2. Guesses a resource category based on keywords
  3. Prints follow-up questions a staff member could ask
  4. Prints suggested next steps
  5. Prints a short staff summary
 
This is a simple keyword-matching program, NOT real artificial
intelligence. It's meant to show how basic programming concepts
(functions, dictionaries, lists, loops, if/elif) can be combined
into something useful.
 
IMPORTANT: This tool does not replace a caseworker, therapist,
attorney, or emergency service.
"""
 
# ---------------------------------------------------------
# STEP 1: Words that signal an emergency or crisis situation.
# If any of these appear in what the user types, we show
# crisis resources FIRST, before anything else.
# ---------------------------------------------------------
CRISIS_KEYWORDS = [
    "kill myself", "suicide", "hurt myself", "self harm", "self-harm",
    "abuse", "hitting me", "hit me", "afraid for my safety", "unsafe",
    "emergency", "no place to stay tonight", "homeless tonight",
    "nowhere to sleep tonight"
]
 
# ---------------------------------------------------------
# STEP 2: A "database" of resource categories.
# Each category has:
#   - a list of keywords that point to it
#   - a list of follow-up questions
#   - a list of suggested next steps
# This is just a dictionary of dictionaries — a simple way
# to organize related information in Python.
# ---------------------------------------------------------
RESOURCES = {
    "Housing / Rent Assistance": {
        "keywords": ["rent", "evict", "eviction", "landlord", "lease", "housing"],
        "questions": [
            "When is rent due, and how far behind are you (if at all)?",
            "Have you received any written notice from your landlord?",
            "Who else lives in your household?",
            "Do you have any income coming in right now?"
        ],
        "next_steps": [
            "Check eligibility for local rental assistance programs.",
            "Ask if there is an active eviction notice or court date.",
            "Refer to landlord-tenant mediation resources if needed.",
            "Screen for related needs like utility or food assistance."
        ]
    },
    "Employment / Income Support": {
        "keywords": ["job", "fired", "laid off", "unemployed", "unemployment", "income", "work"],
        "questions": [
            "Have you applied for unemployment benefits yet?",
            "When did you lose your job or income?",
            "Do you have any savings or other income sources?",
            "Are you currently looking for new work?"
        ],
        "next_steps": [
            "Help confirm unemployment insurance application status.",
            "Refer to local job placement or career services.",
            "Screen for emergency financial assistance programs.",
            "Check eligibility for SNAP (food assistance)."
        ]
    },
    "Food Assistance": {
        "keywords": ["food", "hungry", "groceries", "snap", "meals"],
        "questions": [
            "Do you currently have access to enough food for your household?",
            "Have you applied for SNAP or other food benefits?",
            "Are there children or elderly family members in the home?",
            "Is there a food pantry near you that you've used before?"
        ],
        "next_steps": [
            "Refer to local food pantries or community meal programs.",
            "Help with SNAP application if not already enrolled.",
            "Screen for other related needs (housing, income)."
        ]
    },
    "Utility Assistance": {
        "keywords": ["electric", "electricity", "gas bill", "utility", "utilities", "water bill", "heat"],
        "questions": [
            "Which utility is at risk of being shut off (if any)?",
            "Have you received a shutoff notice?",
            "Have you applied for utility assistance before (e.g. LIHEAP)?",
            "Is anyone in the home dependent on electricity for medical equipment?"
        ],
        "next_steps": [
            "Check eligibility for utility assistance programs (e.g. LIHEAP).",
            "Contact the utility company about payment plans.",
            "Screen for related housing or income needs."
        ]
    },
    "Healthcare Needs": {
        "keywords": ["sick", "doctor", "medical", "health insurance", "medication", "hospital"],
        "questions": [
            "Do you currently have health insurance coverage?",
            "Is this a medical emergency or an ongoing health issue?",
            "Have you been able to access medications you need?",
            "Do you have a primary care provider?"
        ],
        "next_steps": [
            "Refer to community health clinics or sliding-scale providers.",
            "Help check eligibility for Medicaid or other coverage.",
            "If symptoms are urgent, recommend seeking medical care right away."
        ]
    }
}
 
 
def check_for_crisis(text):
    """
    Looks through the user's text for crisis-related keywords.
    Returns True if a possible crisis is detected, otherwise False.
    """
    text_lower = text.lower()
    for keyword in CRISIS_KEYWORDS:
        if keyword in text_lower:
            return True
    return False
 
 
def show_crisis_message():
    """Prints emergency resources. Used when a crisis keyword is found."""
    print("\n" + "=" * 60)
    print("THIS SOUNDS LIKE IT MAY BE AN EMERGENCY")
    print("=" * 60)
    print("If you or someone else is in immediate danger, call 911.")
    print("For mental health crisis support, call or text 988")
    print("(Suicide & Crisis Lifeline) — available 24/7.")
    print("This program is not a substitute for emergency services.")
    print("=" * 60 + "\n")
 
 
def find_category(text):
    """
    Looks through the RESOURCES dictionary and tries to match
    keywords found in the user's text. Returns the matching
    category name, or None if nothing matches.
    """
    text_lower = text.lower()
    for category_name, info in RESOURCES.items():
        for keyword in info["keywords"]:
            if keyword in text_lower:
                return category_name
    return None  # No match found
 
 
def print_list(title, items):
    """A small helper function to print a labeled list neatly."""
    print(title)
    for item in items:
        print(f"  - {item}")
    print()
 
 
def print_staff_summary(original_text, category):
    """Prints a short, staff-facing summary of the situation."""
    print("STAFF SUMMARY")
    print("-" * 60)
    if category:
        print(f"Client situation: \"{original_text}\"")
        print(f"Likely resource category: {category}")
        print("Recommend confirming urgency and beginning intake")
        print("for the category above. Screen for related needs.")
    else:
        print(f"Client situation: \"{original_text}\"")
        print("No clear category matched automatically.")
        print("Recommend a manual conversation to clarify needs.")
    print("-" * 60 + "\n")
 
 
def main():
    """The main function that runs the whole program."""
    print("=" * 60)
    print("COMMUNITY RESOURCE NAVIGATOR (Practice Tool)")
    print("=" * 60)
    print("This tool helps staff get a starting point — it does")
    print("not replace a caseworker, therapist, or emergency service.\n")
 
    # Step 1: Get input from the user
    situation = input("Please describe the situation: ")
    print()  # blank line for spacing
 
    # Step 2: Check for crisis keywords FIRST
    if check_for_crisis(situation):
        show_crisis_message()
 
    # Step 3: Try to find a matching resource category
    category = find_category(situation)
 
    if category:
        print(f"RESOURCE CATEGORY: {category}\n")
        print_list("FOLLOW-UP QUESTIONS TO ASK:", RESOURCES[category]["questions"])
        print_list("SUGGESTED NEXT STEPS:", RESOURCES[category]["next_steps"])
    else:
        print("RESOURCE CATEGORY: Not clearly identified.\n")
        print("Consider asking the client more about their situation,")
        print("or manually choosing the closest matching category.\n")
 
    # Step 4: Always show a staff summary at the end
    print_staff_summary(situation, category)
 
 
# This line makes sure main() only runs when this file is run directly
# (a common beginner Python pattern worth learning!)
if __name__ == "__main__":
    main()
