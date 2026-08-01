import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, ApiError } from "../api/apiClient";
import { useSession } from "../context/SessionContext";

const ROLES = [
  "SDE",
  "AI Engineer",
  "Data Analyst",
  "Data Scientist",
  "Frontend Developer",
  "Backend Developer",
  "Full Stack Developer",
  "DevOps Engineer",
];

const YEARS = ["1st Year", "2nd Year", "3rd Year", "4th Year", "Final Year"];

export default function AuthPage() {
  const [mode, setMode] = useState("register"); // "register" | "resume"
  const navigate = useNavigate();
  const { setStudentId, setProfile } = useSession();

  return (
    <div className="min-h-screen bg-ink text-white flex items-center justify-center px-6">
      <div className="w-full max-w-5xl grid md:grid-cols-2 gap-0 rounded-card overflow-hidden shadow-card">
        {/* Left panel — brand / thesis */}
        <div className="hidden md:flex flex-col justify-between bg-ink-soft p-10 border-r border-white/10">
          <div>
            <div className="font-display font-bold text-2xl">
              Placement<span className="text-signal">Mentor</span>
            </div>
            <p className="text-white/50 text-sm mt-2">Prep season control center</p>
          </div>
          <div>
            <p className="font-display text-3xl leading-tight text-white/90">
              You don't need more advice.
              <br />
              You need a <span className="text-signal">score</span>, a{" "}
              <span className="text-ready">gap list</span>, and a{" "}
              <span className="text-white">plan</span>.
            </p>
            <p className="text-white/40 text-sm mt-6">
              Upload your resume once — get your readiness score, missing skills, a day-by-day
              roadmap, and a recruiter who tells you the truth.
            </p>
          </div>
          <div className="font-mono-score text-xs text-white/30">v1.0 — hackathon build</div>
        </div>

        {/* Right panel — form */}
        <div className="bg-paper text-ink p-10">
          <div className="flex gap-2 mb-8 bg-ink/5 rounded-lg p-1 w-fit">
            <TabButton active={mode === "register"} onClick={() => setMode("register")}>
              New here
            </TabButton>
            <TabButton active={mode === "resume"} onClick={() => setMode("resume")}>
              Resume session
            </TabButton>
          </div>

          {mode === "register" ? (
            <RegisterForm
              onSuccess={(id, profile) => {
                setStudentId(id);
                setProfile(profile);
                navigate("/resume");
              }}
            />
          ) : (
            <ResumeSessionForm
              onSuccess={(id, profile) => {
                setStudentId(id);
                setProfile(profile);
                navigate("/dashboard");
              }}
            />
          )}
        </div>
      </div>
    </div>
  );
}

function TabButton({ active, onClick, children }) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 rounded-md text-sm font-semibold transition-colors ${
        active ? "bg-white shadow-sm text-ink" : "text-slate-text hover:text-ink"
      }`}
    >
      {children}
    </button>
  );
}

function Field({ label, children }) {
  return (
    <label className="block mb-4">
      <span className="block text-xs font-semibold text-slate-text uppercase tracking-wide mb-1.5">
        {label}
      </span>
      {children}
    </label>
  );
}

const inputClass =
  "w-full px-4 py-2.5 rounded-lg border border-ink/10 bg-white text-sm focus:border-signal outline-none";

function RegisterForm({ onSuccess }) {
  const [form, setForm] = useState({
    name: "",
    college: "",
    year: "3rd Year",
    cgpa: "",
    target_role: "SDE",
    target_company: "",
    study_hours: 3,
    current_skills: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const update = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);

    if (!form.name.trim() || !form.college.trim() || !form.target_company.trim()) {
      setError("Please fill in name, college, and target company.");
      return;
    }
    const cgpaNum = parseFloat(form.cgpa);
    if (isNaN(cgpaNum) || cgpaNum < 0 || cgpaNum > 10) {
      setError("CGPA must be a number between 0 and 10.");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        name: form.name.trim(),
        college: form.college.trim(),
        year: form.year,
        cgpa: cgpaNum,
        target_role: form.target_role,
        target_company: form.target_company.trim(),
        study_hours: Number(form.study_hours),
        current_skills: form.current_skills
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean),
      };
      const res = await api.createProfile(payload);
      onSuccess(res.student_id, { ...payload, student_id: res.student_id });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h1 className="font-display text-2xl font-bold mb-1">Create your profile</h1>
      <p className="text-slate-text text-sm mb-6">
        Takes 30 seconds. This powers every score and recommendation you'll see.
      </p>

      <div className="grid grid-cols-2 gap-x-4">
        <Field label="Full name">
          <input className={inputClass} value={form.name} onChange={update("name")} placeholder="Riya Sharma" />
        </Field>
        <Field label="College">
          <input
            className={inputClass}
            value={form.college}
            onChange={update("college")}
            placeholder="ABC Institute of Tech"
          />
        </Field>
        <Field label="Year">
          <select className={inputClass} value={form.year} onChange={update("year")}>
            {YEARS.map((y) => (
              <option key={y}>{y}</option>
            ))}
          </select>
        </Field>
        <Field label="CGPA">
          <input
            className={inputClass}
            value={form.cgpa}
            onChange={update("cgpa")}
            placeholder="8.2"
            inputMode="decimal"
          />
        </Field>
        <Field label="Target role">
          <select className={inputClass} value={form.target_role} onChange={update("target_role")}>
            {ROLES.map((r) => (
              <option key={r}>{r}</option>
            ))}
          </select>
        </Field>
        <Field label="Target company">
          <input
            className={inputClass}
            value={form.target_company}
            onChange={update("target_company")}
            placeholder="Google"
          />
        </Field>
      </div>

      <Field label={`Study hours / day — ${form.study_hours}h`}>
        <input
          type="range"
          min="1"
          max="12"
          value={form.study_hours}
          onChange={update("study_hours")}
          className="w-full accent-signal"
        />
      </Field>

      <Field label="Current skills (comma separated)">
        <input
          className={inputClass}
          value={form.current_skills}
          onChange={update("current_skills")}
          placeholder="Python, React, SQL"
        />
      </Field>

      {error && <p className="text-gap text-sm mb-4">{error}</p>}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-ink text-white font-semibold py-3 rounded-lg hover:bg-ink-soft transition-colors disabled:opacity-50"
      >
        {loading ? "Creating profile…" : "Create profile & continue"}
      </button>
    </form>
  );
}

function ResumeSessionForm({ onSuccess }) {
  const [studentId, setId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    if (!studentId.trim()) {
      setError("Enter your Student ID.");
      return;
    }
    setLoading(true);
    try {
      const profile = await api.getProfile(studentId.trim());
      onSuccess(studentId.trim(), profile);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? "No student found with that ID. Double-check it or create a new profile."
          : "Something went wrong. Is the backend running?"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h1 className="font-display text-2xl font-bold mb-1">Resume your session</h1>
      <p className="text-slate-text text-sm mb-6">
        Enter the Student ID you received when you first created your profile.
      </p>
      <Field label="Student ID">
        <input
          className={`${inputClass} font-mono-score`}
          value={studentId}
          onChange={(e) => setId(e.target.value)}
          placeholder="e.g. 3c8e7fec"
        />
      </Field>
      {error && <p className="text-gap text-sm mb-4">{error}</p>}
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-ink text-white font-semibold py-3 rounded-lg hover:bg-ink-soft transition-colors disabled:opacity-50"
      >
        {loading ? "Looking you up…" : "Continue"}
      </button>
    </form>
  );
}
