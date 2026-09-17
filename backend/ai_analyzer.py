import json
import re

from strands import Agent
from strands.models.ollama import OllamaModel


MODEL_NAME = "llama3.2:3b"
OLLAMA_HOST = "http://localhost:11434"

model = OllamaModel(host=OLLAMA_HOST, model_id=MODEL_NAME)
agent = Agent(model=model)


# ============================================================
# Utilities
# ============================================================

def deduplicate(items):
    result = []
    seen = set()
    for item in items:
        if not isinstance(item, str):
            continue
        cleaned = item.strip()
        if not cleaned:
            continue
        key = cleaned.lower()
        if key not in seen:
            seen.add(key)
            result.append(cleaned)
    return result


def extract_json(text):
    if not text:
        return None

    text = str(text).strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    return None


def extract_response_text(response):
    if response is None:
        return ""
    if isinstance(response, str):
        return response
    try:
        return str(response)
    except Exception:
        return ""


# ============================================================
# Safety analysis
# ============================================================

def detect_safety_signals(text):
    text_lower = text.lower()
    signals = []

    sentences = re.split(r"(?<=[.!?])\s+|\n+", text_lower)

    # Payment: detect requests, while respecting explicit negation.
    payment_patterns = [
        r"registration fee", r"registration fees",
        r"joining fee", r"joining fees",
        r"application fee", r"application fees",
        r"processing fee", r"processing fees",
        r"security deposit",
        r"pay.*before joining", r"pay.*to join",
        r"pay.*to secure", r"fee.*before joining",
        r"fee.*to join", r"fee.*to secure",
        r"₹\s?[\d,]+.*fee", r"rs\.?\s?[\d,]+.*fee",
        r"inr\s?[\d,]+.*fee",
    ]
    negative_payment_patterns = [
        r"no registration fee", r"no registration fees",
        r"no application fee", r"no application fees",
        r"no joining fee", r"no joining fees",
        r"no processing fee", r"no processing fees",
        r"no payment is required", r"no payment required",
        r"without any payment", r"without payment",
        r"do not pay", r"does not require payment",
        r"doesn't require payment",
    ]

    payment_detected = False
    for sentence in sentences:
        if any(re.search(p, sentence) for p in payment_patterns):
            if not any(re.search(p, sentence) for p in negative_payment_patterns):
                payment_detected = True
                break

    if payment_detected:
        signals.append("The listing appears to request an upfront payment or fee.")

    # Guaranteed employment / placement.
    guaranteed_patterns = [
        r"guaranteed job", r"job guaranteed",
        r"100% job", r"100 percent job",
        r"guaranteed placement", r"placement guaranteed",
        r"assured placement", r"job assured",
    ]
    if any(re.search(p, text_lower) for p in guaranteed_patterns):
        signals.append("The listing makes a guaranteed job or placement claim.")

    # Sensitive financial/account credentials.
    sensitive_patterns = [
        r"send.*bank account", r"provide.*bank account",
        r"bank details", r"bank account details",
        r"credit card", r"debit card", r"card details",
        r"\bcvv\b", r"\botp\b", r"one time password",
        r"password", r"upi pin", r"aadhaar.*before", r"pan card.*before",
    ]
    if any(re.search(p, text_lower) for p in sensitive_patterns):
        signals.append("The listing appears to request sensitive financial or account information.")

    # Pressure language is a signal, but not a serious risk category by itself.
    urgency_patterns = [
        r"limited seats", r"limited slots", r"apply immediately",
        r"apply now", r"act immediately", r"\burgent\b",
        r"last few seats", r"few seats left", r"only .* seats",
    ]
    if any(re.search(p, text_lower) for p in urgency_patterns):
        signals.append("The listing uses urgency or limited-seat language that may pressure applicants.")

    return deduplicate(signals)


# ============================================================
# Opportunity analysis
# ============================================================

