import { useEffect, useState } from "react";

import { apiFetch } from "@/shared/api/apiClient";
import { CustomerRelation } from "@/shared/types/relations";

/**
 * Hook: relaties van één klant ophalen (website-admin)
 */
export function useCustomerRelations(customerId: string) {
  const [relations, setRelations] = useState<CustomerRelation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  async function fetchRelations() {
    if (!customerId) return;

    try {
      setLoading(true);
      setError(null);

      const data = await apiFetch<CustomerRelation[]>(
        `/api/admin/customers/${customerId}/relations`
      );

      setRelations(data);
    } catch (err) {
      console.error("Failed to fetch relations", err);
      setError("Relaties konden niet geladen worden.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchRelations();
  }, [customerId]);

  return {
    relations,
    loading,
    error,
    refresh: fetchRelations,
  };
}
