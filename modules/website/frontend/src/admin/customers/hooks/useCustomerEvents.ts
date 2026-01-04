import { useEffect, useState } from "react";

import { apiFetch } from "@/shared/api/apiClient";
import { CustomerEvent } from "@/shared/types/audit";

/**
 * Hook: events / auditlog van één klant ophalen (website-admin)
 */
export function useCustomerEvents(customerId: string) {
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
      setError("Activiteiten konden niet geladen worden.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchEvents();
  }, [customerId]);

  return {
    events,
    loading,
    error,
    refresh: fetchEvents,
  };
}
