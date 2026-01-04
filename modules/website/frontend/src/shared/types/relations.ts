/**
 * Customer Relations types
 * Website Admin – gedeelde types
 */

/**
 * Modules waarmee een klant gelinkt kan zijn
 * Moet overeenkomen met backend values
 */
export type RelationModule =
  | "verkoop"
  | "facturatie"
  | "magazijn"
  | "productie"
  | "inventaries"
  | "website"
  | "core";

/**
 * Type relatie tussen klant en module
 */
export type RelationType =
  | "owner"
  | "viewer"
  | "editor"
  | "linked";

/**
 * Status van de relatie
 */
export type RelationStatus =
  | "active"
  | "inactive"
  | "blocked";

/**
 * Relatie object
 */
export interface CustomerRelation {
  id: string;

  customer_id: string;

  module: RelationModule;
  relation_type: RelationType;
  status: RelationStatus;

  /**
   * Optionele externe ID
   * vb. seller_id, account_id, customer_ref
   */
  external_reference?: string;

  created_at: string; // ISO datetime
  updated_at?: string; // ISO datetime
}

/**
 * API response voor lijst van relaties
 */
export interface CustomerRelationsResponse {
  items: CustomerRelation[];
  total: number;
}
