import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../lib/api";

interface CustomerDetail {
  id: number;
  website_customer_id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number?: string | null;

  customer_type: string;
  description?: string | null;

  company_name?: string | null;
  tax_id?: string | null;

  address_street?: string | null;
  address_ext_number?: string | null;
  address_int_number?: string | null;
  address_neighborhood?: string | null;
  address_city?: string | null;
  address_state?: string | null;
  address_postal_code?: string | null;
  address_country?: string | null;

  is_active: boolean;
  source?: string | null;

  created_at: string;
  updated_at: string;

  current_seller_id?: number | null;
  current_seller_code?: string | null;
  current_seller_name?: string | null;
}

interface CustomerAssignmentHistoryItem {
  id: number;
  seller_id: number;
  seller_code: string;
  seller_name: string;
  assigned_at: string;
  unassigned_at?: string | null;
  assigned_by?: string | null;
}

const CustomerDetailPage: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [customer, setCustomer] = useState<CustomerDetail | null>(null);
  const [history, setHistory] = useState<CustomerAssignmentHistoryItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [assignSellerCode, setAssignSellerCode] = useState<string>("");
  const [assignLoading, setAssignLoading] = useState<boolean>(false);
  const [assignError, setAssignError] = useState<string | null>(null);
  const [assignSuccess, setAssignSuccess] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      if (!id) return;
      setLoading(true);
      setError(null);
      try {
        const [detail, hist] = await Promise.all([
          api.get<CustomerDetail>(`/admin/customers/${id}`),
          api.get<CustomerAssignmentHistoryItem[]>(
            `/admin/customers/${id}/assignments`
          ),
        ]);
        setCustomer(detail);
        setHistory(hist);
      } catch (err: any) {
        console.error(err);
        if (err?.status === 401) {
          setError("Je sessie is verlopen. Log opnieuw in.");
        } else if (err?.status === 404) {
          setError("Klant werd niet gevonden.");
        } else {
          setError("Kon klantdetails niet laden.");
        }
      } finally {
        setLoading(false);
      }
    }

    void load();
  }, [id]);

  async function handleAssign(e: React.FormEvent) {
    e.preventDefault();
    if (!id) return;

    if (!assignSellerCode.trim()) {
      setAssignError("Gelieve een verkopercode in te vullen (bv. S-0001).");
      setAssignSuccess(null);
      return;
    }

    setAssignLoading(true);
    setAssignError(null);
    setAssignSuccess(null);

    try {
      const updated = await api.post<CustomerDetail>(
        `/admin/customers/${id}/assign`,
        {
          seller_code: assignSellerCode.trim(),
          assigned_by: "verkoop-admin-ui",
        }
      );
      setCustomer(updated);
      setAssignSuccess(
        `Klant is gekoppeld aan verkoper ${
          updated.current_seller_name || updated.current_seller_code
        }.`
      );

      const hist = await api.get<CustomerAssignmentHistoryItem[]>(
        `/admin/customers/${id}/assignments`
      );
      setHistory(hist);
    } catch (err: any) {
      console.error(err);
      if (err?.status === 404) {
        setAssignError("Verkoper met deze code werd niet gevonden.");
      } else if (err?.status === 401) {
        setAssignError("Je sessie is verlopen. Log opnieuw in.");
      } else {
        setAssignError("Koppelen van verkoper is mislukt.");
      }
    } finally {
      setAssignLoading(false);
    }
  }

  if (loading) {
    return <p>Laden...</p>;
  }

  if (error) {
    return (
      <div className="card">
        <button
          type="button"
          className="button secondary"
          style={{ marginBottom: "0.75rem" }}
          onClick={() => navigate(-1)}
        >
          ← Terug
        </button>
        <div className="alert error">{error}</div>
      </div>
    );
  }

  if (!customer) {
    return (
      <div className="card">
        <button
          type="button"
          className="button secondary"
          style={{ marginBottom: "0.75rem" }}
          onClick={() => navigate(-1)}
        >
          ← Terug
        </button>
        <p>Geen klant gevonden.</p>
      </div>
    );
  }

  const fullName = `${customer.first_name} ${customer.last_name}`.trim();

  return (
    <div className="card">
      <button
        type="button"
        className="button secondary"
        style={{ marginBottom: "0.75rem" }}
        onClick={() => navigate(-1)}
      >
        ← Terug naar klantenlijst
      </button>

      <h1 style={{ marginTop: 0, marginBottom: "0.25rem" }}>
        {fullName || customer.email}
      </h1>
      <p style={{ marginTop: 0, marginBottom: "1rem", fontSize: "0.9rem" }}>
        Website-ID: {customer.website_customer_id}
      </p>

      <div className="grid-2">
        <section>
          <h2>Basisgegevens</h2>
          <p>
            <strong>Email:</strong> {customer.email}
          </p>
          {customer.phone_number && (
            <p>
              <strong>Telefoon:</strong> {customer.phone_number}
            </p>
          )}
          <p>
            <strong>Type:</strong> {customer.customer_type}
          </p>
          {customer.description && (
            <p>
              <strong>Omschrijving:</strong> {customer.description}
            </p>
          )}
          <p>
            <strong>Status:</strong>{" "}
            {customer.is_active ? "Actief" : "Inactief"}
          </p>
          <p>
            <strong>Bron:</strong> {customer.source || "-"}
          </p>
          <p>
            <strong>Aangemaakt:</strong>{" "}
            {new Date(customer.created_at).toLocaleString()}
          </p>
          <p>
            <strong>Laatst bijgewerkt:</strong>{" "}
            {new Date(customer.updated_at).toLocaleString()}
          </p>
        </section>

        <section>
          <h2>Bedrijf & adres</h2>
          {customer.customer_type === "bedrijf" && (
            <>
              <p>
                <strong>Bedrijf:</strong>{" "}
                {customer.company_name || "(geen naam opgegeven)"}
              </p>
              <p>
                <strong>BTW/Tax ID:</strong> {customer.tax_id || "-"}
              </p>
            </>
          )}

          <p>
            <strong>Adres:</strong>{" "}
            {[customer.address_street, customer.address_ext_number]
              .filter(Boolean)
              .join(" ")}
          </p>
          {customer.address_int_number && (
            <p>
              <strong>Int. nr.:</strong> {customer.address_int_number}
            </p>
          )}
          {customer.address_neighborhood && (
            <p>
              <strong>Wijk:</strong> {customer.address_neighborhood}
            </p>
          )}
          <p>
            <strong>Stad:</strong>{" "}
            {[customer.address_postal_code, customer.address_city]
              .filter(Boolean)
              .join(" ")}
          </p>
          <p>
            <strong>Staat:</strong> {customer.address_state || "-"}
          </p>
          <p>
            <strong>Land:</strong> {customer.address_country || "-"}
          </p>
        </section>
      </div>

      <section style={{ marginTop: "1.5rem" }}>
        <h2>Verkoper-koppeling</h2>
        <p>
          <strong>Huidige verkoper:</strong>{" "}
          {customer.current_seller_name ||
            customer.current_seller_code ||
            "Nog geen verkoper gekoppeld"}
        </p>

        <form
          onSubmit={handleAssign}
          style={{
            marginTop: "0.75rem",
            display: "flex",
            flexWrap: "wrap",
            gap: "0.5rem",
            alignItems: "center",
          }}
        >
          <label style={{ fontSize: "0.9rem" }}>
            Verkoper-code:&nbsp;
            <input
              type="text"
              value={assignSellerCode}
              onChange={(e) => setAssignSellerCode(e.target.value)}
              placeholder="bv. S-0001"
              style={{ minWidth: "140px" }}
            />
          </label>
          <button
            type="submit"
            className="button primary"
            disabled={assignLoading}
          >
            {assignLoading ? "Bezig..." : "Koppel verkoper"}
          </button>
        </form>

        {assignError && (
          <div
            className="alert error"
            style={{ marginTop: "0.5rem", maxWidth: "480px" }}
          >
            {assignError}
          </div>
        )}
        {assignSuccess && (
          <div
            className="alert success"
            style={{ marginTop: "0.5rem", maxWidth: "480px" }}
          >
            {assignSuccess}
          </div>
        )}
      </section>

      <section style={{ marginTop: "1.5rem" }}>
        <h2>Historiek verkoper-koppelingen</h2>
        {history.length === 0 ? (
          <p>Er zijn nog geen koppelingen geregistreerd.</p>
        ) : (
          <div style={{ overflowX: "auto" }}>
            <table className="table">
              <thead>
                <tr>
                  <th>Verkoper</th>
                  <th>Geactiveerd op</th>
                  <th>Gedeactiveerd op</th>
                  <th>Door</th>
                </tr>
              </thead>
              <tbody>
                {history.map((h) => (
                  <tr key={h.id}>
                    <td>
                      {h.seller_name} ({h.seller_code})
                    </td>
                    <td>{new Date(h.assigned_at).toLocaleString()}</td>
                    <td>
                      {h.unassigned_at
                        ? new Date(h.unassigned_at).toLocaleString()
                        : "-"}
                    </td>
                    <td>{h.assigned_by || "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
};

export default CustomerDetailPage;
