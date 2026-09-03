# 🇪🇺 EU AI Act Compliance Checker

A REST API and Streamlit UI that screens AI use cases against a simplified version of the EU AI Act risk framework and classifies them as **Unacceptable**, **High**, **Limited**, or **Minimal** risk.

## Demo Results

Example use cases tested against the live API / UI:

| Use case | Risk level | EU AI Act category |
|----------|------------|--------------------|
| Real-time biometric identification of citizens in public spaces | Unacceptable Risk | Title II — Prohibited AI Practices |
| AI tool that screens job applicants and ranks CVs | High Risk | Title III — High-Risk AI Systems |
| Customer service chatbot handling product enquiries | Limited Risk | Transparency Obligations |
| Movie recommendation engine based on viewing history | Minimal Risk | Minimal or No Specific Obligation |

Each response includes:

- `risk_level` – Unacceptable / High / Limited / Minimal  
- `badge_class` – CSS class for UI badge (danger/warning/info/success)  
- `eu_ai_act_category` – Human-readable category label  
- `verdict` – One-line summary in plain language  
- `matched_trigger` – The keyword that triggered the classification  
- `recommendation` – Next compliance action  
- `why` – Short explanation of the logic used  

**Note:** This is a simplified screening tool for learning and portfolio purposes. It does not replace formal legal advice or a full AI risk assessment.

## 🔒 Security controls (demo)

This demo includes basic security and governance controls suitable for a portfolio/educational project:

- **Input validation & sanitisation** (`security.py`)  
  - Enforces minimum/maximum input length  
  - Blocks obviously malicious patterns (e.g. script tags, dangerous shell commands)  
  - Returns clear error messages for invalid input  

- **Audit logging** (`classifier.py` + `logs/`)  
  - Logs every classification attempt to `logs/classification_audit.log`  
  - Records timestamp, risk level, matched trigger, and a **hash** of the input (not raw text)  
  - Supports traceability and post‑hoc review without storing sensitive data in logs  

- **Rate limiting** (`streamlit_app.py`)  
  - Limits the number of classification requests per minute per browser session  
  - Shows a user‑friendly error when the limit is exceeded  
  - Demonstrates basic abuse prevention for interactive demos  

- **Secrets handling pattern** (`secrets_helper.py`, `.env.example`, `.gitignore`)  
  - Uses `python-dotenv` to load environment variables from a local `.env` file  
  - Provides a `get_secret()` helper for future API keys or credentials  
  - Ensures `.env` is ignored by Git so secrets are never committed  

These controls are intentionally lightweight but illustrate good practices around input validation, logging, abuse prevention, and secret management — aligned with themes from the EU AI Act (robustness, logging, technical documentation) and general application security guidance.

## Tech Stack

| Layer | Technology |
|-------|------------|
| API | FastAPI |
| UI | Streamlit |
| Language | Python 3.11+ |
| Risk logic | Keyword-based rules approximating EU AI Act risk tiers |
| Security helpers | Custom `security.py` + `secrets_helper.py`, `python-dotenv` |

## Project Structure

```text
eu-ai-act-checker/
├── main.py              # FastAPI app and /check endpoint
├── classifier.py        # Risk classification rules and logic
├── security.py          # Input validation, hashing, sanitisation
├── secrets_helper.py    # Environment variable / secrets helper
├── streamlit_app.py     # Streamlit UI for interactive use
├── requirements.txt     # Python dependencies
├── .env.example         # Example env file (do not commit real .env)
├── .gitignore
├── logs/
│   └── classification_audit.log  # Audit log (generated at runtime)
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ShivamKumar20-AI/eu-ai-act-checker.git
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

The API will be live at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 5. Run the Streamlit UI (optional but recommended)

```bash
streamlit run streamlit_app.py
```

Open the URL shown in your terminal (usually [http://localhost:8501](http://localhost:8501)).

## API Usage

### Endpoint

`POST /check`

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

## How the Classification Works

1. The API/Streamlit app passes the `use_case` string through `security.sanitize_input()` for length and pattern checks.
2. The cleaned text is converted to lowercase.
3. It checks for keywords associated with:
   - **Unacceptable Risk** (e.g. real-time biometric identification, social scoring).
   - **High Risk** (e.g. recruitment, credit scoring, law enforcement, medical diagnosis, education, critical infrastructure).
   - **Limited Risk** (e.g. chatbots, deepfakes, synthetic media).
4. If a keyword is found, the corresponding risk level, category, and recommendation are returned.
5. If no keywords match, the system defaults to **Minimal Risk** with a suggestion to still apply voluntary governance checks.

This mirrors the four risk tiers defined in the EU AI Act (unacceptable, high, limited, minimal) in a simplified, programmatic form suitable for early-stage AI governance tooling.

## Limitations

- Rule-based and keyword-driven — does not understand full legal context or nuanced descriptions.  
- Not a substitute for legal advice or a full AI impact assessment.  
- Intended for learning, portfolio demonstration, and early triage, not production compliance decisions.  
- Security controls (validation, logging, rate limiting, secrets pattern) are demo-grade, not production-hardened.

## Author

**Shivam Kumar** — AI Governance Analyst & AI Engineer  
[GitHub](https://github.com/ShivamKumar20-AI/eu-ai-act-checker)
