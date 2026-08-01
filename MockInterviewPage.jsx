import { Outlet, Navigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import { useSession } from "../context/SessionContext";

export default function AppLayout() {
  const { studentId, bootstrapping } = useSession();

  if (bootstrapping) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-paper">
        <div className="font-mono-score text-slate-text text-sm animate-pulse">
          Loading your session…
        </div>
      </div>
    );
  }

  if (!studentId) {
    return <Navigate to="/auth" replace />;
  }

  return (
    <div className="flex min-h-screen bg-paper">
      <Sidebar />
      <main className="flex-1 min-w-0">
        <div className="max-w-6xl mx-auto px-8 py-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
