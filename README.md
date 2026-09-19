# InternLens

## Internship Safety & Opportunity Analyzer

InternLens is a web-based tool that helps students review internship listings before applying.

It analyzes an internship listing for potential risk signals, career-value signals, missing information, useful questions to ask, and safe next steps.

InternLens is designed as a decision-support tool. It does not claim to definitively determine whether an internship is legitimate or fraudulent.

## Demo

Demo Video:
https://youtu.be/KXlVnhfjPVQ

GitHub Repository:
https://github.com/kkrupaprafulla-code/InternLens

## Problem

Students discover internship opportunities through job boards, social media, messaging groups, and recruiter outreach.

Some internship listings may contain warning signs such as:

- Upfront registration or training fees
- Urgency or pressure to apply
- Unclear company information
- Missing role responsibilities
- Missing mentorship or supervision details
- Vague compensation or work conditions

At the same time, legitimate internship opportunities can contain useful career signals such as:

- Technical responsibilities
- Mentorship
- Code reviews
- Real project work
- Git or version-control usage
- Portfolio-building opportunities
- Clear duration
- Compensation information

Manually reviewing all of these details can be difficult and time-consuming for students.

## Solution

InternLens allows a student to paste an internship listing into the application and receive a structured analysis.

The application identifies:

- Potential risk signals
- Career and opportunity signals
- Missing information
- Questions to ask the recruiter or company
- Safer next steps
- A concise AI-generated summary

The goal is not to make the decision for the student.

Instead, InternLens highlights evidence, missing information, and areas that deserve further verification so students can make more informed decisions.

## Key Features

### Risk Signals

Identifies potentially concerning patterns in an internship listing, including:

- Upfront payment requests
- Registration fees
- Urgency or pressure
- Missing company information
- Other potentially concerning details

### Opportunity Signals

Highlights potentially useful career indicators, including:

- Technical work
- Mentorship
- Code reviews
- Git or version control
- Real project experience
- Portfolio opportunities
- Internship duration
- Compensation information

### Missing Information

Identifies important details that are not clearly provided in the listing.

Examples include:

- Company background
- Mentor or supervisor
- Work schedule
- Work mode
- Technical requirements
- Responsibilities

### Questions to Ask

Provides practical questions that students can ask recruiters or companies before applying.

### Safe Next Steps

Provides general verification steps such as:

- Verify the company independently
- Verify the recruiter through official channels
- Ask for complete written internship details
- Avoid unexpected payments
- Avoid sharing sensitive financial information unnecessarily

### AI Summary

Uses an AI agent to generate a concise natural-language summary of the structured analysis.

## Architecture

Student
    |
    v
Internship Listing
    |
    v
Frontend
HTML / CSS / JavaScript
    |
    v
Flask API
Python Backend
    |
    +----------------------+
    |                      |
    v                      v
Deterministic          AWS Strands
Python Analysis        Agent
    |                      |
    |                      v
    |                  Ollama
    |                      |
    |                      v
    |                 Llama 3.2 3B
    |                      |
    +----------+-----------+
               |
               v
        Structured Analysis
               +
          AI Summary

The core risk, opportunity, and missing-information checks are handled using deterministic Python logic.

The AWS Strands Agent is used for the AI-assisted natural-language summary.

This separation keeps the important structured signals predictable while still using generative AI where it adds value.

## AWS Usage

InternLens uses the AWS Strands Agents SDK as its AWS open-source technology for the Build It track.

The Flask backend integrates a Strands Agent configured with the Ollama model provider and a locally running Llama 3.2 3B model.

The workflow is:

Internship Listing
        |
        v
Structured Python Analysis
        |
        v
AWS Strands Agent
        |
        v
Ollama + Llama 3.2 3B
        |
        v
Concise AI Summary

The project uses AWS Strands Agents SDK locally rather than deploying the application to AWS cloud services.

No AWS Bedrock, Lambda, S3, EC2, or other AWS cloud services are claimed as part of this implementation.

## Responsible AI Design

