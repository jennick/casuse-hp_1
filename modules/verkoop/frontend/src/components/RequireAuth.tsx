import React, { ReactNode } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { loadAuthToken } from "../lib/api";

type RequireAuthProps = {
  children: ReactNode;
};

export const RequireAuth: React.FC<RequireAuthProps> = ({ children }) => {
  const location = useLocation();
  const token = loadAuthToken();

  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};
