import { useEffect, useState } from 'react';

import { fetchCustomers } from './customers.api';
import { CustomerListItem } from './customers.types';

import CustomersFilters from './CustomersFilters';
import CustomersTable from './CustomersTable';

export default function CustomersPage() {
  const [customers, setCustomers] = useState<CustomerListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // filters (kan later uitgebreid worden)
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<'active' | 'inactive' | 'all'>('active');

  useEffect(() => {
    loadCustomers();
  }, []);

  async function loadCustomers() {
    try {
      setLoading(true);
      setError(null);

      const data = await fetchCustomers({
        search,
        status: statusFilter === 'all' ? undefined : statusFilter,
      });

      setCustomers(data.items);
    } catch (err: any) {
      setError(err?.message ?? 'Fout bij laden van klanten');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>Klanten</h1>

      <CustomersFilters
        search={search}
        status={statusFilter}
        onSearchChange={setSearch}
        onStatusChange={setStatusFilter}
        onApply={loadCustomers}
      />

      {loading && <p>Laden…</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {!loading && !error && (
        <CustomersTable customers={customers} />
      )}
    </div>
  );
}
