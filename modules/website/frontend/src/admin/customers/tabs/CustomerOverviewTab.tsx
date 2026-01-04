import StatusBadge from "@/shared/ui/StatusBadge";

type Props = {
  customer: {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
    is_active: boolean;

    // ✅ CORRECT veld (komt uit backend / schemas.py)
    has_login: boolean;

    created_at: string;
    updated_at?: string | null;
  };
};

export default function CustomerOverviewTab({ customer }: Props) {
  return (
    <div className="customer-overview">
      <h3>Algemene informatie</h3>

      <table className="table">
        <tbody>
          <tr>
            <th>Voornaam</th>
            <td>{customer.first_name}</td>
          </tr>

          <tr>
            <th>Achternaam</th>
            <td>{customer.last_name}</td>
          </tr>

          <tr>
            <th>E-mail</th>
            <td>{customer.email}</td>
          </tr>

          <tr>
            <th>Loginstatus</th>
            <td>
              {customer.has_login ? (
                <StatusBadge status="active" label="Ingelogd" />
              ) : (
                <StatusBadge status="pending" label="Nog niet ingelogd" />
              )}
            </td>
          </tr>

          <tr>
            <th>Status</th>
            <td>
              {customer.is_active ? (
                <StatusBadge status="active" label="Actief" />
              ) : (
                <StatusBadge status="blocked" label="Geblokkeerd" />
              )}
            </td>
          </tr>

          <tr>
            <th>Aangemaakt op</th>
            <td>
              {new Date(customer.created_at).toLocaleString("nl-BE")}
            </td>
          </tr>

          {customer.updated_at && (
            <tr>
              <th>Laatst gewijzigd</th>
              <td>
                {new Date(customer.updated_at).toLocaleString("nl-BE")}
              </td>
            </tr>
          )}
        </tbody>
      </table>

      <div className="admin-notes">
        <p>
          Dit overzicht toont de kerngegevens van de klant.
          Acties zoals blokkeren, heruitnodigen of wijzigen van gegevens
          worden hier later toegevoegd.
        </p>
      </div>
    </div>
  );
}
