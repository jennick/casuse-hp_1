import { useEffect, useState } from "react";
import { apiFetch } from "@/shared/api/apiClient";
import StatusBadge from "@/shared/ui/StatusBadge";

type CustomerRelation = {
  id: string;
  module: string;
  status: string;
  created_at: string;
};

type Props = {
  customerId: string;
};

function renderModuleName(module: string): string {
  switch (module) {
    case "verkoop":
      return "Verkoop";
    case "facturatie":
      return "Facturatie";
    case "magazijn":
      return "Magazijn";
    case "productie":
      return "Productie";
    case "inventaries":
      return "Inventaris";
    default:
      return module;
  }
}

function renderStatus(status: string) {
  switch (status) {
    case "active":
      return <StatusBadge status="active" />;
    case "blocked":
      return <StatusBadge status="blocked" />;
    default:
      return <StatusBadge status="inactive" />;
  }
}

export default function CustomerRelationsTab({ customerId }: Props) {
  const [relations, setRelations] = useState<CustomerRelation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!customerId) return;
    fetchRelations();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [customerId]);

  async function fetchRelations() {
    try {
      setLoading(true);

      const data = await apiFetch<CustomerRelation[]>(
        `/api/admin/customers/${customerId}/relations`
      );

      setRelations(data);
    } catch (err) {
      console.error(err);
      setError("Kon module-relaties niet laden.");
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div>Relaties laden…</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (relations.length === 0) {
    return <div>Geen module-relaties gevonden voor deze klant.</div>;
  }

  return (
    <table className="table">
      <thead>
        <tr>
          <th>Module</th>
          <th>Status</th>
          <th>Gekoppeld sinds</th>
        </tr>
      </thead>
      <tbody>
        {relations.map((relation) => (
          <tr key={relation.id}>
            <td>{renderModuleName(relation.module)}</td>
            <td>{renderStatus(relation.status)}</td>
            <td>
              {new Date(relation.created_at).toLocaleString("nl-BE")}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
