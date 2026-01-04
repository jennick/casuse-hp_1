import { Navigate, Outlet } from "react-router-dom";
import { getWebsiteAdminToken } from "@/shared/auth/tokens";

export default function ProtectedRoute() {
  const token = getWebsiteAdminToken();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
