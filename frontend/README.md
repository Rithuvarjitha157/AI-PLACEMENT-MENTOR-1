# AI Placement Mentor — React Frontend

React + Tailwind web frontend that connects to your existing Flask backend
(`backend/app.py` in the parent project). No backend changes needed — CORS is
already enabled there.

## Pages

| Route | Page | Backend endpoint(s) used |
|---|---|---|
| `/auth` | Login/Register (create profile or resume by Student ID) | `POST /api/profile`, `GET /api/profile/:id` |
| `/dashboard` | Student dashboard (score cards) | `GET /api/dashboard/:id`, `GET /api/readiness/:id` |
| `/resume` | Resume upload & analysis | `POST /api/resume/upload/:id` |
| `/skill-gap` | Skill gap analysis | `GET /api/readiness/:id` |
| `/roadmap` | Personalized roadmap | `GET /api/roadmap/:id?days=N` |
| `/mentor` | AI career mentor chatbot | `POST /api/chat/:id`, `GET /api/chat/:id/history` |
| `/mock-interview` | Recruiter simulator | `POST /api/recruiter-simulator/:id` |

## ⚠️ Important note on auth

Your Flask backend has **no password-based login** — only `POST /api/profile`
to create a student and get back a `student_id`. So the "Login/Register" page
is built honestly around what the backend actually supports:

- **New here** → fills the profile form → calls `POST /api/profile` → stores
  the returned `student_id` in `localStorage` and starts the session.
- **Resume session** → enter a previously-issued `student_id` → calls
  `GET /api/profile/:id` to verify it exists → resumes the session.

If you want real email/password auth later, add a small auth layer to the
Flask backend (e.g. Firebase Auth or a `users` collection with hashed
passwords) and swap `ResumeSessionForm` in `AuthPage.jsx` for a real login
call — the rest of the app doesn't need to change since everything keys off
`studentId` in `SessionContext`.

## Setup

```bash
cd frontend-web
npm install
cp .env.example .env    # point VITE_API_BASE_URL at your Flask backend
npm run dev
```

Opens at `http://localhost:5173`. Make sure the Flask backend
(`cd ../backend && python app.py`) is running at the URL in `.env`
(default `http://127.0.0.1:5000`).

## Folder structure

```
frontend-web/
├── src/
│   ├── main.jsx                  # entry point
│   ├── App.jsx                   # routes
│   ├── index.css                 # Tailwind + global styles
│   ├── api/apiClient.js          # all HTTP calls to Flask
│   ├── context/SessionContext.jsx# studentId + cached data, replaces auth state
│   ├── layouts/AppLayout.jsx     # sidebar shell + route guard
│   ├── components/
│   │   ├── Sidebar.jsx
│   │   ├── ReadinessGauge.jsx    # signature radial score dial
│   │   └── UiKit.jsx             # Card, SkillChip, StatusBadge, etc.
│   └── pages/
│       ├── AuthPage.jsx
│       ├── DashboardPage.jsx
│       ├── ResumeUploadPage.jsx
│       ├── SkillGapPage.jsx
│       ├── RoadmapPage.jsx
│       ├── ChatbotPage.jsx
│       └── MockInterviewPage.jsx
├── tailwind.config.js            # design tokens (colors, fonts)
├── vite.config.js
└── package.json
```

## Design system

- **Colors**: `paper #F4F6F9` (background), `ink #14182B` (dark surfaces/text),
  `signal #FFB100` (highlight accent), `ready #14B8A6` (good/success),
  `gap #FF6B5E` (missing/danger).
- **Type**: Space Grotesk (headlines), Public Sans (body), JetBrains Mono
  (every score/percentage — deliberate "scoreboard" treatment).
- **Signature element**: `ReadinessGauge` — a radial mission-control style dial
  used consistently for every score in the app (resume score, skill match,
  placement readiness), instead of generic progress bars.

## Notes

- I couldn't run `npm install` / `npm run dev` in the sandbox that generated
  this code (no network access), so run those yourself as the first step —
  I manually verified bracket/paren balance across all files, but a real
  `npm run dev` will catch anything environment-specific.
- `recharts` is included in `package.json` in case you want to add charts
  (e.g. a skill-match-over-time trend) — not required for the current pages.
