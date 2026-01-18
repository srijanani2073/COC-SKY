import { useAuth } from "../context/AuthContext";

export default function TopBar() {
  const { user, logout } = useAuth();

  return (
    <div className="topbar">
      <div className="app-name">Chain of Custody System</div>
      <div className="user-info">
        {user.username} | {user.role}
        <button onClick={logout}>Logout</button>
      </div>
    </div>
  );
}