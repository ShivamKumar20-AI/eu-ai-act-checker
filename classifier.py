import logging
from datetime import datetime
from pathlib import Path

from security import sanitize_input, hash_input
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


# Configure audit logging
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "classification_audit.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def classify(use_case: str) -> Dict:
    # --- Validation ---
    try:
        clean_use_case = sanitize_input(use_case)
    except ValueError as e:
        input_hash = hash_input(use_case)
        logger.warning("Invalid input: input_hash=%s reason=%s", input_hash, str(e))
        return {
            "risk_level": "Error",
            "badge_class": "badge-danger",
            "eu_ai_act_category": "Input Validation Error",
            "verdict": "Invalid input.",
            "matched_trigger": "validation",
            "recommendation": f"Fix input: {str(e)}",
            "why": "The description failed basic security and length checks."
        }

    text = clean_use_case.lower()

    # --- Unacceptable Risk ---
    for keyword in UNACCEPTABLE_KEYWORDS:
        if keyword in text:
            input_hash = hash_input(clean_use_case)
            logger.info(
                "Classification: input_hash=%s risk_level=%s matched_trigger=%s",
                input_hash,
                "Unacceptable Risk",
                keyword,
            )
            return {
                "risk_level": "Unacceptable Risk",
                "badge_class": "badge-danger",
                "eu_ai_act_category": "Title II — Prohibited AI Practices",
                "verdict": "This AI use case is prohibited under the EU AI Act.",
                "matched_trigger": keyword,
                "recommendation": "Do not deploy this system. Escalate to legal and compliance teams immediately.",
                "why": "The description includes a prohibited practice trigger under the EU AI Act risk framework."
            }

    # --- High Risk ---
    for keyword in HIGH_RISK_KEYWORDS:
        if keyword in text:
            input_hash = hash_input(clean_use_case)
            logger.info(
                "Classification: input_hash=%s risk_level=%s matched_trigger=%s",
                input_hash,
                "High Risk",
                keyword,
            )
            return {
                "risk_level": "High Risk",
                "badge_class": "badge-warning",
                "eu_ai_act_category": "Title III — High-Risk AI Systems",
                "verdict": "This AI use case is likely high risk under the EU AI Act.",
                "matched_trigger": keyword,
                "recommendation": "Before deployment, assess conformity requirements, human oversight, record keeping, and risk management obligations.",
                "why": "The use case matches an area commonly associated with high-impact decisions affecting rights, safety, or access."
            }

    # --- Limited Risk ---
    for keyword in LIMITED_RISK_KEYWORDS:
        if keyword in text:
            input_hash = hash_input(clean_use_case)
            logger.info(
                "Classification: input_hash=%s risk_level=%s matched_trigger=%s",
                input_hash,
                "Limited Risk",
                keyword,
            )
            return {
                "risk_level": "Limited Risk",
                "badge_class": "badge-info",
                "eu_ai_act_category": "Transparency Obligations",
                "verdict": "This AI use case appears to have limited risk obligations.",
                "matched_trigger": keyword,
                "recommendation": "Add clear disclosure so users know they are interacting with AI or AI-generated content.",
                "why": "The system appears to trigger transparency expectations rather than full high-risk compliance controls."
            }

    # --- Minimal Risk ---
    input_hash = hash_input(clean_use_case)
    logger.info(
        "Classification: input_hash=%s risk_level=%s matched_trigger=%s",
        input_hash,
        "Minimal Risk",
        "none",
    )

    return {
        "risk_level": "Minimal Risk",
        "badge_class": "badge-success",
        "eu_ai_act_category": "Minimal or No Specific Obligation",
        "verdict": "This AI use case appears to be minimal risk.",
        "matched_trigger": "none",
        "recommendation": "No specific mandatory controls are apparent from this description, but voluntary governance checks are still good practice.",
        "why": "The description does not match any obvious prohibited, high-risk, or limited-risk trigger in this simplified checker."
    }