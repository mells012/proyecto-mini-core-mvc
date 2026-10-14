import axios from "axios";

// La URL base de la API se toma de una variable de entorno (definida en
// Vite con el prefijo VITE_) para poder apuntar a localhost en desarrollo
// y al backend desplegado en Render en produccion.
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Log simple de requests y responses, util para depurar durante el desarrollo.
api.interceptors.request.use((config) => {
  console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("[API] Error:", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default api;
