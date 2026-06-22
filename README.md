# Claude Community Resource Navigator

## Overview

Claude Community Resource Navigator is an AI-powered Python tool that helps social service staff organize client needs, assess urgency, create follow-up questions, and suggest next steps.

This project demonstrates how AI can support community organizations by helping staff quickly assess client needs, prioritize resources, and create structured action plans.

## Features

* Uses the Anthropic Claude API
* Detects crisis-related keywords before generating results
* Supports staff roles like caseworker, intake worker, volunteer, and supervisor
* Identifies client needs and resource categories
* Creates follow-up questions
* Suggests next steps
* Generates a professional staff summary
* Keeps API keys out of the code

## Technologies Used

* Python
* Anthropic Claude API
* JSON
* Prompt Engineering
* Command Line Interface (CLI)

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

* Identify the main resource category
* Assess urgency
* Ask better follow-up questions
* Suggest next steps
* Create a short staff summary

## Important Notice

This tool does not replace a caseworker, therapist, attorney, healthcare provider, or emergency service.

If someone is in immediate danger, call 911. For mental health crisis support, call or text 988.

## AI Collaboration

I used Claude AI to help create this project, including planning features, generating code, and improving functionality. I reviewed, tested, and customized the final project to ensure it met the goals of the application.

## Future Improvements

* Add ZIP-code based resource matching
* Add a web app version
* Add downloadable case note summaries
* Add local Chicago-area referral data
* Add multi-language support
