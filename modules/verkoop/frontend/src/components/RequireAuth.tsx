import React from "react";
import { Navigate, useLocation } from "react-router-dom";

interface RequireAuthProps {
  children: React.ReactNode;
}

/**
 * Simple auth guard for the verkoopmodule.
 * We only check for a localStorage token for now.
 * Later this can be wired to real JWT from Casuse-Core.
 */
const RequireAuth: React.FC<RequireAuthProps> = ({ children }) => {
  const location = useLocation();

  let token: string | null = null;
  if (typeof window !== "undefined") {
    try {
      token = localStorage.getItem("verkoop_access_token");
    } catch {
      token = null;
    }
  }

  if (!token) {
    // Not authenticated: send to login page, remember where we came from
    return (
      <Navigate
        to="/login"
        replace
        state={{ from: location }}
      />
    );
  }

  return <>{children}</>;
};

export default RequireAuth;
