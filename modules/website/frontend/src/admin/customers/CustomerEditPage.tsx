import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { apiFetch } from "@/shared/api/apiClient";

/* ======================================================
   Types — frontend equivalent van CustomerUpdate
====================================================== */

type CustomerType = "particulier" | "bedrijf";

type CustomerForm = {
  email: string;
  first_name: string;
  last_name: string;
  phone_number: string;

  customer_type: CustomerType;
  description: string;

  company_name: string;
  tax_id: string;

  address_street: string;
  address_ext_number: string;
  address_int_number: string;
  address_neighborhood: string;
  address_city: string;
  address_state: string;
  address_postal_code: string;
  address_country: string;

  is_active: boolean;
};

/* ======================================================
   PATCH normalisatie — CRUCIAAL
====================================================== */

/**
 * FastAPI + Pydantic PATCH regels:
 * - ""        ❌ invalid
 * - null      ✅ OK
 * - afwezig   ✅ OK
 */
function normalizePatchBody<T extends Record<string, any>>(
  data: T
): Partial<T> {
  const result: Partial<T> = {};

  for (const [key, value] of Object.entries(data)) {
    if (value === "") {
      result[key as keyof T] = null as any;
    } else if (value !== undefined) {
      result[key as keyof T] = value;
    }
  }

  return result;
}

/* ======================================================
   Component
====================================================== */

export default function CustomerEditPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [form, setForm] = useState<CustomerForm | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /* ================= Load ================= */

  useEffect(() => {
    if (!id) return;
    loadCustomer();
  }, [id]);

  async function loadCustomer() {
    try {
      setLoading(true);
      setError(null);

      const data = await apiFetch<any>(`/api/admin/customers/${id}`);

      setForm({
        email: data.email ?? "",
        first_name: data.first_name ?? "",
        last_name: data.last_name ?? "",
        phone_number: data.phone_number ?? "",

        customer_type: data.customer_type ?? "particulier",
        description: data.description ?? "",

        company_name: data.company_name ?? "",
        tax_id: data.tax_id ?? "",

        address_street: data.address_street ?? "",
        address_ext_number: data.address_ext_number ?? "",
        address_int_number: data.address_int_number ?? "",
        address_neighborhood: data.address_neighborhood ?? "",
        address_city: data.address_city ?? "",
        address_state: data.address_state ?? "",
        address_postal_code: data.address_postal_code ?? "",
        address_country: data.address_country ?? "",

        is_active: Boolean(data.is_active),
      });
    } catch (e) {
      console.error(e);
      setError("Kon klant niet laden.");
    } finally {
      setLoading(false);
    }
  }

  /* ================= Helpers ================= */

  function update<K extends keyof CustomerForm>(
    key: K,
    value: CustomerForm[K]
  ) {
    if (!form) return;
    setForm({ ...form, [key]: value });
  }

  /* ================= Submit ================= */

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form || !id) return;

    const payload = normalizePatchBody(form);

    console.log("PATCH payload →", payload);

    try {
      setSaving(true);
      setError(null);

      await apiFetch(`/api/admin/customers/${id}`, {
        method: "PATCH",
        json: payload,
      });

      navigate(`/customers/${id}`);
    } catch (e) {
      console.error(e);
      setError("Opslaan mislukt.");
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <div>Klant laden…</div>;
  if (error || !form) return <div>{error}</div>;

  /* ================= Render ================= */

  return (
    <div className="customer-edit-page">
      <h1>Klant bewerken</h1>

      <button onClick={() => navigate(`/customers/${id}`)}>
        ← Terug
      </button>

      <form onSubmit={handleSubmit} style={{ marginTop: "1.5rem" }}>
        <fieldset>
          <legend>Algemeen</legend>

          <input value={form.first_name} onChange={e => update("first_name", e.target.value)} />
          <input value={form.last_name} onChange={e => update("last_name", e.target.value)} />
          <input type="email" value={form.email} onChange={e => update("email", e.target.value)} />
          <input value={form.phone_number} onChange={e => update("phone_number", e.target.value)} />

          <select
            value={form.customer_type}
            onChange={e => update("customer_type", e.target.value as CustomerType)}
          >
            <option value="particulier">Particulier</option>
            <option value="bedrijf">Bedrijf</option>
          </select>
        </fieldset>

        <fieldset>
          <legend>Status</legend>
          <label>
            <input
              type="checkbox"
              checked={form.is_active}
              onChange={e => update("is_active", e.target.checked)}
            />
            Actief
          </label>
        </fieldset>

        <button type="submit" disabled={saving}>
          {saving ? "Opslaan…" : "Opslaan"}
        </button>
      </form>
    </div>
  );
}
