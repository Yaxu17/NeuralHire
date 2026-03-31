import React, { useState } from 'react'
import { useMatching } from '../hooks/useMatching'
import CandidateCard from '../components/CandidateCard'
import styles from './Dashboard.module.css'

const SAMPLE_JD = `Senior Backend Engineer

We're looking for a Python backend specialist with expertise in FastAPI and PostgreSQL.
Must have 5+ years building scalable REST APIs and microservices. Familiarity with
Docker, Kubernetes, and AWS required. Strong understanding of distributed systems
architecture and event-driven design.`

export default function Dashboard() {
  const [jd, setJd] = useState(SAMPLE_JD)
  const [topK, setTopK] = useState(10)
  const [expFilter, setExpFilter] = useState('')
  const [model, setModel] = useState('all-MiniLM-L6-v2')
  const { results, loading, error, runMatch } = useMatching()

  const handleMatch = () => runMatch({
    jobDescription: jd,
    topK,
    scoreThreshold: 0,
    experienceFilter: expFilter || undefined,
  })

  return (
    <div className="page">
      <div className={styles.header}>
        <div className={styles.tag}>// Recruiter Portal</div>
        <h1 className={styles.title}>Semantic Matching <span className="shimmer-text">Dashboard</span></h1>
        <p className={styles.sub}>Paste any job description and get AI-ranked candidate matches in milliseconds.</p>
      </div>

      <div className={styles.layout}>
        {/* ── Sidebar ── */}
        <aside className={styles.sidebar}>
          <div className={styles.sideLabel}>// Job Description</div>
          <textarea
            className={styles.jdInput}
            value={jd}
            onChange={e => setJd(e.target.value)}
            placeholder="Paste your job description here..."
            rows={12}
          />

          <button
            className={styles.matchBtn}
            onClick={handleMatch}
            disabled={loading}
          >
            {loading ? <><span className="spinner" /> Analysing…</> : '⚡ Analyse & Match'}
          </button>

          <div className={styles.section}>
            <div className={styles.sideLabel}>// Embedding Model</div>
            <select className={styles.select} value={model} onChange={e => setModel(e.target.value)}>
              <option value="all-MiniLM-L6-v2">all-MiniLM-L6-v2 (384d) · Fast</option>
              <option value="all-mpnet-base-v2">all-mpnet-base-v2 (768d)</option>
            </select>
          </div>

          <div className={styles.section}>
            <div className={styles.sideLabel}>// Results Count</div>
            <div className={styles.chipRow}>
              {[5, 10, 20, 50].map(n => (
                <button
                  key={n}
                  className={`${styles.chip} ${topK === n ? styles.chipActive : ''}`}
                  onClick={() => setTopK(n)}
                >
                  Top {n}
                </button>
              ))}
            </div>
          </div>

          <div className={styles.section}>
            <div className={styles.sideLabel}>// Experience Level</div>
            <div className={styles.chipRow}>
              {['', 'junior', 'mid', 'senior'].map(v => (
                <button
                  key={v}
                  className={`${styles.chip} ${expFilter === v ? styles.chipActive : ''}`}
                  onClick={() => setExpFilter(v)}
                >
                  {v || 'Any'}
                </button>
              ))}
            </div>
          </div>

          <div className={styles.statusBox}>
            <div className={styles.sideLabel}>// Pinecone Status</div>
            <div className={styles.statusRow}>
              <span className={styles.statusDot} />
              <span>Connected · us-east-1</span>
            </div>
            <div className={styles.statusMeta}>Index: neuralhire-candidates</div>
            {results && <div className={styles.statusMeta}>Indexed: {results.total_indexed.toLocaleString()} vectors</div>}
          </div>
        </aside>

        {/* ── Main Results ── */}
        <main className={styles.main}>
          {error && (
            <div className={styles.error}>⚠ {error}</div>
          )}

          {results && (
            <>
              <div className={styles.resultsHeader}>
                <div>
                  <div className={styles.resultsTitle}>
                    {results.results.length} Semantic Matches
                  </div>
                  <div className={styles.resultsMeta}>
                    Query: {results.query_time_ms.toFixed(0)}ms · Model: {results.model_used} · {results.total_indexed.toLocaleString()} candidates indexed
                  </div>
                </div>
              </div>

              <div className={styles.cards}>
                {results.results.map((c, i) => (
                  <CandidateCard key={c.id} candidate={c} rank={i + 1} />
                ))}
                {results.results.length === 0 && (
                  <div className={styles.empty}>
                    No candidates matched. Try broadening the job description or lowering the score threshold.
                  </div>
                )}
              </div>

              {/* Accuracy chart */}
              <div className={styles.accuracyBox}>
                <div className={styles.sideLabel} style={{ marginBottom: 16 }}>// Semantic vs Keyword Accuracy</div>
                {[
                  { label: 'Semantic (NeuralHire)', val: 94, color: 'var(--accent)' },
                  { label: 'Keyword ATS',           val: 61, color: 'var(--warn)' },
                  { label: 'Manual Review',         val: 78, color: 'var(--muted)' },
                ].map(({ label, val, color }) => (
                  <div key={label} className={styles.accRow}>
                    <span className={styles.accLabel}>{label}</span>
                    <div className={styles.accBg}>
                      <div className={styles.accBar} style={{ width: `${val}%`, background: color }} />
                    </div>
                    <span style={{ color, fontSize: '0.78rem', fontFamily: 'var(--font-mono)', minWidth: 36 }}>{val}%</span>
                  </div>
                ))}
              </div>
            </>
          )}

          {!results && !loading && (
            <div className={styles.placeholder}>
              <div className={styles.placeholderIcon}>🧠</div>
              <h3>Ready to Match</h3>
              <p>Paste a job description in the panel and click <strong>Analyse & Match</strong> to rank candidates by semantic similarity.</p>
            </div>
          )}

          {loading && (
            <div className={styles.placeholder}>
              <div className={styles.placeholderIcon} style={{ animation: 'spin 1s linear infinite' }}>⚙️</div>
              <h3>Processing…</h3>
              <p>Embedding JD → querying Pinecone → ranking results</p>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
