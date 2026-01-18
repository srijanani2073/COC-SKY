import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Cases from "./pages/Cases";
import Evidence from "./pages/Evidence";
import Timeline from "./pages/Timeline";
import Reports from "./pages/Reports";
import Alerts from "./pages/Alerts";
import TopBar from "./components/TopBar";
import Sidebar from "./components/Sidebar";
import ProtectedRoute from "./components/ProtectedRoute";
import { useAuth } from "./context/AuthContext";
import { RBAC } from "./config/rbac";
import Custody from "./pages/Custody";

export default function App() {
  const { user } = useAuth();
  if (!user) return <Login />;

  return (
    <div className="app-layout">
      <TopBar />
      <div className="body-area">
        <Sidebar />
        <div className="content-area">
          <Routes>
            <Route path="/" element={
              <ProtectedRoute allowedRoles={RBAC.Dashboard}>
                <Dashboard />
              </ProtectedRoute>
            } />

            <Route path="/cases" element={
              <ProtectedRoute allowedRoles={RBAC.Cases}>
                <Cases />
              </ProtectedRoute>
            } />

            <Route path="/evidence" element={
              <ProtectedRoute allowedRoles={RBAC.Evidence}>
                <Evidence />
              </ProtectedRoute>
            } />

            <Route path="/timeline" element={
              <ProtectedRoute allowedRoles={RBAC.Timeline}>
                <Timeline />
              </ProtectedRoute>
            } />

            <Route path="/reports" element={
              <ProtectedRoute allowedRoles={RBAC.Reports}>
                <Reports />
              </ProtectedRoute>
            } />

            <Route path="/alerts" element={
              <ProtectedRoute allowedRoles={RBAC.Alerts}>
                <Alerts />
              </ProtectedRoute>
            } />

            <Route path="*" element={<Navigate to="/" />} />
            <Route path="/custody" element={
              <ProtectedRoute allowedRoles={RBAC.Custody}>
                <Custody />
              </ProtectedRoute>
            }/>
          </Routes>
        </div>
      </div>
    </div>
  );
}