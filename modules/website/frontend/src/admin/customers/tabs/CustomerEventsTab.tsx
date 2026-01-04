import { useEffect, useState } from "react";

import { apiFetch } from "@/shared/api/apiClient";
import StatusBadge from "@/shared/ui/StatusBadge";

type CustomerEvent = {
  id: string;
  event_type: string;
  description: string | null;
  created_at: string;
};

type Props = {
  customerId: string;
};

function renderEventType(type: string) {
  switch (type) {
    case "login":
      return <StatusBadge status="active" label="Login" />;
    case "password_reset":
      return <StatusBadge status="pending" label="Wachtwoord reset" />;
    case "created":
      return <StatusBadge status="invited" label="Aangemaakt" />;
    case "status_change":
      return <StatusBadge status="inactive" label="Statuswijziging" />;
    default:
      return <StatusBadge status="inactive" label={type} />;
  }
}

export default function CustomerEventsTab({ customerId }: Props) {
  const [events, setEvents] = useState<CustomerEvent[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  async function fetchEvents() {
    if (!customerId) return;

    try {
      setLoading(true);
      setError(null);

      const data = await apiFetch<CustomerEvent[]>(
        `/api/admin/customers/${customerId}/events`
      );

      setEvents(data);
    } catch (err) {
      console.error("Failed to fetch events", err);
      setError("Kon events niet laden.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchEvents();
  }, [customerId]);

  if (loading) {
    return <div>Events laden…</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (events.length === 0) {
    return <div>Nog geen events voor deze klant.</div>;
  }

  return (
    <table className="table">
      <thead>
        <tr>
          <th>Type</th>
          <th>Beschrijving</th>
          <th>Datum</th>
        </tr>
      </thead>
      <tbody>
        {events.map((event) => (
          <tr key={event.id}>
            <td>{renderEventType(event.event_type)}</td>
            <td>{event.description ?? "-"}</td>
            <td>
              {new Date(event.created_at).toLocaleString("nl-BE")}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