InternLens is intentionally designed as a decision-support system.

It does not claim to definitively determine whether an internship is legitimate or fraudulent.

Instead, the application:

1. Identifies observable signals.
2. Highlights missing information.
3. Suggests questions to investigate.
4. Provides safer verification steps.
5. Uses AI primarily to summarize the structured analysis.

A risk signal is not proof of fraud, and the absence of a risk signal does not guarantee that an opportunity is safe.

Students should independently verify important information before making decisions.

## Technology Stack

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- Flask
- Flask-CORS

### AI

- AWS Strands Agents SDK
- Ollama
- Llama 3.2 3B

### Development

- Git
- GitHub
- Python virtual environment
- PowerShell

## Project Structure

InternLens/
|
├── backend/
│   ├── app.py
│   └── ai_analyzer.py
|
├── frontend/
│   └── index.html
|
├── DEMO_SCRIPT.md
└── README.md
└── requirements.txt

## Running Locally

### 1. Clone the repository

git clone https://github.com/kkrupaprafulla-code/InternLens.git

cd InternLens

### 2. Create a virtual environment

python -m venv .venv

### 3. Activate the virtual environment on Windows

.venv\Scripts\Activate.ps1

### 4. Install dependencies

pip install -r requirements.txt

### 5. Install and run Ollama

Install Ollama and make sure it is running locally.

Pull the Llama 3.2 3B model:

ollama pull llama3.2:3b

### 6. Start the Flask backend

python backend/app.py

The backend runs locally at:

http://127.0.0.1:5000

### 7. Open the frontend

Open the frontend through the local application workflow and use the internship analysis interface.

## Example

### Example Input

3-month software development internship.

Work includes project development and a completion certificate.

A refundable registration fee of ₹2,999 is required.

Limited seats available.

### Example Analysis

Potential Risk Signals:

- Upfront payment request
- Urgency or limited seats

Opportunity Signals:

- Project work
- Internship duration
- Certificate

Missing Information:

- Company background
- Mentor or supervisor
- Technical requirements
- Work schedule
- Work mode

Questions to Ask:

- What company or team will supervise the internship?
- What technical work will interns perform?
- Why is a registration fee required?

Safe Next Steps:

- Verify the company independently.
- Verify the recruiter through official channels.
- Request complete written internship details.
- Avoid sharing sensitive financial information unnecessarily.

The AI agent then generates a concise summary of the analysis.

## Learning

Building InternLens provided hands-on experience with:

- AWS Strands Agents SDK
- Agent integration in a Python application
- Ollama and local LLM integration
- Llama 3.2 3B
- Combining deterministic logic with generative AI
- Flask API development
- Frontend and backend integration
- API response handling
- Loading and error states
- Local AI inference
- Designing AI output around uncertainty and verification
- Git and GitHub development workflows

## Challenges

One of the main challenges was balancing AI-generated output with predictable application behavior.

Instead of asking the language model to make the entire decision, the structured risk, opportunity, and missing-information analysis is handled using deterministic Python logic.

The AI agent is then used primarily to generate a concise explanation of those results.

Another challenge was integrating a locally running model into a web application while keeping the frontend responsive and handling loading and error states correctly.

## Future Improvements

Possible future improvements include:

- Company and domain verification
- Source-based evidence collection
- More configurable analysis rules
- Improved internship category detection
- Better accessibility
- Persistent analysis history
- More detailed recruiter and company verification workflows
- Optional public deployment

## AI Tools Used

### ChatGPT

Used during development for:

- Debugging
- Code assistance
- Architecture discussion
- Frontend and backend troubleshooting
- Documentation
- README preparation
- Project presentation and demo preparation

### Ollama + Llama 3.2 3B

Used by the InternLens application to generate the concise AI summary from the structured analysis.

## Hackathon

Built for AWS First Commit 2026.

Track:

Build It

AWS Technology:

AWS Strands Agents SDK

## Author

Krupa

GitHub:
https://github.com/kkrupaprafulla-code/InternLens

## License

This project is an open-source hackathon project.
