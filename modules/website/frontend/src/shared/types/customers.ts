// src/shared/types/customers.ts

export type CustomerType = "particulier" | "bedrijf";

/* ===============================
   Auth / token
================================ */
export interface TokenResponse {
  access_token: string;
  token_type: string;
}

/* ===============================
   Customer list item (admin UI)
================================ */
export interface CustomerListItem {
  id: string;

  // 🔐 extern, stabiel ID (read-only)
  customer_uuid: string;

  email: string;
  first_name: string;
  last_name: string;
  phone_number?: string | null;

  customer_type: CustomerType;
  description?: string | null;

  company_name?: string | null;
  tax_id?: string | null;

  address_street?: string | null;
  address_ext_number?: string | null;
  address_int_number?: string | null;
  address_neighborhood?: string | null;
  address_city?: string | null;
  address_state?: string | null;
  address_postal_code?: string | null;
  address_country?: string | null;

  is_active: boolean;

  // ───── Portal / login status (van backend) ─────
  has_login: boolean;
  portal_status?: string | null;
  deactivated_at?: string | null;
}

/* ===============================
   Customer list response
================================ */
export interface CustomersListResponse {
  items: CustomerListItem[];
  total: number;
}

/* ===============================
   Customer detail (admin detail)
================================ */
export interface CustomerDetail extends CustomerListItem {
  is_admin: boolean;
  created_at: string;
  updated_at: string;

  hashed_password?: string | null;
}

/* ===============================
   Password reset
================================ */
export interface PasswordResetResponse {
  success: boolean;
  token?: string;
}
