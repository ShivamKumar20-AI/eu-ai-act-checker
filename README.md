# EU AI Act Compliance Checker API

A REST API that screens AI use cases against a simplified version of the EU AI Act risk framework and classifies them as **Unacceptable**, **High**, **Limited**, or **Minimal** risk.

---

## Demo Results

Example use cases tested against the live API:

| Use case | Risk level | EU AI Act category |
|---------|------------|--------------------|
| Real-time biometric identification of citizens in public spaces | Unacceptable Risk | Title II — Prohibited AI Practices |
| AI tool that screens job applicants and ranks CVs | High Risk | Title III — High-Risk AI Systems |
| Customer service chatbot handling product enquiries | Limited Risk | Transparency Obligations |
| Movie recommendation engine based on viewing history | Minimal Risk | Minimal or No Specific Obligation |

Each response includes:

- `risk_level` – Unacceptable / High / Limited / Minimal  
- `eu_ai_act_category` – Human-readable category label  
- `verdict` – One-line summary in plain language  
- `matched_trigger` – The keyword that triggered the classification  
- `recommendation` – Next compliance action  
- `why` – Short explanation of the logic used  

> **Note:** This is a simplified screening tool for learning and portfolio purposes. It does not replace formal legal advice or a full AI risk assessment.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| API | FastAPI |
| Language | Python 3.11+ |
| Risk logic | Keyword-based rules approximating EU AI Act risk tiers |

---

## Project Structure

```text
eu-ai-act-checker/
├── main.py          # FastAPI app and /check endpoint
├── classifier.py    # Risk classification rules and logic
├── requirements.txt # Python dependencies
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YourGitHub/eu-ai-act-checker.git
cd eu-ai-act-checker
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn main:app --reload
```

The API will be live at `http://127.0.0.1:8000`.

---

## API Usage

### Endpoint

```text
POST /check
```

### Request

Send a JSON body with a `use_case` field:

```bash
curl -X POST "http://127.0.0.1:8000/check" \
     -H "Content-Type: application/json" \
     -d '{"use_case": "An AI tool that screens job applicants and ranks CVs for recruitment decisions."}'
```

### Example Response

```json
{
  "risk_level": "High Risk",
  "badge_class": "badge-warning",
  "eu_ai_act_category": "Title III — High-Risk AI Systems",
  "verdict": "This AI use case is likely high risk under the EU AI Act.",
  "matched_trigger": "recruitment",
  "recommendation": "Before deployment, assess conformity requirements, human oversight, record keeping, and risk management obligations.",
  "why": "The use case matches an area commonly associated with high-impact decisions affecting rights, safety, or access."
}
```

---

## How the Classification Works

1. The API converts the `use_case` string to lowercase.
2. It checks for keywords associated with:
   - **Unacceptable Risk** (e.g. real-time biometric identification, social scoring).
   - **High Risk** (e.g. recruitment, credit scoring, law enforcement, medical diagnosis, education, critical infrastructure).
   - **Limited Risk** (e.g. chatbots, deepfakes, synthetic media).
3. If a keyword is found, the corresponding risk level, category, and recommendation are returned.
4. If no keywords match, the system defaults to **Minimal Risk** with a suggestion to still apply voluntary governance checks.

This mirrors the four risk tiers defined in the EU AI Act (unacceptable, high, limited, minimal) in a simplified, programmatic form suitable for early-stage AI governance tooling.

---

## Limitations

- Rule-based and keyword-driven — does not understand full legal context or nuanced descriptions.
- Not a substitute for legal advice or a full AI impact assessment.
- Intended for learning, portfolio demonstration, and early triage, not production compliance decisions.

---

## Author

**Shivam Kumar** — AI Governance Analyst & AI Engineer

[GitHub Profile](https://github.com/ShivamKumar20-AI)