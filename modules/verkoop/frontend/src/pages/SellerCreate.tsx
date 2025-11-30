import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../lib/api";
import PageHeader from "../components/PageHeader";

interface SellerDto {
  id: number;
  seller_code: string;
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

type SellerCreatePayload = Omit<SellerDto, "id">;

const SellerCreatePage: React.FC = () => {
  const navigate = useNavigate();
  const [seller, setSeller] = useState<SellerCreatePayload>({
    seller_code: "",
    first_name: "",
    last_name: "",
    email_work: "",
    phone_mobile: "",
    phone_internal: "", // wordt door backend overschreven met intern nummer
    address_line1: "",
    address_line2: "",
    postal_code: "",
    city: "",
    country: "BE",
    region_code: "",
    employment_type: "",
    max_discount_percent: 0,
    default_margin_target_percent: 0,
    is_active: true,
    role: "seller",
  });

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleChange<K extends keyof SellerCreatePayload>(
    field: K,
    value: SellerCreatePayload[K]
  ) {
    setSeller((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      setSaving(true);
      setError(null);
      const payload: SellerCreatePayload = { ...seller };
      const created = await api.post<SellerDto>("/sellers", payload);
      navigate(`/sellers/${created.id}`);
    } catch (e: any) {
      console.error(e);
      setError(e?.message ?? "Fout bij opslaan van nieuwe verkoper");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="card">
      <PageHeader
        title="Nieuwe verkoper"
        showBack
        backLabel="Terug naar lijst"
        backTo="/sellers"
      />
      <form onSubmit={handleSubmit} className="form-grid">
        <div className="form-field">
          <label>Code</label>
          <input
            value={seller.seller_code}
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

        <div className="form-field">
          <label>Adres lijn 1</label>
          <input
            value={seller.address_line1}
            onChange={(e) =>
              handleChange("address_line1", e.target.value)
            }
          />
        </div>
        <div className="form-field">
          <label>Adres lijn 2</label>
          <input
            value={seller.address_line2 ?? ""}
            onChange={(e) =>
              handleChange("address_line2", e.target.value)
            }
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

        <div style={{ gridColumn: "1 / -1", marginTop: "0.75rem" }}>
          {error && (
            <p style={{ color: "#b91c1c", marginBottom: "0.5rem" }}>
              {error}
            </p>
          )}
          <button className="button" type="submit" disabled={saving}>
            {saving ? "Opslaan…" : "Opslaan"}
          </button>{" "}
          <button
            type="button"
            className="button secondary"
            onClick={() => navigate("/sellers")}
          >
            Annuleren
          </button>
        </div>
      </form>
    </div>
  );
};

export default SellerCreatePage;
