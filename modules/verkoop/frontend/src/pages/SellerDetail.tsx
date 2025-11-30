import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../lib/api";
import PageHeader from "../components/PageHeader";

interface SellerDto {
  id: number;
  seller_code: string | null;
  first_name: string;
  last_name: string;
  email_work: string;
  phone_mobile: string;
  phone_internal: string | null;
  address_line1: string;
  address_line2: string | null;
  postal_code: string;
  city: string;
  country: string;
  region_code: string;
  employment_type: string;
  max_discount_percent: number;
  default_margin_target_percent: number;
  is_active: boolean;
  role: string;
}

const SellerDetailPage: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [seller, setSeller] = useState<SellerDto | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Nieuw voor stap 4: status van reset-link
  const [resetLoading, setResetLoading] = useState(false);
  const [resetInfo, setResetInfo] = useState<string | null>(null);
  const [resetError, setResetError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    async function load() {
      try {
        setLoading(true);
        setError(null);
        const data = await api.get<SellerDto>(`/sellers/${id}`);
        setSeller(data);
      } catch (e: any) {
        console.error(e);
        setError(e?.message ?? "Kon verkoper niet laden");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  function handleChange<K extends keyof SellerDto>(
    field: K,
    value: SellerDto[K]
  ) {
    setSeller((prev) => (prev ? { ...prev, [field]: value } : prev));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!seller || !id) return;
    try {
      setSaving(true);
      setError(null);
      const payload = { ...seller };
      const updated = await api.patch<SellerDto>(`/sellers/${id}`, payload);
      setSeller(updated);
    } catch (e: any) {
      console.error(e);
      setError(e?.message ?? "Fout bij opslaan");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete() {
    if (!seller || !seller.id) return;
    const ok = window.confirm(
      `Ben je zeker dat je verkoper ${
        seller.seller_code || seller.first_name + " " + seller.last_name
      } definitief wil verwijderen?`
    );
    if (!ok) return;

    try {
      setDeleting(true);
      setError(null);
      await api.delete<void>(`/sellers/${seller.id}`);
      navigate("/sellers");
    } catch (e: any) {
      console.error(e);
      setError(e?.message ?? "Fout bij verwijderen");
    } finally {
      setDeleting(false);
    }
  }

  // Nieuw voor stap 4: reset-link genereren
  async function handlePasswordResetLink() {
    if (!seller || !seller.id) return;

    try {
      setResetLoading(true);
      setResetError(null);
      setResetInfo(null);

      const data = await api.post<{
        reset_url: string;
        valid_until: string;
      }>(`/sellers/${seller.id}/password-reset-request`, {});

      const geldigTot = new Date(data.valid_until);
      const geldigTekst = geldigTot.toLocaleString();

      setResetInfo(
        `Resetlink gegenereerd: ${data.reset_url} (geldig tot ${geldigTekst}).`
      );
    } catch (e: any) {
      console.error(e);
      setResetError(e?.message ?? "Fout bij genereren van resetlink");
    } finally {
      setResetLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="card">
        <p>Verkoper laden…</p>
      </div>
    );
  }

  if (error && !seller) {
    return (
      <div className="card">
        <p style={{ color: "#b91c1c" }}>Fout: {error}</p>
        <button className="button secondary" onClick={() => navigate(-1)}>
          Terug
        </button>
      </div>
    );
  }

  if (!seller) {
    return (
      <div className="card">
        <p>Verkoper niet gevonden.</p>
        <button className="button secondary" onClick={() => navigate(-1)}>
          Terug
        </button>
      </div>
    );
  }

  return (
    <div className="card">
      <PageHeader
        title={
          seller.seller_code
            ? `Verkoper ${seller.seller_code}`
            : "Verkoper"
        }
        showBack
        backLabel="Terug naar lijst"
        backTo="/sellers"
      />

      <form onSubmit={handleSubmit} className="form-grid">
        {/* Codeveld, gekoppeld aan seller_code */}
        <div className="form-field">
          <label>Code</label>
          <input
            value={seller.seller_code ?? ""}
            onChange={(e) => handleChange("seller_code", e.target.value)}
          />
        </div>

        <div className="form-field">
          <label>Voornaam</label>
          <input
            value={seller.first_name}
            onChange={(e) => handleChange("first_name", e.target.value)}
          />
        </div>
        <div className="form-field">
          <label>Familienaam</label>
          <input
            value={seller.last_name}
            onChange={(e) => handleChange("last_name", e.target.value)}
          />
        </div>
        <div className="form-field">
          <label>E-mail werk</label>
          <input
            type="email"
            value={seller.email_work}
            onChange={(e) => handleChange("email_work", e.target.value)}
          />
        </div>
        <div className="form-field">
          <label>GSM</label>
          <input
            value={seller.phone_mobile}
            onChange={(e) => handleChange("phone_mobile", e.target.value)}
          />
        </div>

        {/* Intern nummer: read-only, automatisch gegenereerd */}
        <div className="form-field">
          <label>Intern nummer</label>
          <input value={seller.phone_internal ?? ""} readOnly />
          <small className="form-help">
            Dit interne nummer wordt automatisch aangemaakt en kan niet worden
            gewijzigd.
          </small>
        </div>

        <div className="form-field">
          <label>Adres lijn 1</label>
          <input
            value={seller.address_line1}
            onChange={(e) => handleChange("address_line1", e.target.value)}
          />
        </div>
        <div className="form-field">
          <label>Adres lijn 2</label>
          <input
            value={seller.address_line2 ?? ""}
            onChange={(e) => handleChange("address_line2", e.target.value)}
          />
        </div>
        <div className="form-field">
          <label>Postcode</label>
          <input
            value={seller.postal_code}
            onChange={(e) => handleChange("postal_code", e.target.value)}
          />
        </div>
        <div className="form-field">
          <label>Stad</label>
          <input
            value={seller.city}
            onChange={(e) => handleChange("city", e.target.value)}
          />
        </div>
        <div className="form-field">
          <label>Land (ISO)</label>
          <input
            value={seller.country}
            onChange={(e) => handleChange("country", e.target.value)}
          />
        </div>
        <div className="form-field">
          <label>Regiocode</label>
          <input
            value={seller.region_code}
            onChange={(e) => handleChange("region_code", e.target.value)}
          />
        </div>
        <div className="form-field">
          <label>Type tewerkstelling</label>
          <input
            value={seller.employment_type}
            onChange={(e) =>
              handleChange("employment_type", e.target.value)
            }
          />
        </div>
        <div className="form-field">
          <label>Max. korting (%)</label>
          <input
            type="number"
            value={seller.max_discount_percent}
            onChange={(e) =>
              handleChange(
                "max_discount_percent",
                Number(e.target.value) || 0
              )
            }
          />
        </div>
        <div className="form-field">
          <label>Doel-marge (%)</label>
          <input
            type="number"
            value={seller.default_margin_target_percent}
            onChange={(e) =>
              handleChange(
                "default_margin_target_percent",
                Number(e.target.value) || 0
              )
            }
          />
        </div>
        <div className="form-field">
          <label>Rol</label>
          <select
            value={seller.role}
            onChange={(e) => handleChange("role", e.target.value)}
          >
            <option value="seller">Seller</option>
            <option value="manager">Manager</option>
          </select>
        </div>
        <div className="form-field">
          <label>Status</label>
          <select
            value={seller.is_active ? "1" : "0"}
            onChange={(e) =>
              handleChange("is_active", e.target.value === "1")
            }
          >
            <option value="1">Actief</option>
            <option value="0">Inactief</option>
          </select>
        </div>

        <div
          style={{
            gridColumn: "1 / -1",
            marginTop: "0.75rem",
            display: "flex",
            gap: "0.5rem",
            alignItems: "center",
            flexWrap: "wrap",
          }}
        >
          {error && (
            <p
              style={{
                color: "#b91c1c",
                marginBottom: "0.5rem",
                marginRight: "1rem",
              }}
            >
              {error}
            </p>
          )}

          <button className="button" type="submit" disabled={saving}>
            {saving ? "Opslaan…" : "Opslaan"}
          </button>

          <button
            type="button"
            className="button secondary"
            onClick={() => navigate("/sellers")}
          >
            Annuleren
          </button>

          <button
            type="button"
            className="button secondary"
            onClick={handlePasswordResetLink}
            disabled={resetLoading}
          >
            {resetLoading ? "Resetlink genereren…" : "Wachtwoord resetten"}
          </button>

          <button
            type="button"
            className="button danger"
            onClick={handleDelete}
            disabled={deleting}
          >
            {deleting ? "Verwijderen…" : "Verkoper verwijderen"}
          </button>
        </div>

        {(resetInfo || resetError) && (
          <div
            style={{
              gridColumn: "1 / -1",
              marginTop: "0.5rem",
            }}
          >
            {resetInfo && (
              <p className="form-help" style={{ marginBottom: "0.25rem" }}>
                {resetInfo}
              </p>
            )}
            {resetError && (
              <p style={{ color: "#b91c1c" }}>{resetError}</p>
            )}
          </div>
        )}
      </form>
    </div>
  );
};

export default SellerDetailPage;
