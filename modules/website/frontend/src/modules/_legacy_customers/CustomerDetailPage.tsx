// modules/customers/CustomerDetailPage.tsx
import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { apiFetch } from '@/shared/api/apiClient'
import {
  CustomerDetail,
  PasswordResetResponse,
} from '@/shared/types/customers'
import { getCustomerStatusDisplay } from '@/shared/utils/customerStatus'

const CustomerDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const [customer, setCustomer] = useState<CustomerDetail | null>(null)
  const [loading, setLoading] = useState(true)

  const [actionLoading, setActionLoading] = useState(false)
  const [actionError, setActionError] = useState<string | null>(null)
  const [actionSuccess, setActionSuccess] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return

    const load = async () => {
      try {
        const data = await apiFetch<CustomerDetail>(
          `/api/admin/customers/${id}`
        )
        setCustomer(data)
      } catch (err) {
        console.error(err)
        navigate('/customers', { replace: true })
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [id, navigate])

  const reloadCustomer = async () => {
    if (!id) return
    const data = await apiFetch<CustomerDetail>(
      `/api/admin/customers/${id}`
    )
    setCustomer(data)
  }

  const handleDeactivate = async () => {
    if (!id) return
    if (!window.confirm('Klant deactiveren?')) return

    try {
      setActionLoading(true)
      setActionError(null)
      setActionSuccess(null)

      await apiFetch(
        `/api/admin/customers/${id}/deactivate`,
        { method: 'POST' }
      )

      await reloadCustomer()
      setActionSuccess('Klant gedeactiveerd.')
    } catch (err) {
      console.error(err)
      setActionError('Deactiveren mislukt.')
    } finally {
      setActionLoading(false)
    }
  }

  const handleActivate = async () => {
    if (!id) return

    try {
      setActionLoading(true)
      setActionError(null)
      setActionSuccess(null)

      await apiFetch(
        `/api/admin/customers/${id}/activate`,
        { method: 'POST' }
      )

      await reloadCustomer()
      setActionSuccess('Klant geactiveerd.')
    } catch (err) {
      console.error(err)
      setActionError('Activeren mislukt.')
    } finally {
      setActionLoading(false)
    }
  }

  const handleResetPassword = async () => {
    if (!id) return
    if (!window.confirm('Wachtwoord resetten?')) return

    try {
      setActionLoading(true)
      setActionError(null)
      setActionSuccess(null)

      const data = await apiFetch<PasswordResetResponse>(
        `/api/admin/customers/${id}/reset_password`,
        { method: 'POST' }
      )

      let msg = 'Reset-link aangemaakt.'
      if (data.token) {
        msg += ` (debug token: ${data.token})`
      }

      setActionSuccess(msg)
    } catch (err) {
      console.error(err)
      setActionError('Reset mislukt.')
    } finally {
      setActionLoading(false)
    }
  }

  if (loading) {
    return <p>Laden…</p>
  }

  if (!customer) {
    return null
  }

  const status = getCustomerStatusDisplay(customer)

  return (
    <div>
      <button type="button" onClick={() => navigate('/customers')}>
        ← Terug naar klanten
      </button>

      <h1>
        {customer.first_name} {customer.last_name}
      </h1>

      <span
        style={{
          backgroundColor: status.backgroundColor,
          color: status.color,
          border: `1px solid ${status.borderColor}`,
          padding: '0.2rem 0.6rem',
          borderRadius: 9999,
          fontSize: '0.75rem',
          display: 'inline-block',
          marginBottom: '0.75rem',
        }}
      >
        {status.label}
      </span>

      {actionSuccess && (
        <p style={{ color: 'green' }}>{actionSuccess}</p>
      )}
      {actionError && (
        <p style={{ color: 'red' }}>{actionError}</p>
      )}

      <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem' }}>
        {customer.is_active ? (
          <button
            type="button"
            onClick={handleDeactivate}
            disabled={actionLoading}
          >
            Deactiveren
          </button>
        ) : (
          <button
            type="button"
            onClick={handleActivate}
            disabled={actionLoading}
          >
            Activeren
          </button>
        )}

        {customer.is_active && (
          <button
            type="button"
            onClick={handleResetPassword}
            disabled={actionLoading}
          >
            Reset wachtwoord
          </button>
        )}
      </div>
    </div>
  )
}

export default CustomerDetailPage
