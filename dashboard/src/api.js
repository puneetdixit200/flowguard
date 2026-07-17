// Centralized API client — every component imports from here instead of
// hardcoding fetch calls, so if the backend URL changes, we edit ONE file.
import axios from "axios";

const api = axios.create({ baseURL: "http://127.0.0.1:8000" });

export const getHealth = () => api.get("/health").then(r => r.data);
export const getFlows = () => api.get("/flows/recent?limit=50").then(r => r.data);
export const getAlerts = () => api.get("/alerts").then(r => r.data);
export const getGnnStatus = () => api.get("/gnn/status").then(r => r.data);
export const runAnalysis = () => api.post("/analyze");

export default api;
