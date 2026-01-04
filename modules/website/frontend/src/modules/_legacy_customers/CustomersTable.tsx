import { useNavigate } from 'react-router-dom'
import { CustomerListItem } from './customers.types'

/* ======================================================
   Lokale badges (tijdelijk, build-safe)
   ====================================================== */

function AccountStatusBadge({ status }: { status: AccountStatus }) {
  const map: Record<AccountStatus, { label: string; className: string }> = {
    invited: { label: 'Uitgenodigd', className: 'bg-gray-200 text-gray-800' },
    not_activated: { label: 'Niet geactiveerd', className: 'bg-orange-200 text-orange-900' },
    activated: { label: 'Geactiveerd', className: 'bg-blue-200 text-blue-900' },
    logged_in: { label: 'Ingelogd', className: 'bg-green-200 text-green-900' },
  }

  const cfg = map[status]

  return (
    <span className={`px-2 py-1 rounded text-xs font-medium ${cfg.className}`}>
      {cfg.label}
    </span>
  )
}

function StatusBadge({ active }: { active: boolean }) {
  return (
    <span
      className={`px-2 py-1 rounded text-xs font-medium ${
        active ? 'bg-green-200 text-green-900' : 'bg-red-200 text-red-900'
      }`}
    >
      {active ? 'Actief' : 'Geblokkeerd'}
    </span>
  )
}

/* ======================================================
   Types
   ====================================================== */

type AccountStatus =
  | 'invited'
  | 'not_activated'
  | 'activated'
  | 'logged_in'

interface Props {
  customers: CustomerListItem[]
}

/* ======================================================
   Helper: accountstatus bepalen (tijdelijk)
   ====================================================== */

function resolveAccountStatus(customer: CustomerListItem): AccountStatus {
  // ⚠️ Tijdelijke logica — backend volgt later
  if (!customer.invited_at) return 'invited'
  if (!customer.has_password) return 'not_activated'
  if (customer.last_login_at) return 'logged_in'
  return 'activated'
}

/* ======================================================
   Component
   ====================================================== */

export default function CustomersTable({ customers }: Props) {
  const navigate = useNavigate()

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full border border-gray-200 rounded-md">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-2 text-left text-sm font-semibold">Naam</th>
            <th className="px-4 py-2 text-left text-sm font-semibold">Email</th>
            <th className="px-4 py-2 text-left text-sm font-semibold">Type</th>
            <th className="px-4 py-2 text-left text-sm font-semibold">
              Accountstatus
            </th>
            <th className="px-4 py-2 text-left text-sm font-semibold">Status</th>
            <th className="px-4 py-2 text-right text-sm font-semibold">Acties</th>
          </tr>
        </thead>

        <tbody>
          {customers.map((customer) => {
            const accountStatus = resolveAccountStatus(customer)

            return (
              <tr
                key={customer.id}
                className="border-t hover:bg-gray-50"
              >
                <td className="px-4 py-2">{customer.name}</td>
                <td className="px-4 py-2">{customer.email}</td>
                <td className="px-4 py-2">{customer.customer_type}</td>

                <td className="px-4 py-2">
                  <AccountStatusBadge status={accountStatus} />
                </td>

                <td className="px-4 py-2">
                  <StatusBadge active={customer.is_active} />
                </td>

                <td className="px-4 py-2 text-right">
                  <button
                    onClick={() => navigate(customer.id)}
                    className="text-sm text-blue-600 hover:underline"
                  >
                    Bekijk
                  </button>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
