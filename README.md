# Smart Resume Analyzer — Module 1 & Module 4

This is the Flask backend implementation of two modules from the
"Smart Resume Analyzer with AI-Based Feedback" capstone project:

- **Module 1 — Resume Score Analyzer**: scores a resume out of 100 across six weighted sections.
- **Module 4 — Smart Feedback System**: takes Module 1's output and generates personalized feedback.

## Project Structure

```
resume_analyzer/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── modules/
│   │   ├── resume_score_analyzer.py     # Module 1 logic
│   │   └── smart_feedback_system.py     # Module 4 logic
│   ├── routes/
│   │   └── api_routes.py        # Flask API endpoints
│   └── utils/
│       └── section_detector.py  # Shared section-detection logic
├── run.py                       # App entry point
└── requirements.txt
```

## Setup

```bash
cd resume_analyzer
pip install -r requirements.txt
python run.py
```

The server starts at `http://localhost:5000`.

## Module 1 — `/api/resume-score` (POST)

**Request:**
```json
{ "resume_text": "John Doe john@email.com ... SKILLS Python SQL ..." }
```

**Response:**
```json
{
  "resume_score": 74,
  "contact_score": 10,
  "education_score": 15,
  "skills_score": 20,
  "projects_score": 20,
  "experience_score": 0,
  "certification_score": 9,
  "missing_sections": ["experience"],
  "section_details": { "...": "per-section detection info" }
}
```

Note: `missing_sections` and `section_details` are extras beyond the
original spec's example JSON — they're what let Module 4 work without
re-scanning the resume text from scratch. The six score fields match
your spec exactly.

## Module 4 — `/api/resume-feedback` (POST)

**Request:**
```json
{
  "resume_score": 74,
  "resume_text": "...",
  "missing_sections": ["experience"],
  "skills_found": ["python", "sql", "java"],
  "section_details": { "...optional, improves accuracy..." }
}
```

**Response:**
```json
{
  "overall_feedback": "Good, but needs improvement. ...",
  "strengths": ["Contact information is complete...", "..."],
  "improvements": ["No work experience or internship details were found."],
  "recommendations": ["Include internships, training programs, ..."]
}
```

## Combined endpoint (bonus) — `/api/analyze-resume` (POST)

Runs Module 1 then feeds its output straight into Module 4, returning
both results in one call. Useful for the Module 5 dashboard so it
doesn't have to call two endpoints and wire the data together itself.

```json
{ "resume_text": "..." }
```
returns
```json
{ "score_analysis": { ... }, "feedback": { ... } }
```

## How the scoring logic works

`app/utils/section_detector.py` scans the resume text for six sections:

- **Contact**: detected via regex (email, phone, LinkedIn, GitHub URLs) — no heading needed.
- **Education / Projects / Experience / Certifications**: detected by searching for common heading variants (e.g. "experience", "internship", "work experience") and capturing the text until the next heading.
- **Skills**: detected by heading, and cross-checked against a list of ~35 common technical/professional keywords.

Each section is marked `present` (found at all) and `detailed` (has
enough content — e.g. 15+ words, or 5+ skill keywords, or 2+ contact
channels). Scoring then applies:

- Missing → 0 marks
- Present but brief → 60% of that section's max marks
- Present and detailed → 100% of max marks

(Skills uses a slightly different tiered scale based on skill count: 0 / 30% / 60% / 100%.)

## How the feedback logic works

`app/modules/smart_feedback_system.py` is pure rule-based logic (no ML/LLM, per the project's scope limitations):

1. **Overall feedback** comes from the score band (`<50`, `50–75`, `>75`), exact wording as specified in your prompt.
2. **Strengths** are sections that are both present and detailed.
3. **Improvements + recommendations** are generated per the exact rules you listed (missing projects → suggest projects, weak skills → suggest skills, missing experience → suggest internships/freelancing, missing certifications → suggest certifications), plus two extra rules for education/contact since Module 1 scores those too.

## Testing manually with curl

```bash
curl -X POST http://localhost:5000/api/analyze-resume \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "Email: a@b.com Phone: 9876543210 SKILLS Python SQL Flask Git Docker PROJECTS Built a resume analyzer using Flask and NLP."}'
```

## Notes / things you may want to extend later

- `section_detector.py` uses simple keyword/regex matching rather than spaCy/NLTK NLP parsing. This was a deliberate choice to keep Module 1 fast and dependency-light, but you can swap in spaCy NER (e.g. to pull out degree names or job titles) without changing the API contract — only `section_detector.py` would need to change.
- The skill keyword list in `section_detector.py` is intentionally short (~35 terms). You'll likely want to expand it per target role (this pairs naturally with your Module 3: ATS Keyword Checker, which already plans role-based keyword lists).
- There's no file upload handling here yet (that's Module 1 in your original doc — "Resume Upload and Parsing"). This code assumes `resume_text` has already been extracted from the PDF/DOCX. If you want, I can build that upload+parsing piece next so it feeds directly into this scorer.
