import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../lib/api";

interface CustomerListItem {
  id: number;
  website_customer_id: string;
  email: string;
  first_name: string;
  last_name: string;
  customer_type: string;
  company_name?: string | null;
  is_active: boolean;
  source?: string | null;
  current_seller_id?: number | null;
  current_seller_code?: string | null;
  current_seller_name?: string | null;
  created_at: string;
}

interface CustomerListResponse {
  items: CustomerListItem[];
  total: number;
}

const CustomersPage: React.FC = () => {
  const navigate = useNavigate();

  const [items, setItems] = useState<CustomerListItem[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState<string>("");
  const [statusFilter, setStatusFilter] = useState<
    "all" | "active" | "inactive"
  >("all");

  const [syncing, setSyncing] = useState<boolean>(false);
  const [syncMessage, setSyncMessage] = useState<string | null>(null);

  async function loadCustomers() {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams();

      if (search.trim()) {
        params.set("search", search.trim());
      }
      if (statusFilter === "active") {
        params.set("is_active", "true");
      } else if (statusFilter === "inactive") {
        params.set("is_active", "false");
      }

      const query = params.toString();
      const path = query ? `/customers?${query}` : "/customers";

      const res = await api.get<CustomerListResponse>(path);
      setItems(res.items ?? []);
      setTotal(res.total ?? 0);
    } catch (err: any) {
      console.error(err);
      if (err?.status === 401) {
        setError("Je sessie is verlopen. Log opnieuw in.");
      } else {
        setError("Kon klanten niet laden.");
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadCustomers();
  }, []);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    void loadCustomers();
  }

  async function handleSync() {
    setSyncing(true);
    setSyncMessage(null);
    setError(null);

    try {
      await api.post("/customers-sync/run");
      setSyncMessage("Synchronisatie succesvol uitgevoerd.");
      await loadCustomers();
    } catch (err) {
      console.error(err);
      setError("Synchronisatie mislukt. Controleer backend.");
    } finally {
      setSyncing(false);
    }
  }

  function renderStatus(c: CustomerListItem) {
    const active = c.is_active;
    return (
      <span
        style={{
          display: "inline-block",
          padding: "0.1rem 0.5rem",
          borderRadius: 9999,
          fontSize: "0.75rem",
          fontWeight: 500,
          backgroundColor: active ? "#dcfce7" : "#fee2e2",
          color: active ? "#166534" : "#991b1b",
          border: `1px solid ${active ? "#bbf7d0" : "#fecaca"}`,
        }}
      >
        {active ? "Actief" : "Inactief"}
      </span>
    );
  }

  return (
    <div className="card">
      <h1>Klanten</h1>
      <p>
        Overzicht van alle klanten die vanuit de Website-module zijn
        gesynchroniseerd naar de verkoopmodule.
      </p>

      <div style={{ marginBottom: "1rem" }}>
        <button
          className="button secondary"
          onClick={handleSync}
          disabled={syncing}
        >
          {syncing ? "Synchroniseren..." : "Synchroniseer klanten met Website"}
        </button>
      </div>

      {syncMessage && <div className="alert success">{syncMessage}</div>}

      <form
        onSubmit={handleSubmit}
        style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}
      >
        <input
          type="text"
          placeholder="Zoek op naam of e-mail..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          value={statusFilter}
          onChange={(e) =>
            setStatusFilter(e.target.value as "all" | "active" | "inactive")
          }
        >
          <option value="all">Alle statussen</option>
          <option value="active">Actief</option>
          <option value="inactive">Inactief</option>
        </select>
        <button className="button primary" type="submit">
          Zoeken
        </button>
      </form>

      {error && <div className="alert error">{error}</div>}

      {loading ? (
        <p>Laden...</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Naam</th>
              <th>Email</th>
              <th>Type</th>
              <th>Bedrijf</th>
              <th>Verkoper</th>
              <th>Bron</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {items.map((c) => (
              <tr
                key={c.id}
                onClick={() => navigate(`/customers/${c.id}`)}
                style={{ cursor: "pointer" }}
              >
                <td>
                  {c.first_name} {c.last_name}
                </td>
                <td>{c.email}</td>
                <td>{c.customer_type}</td>
                <td>{c.company_name || "-"}</td>
                <td>{c.current_seller_name || c.current_seller_code || "-"}</td>
                <td>{c.source || "-"}</td>
                <td>{renderStatus(c)}</td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr>
                <td colSpan={7}>Geen klanten gevonden.</td>
              </tr>
            )}
          </tbody>
        </table>
      )}

      <p style={{ marginTop: "0.5rem" }}>Totaal: {total}</p>
    </div>
  );
};

export default CustomersPage;
