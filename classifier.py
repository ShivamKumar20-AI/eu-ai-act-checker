from typing import Dict

UNACCEPTABLE_KEYWORDS = [
    "social scoring", "mass surveillance", "real-time biometric",
    "subliminal manipulation", "exploit vulnerabilities", "emotion recognition school",
    "emotion recognition workplace"
]

HIGH_RISK_KEYWORDS = [
    "recruitment", "hiring", "cv screening", "job applicant",
    "credit scoring", "loan", "insurance", "benefits",
    "criminal", "law enforcement", "border control",
    "medical", "diagnosis", "clinical", "healthcare",
    "education", "exam", "student assessment",
    "critical infrastructure", "energy", "water", "transport",
    "biometric identification"
]

LIMITED_RISK_KEYWORDS = [
    "chatbot", "deepfake", "synthetic media", "ai-generated",
    "virtual assistant", "emotion detection"
]

def classify(use_case: str) -> Dict:
    text = use_case.lower()

    for keyword in UNACCEPTABLE_KEYWORDS:
        if keyword in text:
            return {
                "risk_level": "Unacceptable Risk",
                "badge_class": "badge-danger",
                "eu_ai_act_category": "Title II — Prohibited AI Practices",
                "verdict": "This AI use case is prohibited under the EU AI Act.",
                "matched_trigger": keyword,
                "recommendation": "Do not deploy this system. Escalate to legal and compliance teams immediately.",
                "why": "The description includes a prohibited practice trigger under the EU AI Act risk framework."
            }

    for keyword in HIGH_RISK_KEYWORDS:
        if keyword in text:
            return {
                "risk_level": "High Risk",
                "badge_class": "badge-warning",
                "eu_ai_act_category": "Title III — High-Risk AI Systems",
                "verdict": "This AI use case is likely high risk under the EU AI Act.",
                "matched_trigger": keyword,
                "recommendation": "Before deployment, assess conformity requirements, human oversight, record keeping, and risk management obligations.",
                "why": "The use case matches an area commonly associated with high-impact decisions affecting rights, safety, or access."
            }

    for keyword in LIMITED_RISK_KEYWORDS:
        if keyword in text:
            return {
                "risk_level": "Limited Risk",
                "badge_class": "badge-info",
                "eu_ai_act_category": "Transparency Obligations",
                "verdict": "This AI use case appears to have limited risk obligations.",
                "matched_trigger": keyword,
                "recommendation": "Add clear disclosure so users know they are interacting with AI or AI-generated content.",
                "why": "The system appears to trigger transparency expectations rather than full high-risk compliance controls."
            }

    return {
        "risk_level": "Minimal Risk",
        "badge_class": "badge-success",
        "eu_ai_act_category": "Minimal or No Specific Obligation",
        "verdict": "This AI use case appears to be minimal risk.",
        "matched_trigger": "none",
        "recommendation": "No specific mandatory controls are apparent from this description, but voluntary governance checks are still good practice.",
        "why": "The description does not match any obvious prohibited, high-risk, or limited-risk trigger in this simplified checker."
    }