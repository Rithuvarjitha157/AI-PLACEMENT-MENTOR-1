# 🎓 AI Placement Mentor

An AI-powered career guidance platform that analyzes a student's resume, identifies placement gaps,
and builds a personalized roadmap to improve their hiring chances — like having a personal placement
mentor in your pocket.

Built for hackathon delivery: **fully working offline in mock mode**, and drops in a real LLM key
(OpenAI or Anthropic) with one `.env` change.

---

## ✨ Features

| # | Feature | Description |
|---|---------|--------------|
| 1 | **Student Profile** | Name, college, year, CGPA, target role/company, study hours, current skills |
| 2 | **Resume Upload & Analysis** | PDF text extraction (PyMuPDF) + AI analysis → resume score, strengths, weaknesses, missing skills |
| 3 | **Placement Readiness Analysis** | AI compares profile + resume vs. target role → readiness %, skill gap table, suggestions |
| 4 | **Personalized Roadmap** | AI generates a 30-day week-by-week study plan scaled to available study hours |
| 5 | **AI Career Mentor Chat** | Chatbot that remembers the student's profile & resume context across the conversation |
| 6 | **Recruiter Simulator** | AI role-plays as a recruiter at the target company → shortlist Yes/No, probability, reject reasons, action items |
| — | **Dashboard** | Clean cards: Placement Readiness, Resume Score, Skill Match %, Missing Skills, Today's Task |

---

## 🧱 Tech Stack

- **Frontend:** Flutter (Dart) — clean modern UI, responsive, `provider` for state
- **Backend:** Python Flask REST API
- **Database:** Firebase Firestore (simple 1-collection structure) — with an **in-memory mock DB**
  fallback so you never need Firebase to run the demo
- **AI:** Pluggable LLM layer (OpenAI / Anthropic / Mock) driven by `.env`
- **Resume Parsing:** PyMuPDF (`fitz`) for PDF text extraction

---

## 📁 Project Structure

```
ai-placement-mentor/
├── backend/
│   ├── app.py                     # Flask app + all REST endpoints
│   ├── requirements.txt
│   ├── .env.example
│   ├── services/
│   │   ├── ai_service.py          # LLM abstraction (OpenAI/Anthropic/Mock)
│   │   ├── resume_parser.py       # PyMuPDF text extraction + keyword scan
│   │   └── firebase_service.py    # Firestore + in-memory mock DB
│   └── prompts/
│       └── prompts.py             # All AI prompt templates, centralized
├── frontend/
│   ├── pubspec.yaml
│   └── lib/
│       ├── main.dart
│       ├── theme/app_theme.dart
│       ├── models/student_profile.dart
│       ├── services/
│       │   ├── api_service.dart       # All HTTP calls to Flask backend
│       │   └── session_provider.dart  # App-wide state (Provider)
│       ├── widgets/score_card.dart     # Reusable dashboard cards/chips
│       └── screens/
│           ├── splash_screen.dart
│           ├── profile_screen.dart
│           ├── main_shell.dart          # Bottom nav shell
│           ├── dashboard_screen.dart
│           ├── resume_screen.dart
│           ├── roadmap_screen.dart
│           ├── chat_screen.dart
│           └── recruiter_simulator_screen.dart
├── firebase_setup.md
└── README.md
```

---

## 🚀 Quick Start (Local Demo — Zero API Keys Needed)

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # defaults to LLM_PROVIDER=mock, USE_MOCK_DB=true
python app.py
```

Backend runs at `http://127.0.0.1:5000`. Test it:
```bash
curl http://127.0.0.1:5000/api/health
```

### 2. Frontend

```bash
cd frontend
flutter pub get
flutter run -d chrome     # easiest for a hackathon demo
# or: flutter run -d <device_id> for mobile/emulator
```

> **Important:** In `lib/services/api_service.dart`, set `baseUrl` to match how your backend is reachable:
> - Chrome/web or desktop → `http://127.0.0.1:5000` (default, already set)
> - Android emulator → `http://10.0.2.2:5000`
> - Physical phone on same Wi-Fi → `http://<your-laptop-LAN-IP>:5000`

### 3. Demo Flow
1. Fill in the profile form → Continue
2. Upload a PDF resume → see AI analysis (score, strengths, weaknesses, missing skills)
3. Dashboard auto-loads Placement Readiness, Resume Score, Skill Match, Missing Skills, Today's Task
4. Tap **Roadmap** → see the 30-day week-by-week plan
5. Tap **Mentor** → chat ("Am I ready for Google?", "What should I learn next?")
6. Tap **Recruiter Sim** → run a recruiter screening simulation for your target company

Everything above works **out of the box in mock mode** — no API keys, no Firebase setup required.

---

## 🔑 Enabling a Real LLM (Optional)

Edit `backend/.env`:

```
# Option A: OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# Option B: Anthropic
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-4-6
```

Restart the Flask server. If the real API call ever fails mid-demo (rate limit, network hiccup),
`ai_service.py` automatically falls back to the mock response so your demo never crashes on stage.

---

## 🔥 Enabling Real Firebase Firestore (Optional)

See [`firebase_setup.md`](./firebase_setup.md) for step-by-step instructions. By default the app
uses `USE_MOCK_DB=true`, an in-memory store — fine for any single-session hackathon demo.

---

## 📡 API Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Health check |
| POST | `/api/profile` | Create student profile → returns `student_id` |
| GET | `/api/profile/<student_id>` | Fetch profile |
| PUT | `/api/profile/<student_id>` | Update profile |
| POST | `/api/resume/upload/<student_id>` | Upload PDF (`multipart/form-data`, field `resume`) → AI analysis |
| GET | `/api/resume/analysis/<student_id>` | Fetch last resume analysis |
| GET/POST | `/api/readiness/<student_id>` | Placement readiness % + skill gap analysis |
| GET/POST | `/api/roadmap/<student_id>?days=30` | Personalized roadmap |
| POST | `/api/chat/<student_id>` | Send message to AI mentor `{ "message": "..." }` |
| GET | `/api/chat/<student_id>/history` | Chat history |
| POST | `/api/recruiter-simulator/<student_id>` | Run recruiter simulation `{ "target_company": "..." }` |
| GET | `/api/dashboard/<student_id>` | Aggregated dashboard summary |

---

## 🛠️ Design Notes / Why This Architecture

- **Mock-first design**: Every AI call and DB call has a deterministic mock fallback. This means
  the app is always demoable — judges' Wi-Fi, API rate limits, or missing Firebase credentials
  never break the flow.
- **Centralized prompts** (`prompts/prompts.py`): Easy to tune AI behavior without touching route
  logic — useful for last-minute demo polishing.
- **Simple Firestore schema**: One `students` collection, one document per student, with nested
  maps for each feature's output. No complex joins needed for an MVP.
- **Provider for Flutter state**: Lightweight, no boilerplate — perfect for hackathon speed.

---

## 🩹 Troubleshooting

- **"Could not extract any text from this PDF"** → the PDF is likely a scanned image; use a
  text-based PDF resume (e.g., exported from Word/Google Docs).
- **Flutter can't reach backend** → double-check `baseUrl` in `api_service.dart` matches your
  platform (see Quick Start above), and confirm the Flask server is running.
- **Firestore errors** → make sure `USE_MOCK_DB=true` unless you've completed `firebase_setup.md`.

---

Built to be demoed in under 36 hours. Good luck at the hackathon! 🚀
