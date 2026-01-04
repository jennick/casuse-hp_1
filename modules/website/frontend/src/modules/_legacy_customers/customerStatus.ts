import { CustomerListItem } from './customers.types';

export function getCustomerStatusDisplay(c: CustomerListItem) {
  // 1) Gedeactiveerd
  if (!c.is_active) {
    return {
      label: 'Gedeactiveerd',
      backgroundColor: '#fee2e2',
      color: '#991b1b',
      borderColor: '#fecaca',
    };
  }

  // 2) Actief + login
  if (c.has_login) {
    return {
      label: 'Actief – login aangemaakt',
      backgroundColor: '#dcfce7',
      color: '#166534',
      borderColor: '#bbf7d0',
    };
  }

  // 3) Actief zonder login
  return {
    label: 'Actief – géén login',
    backgroundColor: '#fef3c7',
    color: '#92400e',
    borderColor: '#fed7aa',
  };
}
