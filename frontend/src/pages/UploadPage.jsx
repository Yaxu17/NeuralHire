import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { useUpload } from '../hooks/useUpload'
import styles from './UploadPage.module.css'

export default function UploadPage() {
  const { uploading, uploaded, upload } = useUpload()
  const [form, setForm] = useState({ name: '', email: '', role: '', years_experience: '', skills: '' })
  const [file, setFile] = useState(null)

  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles[0]) setFile(acceptedFiles[0])
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'], 'text/plain': ['.txt'] },
    maxFiles: 1,
    maxSize: 5 * 1024 * 1024,
  })

  const handleChange = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }))

  const handleSubmit = async e => {
    e.preventDefault()
    if (!file) { alert('Please upload a resume file.'); return }
    if (!form.name || !form.email) { alert('Name and email are required.'); return }
    const result = await upload({ file, ...form })
    if (result) {
      setFile(null)
      setForm({ name: '', email: '', role: '', years_experience: '', skills: '' })
    }
  }

  return (
    <div className="page">
      <div className={styles.header}>
        <div className={styles.tag}>// Candidate Ingestion</div>
        <h1 className={styles.title}>Add <span className="shimmer-text">Candidates</span></h1>
        <p className={styles.sub}>Upload resumes (PDF, DOCX, TXT). The system will extract text, generate embeddings, and index into Pinecone automatically.</p>
      </div>

      <div className={styles.layout}>
        <form className={styles.form} onSubmit={handleSubmit}>
          {/* Dropzone */}
          <div className={styles.sideLabel}>// Resume File</div>
          <div {...getRootProps()} className={`${styles.dropzone} ${isDragActive ? styles.drag : ''} ${file ? styles.hasFile : ''}`}>
            <input {...getInputProps()} />
            {file ? (
              <div className={styles.fileInfo}>
                <span className={styles.fileIcon}>📄</span>
                <span className={styles.fileName}>{file.name}</span>
                <span className={styles.fileSize}>({(file.size / 1024).toFixed(0)} KB)</span>
                <button type="button" className={styles.removeFile} onClick={e => { e.stopPropagation(); setFile(null) }}>✕</button>
              </div>
            ) : (
              <div className={styles.dropPlaceholder}>
                <div className={styles.dropIcon}>☁️</div>
                <div className={styles.dropText}>{isDragActive ? 'Drop it!' : 'Drag & drop resume or click to browse'}</div>
                <div className={styles.dropSub}>PDF · DOCX · TXT · Max 5MB</div>
              </div>
            )}
          </div>

          {/* Fields */}
          <div className={styles.fields}>
            <div className={styles.fieldGroup}>
              <label className={styles.sideLabel}>// Full Name *</label>
              <input className={styles.input} name="name" value={form.name} onChange={handleChange} placeholder="e.g. Aisha Mehta" required />
            </div>
            <div className={styles.fieldGroup}>
              <label className={styles.sideLabel}>// Email *</label>
              <input className={styles.input} name="email" type="email" value={form.email} onChange={handleChange} placeholder="aisha@example.com" required />
            </div>
            <div className={styles.fieldGroup}>
              <label className={styles.sideLabel}>// Current Role</label>
              <input className={styles.input} name="role" value={form.role} onChange={handleChange} placeholder="e.g. Senior Backend Engineer" />
            </div>
            <div className={styles.fieldGroup}>
              <label className={styles.sideLabel}>// Years of Experience</label>
              <input className={styles.input} name="years_experience" type="number" min="0" max="60" value={form.years_experience} onChange={handleChange} placeholder="e.g. 5" />
            </div>
            <div className={styles.fieldGroup} style={{ gridColumn: '1 / -1' }}>
              <label className={styles.sideLabel}>// Key Skills (comma-separated)</label>
              <input className={styles.input} name="skills" value={form.skills} onChange={handleChange} placeholder="Python, FastAPI, PostgreSQL, Docker, AWS" />
            </div>
          </div>

          <button className={styles.submitBtn} type="submit" disabled={uploading}>
            {uploading ? <><span className="spinner" /> Indexing…</> : '⚡ Index Candidate'}
          </button>
        </form>

        {/* Recent uploads */}
        <div className={styles.recentPanel}>
          <div className={styles.sideLabel}>// Recently Indexed</div>
          {uploaded.length === 0 ? (
            <div className={styles.emptyUploads}>
              <div style={{ fontSize: '2rem', marginBottom: 12 }}>📂</div>
              <p>No candidates indexed yet this session.</p>
            </div>
          ) : (
            uploaded.map(c => (
              <div key={c.id} className={styles.uploadedCard}>
                <div className={styles.uploadedName}>{c.name}</div>
                <div className={styles.uploadedRole}>{c.role || 'Candidate'} · {c.email}</div>
                <div className={styles.uploadedSkills}>
                  {(c.skills || []).slice(0, 4).map(s => (
                    <span key={s} className={styles.uploadedSkill}>{s}</span>
                  ))}
                </div>
                <div className={styles.uploadedId}>ID: {c.id.slice(0, 8)}…</div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
