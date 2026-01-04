/**
 * Audit / Event types voor Website Admin
 * Backend: website-backend (FastAPI)
 */

/**
 * Ondersteunde event types
 * Moet 1-op-1 overeenkomen met backend enums / strings
 */
export type AuditEventType =
  | "customer_created"
  | "customer_updated"
  | "customer_activated"
  | "customer_deactivated"
  | "login_invited"
  | "password_reset_requested"
  | "password_set"
  | "email_sent"
  | "document_uploaded"
  | "document_deleted"
  | "relation_added"
  | "relation_removed"
  | "system";

/**
 * Actor die de actie uitvoerde
 */
export interface AuditActor {
  id?: string;
  email?: string;
  type: "admin" | "system" | "customer";
}

/**
 * Hoofd Audit Event object
 */
export interface AuditEvent {
  id: string;
  customer_id: string;

  event_type: AuditEventType;
  message: string;

  actor: AuditActor;

  /**
   * Extra context (vrij JSON-object)
   * vb. { ip, user_agent, document_id, old_value, new_value }
   */
  metadata?: Record<string, unknown>;

  created_at: string; // ISO datetime
}

/**
 * API response voor event-lijsten
 */
export interface AuditEventListResponse {
  items: AuditEvent[];
  total: number;
}
