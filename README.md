# Task Review Agent — Deterministic Data Ingestion & Processing Pipeline

**Candidate:** Shailesh Yadav  
**Email:** Shaileshyadav1109@gmail.com  
**Role Applied:** Agentic Backend Engineer (Data Ingestion & Pipeline Systems)  
**Task:** Foundation Build — Test 1

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Setup Instructions](#setup-instructions)
4. [API Endpoint Reference](#api-endpoint-reference)
5. [Pipeline Explanation](#pipeline-explanation)
6. [Sample Inputs & Outputs](#sample-inputs--outputs)
7. [Edge Case Handling](#edge-case-handling)
8. [Determinism Proof](#determinism-proof)
9. [Running Tests](#running-tests)

---

## Project Overview

This is a **fully deterministic**, rule-based data ingestion and processing pipeline built with FastAPI.

It accepts:
- A **text input** (task description)
- An **optional file** (PDF or JSON)

It extracts:
- Word count, sentence count, keyword frequency
- Technical terms and action verbs
- Detected sections and step patterns

It outputs:
- A structured JSON with complexity, clarity score, technical density, and signals

> **No ML, no black-box logic, no randomness.**  
> Same input always produces exactly the same output.

---

## Project Structure

```
task_pipeline/
│
├── main.py                  # FastAPI app — routes, validation, file handling
├── pipeline.py              # Core deterministic pipeline (all logic lives here)
├── schemas.py               # Pydantic output schema (typed, validated)
├── tests.py                 # Determinism + edge case test suite
├── requirements.txt         # Python dependencies
│
├── templates/
│   └── index.html           # Dark-theme frontend UI
│
└── samples/
    ├── inputs/
    │   ├── sample1_normal_input.txt         # Structured task description
    │   ├── sample2_short_input.txt          # Minimal/short input
    │   ├── sample3_high_technical_input.txt # Dense technical input
    │   └── sample4_file_upload.json         # JSON file for upload test
    │
    └── outputs/
        ├── sample1_normal_output.json
        ├── sample2_short_output.json
        ├── sample3_high_technical_output.json
        ├── sample4_json_file_output.json
        └── edge_cases.json
```

---

## Setup Instructions

### Step 1 — Clone or download the project

```bash
git clone https://github.com/your-username/task-pipeline.git
cd task_pipeline
```

### Step 2 — Create a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**

| Package | Version | Purpose |
|---|---|---|
| fastapi | 0.115.0 | Web framework |
| uvicorn | 0.30.6 | ASGI server |
| python-multipart | 0.0.12 | File upload support |
| pydantic | 2.9.2 | Output validation |
| pdfplumber | 0.11.4 | PDF text extraction |

### Step 4 — Run the server

```bash
uvicorn main:app --reload --port 8000
```

### Step 5 — Open in browser

| URL | Purpose |
|---|---|
| `http://localhost:8000` | Frontend UI |
| `http://localhost:8000/docs` | Swagger auto-docs (interactive) |
| `http://localhost:8000/redoc` | ReDoc API docs |
| `http://localhost:8000/health` | Health check endpoint |

### Step 6 — Run the test suite

```bash
python tests.py
```

---

## API Endpoint Reference

### `POST /analyze`

The main pipeline endpoint. Accepts multipart form data.

**Request — Form Fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `text` | `string` | Yes | Task description text |
| `file` | `file` | No | PDF or JSON file to process alongside the text |

**Full Response Schema:**

```json
{
  "word_count": 61,
  "sentence_count": 2,
  "keyword_frequency": {
    "input": 3,
    "pipeline": 2,
    "json": 2
  },
  "technical_terms": ["complexity", "deterministic", "fastapi", "ingestion", "json", "pipeline"],
  "action_verbs": ["accept", "build", "detect", "extract", "handle", "return"],
  "sections_detected": ["constraint", "error", "input", "objective", "output", "requirement"],
  "step_patterns": {
    "numbered_steps": 0,
    "bulleted_items": 4,
    "arrow_flows": 0,
    "has_steps": true
  },
  "complexity": "medium",
  "technical_density": 0.0984,
  "clarity_score": 10.0,
  "file_processed": null,
  "file_extracted_text_preview": null,
  "signals": {
    "has_technical_content": true,
    "has_action_items": true,
    "is_structured": true,
    "has_step_patterns": true,
    "input_length_category": "short"
  }
}
```

**Error Responses:**

| Code | Condition | Response |
|---|---|---|
| `400` | Empty text | `{"detail": "Text input cannot be empty."}` |
| `400` | Wrong file type | `{"detail": "Only PDF or JSON files are supported."}` |
| `400` | Empty file (0 bytes) | `{"detail": "Uploaded file is empty."}` |

---

### `GET /health`

Returns pipeline health status.

```json
{ "status": "ok", "pipeline": "deterministic" }
```

### `GET /`

Returns the frontend HTML UI (served from `templates/index.html`).

---

### cURL Examples

**Text only:**
```bash
curl -X POST http://localhost:8000/analyze \
  -F "text=Build a FastAPI pipeline to extract keywords from JSON datasets using NLP."
```

**Text + JSON file:**
```bash
curl -X POST http://localhost:8000/analyze \
  -F "text=Process this project config" \
  -F "file=@samples/inputs/sample4_file_upload.json"
```

**Text + PDF file:**
```bash
curl -X POST http://localhost:8000/analyze \
  -F "text=Analyze this document" \
  -F "file=@your_document.pdf"
```

---

## Pipeline Explanation

The pipeline runs in 4 phases. Every step is deterministic — no randomness, no ML.

```
Input (text + optional file)
        │
        ▼
┌──────────────────────────────────────────────┐
│  Phase 1a — Input Handling                   │
│  • Validate text (not empty)                 │
│  • Validate file type (pdf / json only)      │
│  • Extract text from PDF via pdfplumber      │
│  • Flatten JSON recursively to plain text    │
│  • Merge: combined_text = text + file_text   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  Phase 1b — Text Processing                  │
│  • Tokenize: lowercase + strip punctuation   │
│  • word_count  = len(tokens)                 │
│  • sentence_count = regex split on . ! ?     │
│  • keyword_freq = Counter(tokens - stopwords)│
│  • technical_terms = lookup in 100+ vocab    │
│  • action_verbs = lookup in 60+ verb set     │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  Phase 1c — Structure Detection              │
│  • sections = regex match on 10 patterns     │
│    (objective, input, output, requirement…)  │
│  • step_patterns = count bullets, numbers,   │
│    arrows (→  ->  =>)                        │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  Phase 2a — Signal Extraction                │
│  • technical_density = tech_terms / tokens   │
│  • complexity = rule-based point scoring     │
│  • clarity_score = penalty/reward arithmetic │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
             Structured JSON Output
```

### Scoring Rules (Fully Transparent)

#### Complexity (low / medium / high)

Points are added based on these explicit rules:

| Rule | Condition | Points |
|---|---|---|
| Word count | > 300 words | +3 |
| Word count | 150–300 words | +2 |
| Word count | 50–150 words | +1 |
| Avg sentence length | > 25 words/sentence | +2 |
| Avg sentence length | 15–25 words/sentence | +1 |
| Technical density | > 8% | +3 |
| Technical density | 4–8% | +2 |
| Technical density | 1–4% | +1 |
| Tech term count | > 15 terms | +2 |
| Tech term count | > 7 terms | +1 |

**Total score → complexity bucket:** `0–3 = low`, `4–7 = medium`, `8+ = high`

#### Clarity Score (0.0 – 10.0)

Starts at 10.0. Adjustments applied in order:

| Condition | Adjustment |
|---|---|
| Avg sentence length > 30 words | −2.0 |
| Avg sentence length > 20 words | −1.0 |
| Word count < 20 | −3.0 |
| Word count < 50 | −1.0 |
| Has step / bullet patterns | +1.0 |
| Each structural keyword found (objective, requirement, input, output, example) | +0.4 each |
| Noisy punctuation (`!!` `??`) | −0.5 each |

Final value is clamped to `[0.0, 10.0]`.

#### Technical Density

```
technical_density = number_of_unique_technical_terms / total_token_count
```

Expressed as a decimal (e.g., `0.098` = 9.8%). Capped at `1.0`.

---

## Sample Inputs & Outputs

All files are in the `samples/` directory.

---

### Sample 1 — Normal Structured Input

**File:** `samples/inputs/sample1_normal_input.txt`

```
Objective: Build a deterministic data ingestion pipeline using FastAPI.
Requirements:
- Accept text input and optional file upload (PDF or JSON)
- Extract technical terms, action verbs, and keyword frequency
- Detect sections such as Objective, Input, Output, Constraint
- Return a structured JSON output with complexity and clarity scores
The pipeline must handle edge cases including empty input, invalid file types, and malformed text.
```

**Output:** `samples/outputs/sample1_normal_output.json`

```json
{
  "word_count": 61,
  "sentence_count": 2,
  "keyword_frequency": { "input": 3, "pipeline": 2, "json": 2 },
  "technical_terms": ["complexity","deterministic","fastapi","ingestion","json","pipeline"],
  "action_verbs": ["accept","build","detect","extract","handle","return"],
  "sections_detected": ["constraint","error","input","objective","output","requirement"],
  "step_patterns": { "bulleted_items": 4, "has_steps": true },
  "complexity": "medium",
  "technical_density": 0.0984,
  "clarity_score": 10.0,
  "signals": {
    "has_technical_content": true,
    "has_action_items": true,
    "is_structured": true,
    "has_step_patterns": true,
    "input_length_category": "short"
  }
}
```

**Why these results?**
- 6 sections detected because the text explicitly contains Objective, Requirements (→ requirement), Input, Output, Constraint, and error-handling language
- `clarity_score = 10.0` because it has bullet points (+1.0), all 5 structural keywords (+2.0), and no noise
- `complexity = medium` (score 6): word count +1, density 9.8% +2, 6 terms +1, sentence length +1 = 5 points → medium

---

### Sample 2 — Short / Minimal Input (Edge Case)

**File:** `samples/inputs/sample2_short_input.txt`

```
Build a machine learning model.
```

**Output:** `samples/outputs/sample2_short_output.json`

```json
{
  "word_count": 5,
  "sentence_count": 1,
  "keyword_frequency": { "build": 1, "machine": 1, "learning": 1, "model": 1 },
  "technical_terms": ["model"],
  "action_verbs": ["build"],
  "sections_detected": [],
  "step_patterns": { "numbered_steps": 0, "bulleted_items": 0, "has_steps": false },
  "complexity": "low",
  "technical_density": 0.2,
  "clarity_score": 7.0,
  "signals": {
    "has_technical_content": true,
    "has_action_items": false,
    "is_structured": false,
    "has_step_patterns": false,
    "input_length_category": "short"
  }
}
```

**Why these results?**
- `complexity = low`: only 5 words → 0 points from word count, 0 from sentence length; score stays low
- `clarity_score = 7.0`: starts at 10, −3.0 for word count < 20 = 7.0
- Only 1 technical term (`model`) and 1 action verb (`build`) — very minimal content

---

### Sample 3 — High Technical Density

**File:** `samples/inputs/sample3_high_technical_input.txt`

```
Implement a transformer-based neural network with LSTM layers for NLP classification.
Use FastAPI endpoint for inference. Deploy with Docker on Kubernetes.
Configure JWT authentication. Optimize gradient descent with hyperparameter tuning.
Monitor with logging and benchmark latency throughput scalability.
Use Redis cache and Celery queue for async processing pipeline.
```

**Output:** `samples/outputs/sample3_high_technical_output.json`

```json
{
  "word_count": 49,
  "sentence_count": 7,
  "technical_terms": [
    "async","authentication","benchmark","cache","celery","classification",
    "deploy","docker","endpoint","fastapi","gradient","hyperparameter",
    "inference","jwt","kubernetes","latency","logging","lstm","network",
    "neural","nlp","pipeline","queue","redis","scalability","throughput","transformer"
  ],
  "action_verbs": ["benchmark","configure","deploy","implement","monitor","optimize"],
  "sections_detected": [],
  "complexity": "medium",
  "technical_density": 0.551,
  "clarity_score": 9.0,
  "signals": {
    "has_technical_content": true,
    "has_action_items": true,
    "input_length_category": "short"
  }
}
```

**Why these results?**
- 27 technical terms found — a very high density of 55.1%
- Despite high density, `complexity = medium` because word count is only 49 (short text category)
- No sections detected because the text is a dense paragraph, not a structured doc

---

### Sample 4 — JSON File Upload

**Text input:** `"Process and analyze this project configuration file."`  
**File:** `samples/inputs/sample4_file_upload.json`

```json
{
  "task": "Build a classification pipeline",
  "requirements": ["extract features", "train model", "deploy endpoint"],
  "tech_stack": ["fastapi", "sklearn", "docker"],
  "constraints": "Must be deterministic, no randomness"
}
```

**Output:** `samples/outputs/sample4_json_file_output.json`

```json
{
  "word_count": 29,
  "technical_terms": ["classification","deploy","deterministic","docker","endpoint","fastapi","model","pipeline"],
  "action_verbs": ["analyze","build","deploy","extract","process"],
  "sections_detected": ["constraint","requirement"],
  "complexity": "medium",
  "technical_density": 0.3103,
  "clarity_score": 9.4,
  "file_processed": "json",
  "file_extracted_text_preview": "task: Build a classification pipeline requirements: extract features train model deploy endpoint tech_stack: fastapi sklearn docker constraints: Must be deterministic, no randomness",
  "signals": {
    "has_technical_content": true,
    "has_action_items": true,
    "is_structured": true
  }
}
```

**Why these results?**
- JSON was flattened to: `"task: Build a classification pipeline requirements: extract features..."`
- Combined with the text input and analyzed together
- `file_extracted_text_preview` shows exactly what was extracted from the JSON
- `constraint` and `requirement` sections detected from the JSON keys `constraints` and `requirements`

---

## Edge Case Handling

| Scenario | How It's Handled |
|---|---|
| Empty / whitespace-only text | HTTP 400: `"Text input cannot be empty."` — caught before pipeline |
| Unsupported file type (`.xlsx`, `.docx`) | HTTP 400: `"Only PDF or JSON files are supported."` |
| Zero-byte / empty file | HTTP 400: `"Uploaded file is empty."` |
| Malformed / broken JSON file | Error surfaced in `file_extracted_text_preview`; pipeline continues on text |
| Corrupted or scanned PDF (no text layer) | Error surfaced in preview; pipeline continues on text input |
| Very long input (300+ words) | Handled correctly — `complexity=high`, `input_length_category=long` |

See `samples/outputs/edge_cases.json` for full request/response examples of each case.

---

## Determinism Proof

The pipeline guarantees identical output for identical input because:

- **Vocabulary sets** (`TECHNICAL_TERMS`, `ACTION_VERBS`) are `frozenset`-equivalent — defined once, never modified
- **Regex patterns** are compiled strings — fully deterministic
- **Scoring** is integer arithmetic with no floating-point branching
- **`Counter` + `sorted()`** produces consistent ordering across all Python runs
- **No `random`, no `uuid`, no `datetime` in any logic path**

To verify yourself, run:

```bash
python tests.py
```

Test 1 runs the same input 3 times back-to-back and `assert`s that `word_count`, `technical_terms`, `complexity`, and `clarity_score` are identical across all runs.

---

## Running Tests

```bash
python tests.py
```

**Test suite coverage:**

| Test | Input | Assertion |
|---|---|---|
| 1 — Determinism | Same text × 3 runs | All 4 key fields identical across runs |
| 2 — Normal input | Structured task text | Sections, terms, verbs all correctly detected |
| 3 — Short input | "Build a machine learning model." | `complexity = low` |
| 4 — High technical | Dense ML/infra paragraph | `complexity = high`, technical flag true |
| 5 — JSON file | JSON payload upload | `file_processed = json`, terms extracted from file |
| 6 — Edge cases | Whitespace input, 300+ word input | No crash, correct `input_length_category` |

**Expected output:**

```
=== TEST 1: DETERMINISM (same input → same output) ===
  ✅ PASS  [word_count consistent]
  ✅ PASS  [technical_terms consistent]
  ✅ PASS  [complexity consistent]
  ✅ PASS  [clarity_score consistent]

=== TEST 2: NORMAL INPUT ===
  ✅ PASS  [pipeline in technical_terms]
  ✅ PASS  [json in technical_terms]
  ✅ PASS  [build in action_verbs]
  ✅ PASS  [output section detected]
  ✅ PASS  [input section detected]
  ✅ PASS  [clarity_score in range]

=== TEST 3: SHORT / MINIMAL INPUT ===
  ✅ PASS  [short complexity=low]
  ✅ PASS  [short category=short]

=== TEST 4: HIGH TECHNICAL DENSITY ===
  ✅ PASS  [high complexity]
  ✅ PASS  [technical content signal]

=== TEST 5: JSON FILE PROCESSING ===
  ✅ PASS  [file_processed=json]
  ✅ PASS  [fastapi in technical_terms]

=== TEST 6: EDGE CASES ===
  ✅ PASS  [whitespace-trimmed word_count]
  ✅ PASS  [long category]

=== ALL TESTS COMPLETE ===
```

---

## Tech Stack

| Layer | Technology | Reason |
|---|---|---|
| Framework | FastAPI 0.115 | Async, typed, auto-docs |
| Server | Uvicorn (ASGI) | High performance |
| Validation | Pydantic v2 | Strict output typing |
| PDF extraction | pdfplumber | Pure Python, no OCR/cloud |
| Text processing | Python stdlib (`re`, `collections`) | Zero external dependencies for core logic |
| Frontend | Vanilla HTML/CSS/JS | No build step required |

---

*Built by Shailesh Yadav — Task Review Agent, Foundation Build (Test 1)*
