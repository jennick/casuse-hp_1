import { useEffect, useState } from "react";

import CustomersTable from "./CustomersTable";
import { apiFetch } from "@/shared/api/apiClient";

/* =========================================================
   Types
   ========================================================= */

type Customer = {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  has_login: boolean;            // ✅ juiste naam
  portal_status?: string;        // ✅ optioneel, maar nuttig
};


type CustomersResponse = {
  items: Customer[];
};

/* =========================================================
   Component
   ========================================================= */

export default function CustomersPage() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCustomers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function fetchCustomers() {
    try {
      setLoading(true);
      setError(null);

      const response = await apiFetch<CustomersResponse>(
        "/api/admin/customers?status=all"
      );

      // Backend retourneert { items: [...] }
      setCustomers(response.items ?? []);
    } catch (err) {
      console.error("Failed to fetch customers", err);
      setError("Kon klanten niet laden.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="customers-page">
      {/* =====================================================
          Header
          ===================================================== */}
      <header className="page-header">
        <h1>Klanten</h1>
        <p>Overzicht van alle geregistreerde klanten.</p>
      </header>

      {/* =====================================================
          States
          ===================================================== */}
      {loading && <div>Klanten laden…</div>}
      {error && <div>{error}</div>}

      {!loading && !error && (
        <CustomersTable customers={customers} />
      )}
    </div>
  );
}
