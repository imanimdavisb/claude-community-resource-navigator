# Claude Community Resource Navigator

## Overview

Claude Community Resource Navigator is an AI-powered Python tool that helps social service staff organize client needs, assess urgency, create follow-up questions, and suggest next steps.

This project was built to show how AI can support community organizations, caseworkers, volunteers, and intake staff by turning a client situation into a clear action plan.

## Features

- Uses the Anthropic Claude API
- Detects crisis-related keywords before generating results
- Supports staff roles like caseworker, intake worker, volunteer, and supervisor
- Identifies client needs and resource categories
- Creates follow-up questions
- Suggests next steps
- Generates a professional staff summary
- Keeps API keys out of the code

## Technologies Used

- Python
- Anthropic Claude API
- JSON
- Prompt Engineering
- Command Line Interface (CLI)

## How to Run

Install the dependency:

```bash
pip install anthropic
```

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Run the project:

```bash
python community_resource_navigator.py
```

The script will ask for your API key if you have not set it as an environment variable.

## Example Use Case

A client says they are behind on rent, recently lost their job, and need food assistance.

The tool can help staff:

- Identify the main resource category
- Assess urgency
- Ask better follow-up questions
- Suggest next steps
- Create a short staff summary

## Important Notice

This tool does not replace a caseworker, therapist, attorney, healthcare provider, or emergency service.

If someone is in immediate danger, call 911. For mental health crisis support, call or text 988.

## Future Improvements

- Add ZIP-code based resource matching
- Add a web app version
- Add downloadable case note summaries
- Add local Chicago-area referral data
- Add multi-language support
