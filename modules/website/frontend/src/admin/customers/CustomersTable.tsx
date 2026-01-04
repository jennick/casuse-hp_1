import { useNavigate } from "react-router-dom";
import StatusBadge from "@/shared/ui/StatusBadge";

/* ======================================================
   Types
====================================================== */

type Customer = {
  id: string;
  customer_uuid: string; // 🔐 nieuw

  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;

  has_login: boolean;
  portal_status?: string;
};

type Props = {
  customers: Customer[];
};

/* ======================================================
   Component
====================================================== */

export default function CustomersTable({ customers }: Props) {
  const navigate = useNavigate();

  if (!Array.isArray(customers) || customers.length === 0) {
    return <div>Geen klanten gevonden.</div>;
  }

  return (
    <table className="table">
      <thead>
        <tr>
          <th>Naam</th>
          <th>E-mail</th>
          <th>Customer UUID</th>
          <th>Loginstatus</th>
          <th>Status</th>
        </tr>
      </thead>

      <tbody>
        {customers.map((customer) => (
          <tr
            key={customer.id}
            style={{ cursor: "pointer" }}
            onClick={() => navigate(`/customers/${customer.id}`)}
          >
            <td>
              {customer.first_name} {customer.last_name}
            </td>

            <td>{customer.email}</td>

            <td>
              <code style={{ fontSize: "0.75rem" }}>
                {customer.customer_uuid}
              </code>
            </td>

            <td>
              {customer.has_login ? (
                <StatusBadge status="active" label="Ingelogd" />
              ) : (
                <StatusBadge status="pending" label="Nog niet ingelogd" />
              )}
            </td>

            <td>
              {customer.is_active ? (
                <StatusBadge status="active" label="Actief" />
              ) : (
                <StatusBadge status="blocked" label="Geblokkeerd" />
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
