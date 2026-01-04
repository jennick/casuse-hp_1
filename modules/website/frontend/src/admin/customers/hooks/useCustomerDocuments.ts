import { useEffect, useState } from "react";

import { apiFetch } from "@/shared/api/apiClient";
import { CustomerDocument } from "@/shared/types/documents";

/**
 * Hook: documenten van één klant ophalen (website-admin)
 */
export function useCustomerDocuments(customerId: string) {
  const [documents, setDocuments] = useState<CustomerDocument[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  async function fetchDocuments() {
    if (!customerId) return;

    try {
      setLoading(true);
      setError(null);

      const data = await apiFetch<CustomerDocument[]>(
        `/api/admin/customers/${customerId}/documents`
      );

      setDocuments(data);
    } catch (err) {
      console.error("Failed to fetch documents", err);
      setError("Documenten konden niet geladen worden.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchDocuments();
  }, [customerId]);

  return {
    documents,
    loading,
    error,
    refresh: fetchDocuments,
  };
}