def detect_opportunity_signals(text):
    text_lower = text.lower()
    signals = []

    if any(x in text_lower for x in [
        "mentor", "mentorship", "guided by", "guidance from",
        "senior engineer", "senior developer", "experienced engineer",
        "experienced developer", "supervisor"
    ]):
        signals.append("Mentorship or guidance from experienced people.")

    if any(x in text_lower for x in [
        "software development", "software engineering", "web development",
        "backend development", "frontend development", "full stack",
        "full-stack", "programming", "coding", "develop applications",
        "develop software", "production services", "technical projects",
        "development projects"
    ]):
        signals.append("Hands-on technical or development work.")

    if any(x in text_lower for x in [
        "github", "gitlab", "git", "version control", "open source", "open-source"
    ]):
        signals.append("Experience with GitHub, version control, or open-source collaboration.")

    if any(x in text_lower for x in [
        "code review", "code reviews", "pull request", "pull requests",
        "pull-request", "pull-requests"
    ]):
        signals.append("Code review or pull-request based collaboration.")

    if any(x in text_lower for x in [
        "portfolio", "real-world project", "real world project",
        "real-world projects", "real world projects", "production project",
        "production services", "production environment"
    ]):
        signals.append("The work may provide experience that can contribute to a portfolio.")

    if any(x in text_lower for x in [
        "certificate", "certification", "internship certificate", "completion certificate"
    ]):
        signals.append("The listing mentions an internship or completion certificate.")

    duration_patterns = [
        r"\b\d+\s*(month|months)\b", r"\b\d+\s*(week|weeks)\b",
        r"\b\d+\s*(day|days)\b", r"\b\d+\s*(year|years)\b",
    ]
    if any(re.search(p, text_lower) for p in duration_patterns):
        signals.append("Clearly stated internship duration.")

    compensation_patterns = [
        r"\bstipend\b", r"\bpaid internship\b", r"\bpaid position\b",
        r"\bcompensation\b", r"\bmonthly pay\b", r"\bpay per month\b",
        r"\b₹\s?[\d,]+\s*(per month|monthly)?\b",
        r"\brs\.?\s?[\d,]+\s*(per month|monthly)?\b",
        r"\binr\s?[\d,]+\s*(per month|monthly)?\b",
    ]
    if any(re.search(p, text_lower) for p in compensation_patterns):
        signals.append("Compensation or stipend information is provided.")

    return deduplicate(signals)


# ============================================================
# Missing information
# ============================================================

def detect_missing_information(text):
    text_lower = text.lower()
    missing = []

    if not any(x in text_lower for x in ["company", "organization", "startup", "about us", "about the company"]):
        missing.append("Company or organization background is not clearly provided.")

    if not any(x in text_lower for x in [
        "responsibil", "you will", "role:", "role -", "work on", "work with",
        "develop", "build", "create", "project", "projects"
    ]):
        missing.append("Specific responsibilities or project details are unclear.")

    if not any(x in text_lower for x in [
        "skills", "requirements", "required", "qualifications",
        "experience with", "knowledge of", "proficient"
    ]):
        missing.append("Expected skills or qualifications are not clearly stated.")

    if not any(x in text_lower for x in [
        "mentor", "mentorship", "supervisor", "manager", "report to",
        "reporting to", "senior engineer", "senior developer", "team lead", "lead engineer"
    ]):
        missing.append("Supervisor, mentor, or reporting structure is not clear.")

    duration_patterns = [
        r"\b\d+\s*(month|months)\b", r"\b\d+\s*(week|weeks)\b",
        r"\b\d+\s*(day|days)\b", r"\b\d+\s*(year|years)\b",
    ]
    if not any(re.search(p, text_lower) for p in duration_patterns):
        missing.append("Internship duration is not clearly stated.")

    if not any(x in text_lower for x in [
        "stipend", "salary", "compensation", "paid internship", "unpaid internship",
        "unpaid", "₹", "rs.", "inr"
    ]):
        missing.append("Compensation or stipend information is not provided.")

    if not any(x in text_lower for x in [
        "hours", "hour per week", "hours per week", "full time", "part time",
        "weekly", "schedule", "working hours", "work hours"
    ]):
        missing.append("Expected working schedule or hours are not clearly stated.")

    if not any(x in text_lower for x in [
        "remote", "hybrid", "on-site", "onsite", "in office", "location",
        "work from home", "wfh"
    ]):
        missing.append("Location or remote/hybrid/on-site work mode is not clearly stated.")

    return deduplicate(missing)


def build_questions(missing_information):
    questions = []
    for item in missing_information:
        low = item.lower()
        if "company" in low:
            questions.append("Can you provide more information about the company, team, and the people I would work with?")
        elif "responsibilit" in low or "project" in low:
            questions.append("What specific projects and responsibilities would I handle as an intern?")
        elif "skills" in low or "qualifications" in low:
            questions.append("What technical skills or qualifications are expected for this role?")
        elif "supervisor" in low or "reporting" in low:
            questions.append("Who would supervise or mentor me, and how often would I receive feedback?")
        elif "duration" in low:
            questions.append("What is the exact internship duration and expected start date?")
        elif "compensation" in low or "stipend" in low:
            questions.append("Is the internship paid, unpaid, or stipend-based, and what are the exact terms?")
        elif "schedule" in low or "hours" in low:
            questions.append("What are the expected working hours and weekly time commitment?")
        elif "location" in low or "work mode" in low:
            questions.append("Is the internship remote, hybrid, or on-site, and where is it based?")
    return deduplicate(questions)


