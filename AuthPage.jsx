import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { api } from "../api/apiClient";

const SessionContext = createContext(null);

const STORAGE_KEY = "apm_student_id";

export function SessionProvider({ children }) {
  const [studentId, setStudentIdState] = useState(null);
  const [profile, setProfile] = useState(null);
  const [resumeAnalysis, setResumeAnalysis] = useState(null);
  const [readiness, setReadiness] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [bootstrapping, setBootstrapping] = useState(true);

  const setStudentId = useCallback((id) => {
    setStudentIdState(id);
    if (id) {
      localStorage.setItem(STORAGE_KEY, id);
    } else {
      localStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  const refreshResumeAnalysis = useCallback(async (id) => {
    try {
      const res = await api.getResumeAnalysis(id);
      setResumeAnalysis(res.resume_analysis);
      return res.resume_analysis;
    } catch {
      setResumeAnalysis(null);
      return null;
    }
  }, []);

  const refreshReadiness = useCallback(async (id) => {
    const res = await api.getReadiness(id);
    setReadiness(res.placement_readiness);
    return res.placement_readiness;
  }, []);

  const refreshRoadmap = useCallback(async (id, days = 30) => {
    const res = await api.getRoadmap(id, days);
    setRoadmap(res.roadmap);
    return res.roadmap;
  }, []);

  const logout = useCallback(() => {
    setStudentId(null);
    setProfile(null);
    setResumeAnalysis(null);
    setReadiness(null);
    setRoadmap(null);
  }, [setStudentId]);

  // On first load, try to resume a session from localStorage
  useEffect(() => {
    const savedId = localStorage.getItem(STORAGE_KEY);
    if (!savedId) {
      setBootstrapping(false);
      return;
    }
    (async () => {
      try {
        const profileRes = await api.getProfile(savedId);
        setStudentIdState(savedId);
        setProfile(profileRes);
        await refreshResumeAnalysis(savedId);
      } catch {
        localStorage.removeItem(STORAGE_KEY);
      } finally {
        setBootstrapping(false);
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const value = {
    studentId,
    setStudentId,
    profile,
    setProfile,
    resumeAnalysis,
    setResumeAnalysis,
    readiness,
    setReadiness,
    roadmap,
    setRoadmap,
    refreshResumeAnalysis,
    refreshReadiness,
    refreshRoadmap,
    logout,
    bootstrapping,
    hasResume: !!resumeAnalysis,
  };

  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
}

export function useSession() {
  const ctx = useContext(SessionContext);
  if (!ctx) throw new Error("useSession must be used within a SessionProvider");
  return ctx;
}
