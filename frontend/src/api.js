const API_URL = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8080").replace(/\/$/, "");

async function request(path, options) {
  const response = await fetch(`${API_URL}${path}`, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = Array.isArray(payload.detail)
      ? payload.detail.map((item) => item.msg).join(". ")
      : payload.detail;
    throw new Error(detail || `Error HTTP ${response.status}`);
  }
  return payload;
}

export const getCatalog = () => request("/suites");

export const createRun = (payload) =>
  request("/runs", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

export const getRun = (runId) => request(`/runs/${runId}`);

export const reportUrl = (runId, format) =>
  `${API_URL}/runs/${runId}/reports/${format}`;

export const analyzeRequirement = (payload) =>
  request("/ai/analyses", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

export const generateDraft = (payload) =>
  request("/ai/drafts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

export const reviewDraft = (analysisId, payload) =>
  request(`/ai/analyses/${analysisId}/review`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
