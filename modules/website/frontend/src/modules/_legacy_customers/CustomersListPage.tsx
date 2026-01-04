// modules/customers/CustomersListPage.tsx

import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { apiFetch } from '@/shared/api/apiClient'
import { CustomersListResponse, CustomerListItem } from '@/shared/types/customers'
import { getCustomerStatusDisplay } from '@/shared/utils/customerStatus'
import CustomersFilters from './CustomersFilters'
import CustomersTable from './CustomersTable'

const CustomersListPage: React.FC = () => {
  const navigate = useNavigate()

  const [customers, setCustomers] = useState<CustomerListItem[]>([])
  const [total, setTotal] = useState(0)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [filters, setFilters] = useState<Record<string, string>>({})
  const [page, setPage] = useState(1)
  const pageSize = 25

  const loadCustomers = async () => {
    try {
      setLoading(true)
      setError(null)

      const params = new URLSearchParams({
        page: String(page),
        page_size: String(pageSize),
        ...filters,
      })

      const data = await apiFetch<CustomersListResponse>(
        `/api/admin/customers?${params.toString()}`
      )

      setCustomers(data.items)
      setTotal(data.total)
    } catch (err: any) {
      console.error(err)

      if (err.message?.includes('401')) {
        navigate('/login')
        return
      }

      setError('Kon klanten niet laden.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadCustomers()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, filters])

  const handleRowClick = (customer: CustomerListItem) => {
    navigate(`/customers/${customer.id}`)
  }

  if (loading) {
    return <p>Laden…</p>
  }

  return (
    <div>
      <h1>Klanten</h1>

      <CustomersFilters
        filters={filters}
        onChange={setFilters}
        onReset={() => {
          setFilters({})
          setPage(1)
        }}
      />

      {error && (
        <p style={{ color: 'red', marginBottom: '1rem' }}>
          {error}
        </p>
      )}

      <CustomersTable
        customers={customers}
        getStatusDisplay={getCustomerStatusDisplay}
        onRowClick={handleRowClick}
      />

      <div style={{ marginTop: '1rem' }}>
        <button
          disabled={page === 1}
          onClick={() => setPage(p => p - 1)}
        >
          Vorige
        </button>

        <span style={{ margin: '0 0.75rem' }}>
          Pagina {page} van {Math.ceil(total / pageSize)}
        </span>

        <button
          disabled={page * pageSize >= total}
          onClick={() => setPage(p => p + 1)}
        >
          Volgende
        </button>
      </div>
    </div>
  )
}

export default CustomersListPage
