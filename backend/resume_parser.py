"""
Mock response generators.

These produce realistic, JSON-serializable fake AI outputs so the app works
perfectly in offline demos / when no LLM API key is configured. They also
serve as the `mock_response` fallback passed into ai_service.call_llm(),
so if a real API call fails mid-demo, the app degrades gracefully instead
of crashing.
"""
import json
import random


def mock_resume_analysis(scan: dict, target_role: str) -> str:
    langs = scan.get("found_languages") or ["python"]
    frameworks = scan.get("found_frameworks") or ["flask"]
    score = 50
    score += min(len(langs) * 5, 20)
    score += min(len(frameworks) * 4, 16)
    if scan.get("has_internship"):
        score += 10
    if scan.get("has_projects"):
        score += 8
    if scan.get("has_certifications"):
        score += 4
    if scan.get("has_dsa"):
        score += 6
    score = min(score, 96)

    strengths = []
    for l in langs[:3]:
        strengths.append(f"Solid {l.title()} fundamentals")
    if scan.get("has_projects"):
        strengths.append("Hands-on project experience")
    if not strengths:
        strengths = ["Clear resume formatting", "Relevant coursework listed"]

    weaknesses = []
    missing = []
    if not scan.get("has_dsa"):
        weaknesses.append("No visible DSA / problem-solving practice")
        missing.append("Data Structures & Algorithms")
    if not scan.get("has_internship"):
        weaknesses.append("No internship experience listed")
        missing.append("Internship Experience")
    if not scan.get("has_certifications"):
        weaknesses.append("Few certifications to back up skills")
        missing.append("Relevant Certifications")
    missing.append("System Design basics")
    if not weaknesses:
        weaknesses = ["Could quantify project impact more", "Resume could use more depth in one core project"]

    result = {
        "resume_score": score,
        "programming_languages": [l.title() for l in langs] or ["Python"],
        "frameworks_tools": [f.title() for f in frameworks] or ["Flask"],
        "projects": ["Portfolio project (detected in resume)"] if scan.get("has_projects") else [],
        "internships": ["Internship detected in resume"] if scan.get("has_internship") else [],
        "certifications": ["Certification detected in resume"] if scan.get("has_certifications") else [],
        "strengths": strengths[:5],
        "weaknesses": weaknesses[:5],
        "missing_skills": missing[:5],
    }
    return json.dumps(result)


def mock_placement_readiness(profile: dict, resume_summary: dict) -> str:
    base = 45
    try:
        cgpa = float(profile.get("cgpa", 7.0))
    except (TypeError, ValueError):
        cgpa = 7.0
    base += min(int((cgpa - 6) * 6), 18)
    base += min(len(resume_summary.get("programming_languages", [])) * 3, 15)
    if resume_summary.get("internships"):
        base += 12
    if resume_summary.get("projects"):
        base += 8
    readiness = max(20, min(base, 92))
    skill_match = max(15, min(readiness - random.randint(0, 10), 95))

    gaps = [
        {"skill": "Data Structures & Algorithms", "importance": "High",
         "status": "Missing" if "Data Structures & Algorithms" in resume_summary.get("missing_skills", []) else "Weak"},
        {"skill": "System Design", "importance": "Medium", "status": "Missing"},
        {"skill": "Internship Experience", "importance": "High",
         "status": "Missing" if not resume_summary.get("internships") else "Good"},
        {"skill": "Core CS Fundamentals (OS/DBMS/CN)", "importance": "Medium", "status": "Weak"},
        {"skill": f"{profile.get('target_role', 'Role')}-specific tools", "importance": "High", "status": "Weak"},
    ]

    suggestions = [
        "Solve at least 5 DSA problems per day on LeetCode/GFG focused on Arrays, Strings, and Trees",
        "Build one end-to-end project relevant to your target role and deploy it publicly",
        "Revise core CS subjects: OS, DBMS, Computer Networks",
        f"Tailor your resume specifically for {profile.get('target_role', 'your target role')}",
        "Apply for at least one internship or open-source contribution this month",
    ]

    result = {
        "placement_readiness_percentage": readiness,
        "skill_match_percentage": skill_match,
        "skill_gap_analysis": gaps,
        "improvement_suggestions": suggestions,
        "todays_recommended_task": "Solve 5 Array/String problems on LeetCode (Easy-Medium) and time yourself.",
    }
    return json.dumps(result)


