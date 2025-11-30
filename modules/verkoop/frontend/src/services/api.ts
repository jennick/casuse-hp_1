// modules/verkoop/frontend/src/services/api.ts

import axios from "axios";

// Base API-client — blijft zoals je het had
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_VERKOOP_API_BASE_URL, // bv. http://localhost:20030
  withCredentials: true,
});

/* ===========================
   🔹 SELLERS (reeds werkend)
   =========================== */

export const fetchSellers = async () => {
  const response = await apiClient.get("/api/v1/sellers");
  return response.data;
};

export const getSellerById = async (sellerId: string) => {
  const response = await apiClient.get(`/api/v1/sellers/${sellerId}`);
  return response.data;
};

export const createSeller = async (sellerData: any) => {
  const response = await apiClient.post("/api/v1/sellers", sellerData);
  return response.data;
};

export const updateSeller = async (sellerId: string, data: any) => {
  const response = await apiClient.patch(`/api/v1/sellers/${sellerId}`, data);
  return response.data;
};

export const deleteSeller = async (sellerId: string) => {
  const response = await apiClient.delete(`/api/v1/sellers/${sellerId}`);
  return response.data;
};


/* ===========================
   🔹 CUSTOMERS (toegevoegd!)
   =========================== */

// ✔ Klanten ophalen via GET /api/v1/customers
export const fetchCustomers = async (
  search?: string,
  status?: string
): Promise<any> => {
  const params: any = {};
  if (search) params.search = search;
  if (status) params.status = status;

  const response = await apiClient.get("/api/v1/customers", { params });
  return response.data;
};

// ✔ Synchroniseren vanuit Website-module
// POST /api/v1/customers/sync-from-website
export const syncCustomersFromWebsite = async (): Promise<any> => {
  const response = await apiClient.post(
    "/api/v1/customers/sync-from-website"
  );
  return response.data;
};




/* ===========================
   🔹 AUTH (indien later nodig)
   =========================== */

export const login = async (email: string, password: string) => {
  const response = await apiClient.post("/public/login", { email, password });
  return response.data;
};

export const logout = async () => {
  const response = await apiClient.post("/public/logout");
  return response.data;
};
