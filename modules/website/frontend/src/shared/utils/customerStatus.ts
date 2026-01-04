// src/shared/utils/customerStatus.ts
import { CustomerListItem } from '@/shared/types/customers'

export interface CustomerStatusDisplay {
  label: string
  backgroundColor: string
  color: string
  borderColor: string
}

/**
 * Bepaalt hoe de status van een klant getoond wordt in de UI.
 * Deze logica is CENTRAAL, zodat alle schermen consistent zijn.
 */
export function getCustomerStatusDisplay(
  customer: CustomerListItem
): CustomerStatusDisplay {
  // Gedeactiveerd (altijd hoogste prioriteit)
  if (!customer.is_active) {
    return {
      label: 'Gedeactiveerd',
      backgroundColor: '#fee2e2',
      color: '#991b1b',
      borderColor: '#fca5a5',
    }
  }

  // Actief + kan inloggen
  if (customer.has_login) {
    return {
      label: 'Actief',
      backgroundColor: '#dcfce7',
      color: '#166534',
      borderColor: '#86efac',
    }
  }

  // Nog geen login → kijk naar portal_status
  switch (customer.portal_status) {
    case 'invited':
      return {
        label: 'Uitgenodigd',
        backgroundColor: '#e0f2fe',
        color: '#075985',
        borderColor: '#7dd3fc',
      }

    case 'invitation_expired':
      return {
        label: 'Uitnodiging verlopen',
        backgroundColor: '#fef3c7',
        color: '#92400e',
        borderColor: '#fcd34d',
      }

    case 'no_invitation':
    default:
      return {
        label: 'Nog niet geactiveerd',
        backgroundColor: '#f1f5f9',
        color: '#334155',
        borderColor: '#cbd5e1',
      }
  }
}