# ============================================================
# Risk level — ONLY serious categories determine the level.
# Urgency alone is not MEDIUM.
# ============================================================

def calculate_risk_level(risk_signals, text):
    risk_text = " ".join(risk_signals).lower()
    serious_categories = 0

    if "upfront payment" in risk_text:
        serious_categories += 1

    if "sensitive financial" in risk_text or "account information" in risk_text:
        serious_categories += 1

    if "guaranteed job" in risk_text or "guaranteed job or placement" in risk_text:
        serious_categories += 1

    if serious_categories >= 2:
        return "HIGH"
    if serious_categories == 1:
        return "MEDIUM"
    return "LOW"


# ============================================================
# Safe guidance
# ============================================================

def get_safe_next_steps():
    return [
        "Verify the company and recruiter using an official website or trusted professional profile.",
        "Do not pay money or share sensitive financial/account credentials just to obtain an internship.",
        "Ask for written details about responsibilities, supervision, duration, compensation, and work expectations.",
        "Check whether the contact email and application process match the organization's official channels.",
    ]


# ============================================================
# Short AI summary only
# ============================================================

def build_ai_prompt(internship):
    return f'''You are InternLens.

Give a very short, factual summary of this internship listing.

Rules:
- Maximum 2 sentences.
- Mention only information explicitly present in the listing.
- Do not call the internship a scam or fraudulent.
- Do not treat unpaid status as automatically bad.
- Do not speculate.
- If there is a payment request, mention it.
- If there are concrete technical/career details, mention them.

Return ONLY valid JSON:
{{"summary":"..."}}

Listing:
{internship}'''


def get_ai_summary(internship):
    try:
        response = agent(build_ai_prompt(internship))
        parsed = extract_json(extract_response_text(response))
        if isinstance(parsed, dict):
            summary = parsed.get("summary", "")
            if isinstance(summary, str) and summary.strip():
                return summary.strip()
    except Exception as exc:
        # AI is optional; deterministic analysis must still work.
        print("AI summary failed:", repr(exc))
    return ""


# ============================================================
# Final analysis
# ============================================================

def build_result(internship, ai_summary=""):
    risk_signals = detect_safety_signals(internship)
    opportunity_signals = detect_opportunity_signals(internship)
    missing_information = detect_missing_information(internship)
    questions = build_questions(missing_information)
    safe_next_steps = get_safe_next_steps()
    risk_level = calculate_risk_level(risk_signals, internship)

    if risk_level == "LOW":
        summary = "No major safety warning was identified from the listing."
    elif risk_level == "MEDIUM":
        summary = "The listing contains one or more signals that deserve verification before proceeding."
    else:
        summary = "The listing contains multiple safety signals that warrant careful verification before proceeding."

    if opportunity_signals:
        summary += f" The listing also provides {len(opportunity_signals)} concrete opportunity signal(s)."
    if missing_information:
        summary += f" {len(missing_information)} important detail(s) are not clearly provided."

    # AI summary is optional, but it must never override the deterministic risk level.
    if ai_summary:
        summary = ai_summary

    return {
        "risk_level": risk_level,
        "risk_signals": risk_signals,
        "opportunity_signals": opportunity_signals,
        "missing_information": missing_information,
        "questions_to_ask": questions,
        "safe_next_steps": safe_next_steps,
        "summary": summary,
    }


def analyze_with_ai(internship):
    internship = internship.strip()
    if not internship:
        raise ValueError("Internship listing cannot be empty.")

    # Deterministic analysis is authoritative for structured fields.
    risk_signals = detect_safety_signals(internship)
    opportunity_signals = detect_opportunity_signals(internship)
    missing_information = detect_missing_information(internship)
    questions = build_questions(missing_information)
    safe_next_steps = get_safe_next_steps()
    risk_level = calculate_risk_level(risk_signals, internship)

    ai_summary = get_ai_summary(internship)
    result = build_result(internship, ai_summary)

    # Final safety guard: never allow the AI to change the risk level.
    result["risk_level"] = risk_level
    result["risk_signals"] = risk_signals
    result["opportunity_signals"] = opportunity_signals
    result["missing_information"] = missing_information
    result["questions_to_ask"] = questions
    result["safe_next_steps"] = safe_next_steps

    return result
