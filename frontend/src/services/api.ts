import axios from "axios";
import { getToken, removeToken } from "@/lib/auth";

// Single source of truth for the backend origin. The backend mounts its
// routers at the root (e.g. /auth, /resumes, /apply), so this must NOT
// include an /api/v1 suffix. Override via NEXT_PUBLIC_API_URL in production.
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Automatically attach JWT token to every request
api.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 Unauthorized globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      if (typeof window !== 'undefined') {
        removeToken();
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);