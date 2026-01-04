// src/modules/customers/CustomersFilters.tsx
import React from 'react'

interface CustomersFiltersProps {
  search: string
  onSearchChange: (value: string) => void
}

const CustomersFilters: React.FC<CustomersFiltersProps> = ({
  search,
  onSearchChange,
}) => {
  return (
    <div style={{ marginBottom: '1rem' }}>
      <input
        type="text"
        placeholder="Zoek op naam, email of bedrijf…"
        value={search}
        onChange={(e) => onSearchChange(e.target.value)}
        style={{
          width: '100%',
          padding: '0.5rem',
          borderRadius: 4,
          border: '1px solid #d1d5db',
          fontSize: '0.9rem',
        }}
      />
    </div>
  )
}

export default CustomersFilters
