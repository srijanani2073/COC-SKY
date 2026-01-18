import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { RBAC } from "../config/rbac";
import "../styles/sidebar.css";

export default function Sidebar() {
  const { user } = useAuth();
  const canSee = (screen) => RBAC[screen].includes(user.role);

  return (
    <div className="sidebar">
      {canSee("Dashboard") && <NavLink to="/">Dashboard</NavLink>}
      {canSee("Cases") && <NavLink to="/cases">Cases</NavLink>}
      {canSee("Evidence") && <NavLink to="/evidence">Evidence</NavLink>}
      {canSee("Timeline") && <NavLink to="/timeline">Timeline</NavLink>}
      {canSee("Reports") && <NavLink to="/reports">Reports</NavLink>}
      {canSee("Alerts") && <NavLink to="/alerts">Alerts</NavLink>}
      {canSee("Custody") && <NavLink to="/custody">Custody</NavLink>}
    </div>
  );
}