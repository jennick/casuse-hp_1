import React from "react";

/**
 * Ondersteunde statussen binnen de website-admin context
 * (klanten, accounts, uitnodigingen, blokkeringen, etc.)
 */
export type StatusBadgeType =
  | "active"
  | "inactive"
  | "invited"
  | "blocked"
  | "pending"
  | "error";

export interface StatusBadgeProps {
  /** Status sleutel */
  status: StatusBadgeType;

  /** Optioneel: custom label (overschrijft standaard tekst) */
  label?: string;

  /** Optioneel: extra CSS class */
  className?: string;
}

const STATUS_CONFIG: Record<
  StatusBadgeType,
  { label: string; background: string; color: string }
> = {
  active: {
    label: "Actief",
    background: "#dcfce7",
    color: "#166534",
  },
  inactive: {
    label: "Inactief",
    background: "#f3f4f6",
    color: "#374151",
  },
  invited: {
    label: "Uitgenodigd",
    background: "#e0f2fe",
    color: "#075985",
  },
  blocked: {
    label: "Geblokkeerd",
    background: "#fee2e2",
    color: "#991b1b",
  },
  pending: {
    label: "In afwachting",
    background: "#fef9c3",
    color: "#854d0e",
  },
  error: {
    label: "Fout",
    background: "#fee2e2",
    color: "#7f1d1d",
  },
};

/**
 * Generieke status badge
 * Wordt gebruikt in:
 * - CustomersTable
 * - CustomerDetailPage
 * - Documenten / Events / Relaties
 */
export default function StatusBadge({
  status,
  label,
  className,
}: StatusBadgeProps) {
  const config = STATUS_CONFIG[status];

  return (
    <span
      className={className}
      style={{
        display: "inline-flex",
        alignItems: "center",
        padding: "0.25rem 0.5rem",
        borderRadius: "9999px",
        fontSize: "0.75rem",
        fontWeight: 600,
        backgroundColor: config.background,
        color: config.color,
        whiteSpace: "nowrap",
      }}
    >
      {label ?? config.label}
    </span>
  );
}
