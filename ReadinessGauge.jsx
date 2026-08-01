/**
 * Centralized API client for the AI Placement Mentor Flask backend.
 *
 * Set VITE_API_BASE_URL in a `.env` file at the project root to point at
 * your running Flask server, e.g.:
 *   VITE_API_BASE_URL=http://127.0.0.1:5000
 */
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function handleResponse(res) {
  let body = null;
  try {
    body = await res.json();
  } catch {
    // non-JSON response
  }
  if (!res.ok) {
    throw new ApiError(body?.error || `Request failed (${res.status})`, res.status);
  }
  return body;
}

async function get(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  return handleResponse(res);
}

async function post(path, body) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  return handleResponse(res);
}

async function put(path, body) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  return handleResponse(res);
}

async function uploadFile(path, file, fieldName = "resume") {
  const formData = new FormData();
  formData.append(fieldName, file);
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    body: formData,
  });
  return handleResponse(res);
}

export const api = {
  health: () => get("/api/health"),

  // Profile
  createProfile: (profile) => post("/api/profile", profile),
  getProfile: (studentId) => get(`/api/profile/${studentId}`),
  updateProfile: (studentId, data) => put(`/api/profile/${studentId}`, data),

  // Resume
  uploadResume: (studentId, file) => uploadFile(`/api/resume/upload/${studentId}`, file),
  getResumeAnalysis: (studentId) => get(`/api/resume/analysis/${studentId}`),

  // Placement Readiness
  getReadiness: (studentId) => get(`/api/readiness/${studentId}`),

  // Roadmap
  getRoadmap: (studentId, days = 30) => get(`/api/roadmap/${studentId}?days=${days}`),

  // Mentor Chat
  sendChatMessage: (studentId, message) => post(`/api/chat/${studentId}`, { message }),
  getChatHistory: (studentId) => get(`/api/chat/${studentId}/history`),

  // Recruiter Simulator
  runRecruiterSimulation: (studentId, targetCompany) =>
    post(`/api/recruiter-simulator/${studentId}`, { target_company: targetCompany }),

  // Dashboard
  getDashboard: (studentId) => get(`/api/dashboard/${studentId}`),
};

export { ApiError };
