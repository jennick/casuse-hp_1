import { Routes, Route, Navigate } from "react-router-dom";

import LoginPage from "@/modules/website-admin/LoginPage";
import CustomersPage from "@/admin/customers/CustomersPage";
import CustomerDetailPage from "@/admin/customers/CustomerDetailPage";
import CustomerEditPage from "@/admin/customers/CustomerEditPage";

import AdminLayout from "@/admin/layout/AdminLayout";
import ProtectedRoute from "@/shared/auth/ProtectedRoute";
import { getWebsiteAdminToken } from "@/shared/auth/tokens";

/**
 * Entry route:
 * - token → /customers
 * - geen token → /login
 */
function EntryRedirect() {
  const token = getWebsiteAdminToken();
  return <Navigate to={token ? "/customers" : "/login"} replace />;
}

export default function AppRoutes() {
  return (
    <Routes>
      {/* ENTRYPOINT */}
      <Route path="/" element={<EntryRedirect />} />

      {/* LOGIN */}
      <Route path="/login" element={<LoginPage />} />

      {/* ADMIN (BESCHERMD) */}
      <Route element={<ProtectedRoute />}>
        <Route element={<AdminLayout />}>
          <Route path="/customers" element={<CustomersPage />} />
          <Route path="/customers/:id" element={<CustomerDetailPage />} />
          <Route path="/customers/:id/edit" element={<CustomerEditPage />} />
        </Route>
      </Route>

      {/* FALLBACK */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
