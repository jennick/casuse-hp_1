import { apiFetch } from '@/shared/api/apiClient'
import {
  CustomerListItem,
  CustomersListResponse,
  CustomerDetail,
} from './customers.types'

/**
 * Haal lijst van klanten op (admin)
 */
export async function fetchCustomers(): Promise<CustomersListResponse> {
  return apiFetch<CustomersListResponse>('/api/admin/customers')
}

/**
 * Haal één klant op via ID
 */
export async function fetchCustomerById(
  id: string
): Promise<CustomerDetail> {
  return apiFetch<CustomerDetail>(`/api/admin/customers/${id}`)
}

/**
 * Update klantgegevens
 */
export async function updateCustomer(
  id: string,
  payload: Partial<CustomerDetail>
): Promise<void> {
  await apiFetch<void>(`/api/admin/customers/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

/**
 * Activeer klant
 */
export async function activateCustomer(id: string): Promise<void> {
  await apiFetch<void>(`/api/admin/customers/${id}/activate`, {
    method: 'POST',
  })
}

/**
 * Deactiveer klant
 */
export async function deactivateCustomer(id: string): Promise<void> {
  await apiFetch<void>(`/api/admin/customers/${id}/deactivate`, {
    method: 'POST',
  })
}

/**
 * Reset wachtwoord van klant
 */
export async function resetCustomerPassword(
  id: string
): Promise<{ success: boolean; token?: string }> {
  return apiFetch<{ success: boolean; token?: string }>(
    `/api/admin/customers/${id}/reset_password`,
    {
      method: 'POST',
    }
  )
}
