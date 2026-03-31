import React from 'react'
import styles from './CandidateCard.module.css'
import clsx from 'clsx'

const LABEL_META = {
  hot:    { emoji: '🔥', text: 'HOT MATCH',   cls: 'hot' },
  strong: { emoji: '✓',  text: 'STRONG',      cls: 'strong' },
  fair:   { emoji: '~',  text: 'FAIR',        cls: 'fair' },
  weak:   { emoji: '↓',  text: 'WEAK',        cls: 'weak' },
}

const AVATAR_COLORS = [
  '#0ea5e9','#7c3aed','#10b981','#f59e0b','#ef4444','#8b5cf6','#06b6d4',
]

function getColor(name) {
  let hash = 0
  for (const c of name) hash = c.charCodeAt(0) + ((hash << 5) - hash)
  return AVATAR_COLORS[Math.abs(hash) % AVATAR_COLORS.length]
}

function ScoreRing({ score, label }) {
  const r = 26, circ = 2 * Math.PI * r
  const fill = circ * (score / 100)
  const colors = { hot: '#10B981', strong: '#00D4FF', fair: '#F59E0B', weak: '#5A7A9A' }
  const color = colors[label] || '#5A7A9A'

  return (
    <div className={styles.ring}>
      <svg width="64" height="64" viewBox="0 0 64 64" style={{ transform: 'rotate(-90deg)' }}>
        <circle cx="32" cy="32" r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="4" />
        <circle
          cx="32" cy="32" r={r} fill="none" stroke={color} strokeWidth="4"
          strokeDasharray={`${fill} ${circ - fill}`} strokeLinecap="round"
        />
      </svg>
      <div className={styles.ringLabel} style={{ color }}>
        <span className={styles.ringNum}>{score}</span>
        <span className={styles.ringPct}>%</span>
      </div>
    </div>
  )
}

export default function CandidateCard({ candidate, rank }) {
  const { name, role, skills = [], score_pct, match_label, match_summary, years_experience } = candidate
  const meta = LABEL_META[match_label] || LABEL_META.fair
  const color = getColor(name)
  const initials = name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()

  return (
    <div className={clsx(styles.card, styles[meta.cls])}>
      <div className={styles.rank}>#{rank}</div>

      <div className={styles.avatar} style={{ background: `${color}22`, color, border: `1px solid ${color}44` }}>
        {initials}
      </div>

      <div className={styles.info}>
        <div className={styles.nameRow}>
          <h3 className={styles.name}>{name}</h3>
          <span className={clsx(styles.label, styles[meta.cls])}>
            {meta.emoji} {meta.text}
          </span>
        </div>
        <div className={styles.role}>
          {role || 'Candidate'}{years_experience ? ` · ${years_experience} yrs` : ''}
        </div>
        <div className={styles.skills}>
          {skills.slice(0, 6).map(s => (
            <span key={s} className={styles.skill}>{s}</span>
          ))}
        </div>
        <div className={styles.summary}>{match_summary}</div>
      </div>

      <ScoreRing score={score_pct} label={match_label} />
    </div>
  )
}
