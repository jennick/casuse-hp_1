import React from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Layout from "./components/Layout";
import RequireAuth from "./components/RequireAuth";

import LoginPage from "./pages/Login";
import DashboardPage from "./pages/Dashboard";
import SellersPage from "./pages/Sellers";
import SellerDetailPage from "./pages/SellerDetail";
import SellerCreatePage from "./pages/SellerCreate";
import QuotesPage from "./pages/Quotes";
import OrdersPage from "./pages/Orders";
import AssignmentsPage from "./pages/Assignments";
import PaymentsPage from "./pages/Payments";
import SettingsPage from "./pages/Settings";
import SellerPasswordResetPage from "./pages/SellerPasswordReset";

// Nieuw: klantenpagina's
import CustomersPage from "./pages/Customers";
import CustomerDetailPage from "./pages/CustomerDetail";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Publieke routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/reset-password" element={<SellerPasswordResetPage />} />

        {/* Beschermde routes binnen de verkoopmodule */}
        <Route
          path="/"
          element={
            <RequireAuth>
              <Layout />
            </RequireAuth>
          }
        >
          <Route index element={<DashboardPage />} />
          <Route path="dashboard" element={<DashboardPage />} />

          {/* Verkopersbeheer */}
          <Route path="sellers" element={<SellersPage />} />
          <Route path="sellers/new" element={<SellerCreatePage />} />
          <Route path="sellers/:id" element={<SellerDetailPage />} />

          {/* Klantenbeheer (nieuw) */}
          <Route path="customers" element={<CustomersPage />} />
          <Route path="customers/:id" element={<CustomerDetailPage />} />

          {/* Overige bestaande pagina's */}
          <Route path="quotes" element={<QuotesPage />} />
          <Route path="orders" element={<OrdersPage />} />
          <Route path="assignments" element={<AssignmentsPage />} />
          <Route path="payments" element={<PaymentsPage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>

        {/* Fallback: onbekende route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