def mock_roadmap(profile: dict, weaknesses: list, missing_skills: list, days: int = 30) -> str:
    role = profile.get("target_role", "SDE")
    weeks = [
        {
            "week_number": 1,
            "focus_area": "DSA Foundations",
            "tasks": [
                "Master Arrays & Strings (20 problems)",
                "Learn Time & Space complexity analysis",
                "Revamp resume summary and one project description",
                "Set up LinkedIn + GitHub profile properly",
            ],
        },
        {
            "week_number": 2,
            "focus_area": "Core CS + Linked Structures",
            "tasks": [
                "Linked Lists, Stacks, Queues (15 problems)",
                "DBMS revision: normalization, joins, indexing",
                "Start one new impactful project relevant to " + role,
                "Read 2 company interview experiences on GeeksforGeeks",
            ],
        },
        {
            "week_number": 3,
            "focus_area": "Build & Showcase",
            "tasks": [
                "Finish and deploy the project from Week 2",
                "Trees & Graphs basics (15 problems)",
                "Write a clear README + demo video for the project",
                "Update resume with the new project and quantify impact",
            ],
        },
        {
            "week_number": 4,
            "focus_area": "Interview Readiness",
            "tasks": [
                "2 full mock interviews (DSA + HR round)",
                "Revise System Design basics (if applicable to " + role + ")",
                "Practice behavioral questions using STAR method",
                "Apply to 15+ relevant openings / campus drives",
            ],
        },
    ]
    result = {
        "roadmap_title": f"{days}-Day Roadmap to {role}",
        "total_days": days,
        "weeks": weeks,
    }
    return json.dumps(result)


def mock_mentor_reply(user_message: str, profile: dict) -> str:
    msg = user_message.lower()
    name = profile.get("name", "there")
    company = profile.get("target_company", "your target company")
    role = profile.get("target_role", "your target role")

    if "ready" in msg and ("google" in msg or company.lower() in msg):
        return (f"Honestly {name}, based on your current profile you're at roughly 55-65% readiness for "
                f"{company}. Your fundamentals are okay, but you need stronger DSA practice (aim for 150+ "
                f"problems) and at least one high-impact project. You've got time — stay consistent and "
                f"this is very achievable.")
    if "next" in msg or "learn" in msg:
        return (f"Right now, focus on three things in order: 1) Data Structures & Algorithms — daily "
                f"practice, 2) One strong project aligned with {role}, 3) Core CS subjects (OS/DBMS/CN). "
                f"Skip shiny new frameworks until these are solid — recruiters filter on fundamentals first.")
    if "project" in msg and "review" in msg:
        return ("Share the project details/GitHub link and I'll review it in depth! In general, recruiters "
                "look for: clear problem statement, your specific contribution, technical depth (not just "
                "CRUD), and measurable impact or scale. Add these to make any project stand out.")
    if "resume" in msg:
        return ("To improve your resume: 1) Quantify impact in every bullet (e.g. 'reduced load time by 40%'), "
                "2) Move your strongest project to the top, 3) Add a skills section matched to the job "
                "description, 4) Keep it to one page. Want me to review a specific section?")
    return (f"Good question, {name}. Based on your profile targeting {role} at {company}, I'd suggest "
            f"starting with a focused 30-day plan covering DSA, one solid project, and mock interviews. "
            f"Check your Roadmap tab for the full breakdown, or ask me something more specific!")


def mock_recruiter_simulation(profile: dict, resume_summary: dict, target_company: str) -> str:
    score = 50
    if resume_summary.get("internships"):
        score += 15
    if resume_summary.get("projects"):
        score += 10
    if "Data Structures & Algorithms" not in resume_summary.get("missing_skills", []):
        score += 15
    try:
        cgpa = float(profile.get("cgpa", 7.0))
        if cgpa >= 8.0:
            score += 10
    except (TypeError, ValueError):
        pass
    score = max(15, min(score, 90))
    decision = "Yes" if score >= 60 else "No"

    reject_reasons = []
    if not resume_summary.get("internships"):
        reject_reasons.append("No internship experience")
    if "Data Structures & Algorithms" in resume_summary.get("missing_skills", []):
        reject_reasons.append("Weak DSA preparation signals on resume")
    if len(resume_summary.get("projects", [])) < 2:
        reject_reasons.append("Few impactful/technically deep projects")

    result = {
        "shortlist_decision": decision,
        "shortlist_probability": score,
        "reasoning": (f"As a recruiter at {target_company}, I look for strong fundamentals, at least one "
                      f"substantial project, and relevant experience. This candidate shows "
                      f"{'promising' if score >= 60 else 'developing'} potential but "
                      f"{'meets' if score >= 60 else 'currently falls short of'} our typical bar."),
        "reject_reasons": reject_reasons,
        "missing_requirements": resume_summary.get("missing_skills", ["System Design", "DSA depth"])[:4],
        "suggestions_to_improve": [
            "Complete 100+ DSA problems on LeetCode with a focus on Medium difficulty",
            "Add one full-stack or systems-level project with clear technical depth",
            "Pursue a relevant internship or open-source contribution",
            f"Tailor resume keywords specifically to {target_company}'s job description",
        ],
    }
    return json.dumps(result)
