import axios from "axios";
const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:20010";
export const api = axios.create({ baseURL: API_BASE });
export const login = (email: string, password: string, totp?: string) =>
  api.post("/auth/login", { username: email, password, totp: totp || null }).then(r => r.data);
export const getModules = (token: string) =>
  api.get("/modules", { headers: { Authorization: `Bearer ${token}` } }).then(r => r.data);
export const askAI = (question: string) =>
  api.post("/ai/ask", { question }).then(r => r.data);
