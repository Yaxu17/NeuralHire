import React, { useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import styles from './LandingPage.module.css'

const STATS = [
  { num: '94%', label: 'Match Accuracy' },
  { num: '10x', label: 'Faster Screening' },
  { num: '70%', label: 'Less Manual Waste' },
  { num: '12ms', label: 'Avg Query Time' },
]

const PROBLEMS = [
  { icon: '🎭', title: 'Keyword Stuffing Epidemic', body: 'Candidates game the system by listing buzzwords without genuine expertise. A resume with "Python, ML, AI" passes ATS — whether from a senior engineer or a bootcamp graduate.', stat: '67% of candidates admit to keyword stuffing' },
  { icon: '⏳', title: 'The 70% Manual Waste Problem', body: 'Recruiters lose up to 70% of their time filtering profiles that "passed" keyword filters but lack real context, seniority, or skill depth.', stat: '$4,700 avg cost-per-hire wasted on bad screens' },
  { icon: '☕', title: 'The Java Paradox', body: 'A system that can\'t distinguish "Java Developer" from "Coffee Shop Manager (Java enthusiast)" creates bottlenecks. Literal matching has zero semantic awareness.', stat: '38% of ATS rejections are false negatives' },
  { icon: '🔍', title: 'Lexical vs Semantic Gap', body: '"React.js experience" won\'t match "built SPAs with Facebook\'s component library" — even though they mean the same thing. Context requires NLP-grade understanding.', stat: '45% of qualified candidates are overlooked' },
]

const STEPS = [
  { icon: '📋', num: '1', title: 'Paste Job Description', body: 'Recruiter inputs any complex JD into the portal' },
  { icon: '🧠', num: '2', title: 'Sentence Embedding', body: 'all-MiniLM-L6-v2 encodes it into a 384-dim vector' },
  { icon: '🔎', num: '3', title: 'Pinecone Query', body: 'Cosine similarity search across all indexed candidates' },
  { icon: '📊', num: '4', title: 'Ranked Results', body: 'Candidates ranked 0–100% with match summaries' },
  { icon: '✅', num: '5', title: 'Recruiter Decision', body: 'Data-backed shortlisting in seconds, not hours' },
]

const TECH = [
  { logo: '🤗', name: 'Sentence-Transformers', badge: 'HuggingFace', desc: 'Transforms resume and JD text into dense semantic vectors using all-MiniLM-L6-v2 (384 dimensions).', features: ['all-MiniLM-L6-v2 model', 'Batched encoding pipeline', 'L2-normalised outputs', 'Cross-lingual support'] },
  { logo: '🌲', name: 'Pinecone', badge: 'Vector Database', desc: 'Fully managed vector DB for storing and querying high-dimensional candidate embeddings with ms latency.', features: ['HNSW approximate nearest-neighbour', 'Real-time cosine similarity search', 'Metadata filtering', 'Serverless & auto-scaling'] },
  { logo: '⚡', name: 'FastAPI', badge: 'Backend Framework', desc: 'High-performance async Python API with automatic OpenAPI docs, type-safe endpoints, and CORS middleware.', features: ['Async endpoints with uvicorn', 'Pydantic schema validation', 'OpenAPI auto-docs', 'File upload support'] },
]

export default function LandingPage() {
  const statsRef = useRef(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add(styles.visible) }),
      { threshold: 0.15 }
    )
    document.querySelectorAll(`.${styles.reveal}`).forEach(el => observer.observe(el))
    return () => observer.disconnect()
  }, [])

  return (
    <div className={styles.page}>
      {/* Hero */}
      <section className={styles.hero}>
        <div className={styles.heroGrid} />
        <div className={styles.heroGlow} />
        <div className={styles.heroGlow2} />

        <div className={styles.badge}>
          <span className={styles.badgeDot} />
          AI-Powered · Semantic Matching · Real-time Ranking
        </div>

        <h1 className={styles.heroTitle}>
          Stop Filtering.<br />
          Start <em className={styles.heroEm}>Understanding</em>.
        </h1>

        <p className={styles.heroSub}>
          NeuralHire uses sentence embeddings and vector search to match resumes semantically — not just by keywords. Find the right candidates, not just the right buzzwords.
        </p>

        <div className={styles.heroActions}>
          <Link to="/dashboard" className={styles.btnPrimary}>🚀 Open Dashboard</Link>
          <Link to="/upload"    className={styles.btnGhost}>Add Candidates ↗</Link>
        </div>
      </section>

      {/* Stats */}
      <div className={`${styles.statsBar} ${styles.reveal}`} ref={statsRef}>
        {STATS.map(s => (
          <div key={s.label} className={styles.stat}>
            <div className={styles.statNum}>{s.num}</div>
            <div className={styles.statLabel}>{s.label}</div>
          </div>
        ))}
      </div>

      {/* Problem */}
      <section className={`${styles.section} ${styles.reveal}`}>
        <div className={styles.sectionTag}>The Crisis</div>
        <h2 className={styles.sectionTitle}>Why Traditional ATS Systems Are <span className="shimmer-text">Broken</span></h2>
        <div className={styles.problemGrid}>
          {PROBLEMS.map(p => (
            <div key={p.title} className={styles.problemCard}>
              <div className={styles.problemIcon}>{p.icon}</div>
              <h3 className={styles.problemTitle}>{p.title}</h3>
              <p className={styles.problemBody}>{p.body}</p>
              <div className={styles.problemStat}>⚠ {p.stat}</div>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className={`${styles.howSection} ${styles.reveal}`}>
        <div className={styles.sectionTag}>The Process</div>
        <h2 className={styles.sectionTitle}>From Job Description to Ranked Matches in Seconds</h2>
        <div className={styles.steps}>
          {STEPS.map((s, i) => (
            <React.Fragment key={s.num}>
              <div className={styles.step}>
                <div className={styles.stepNum}>
                  {s.icon}
                  <div className={styles.stepIdx}>{s.num}</div>
                </div>
                <h4 className={styles.stepTitle}>{s.title}</h4>
                <p className={styles.stepBody}>{s.body}</p>
              </div>
              {i < STEPS.length - 1 && <div className={styles.stepArrow}>→</div>}
            </React.Fragment>
          ))}
        </div>
      </section>

      {/* Tech */}
      <section className={`${styles.section} ${styles.reveal}`}>
        <div className={styles.sectionTag}>Technology Stack</div>
        <h2 className={styles.sectionTitle}>Built on Production-Grade <span className="shimmer-text">AI Infrastructure</span></h2>
        <div className={styles.techGrid}>
          {TECH.map(t => (
            <div key={t.name} className={styles.techCard}>
              <div className={styles.techLogo}>{t.logo}</div>
              <div className={styles.techName}>{t.name}</div>
              <div className={styles.techBadge}>{t.badge}</div>
              <p className={styles.techDesc}>{t.desc}</p>
              <ul className={styles.techFeatures}>
                {t.features.map(f => <li key={f}><span className={styles.feat}>▹</span>{f}</li>)}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className={`${styles.cta} ${styles.reveal}`}>
        <div className={styles.ctaGlow} />
        <div className={styles.badge} style={{ marginBottom: 28 }}>
          <span className={styles.badgeDot} />
          FastAPI + Pinecone + HuggingFace
        </div>
        <h2 className={styles.ctaTitle}>Ready to Build Smarter <span className="shimmer-text">Recruitment?</span></h2>
        <p className={styles.ctaSub}>Deploy in minutes. Query thousands of candidates semantically in milliseconds.</p>
        <div className={styles.heroActions}>
          <Link to="/dashboard" className={styles.btnPrimary}>⚡ Open Dashboard</Link>
          <Link to="/upload"    className={styles.btnGhost}>Index Candidates</Link>
        </div>
      </section>
    </div>
  )
}
