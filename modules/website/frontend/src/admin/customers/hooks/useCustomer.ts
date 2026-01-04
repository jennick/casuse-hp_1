import { useEffect, useState } from "react";

import { apiFetch } from "@/shared/api/apiClient";
import { Customer } from "@/shared/types/customers";

export function useCustomers() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  async function fetchCustomers() {
    try {
      setLoading(true);
      setError(null);

      const data = await apiFetch<Customer[]>(
        "/api/admin/customers"
      );

      setCustomers(data);
    } catch (err) {
      console.error("Failed to fetch customers", err);
      setError("Klanten konden niet geladen worden.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchCustomers();
  }, []);

  return {
    customers,
    loading,
    error,
    refresh: fetchCustomers,
  };
}
