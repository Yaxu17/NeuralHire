/**
 * NeuralHire API Client
 * Wraps all backend calls with axios.
 */

import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 30_000,
  headers: { 'Content-Type': 'application/json' },
})

// ── Health ────────────────────────────────────────────────────────────────────
export const fetchHealth = () => api.get('/health').then(r => r.data)

// ── Job Matching ──────────────────────────────────────────────────────────────
/**
 * POST /api/jobs/match
 * @param {object} payload
 * @param {string} payload.job_description
 * @param {number} [payload.top_k=10]
 * @param {number} [payload.score_threshold=0]
 * @param {string} [payload.experience_filter]  junior | mid | senior
 * @returns {Promise<JobMatchResponse>}
 */
export const matchCandidates = (payload) =>
  api.post('/jobs/match', payload).then(r => r.data)

// ── Candidates ────────────────────────────────────────────────────────────────
/**
 * POST /api/candidates/  — add candidate via JSON
 */
export const createCandidate = (data) =>
  api.post('/candidates/', data).then(r => r.data)

/**
 * POST /api/candidates/upload — add candidate via resume file
 */
export const uploadCandidate = (formData) =>
  api.post('/candidates/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }).then(r => r.data)

/**
 * DELETE /api/candidates/:id
 */
export const deleteCandidate = (id) =>
  api.delete(`/candidates/${id}`).then(r => r.data)

export default api
