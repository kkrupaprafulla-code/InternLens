# InternLens Demo Script

## Demo Video

https://youtu.be/KXlVnhfjPVQ

## Duration

Approximately 2 minutes 52 seconds.

## Project

InternLens — Internship Safety & Opportunity Analyzer

## Demo Objective

This demo shows how InternLens helps students review internship listings before applying.

It demonstrates:

- The problem InternLens addresses
- The application workflow
- Risk and opportunity analysis
- Missing information
- Questions and safe next steps
- The AI-generated summary
- The technology stack and architecture
- How AWS Strands Agents SDK is used

---

# Demo Flow

## 1. Introduction

**What to say:**

"InternLens is an internship safety and opportunity analyzer built to help students review internship listings before applying.

Students often have to judge whether an internship opportunity provides real career value while also checking for warning signs and missing information."

---

## 2. Show the Application

**What to say:**

"With InternLens, a student can paste an internship listing into the application and analyze it."

Show the InternLens interface and the internship listing input.

---

## 3. Analyze an Internship

**What to say:**

"The application analyzes the listing and separates the results into potential risk signals, opportunity signals, missing information, questions to ask, and safe next steps."

Click the Analyze button and show the generated results.

---

## 4. Explain the Results

**What to say:**

"For example, the application can identify signals such as upfront payment requests or urgency.

It can also highlight positive career indicators such as technical work, mentorship, project experience, code reviews, and compensation.

Instead of declaring an internship a scam, InternLens shows the evidence and missing information so the student can investigate further."

Show the risk, opportunity, missing information, questions, and safe next-step sections.

---

## 5. AI Summary

**What to say:**

"The structured analysis is handled using deterministic Python logic.

An AWS Strands Agent is then used to generate a concise natural-language summary of the results."

Show the AI-generated summary.

---

## 6. Technology and Architecture

**What to say:**

"The frontend uses HTML, CSS, and JavaScript.

The backend is built with Python and Flask.

For the AI workflow, I use the AWS Strands Agents SDK with the Ollama model provider and a locally running Llama 3.2 3B model."

Show the relevant architecture or project files if included in the demo.

---

## 7. AWS Usage

**What to say:**

"The project uses the AWS Strands Agents SDK as its AWS open-source technology for the Build It track.

The Strands Agent connects the structured analysis with the local Llama 3.2 model to produce the final concise AI summary."

---

## 8. Responsible AI

**What to say:**

"InternLens is designed as a decision-support tool.

A risk signal is not treated as proof of fraud, and the application does not make the final decision for the student."

---

## 9. Closing

**What to say:**

"InternLens helps students understand what deserves attention in an internship listing before they apply, while keeping the final decision with the student."

---

# Technical Stack

## Frontend

- HTML
- CSS
- JavaScript

## Backend

- Python
- Flask
- Flask-CORS

## AI

- AWS Strands Agents SDK
- Ollama
- Llama 3.2 3B

## Development

- Git
- GitHub
- Python virtual environment
- PowerShell

---

# Architecture

```text
Student
   |
   v
Internship Listing
   |
   v
HTML / CSS / JavaScript
   |
   v
Python / Flask API
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
       Structured Results
              +
         AI Summary
         
      
---

# Learning

Building InternLens helped me learn:

- How to integrate the AWS Strands Agents SDK into a Python application
- How to connect an agent to a local model provider
- How to use Ollama with Llama 3.2
- How to combine deterministic application logic with generative AI
- How to connect a Flask backend with a browser frontend
- How to design AI-assisted decision-support workflows
- How to handle loading and error states in an AI application
- How to document and present an AI project

---
