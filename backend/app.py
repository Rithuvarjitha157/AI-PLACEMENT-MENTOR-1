"""
AI Placement Mentor - Flask Backend
=====================================
Main application entry point. Defines all REST API endpoints.

Run with:  python app.py
Default port: 5000 (configurable via .env)
"""
import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from services import ai_service, resume_parser, firebase_service, mock_data
from prompts import prompts

app = Flask(__name__)
CORS(app)  # allow Flutter web/mobile client to call freely during dev

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "AI Placement Mentor API"})


# ---------------------------------------------------------------------------
# 1. STUDENT PROFILE
# ---------------------------------------------------------------------------
@app.route("/api/profile", methods=["POST"])
def create_profile():
    """Create a new student profile. Returns student_id used by all other endpoints."""
    data = request.get_json(force=True) or {}
    required = ["name", "college", "year", "cgpa", "target_role", "target_company", "study_hours"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400

    data.setdefault("current_skills", [])
    student_id = firebase_service.create_student(data)
    return jsonify({"student_id": student_id, "profile": data}), 201


@app.route("/api/profile/<student_id>", methods=["GET"])
def get_profile(student_id):
    student = firebase_service.get_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student)


@app.route("/api/profile/<student_id>", methods=["PUT"])
def update_profile(student_id):
    data = request.get_json(force=True) or {}
    student = firebase_service.get_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    firebase_service.update_student(student_id, data)
    return jsonify({"student_id": student_id, "updated": True})


# ---------------------------------------------------------------------------
# 2. RESUME UPLOAD & ANALYSIS
# ---------------------------------------------------------------------------
@app.route("/api/resume/upload/<student_id>", methods=["POST"])
def upload_resume(student_id):
    student = firebase_service.get_student(student_id)
    if not student:
        return jsonify({"error": "Student not found. Create a profile first."}), 404

    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded. Use form field name 'resume'."}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    filename = f"{student_id}_{uuid.uuid4().hex[:6]}.pdf"
    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)

    try:
        resume_text = resume_parser.extract_text_from_pdf(filepath)
    except Exception as e:
        return jsonify({"error": f"Failed to parse PDF: {e}"}), 500

    if not resume_text:
        return jsonify({"error": "Could not extract any text from this PDF. Try a text-based PDF, not a scanned image."}), 422

    scan = resume_parser.quick_keyword_scan(resume_text)
    target_role = student.get("target_role", "SDE")

    prompt = prompts.resume_analysis_prompt(resume_text, target_role)
    mock_fallback = mock_data.mock_resume_analysis(scan, target_role)
    raw = ai_service.call_llm(prompt, mock_response=mock_fallback)
    analysis = ai_service.safe_json_parse(raw, fallback=ai_service.safe_json_parse(mock_fallback, {}))

    firebase_service.update_student(student_id, {
        "resume_text": resume_text[:10000],
        "resume_analysis": analysis,
    })

    return jsonify({"student_id": student_id, "resume_analysis": analysis})


@app.route("/api/resume/analysis/<student_id>", methods=["GET"])
def get_resume_analysis(student_id):
    student = firebase_service.get_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    analysis = student.get("resume_analysis")
    if not analysis:
        return jsonify({"error": "No resume analyzed yet for this student"}), 404
    return jsonify({"student_id": student_id, "resume_analysis": analysis})


# ---------------------------------------------------------------------------
# 3. PLACEMENT READINESS ANALYSIS
# ---------------------------------------------------------------------------
@app.route("/api/readiness/<student_id>", methods=["GET", "POST"])
def placement_readiness(student_id):
    student = firebase_service.get_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    resume_summary = student.get("resume_analysis")
    if not resume_summary:
        return jsonify({"error": "Upload and analyze a resume first"}), 400

    prompt = prompts.placement_readiness_prompt(student, resume_summary)
    mock_fallback = mock_data.mock_placement_readiness(student, resume_summary)
    raw = ai_service.call_llm(prompt, mock_response=mock_fallback)
    readiness = ai_service.safe_json_parse(raw, fallback=ai_service.safe_json_parse(mock_fallback, {}))

    firebase_service.update_student(student_id, {"placement_readiness": readiness})
    return jsonify({"student_id": student_id, "placement_readiness": readiness})


