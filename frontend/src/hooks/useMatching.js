/**
 * useMatching hook
 * Manages state for the semantic matching flow.
 */

import { useState, useCallback } from 'react'
import { matchCandidates } from '../utils/api'
import toast from 'react-hot-toast'

export function useMatching() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const runMatch = useCallback(async ({ jobDescription, topK, scoreThreshold, experienceFilter }) => {
    if (!jobDescription?.trim()) {
      toast.error('Please enter a job description.')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const data = await matchCandidates({
        job_description: jobDescription,
        top_k: topK ?? 10,
        score_threshold: scoreThreshold ?? 0,
        experience_filter: experienceFilter || undefined,
      })
      setResults(data)
      toast.success(`Found ${data.results.length} matches in ${data.query_time_ms.toFixed(0)}ms`)
    } catch (err) {
      const msg = err.response?.data?.detail || 'Matching failed. Is the backend running?'
      setError(msg)
      toast.error(msg)
    } finally {
      setLoading(false)
    }
  }, [])

  const reset = useCallback(() => {
    setResults(null)
    setError(null)
  }, [])

  return { results, loading, error, runMatch, reset }
}
