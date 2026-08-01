import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { SessionProvider } from "./context/SessionContext";
import AppLayout from "./layouts/AppLayout";
import AuthPage from "./pages/AuthPage";
import DashboardPage from "./pages/DashboardPage";
import ResumeUploadPage from "./pages/ResumeUploadPage";
import SkillGapPage from "./pages/SkillGapPage";
import RoadmapPage from "./pages/RoadmapPage";
import ChatbotPage from "./pages/ChatbotPage";
import MockInterviewPage from "./pages/MockInterviewPage";

export default function App() {
  return (
    <SessionProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/auth" element={<AuthPage />} />

          <Route element={<AppLayout />}>
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/resume" element={<ResumeUploadPage />} />
            <Route path="/skill-gap" element={<SkillGapPage />} />
            <Route path="/roadmap" element={<RoadmapPage />} />
            <Route path="/mentor" element={<ChatbotPage />} />
            <Route path="/mock-interview" element={<MockInterviewPage />} />
          </Route>

          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </SessionProvider>
  );
}
