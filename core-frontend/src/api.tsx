import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:20010";

export const api = axios.create({
  baseURL: API_BASE,
  withCredentials: false,
});

export const login = async (email: string, password: string, totp?: string) => {
  const { data } = await api.post("/auth/login", {
    username: email,
    password,
    totp: totp || null,
  });
  return data;
};

export const getModules = async (token: string) => {
  const { data } = await api.get("/modules", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return data;
};

export const askAI = async (question: string) => {
  const { data } = await api.post("/ai/ask", { question });
  return data;
};
