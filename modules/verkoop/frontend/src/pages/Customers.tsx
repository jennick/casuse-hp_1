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
  const [statusFilter, setStatusFilter] = useState<"all" | "active" | "inactive">(
    "all"
  );

  // ⬇️ Nieuw toegevoegd: Sync‐status en bericht
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
      const path = query ? `/admin/customers?${query}` : "/admin/customers";

      const res = await api.get<CustomerListResponse>(path);
      const list = res.items ?? [];
      setItems(list);
      setTotal(res.total ?? list.length);
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

  // ⬇️ Nieuw toegevoegd: Sync‐functie
  async function handleSync() {
    setSyncing(true);
    setSyncMessage(null);
    setError(null);

    try {
      const res = await api.post("/customers/sync-from-website", {});
      setSyncMessage("Synchronisatie succesvol uitgevoerd.");
      await loadCustomers();
    } catch (err: any) {
      console.error(err);
      setError("Synchronisatie mislukt. Controleer verbinding of backend.");
    } finally {
      setSyncing(false);
    }
  }

  function renderStatus(c: CustomerListItem) {
    const active = c.is_active;
    const label = active ? "Actief" : "Inactief";
    const bg = active ? "#dcfce7" : "#fee2e2";
    const color = active ? "#166534" : "#991b1b";
    const border = active ? "#bbf7d0" : "#fecaca";

    return (
      <span
        style={{
          display: "inline-block",
          padding: "0.1rem 0.5rem",
          borderRadius: 9999,
          fontSize: "0.75rem",
          fontWeight: 500,
          backgroundColor: bg,
          color,
          border: `1px solid ${border}`,
        }}
      >
        {label}
      </span>
    );
  }

  return (
    <div className="card">
      <h1 style={{ marginTop: 0, marginBottom: "0.25rem" }}>Klanten</h1>
      <p style={{ marginTop: 0, marginBottom: "1rem", fontSize: "0.9rem" }}>
        Overzicht van alle klanten die vanuit de Website-module zijn
        gesynchroniseerd naar de verkoopmodule.
      </p>

      {/* ⬇️ Nieuwe knop */}
      <div style={{ marginBottom: "1rem", display: "flex", gap: "0.5rem" }}>
        <button
          className="button secondary"
          onClick={handleSync}
          disabled={syncing}
        >
          {syncing ? "Synchroniseren..." : "Synchroniseer klanten met Website"}
        </button>
      </div>

      {syncMessage && (
        <div className="alert success" style={{ marginBottom: "0.75rem" }}>
          {syncMessage}
        </div>
      )}

      <form
        onSubmit={handleSubmit}
        style={{
          marginBottom: "1rem",
          display: "flex",
          gap: "0.5rem",
          alignItems: "center",
          flexWrap: "wrap",
        }}
      >
        <input
          type="text"
          placeholder="Zoek op naam of e-mail..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ flex: "1 1 220px" }}
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
        <button type="submit" className="button primary">
          Zoeken
        </button>
      </form>

      {error && (
        <div className="alert error" style={{ marginBottom: "0.75rem" }}>
          {error}
        </div>
      )}

      {loading ? (
        <p>Laden...</p>
      ) : (
        <div style={{ overflowX: "auto" }}>
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
          <p style={{ marginTop: "0.5rem", fontSize: "0.85rem" }}>
            Totaal: {total}
          </p>
        </div>
      )}
    </div>
  );
};

export default CustomersPage;