# ---------------------------------------------------------------------------
# 4. PERSONALIZED ROADMAP
# ---------------------------------------------------------------------------
@app.route("/api/roadmap/<student_id>", methods=["GET", "POST"])
def generate_roadmap(student_id):
    student = firebase_service.get_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    resume_summary = student.get("resume_analysis", {}) or {}
    weaknesses = resume_summary.get("weaknesses", [])
    missing_skills = resume_summary.get("missing_skills", [])

    days = request.args.get("days", default=30, type=int) if request.method == "GET" else \
        (request.get_json(silent=True) or {}).get("days", 30)

    prompt = prompts.roadmap_prompt(student, weaknesses, missing_skills, days)
    mock_fallback = mock_data.mock_roadmap(student, weaknesses, missing_skills, days)
    raw = ai_service.call_llm(prompt, mock_response=mock_fallback)
    roadmap = ai_service.safe_json_parse(raw, fallback=ai_service.safe_json_parse(mock_fallback, {}))

    firebase_service.update_student(student_id, {"roadmap": roadmap})
    return jsonify({"student_id": student_id, "roadmap": roadmap})


# ---------------------------------------------------------------------------
# 5. AI CAREER MENTOR CHAT
# ---------------------------------------------------------------------------
@app.route("/api/chat/<student_id>", methods=["POST"])
def mentor_chat(student_id):
    student = firebase_service.get_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(force=True) or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    resume_summary = student.get("resume_analysis", {}) or {}
    system_prompt = prompts.mentor_chat_system_prompt(student, resume_summary)
    mock_reply = mock_data.mock_mentor_reply(user_message, student)

    reply = ai_service.call_llm(user_message, system=system_prompt, mock_response=mock_reply)

    firebase_service.append_chat_message(student_id, "user", user_message)
    firebase_service.append_chat_message(student_id, "mentor", reply)

    return jsonify({"student_id": student_id, "reply": reply})


@app.route("/api/chat/<student_id>/history", methods=["GET"])
def chat_history(student_id):
    student = firebase_service.get_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"student_id": student_id, "history": firebase_service.get_chat_history(student_id)})


# ---------------------------------------------------------------------------
# 6. RECRUITER SIMULATOR
# ---------------------------------------------------------------------------
@app.route("/api/recruiter-simulator/<student_id>", methods=["POST"])
def recruiter_simulator(student_id):
    student = firebase_service.get_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(silent=True) or {}
    target_company = data.get("target_company") or student.get("target_company", "the company")

    resume_summary = student.get("resume_analysis")
    if not resume_summary:
        return jsonify({"error": "Upload and analyze a resume first"}), 400

    prompt = prompts.recruiter_simulator_prompt(resume_summary, student, target_company)
    mock_fallback = mock_data.mock_recruiter_simulation(student, resume_summary, target_company)
    raw = ai_service.call_llm(prompt, mock_response=mock_fallback)
    simulation = ai_service.safe_json_parse(raw, fallback=ai_service.safe_json_parse(mock_fallback, {}))

    firebase_service.append_recruiter_simulation(student_id, {
        "target_company": target_company,
        **simulation,
    })

    return jsonify({"student_id": student_id, "target_company": target_company, "simulation": simulation})


# ---------------------------------------------------------------------------
# DASHBOARD (aggregate endpoint for convenience)
# ---------------------------------------------------------------------------
@app.route("/api/dashboard/<student_id>", methods=["GET"])
def dashboard(student_id):
    student = firebase_service.get_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    resume_analysis = student.get("resume_analysis", {}) or {}
    readiness = student.get("placement_readiness", {}) or {}

    return jsonify({
        "student_id": student_id,
        "profile": {
            "name": student.get("name"),
            "target_role": student.get("target_role"),
            "target_company": student.get("target_company"),
        },
        "resume_score": resume_analysis.get("resume_score"),
        "placement_readiness_percentage": readiness.get("placement_readiness_percentage"),
        "skill_match_percentage": readiness.get("skill_match_percentage"),
        "missing_skills": resume_analysis.get("missing_skills", []),
        "todays_recommended_task": readiness.get("todays_recommended_task"),
    })


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", "5000"))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    print(f"🚀 AI Placement Mentor API running on http://0.0.0.0:{port}")
    print(f"   LLM_PROVIDER = {os.getenv('LLM_PROVIDER', 'mock')}")
    print(f"   USE_MOCK_DB  = {os.getenv('USE_MOCK_DB', 'true')}")
    app.run(host="0.0.0.0", port=port, debug=debug)
