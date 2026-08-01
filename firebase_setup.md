# Firebase Firestore Setup (Optional for Demo)

The backend runs perfectly **without Firebase** in mock mode (`USE_MOCK_DB=true` in `.env`),
using an in-memory store — great for a hackathon demo. Use these steps only if you want
persistent storage with real Firestore.

## 1. Create a Firebase Project
1. Go to https://console.firebase.google.com/
2. Click **Add Project** → name it e.g. `ai-placement-mentor`
3. Disable Google Analytics (not needed) → Create project

## 2. Enable Firestore
1. In the left sidebar, go to **Build → Firestore Database**
2. Click **Create database**
3. Choose **Start in test mode** (fine for hackathon demo; tighten rules for production)
4. Pick a region close to you → Enable

## 3. Generate a Service Account Key
1. Go to **Project Settings** (gear icon) → **Service Accounts**
2. Click **Generate new private key**
3. Save the downloaded JSON file as `firebase_credentials.json` inside the `backend/` folder
   (this file is already gitignored — never commit it)

## 4. Update your `.env`
```
USE_MOCK_DB=false
FIREBASE_CREDENTIALS_PATH=firebase_credentials.json
```

## Firestore Data Structure (kept intentionally simple)

```
students (collection)
  └── {student_id} (document)
        ├── name: string
        ├── college: string
        ├── year: string
        ├── cgpa: number
        ├── target_role: string
        ├── target_company: string
        ├── study_hours: number
        ├── current_skills: array<string>
        ├── resume_text: string
        ├── resume_analysis: map
        │     ├── resume_score: number
        │     ├── programming_languages: array
        │     ├── frameworks_tools: array
        │     ├── projects: array
        │     ├── internships: array
        │     ├── certifications: array
        │     ├── strengths: array
        │     ├── weaknesses: array
        │     └── missing_skills: array
        ├── placement_readiness: map
        │     ├── placement_readiness_percentage: number
        │     ├── skill_match_percentage: number
        │     ├── skill_gap_analysis: array<map>
        │     ├── improvement_suggestions: array
        │     └── todays_recommended_task: string
        ├── roadmap: map
        │     ├── roadmap_title: string
        │     ├── total_days: number
        │     └── weeks: array<map>
        ├── chat_history: array<map> { role, message, timestamp }
        └── recruiter_simulations: array<map>
```

That's it — one collection, one document per student. No subcollections needed for the MVP.
