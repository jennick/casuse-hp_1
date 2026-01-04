import React from "react";

/**
 * Lege-toestand component
 * Gebruikt in tables, tabs en detailpagina’s
 */

export interface EmptyStateProps {
  /** Titel bovenaan */
  title: string;

  /** Beschrijvende tekst */
  description?: string;

  /** Optionele actieknop */
  actionLabel?: string;

  /** Callback voor actieknop */
  onAction?: () => void;

  /** Extra CSS class */
  className?: string;
}

export default function EmptyState({
  title,
  description,
  actionLabel,
  onAction,
  className,
}: EmptyStateProps) {
  return (
    <div
      className={`empty-state ${className ?? ""}`}
      style={{
        padding: "2rem",
        textAlign: "center",
        color: "#555",
      }}
    >
      <div
        style={{
          fontSize: "2rem",
          marginBottom: "0.75rem",
          opacity: 0.6,
        }}
      >
        📄
      </div>

      <h3 style={{ marginBottom: "0.5rem" }}>{title}</h3>

      {description && (
        <p style={{ maxWidth: 420, margin: "0 auto 1rem" }}>
          {description}
        </p>
      )}

      {actionLabel && onAction && (
        <button
          onClick={onAction}
          style={{
            padding: "0.5rem 1rem",
            borderRadius: 6,
            border: "1px solid #ccc",
            background: "#fff",
            cursor: "pointer",
          }}
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
}
