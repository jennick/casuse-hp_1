import React, { useEffect, useState } from "react";
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
  region_code: string;
  role: string;
  is_active: boolean;
}

interface SellerView {
  id: number;
  sellerCode: string;
  name: string;
  email: string;
  phoneMobile: string;
  regionCode: string;
  role: string;
  active: boolean;
}

const SellersPage: React.FC = () => {
  const [sellers, setSellers] = useState<SellerView[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        setError(null);
        const data = await api.get<SellerDto[]>("/sellers");
        const mapped: SellerView[] = data.map((s) => ({
          id: s.id,
          sellerCode: s.seller_code,
          name: s.first_name + " " + s.last_name,
          email: s.email_work,
          phoneMobile: s.phone_mobile,
          regionCode: s.region_code,
          role: s.role,
          active: s.is_active,
        }));
        setSellers(mapped);
      } catch (e: any) {
        console.error(e);
        setError(e?.message ?? "Onbekende fout bij laden van verkopers");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  function handleRowClick(id: number) {
    navigate(`/sellers/${id}`);
  }

  function handleCreate() {
    navigate("/sellers/new");
  }

  return (
    <div className="card">
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-end",
          gap: "1rem",
          marginBottom: "0.75rem",
        }}
      >
        <div style={{ flex: 1 }}>
          <PageHeader
            title="Verkopers"
            description="Overzicht van je sales people, hun contactgegevens, regio's en commerciële parameters."
          />
        </div>
        <div>
          <button className="button" type="button" onClick={handleCreate}>
            + Nieuwe verkoper
          </button>
        </div>
      </div>

      {loading && <p>Bezig met laden…</p>}
      {error && (
        <p style={{ color: "#b91c1c", fontSize: "0.9rem" }}>
          Fout: {error}
        </p>
      )}
      {!loading && !error && (
        <table className="table">
          <thead>
            <tr>
              <th>Code</th>
              <th>Naam</th>
              <th>E-mail</th>
              <th>GSM</th>
              <th>Regio</th>
              <th>Rol</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {sellers.map((s) => (
              <tr
                key={s.id}
                style={{ cursor: "pointer" }}
                onClick={() => handleRowClick(s.id)}
              >
                <td>{s.sellerCode}</td>
                <td>{s.name}</td>
                <td>{s.email}</td>
                <td>{s.phoneMobile}</td>
                <td>{s.regionCode}</td>
                <td>{s.role}</td>
                <td>
                  <span
                    className={
                      "badge " + (s.active ? "badge-green" : "badge-red")
                    }
                  >
                    {s.active ? "Actief" : "Inactief"}
                  </span>
                </td>
              </tr>
            ))}
            {sellers.length === 0 && (
              <tr>
                <td colSpan={7}>Geen verkopers gevonden.</td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default SellersPage;
