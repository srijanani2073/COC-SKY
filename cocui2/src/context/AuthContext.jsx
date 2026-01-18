import { createContext, useContext, useState } from "react";

const AuthContext = createContext();
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const login = (username, password) => {
    let role = "Viewer";

    if (username === "admin") role = "Admin";
    else if (username === "investigator") role = "Investigator";
    else if (username === "analyst") role = "Analyst";

    setUser({ username, role });
  };

  const logout = () => setUser(null);
  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
export const useAuth = () => useContext(AuthContext);