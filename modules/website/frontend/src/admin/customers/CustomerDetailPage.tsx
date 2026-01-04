import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import CustomerEventsTab from "./tabs/CustomerEventsTab";
import CustomerDocumentsTab from "./tabs/CustomerDocumentsTab";
import CustomerRelationsTab from "./tabs/CustomerRelationsTab";

import { apiFetch } from "@/shared/api/apiClient";
import StatusBadge from "@/shared/ui/StatusBadge";

/* ======================================================
   Types
====================================================== */

type Customer = {
  id: string;

  // 🔐 extern, stabiel klant-ID (read-only)
  customer_uuid: string;

  email: string;
  first_name: string;
  last_name: string;
  phone_number?: string;

  customer_type: "particulier" | "bedrijf";
  description?: string;

  company_name?: string;
  tax_id?: string;

  address_street?: string;
  address_ext_number?: string;
  address_int_number?: string;
  address_neighborhood?: string;
  address_city?: string;
  address_state?: string;
  address_postal_code?: string;
  address_country?: string;

  is_active: boolean;
  has_login: boolean;
  portal_status?: string;

  created_at: string;
  updated_at: string;
};

type TabKey = "events" | "documents" | "relations";

/* ======================================================
   Component
====================================================== */

export default function CustomerDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [customer, setCustomer] = useState<Customer | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [activeTab, setActiveTab] = useState<TabKey>("events");

  useEffect(() => {
    fetchCustomer();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  async function fetchCustomer() {
    try {
      setLoading(true);
      setError(null);

      const data = await apiFetch<Customer>(
        `/api/admin/customers/${id}`
      );

      setCustomer(data);
    } catch (err) {
      console.error("Failed to fetch customer", err);
      setError("Kon klantgegevens niet laden.");
    } finally {
      setLoading(false);
    }
  }

  if (loading) return <div>Klant laden…</div>;
  if (error || !customer) return <div>{error ?? "Klant niet gevonden."}</div>;

  /* ======================================================
     Render
  ====================================================== */

  return (
    <div className="customer-detail-page">
      {/* 🔙 TERUG NAAR KLANTEN */}
      <div style={{ marginBottom: "1rem" }}>
        <button
          type="button"
          onClick={() => navigate("/customers")}
          style={linkButtonStyle}
        >
          ← Terug naar klanten
        </button>
      </div>

      {/* HEADER */}
      <header style={{ display: "flex", justifyContent: "space-between" }}>
        <div>
          <h1>
            {customer.first_name} {customer.last_name}
          </h1>

          <StatusBadge
            status={customer.is_active ? "active" : "inactive"}
            label={customer.is_active ? "Actief" : "Geblokkeerd"}
          />
        </div>

        {/* 🔹 ADMIN ACTIES */}
        <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
          <button
            type="button"
            onClick={() => navigate(`/customers/${customer.id}/edit`)}
            style={primaryButtonStyle}
          >
            Bewerken
          </button>

          <button
            type="button"
            disabled
            style={secondaryButtonStyle}
            title="Voor later: activeren / deactiveren"
          >
            Status wijzigen
          </button>
        </div>
      </header>

      {/* ALGEMENE INFO */}
      <section style={{ marginTop: "1.5rem" }}>
        <h2>Algemene informatie</h2>

        <dl>
          <dt>Customer UUID</dt>
          <dd>
            <code style={{ fontSize: "0.8rem" }}>
              {customer.customer_uuid}
            </code>
          </dd>

          <dt>Voornaam</dt>
          <dd>{customer.first_name}</dd>

          <dt>Achternaam</dt>
          <dd>{customer.last_name}</dd>

          <dt>E-mail</dt>
          <dd>{customer.email}</dd>

          {customer.phone_number && (
            <>
              <dt>Telefoon</dt>
              <dd>{customer.phone_number}</dd>
            </>
          )}

          <dt>Klanttype</dt>
          <dd>{customer.customer_type}</dd>

          <dt>Loginstatus</dt>
          <dd>
            <StatusBadge
              status={customer.has_login ? "active" : "pending"}
              label={customer.has_login ? "Ingelogd" : "Nog niet ingelogd"}
            />
          </dd>

          <dt>Aangemaakt op</dt>
          <dd>{new Date(customer.created_at).toLocaleString("nl-BE")}</dd>

          <dt>Laatst gewijzigd</dt>
          <dd>{new Date(customer.updated_at).toLocaleString("nl-BE")}</dd>
        </dl>
      </section>

      {/* BEDRIJFSGEGEVENS */}
      {customer.customer_type === "bedrijf" && (
        <section style={{ marginTop: "1.5rem" }}>
          <h2>Bedrijfsgegevens</h2>

          <dl>
            <dt>Bedrijfsnaam</dt>
            <dd>{customer.company_name ?? "—"}</dd>

            <dt>BTW / RFC</dt>
            <dd>{customer.tax_id ?? "—"}</dd>
          </dl>
        </section>
      )}

      {/* ADRES */}
      <section style={{ marginTop: "1.5rem" }}>
        <h2>Adres</h2>

        <address>
          {customer.address_street} {customer.address_ext_number}
          {customer.address_int_number && ` / ${customer.address_int_number}`}
          <br />
          {customer.address_postal_code} {customer.address_city}
          <br />
          {customer.address_state}
          <br />
          {customer.address_country}
        </address>
      </section>

      {/* OMSCHRIJVING */}
      {customer.description && (
        <section style={{ marginTop: "1.5rem" }}>
          <h2>Omschrijving</h2>
          <p>{customer.description}</p>
        </section>
      )}

      {/* 🔹 TAB NAVIGATIE */}
      <div style={tabNavStyle}>
        <TabButton
          active={activeTab === "events"}
          onClick={() => setActiveTab("events")}
        >
          Events
        </TabButton>

        <TabButton
          active={activeTab === "documents"}
          onClick={() => setActiveTab("documents")}
        >
          Documenten
        </TabButton>

        <TabButton
          active={activeTab === "relations"}
          onClick={() => setActiveTab("relations")}
        >
          Relaties
        </TabButton>
      </div>

      {/* 🔹 TAB INHOUD */}
      <section style={{ marginTop: "1.5rem" }}>
        {activeTab === "events" && (
          <CustomerEventsTab customerId={customer.id} />
        )}

        {activeTab === "documents" && (
          <CustomerDocumentsTab customerId={customer.id} />
        )}

        {activeTab === "relations" && (
          <CustomerRelationsTab customerId={customer.id} />
        )}
      </section>
    </div>
  );
}

/* ======================================================
   UI helpers
====================================================== */

function TabButton({
  active,
  children,
  onClick,
}: {
  active: boolean;
  children: React.ReactNode;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      style={{
        background: "none",
        border: "none",
        borderBottom: active
          ? "2px solid #0b5ed7"
          : "2px solid transparent",
        padding: "0.5rem 0.75rem",
        cursor: "pointer",
        fontWeight: active ? 600 : 400,
        color: active ? "#0b5ed7" : "#374151",
      }}
    >
      {children}
    </button>
  );
}

/* ======================================================
   Styles (inline, bewust lokaal gehouden)
====================================================== */

const linkButtonStyle = {
  background: "none",
  border: "none",
  color: "#0b5ed7",
  cursor: "pointer",
  fontSize: "0.95rem",
  padding: 0,
};

const primaryButtonStyle = {
  background: "#0b5ed7",
  color: "#fff",
  border: "none",
  padding: "0.5rem 0.75rem",
  cursor: "pointer",
  borderRadius: "4px",
};

const secondaryButtonStyle = {
  background: "#e5e7eb",
  color: "#374151",
  border: "none",
  padding: "0.5rem 0.75rem",
  cursor: "not-allowed",
  borderRadius: "4px",
};

const tabNavStyle = {
  display: "flex",
  gap: "0.75rem",
  marginTop: "2rem",
  borderBottom: "1px solid #e5e7eb",
  paddingBottom: "0.5rem",
};
