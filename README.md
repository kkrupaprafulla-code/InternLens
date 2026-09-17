# InternLens 🔎

**See the opportunity before you apply.**

InternLens is an AI-assisted internship safety and opportunity analyzer. A student pastes an internship listing and gets a structured report showing potential risk signals, career-value signals, missing information, questions to ask, safe next steps, and a short AI-generated summary.

> **InternLens does not declare an internship fraudulent. It surfaces evidence and missing information so the student can investigate and make their own decision.**

## The problem

Students see internship listings with very different levels of detail. Some may contain upfront payment requests, guaranteed-placement claims, requests for sensitive information, or pressure language. Other listings may contain valuable signals such as mentorship, technical work, code reviews, real projects, duration, and compensation.

InternLens puts those signals into one simple report before the student applies.

## How it works

```text
Student pastes internship listing
              ↓
       InternLens frontend
              ↓
         Flask backend
              ↓
   Evidence-based Python analysis
              ↓
       AWS Strands Agent
              ↓
       Ollama + Llama 3.2
              ↓
      Short factual summary
              ↓
          Final report
```

### Evidence-based analysis

Python identifies concrete signals such as:

- upfront registration/application/joining fees
- guaranteed job or placement claims
- sensitive financial or account-information requests
- urgency or limited-seat language
- mentorship
- technical development work
- GitHub/version control
- code reviews and pull requests
- portfolio/production experience
- duration and compensation

It also checks whether important details are missing, including company background, responsibilities, skills, supervision, duration, compensation, schedule, and work mode.

### AI summary

The structured risk classification is calculated in Python. The local Llama model is used through the **AWS Strands Agents SDK** only for a concise factual summary. This prevents an AI-generated response from randomly changing the structured LOW/MEDIUM/HIGH classification.

An unpaid internship is **not** treated as risky by itself.

## AWS / Build It

InternLens uses the **AWS Strands Agents SDK** with a local Ollama model. This fits the Build It approach, where AWS open-source tools and local models can be used without requiring an AWS account.

## Tech stack

- Python
- Flask + Flask-CORS
- AWS Strands Agents SDK
- Ollama
- Llama 3.2 3B
- HTML / CSS / JavaScript

## Run locally

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install and prepare Ollama

Make sure Ollama is installed and running, then download the model:

```bash
ollama pull llama3.2:3b
```

You can verify it with:

```bash
ollama run llama3.2:3b
```

### 3. Start the backend

From the project root:

```bash
cd backend
python app.py
```

The backend runs at:

```text
http://127.0.0.1:5000
```

### 4. Open the frontend

Open `frontend/index.html` in a browser.

## Example behavior

### Potential warning

A listing containing a refundable registration fee and limited-seat pressure can produce:

```text
MEDIUM

Risk signals:
- Upfront payment request
- Urgency / limited-seat language
```

The report then explains what information is missing and what the student should verify.

### Career-value signals

A software engineering listing mentioning Python, FastAPI, PostgreSQL, GitHub, pull requests, senior-engineer mentorship, code reviews, duration, and a stipend can produce:

```text
LOW

Opportunity signals:
- Mentorship
- Hands-on technical work
- GitHub / version control
- Code reviews
- Clearly stated duration
- Compensation information
```

## Responsible design

InternLens intentionally avoids absolute claims such as **"This internship is a scam."** A detected signal is not proof of fraud. The product is designed to help students investigate opportunities more carefully.

## What I learned

- Building an agent with the AWS Strands Agents SDK
- Connecting Strands to a local Ollama model
- Combining deterministic analysis with generative AI
- Designing predictable structured output around an AI component
- Building and testing an end-to-end AI application locally
- Designing safety-oriented UX that informs rather than makes the decision for the user

## Future improvements

Possible future additions include URL input, screenshot/PDF analysis, company verification, scan history, and a browser extension. These are intentionally outside the MVP so the core experience stays focused.

## AI tools used

AI assistance was used during development. The final repository contains the project code and configuration used for the submitted application.
