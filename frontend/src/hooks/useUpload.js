/**
 * useUpload hook
 * Manages resume file upload flow.
 */

import { useState, useCallback } from 'react'
import { uploadCandidate } from '../utils/api'
import toast from 'react-hot-toast'

export function useUpload() {
  const [uploading, setUploading] = useState(false)
  const [uploaded, setUploaded] = useState([])

  const upload = useCallback(async ({ file, name, email, role, years_experience, skills }) => {
    setUploading(true)
    const fd = new FormData()
    fd.append('file', file)
    fd.append('name', name)
    fd.append('email', email)
    fd.append('role', role || '')
    fd.append('years_experience', years_experience || 0)
    fd.append('skills', skills || '')

    try {
      const result = await uploadCandidate(fd)
      setUploaded(prev => [result, ...prev])
      toast.success(`${name}'s resume indexed successfully!`)
      return result
    } catch (err) {
      const msg = err.response?.data?.detail || 'Upload failed.'
      toast.error(msg)
      return null
    } finally {
      setUploading(false)
    }
  }, [])

  return { uploading, uploaded, upload }
}
