import { useState } from 'react'
import './App.css'

interface AnalysisResult {
  idea_extraction: {
    title: string
    description: string
    sector: string
    target_customer: string
    revenue_model: string
    location: string
  }
  demand_analysis: {
    score: number
    market_size: string
    competition: string
    opportunities: string[]
    threats: string[]
  }
  regulatory_analysis: {
    risk_score: number
    key_regulators: string[]
    critical_approvals: string
    estimated_timeline: number
    cost_estimate: number
    warnings: string
  }
  business_canvas: {
    key_partners: string[]
    key_activities: string[]
    key_resources: Record<string, unknown>
    value_proposition: string
    customer_segments: string[]
    channels: string[]
    customer_relationships: string[]
    revenue_streams: Record<string, unknown>
    cost_structure: Record<string, unknown>
  }
  investor_questions: Array<{
    question: string
    category: string
  }>
  overall_readiness_score: number
  analysis_status: string
}

function App() {
  const [idea, setIdea] = useState('')
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [backendHealth, setBackendHealth] = useState<string | null>(null)

  React.useEffect(() => {
    checkBackendHealth()
  }, [])

  const checkBackendHealth = async () => {
    try {
      const res = await fetch('http://localhost:8000/health')
      if (res.ok) {
        setBackendHealth('✓ Connected')
      }
    } catch (err) {
      setBackendHealth('✗ Backend not reachable')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!idea.trim()) return

    setLoading(true)
    setError(null)
    setAnalysis(null)

    try {
      const res = await fetch('http://localhost:8000/api/v1/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idea, language: 'english' }),
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.detail || `HTTP ${res.status}`)
      }

      const data: AnalysisResult = await res.json()
      setAnalysis(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze idea')
    } finally {
      setLoading(false)
    }
  }

  const getScoreBadge = (score: number) => {
    if (score >= 8) return { color: '#10b981', label: 'Strong', emoji: '🚀' }
    if (score >= 6) return { color: '#f59e0b', label: 'Moderate', emoji: '⚠️' }
    return { color: '#ef4444', label: 'Weak', emoji: '📉' }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🚀 FounderCheck</h1>
          <p>Bangladesh Startup Validator</p>
          <div className="status">
            Backend: <span className={backendHealth?.includes('✓') ? 'connected' : 'disconnected'}>
              {backendHealth || 'Checking...'}
            </span>
          </div>
        </header>

        <main className="main">
          {!analysis ? (
            <form onSubmit={handleSubmit} className="form">
              <label htmlFor="idea">Describe your startup idea:</label>
              <textarea
                id="idea"
                value={idea}
                onChange={(e) => setIdea(e.target.value)}
                placeholder="E.g., A cloud kitchen in Mirpur serving Dhaka with ready-to-eat meals..."
                rows={5}
                disabled={loading}
              />
              <button type="submit" disabled={loading}>
                {loading ? '🔍 Analyzing... (This takes 30-40 seconds)' : '📊 Analyze My Idea'}
              </button>
            </form>
          ) : null}

          {error && (
            <div className="error">
              <strong>❌ Error:</strong> {error}
              <button onClick={() => setAnalysis(null)} className="reset-btn">
                Start Over
              </button>
            </div>
          )}

          {analysis && (
            <div className="results">
              <button onClick={() => setAnalysis(null)} className="reset-btn">
                ← Start New Analysis
              </button>

              {/* Readiness Score */}
              <div className="score-card">
                <h2>📈 Overall Readiness Score</h2>
                <div className="score-display">
                  <div
                    className="score-circle"
                    style={{
                      background: `conic-gradient(${getScoreBadge(analysis.overall_readiness_score).color} ${analysis.overall_readiness_score * 10}%, #e5e7eb 0)`
                    }}
                  >
                    <span className="score-value">{analysis.overall_readiness_score}/10</span>
                  </div>
                  <div className="score-label">
                    {getScoreBadge(analysis.overall_readiness_score).emoji}
                    {getScoreBadge(analysis.overall_readiness_score).label}
                  </div>
                </div>
              </div>

              {/* Idea Summary */}
              <div className="section">
                <h3>📋 Idea Summary</h3>
                <p><strong>Title:</strong> {analysis.idea_extraction.title}</p>
                <p><strong>Sector:</strong> {analysis.idea_extraction.sector}</p>
                <p><strong>Target Customer:</strong> {analysis.idea_extraction.target_customer}</p>
                <p><strong>Revenue Model:</strong> {analysis.idea_extraction.revenue_model}</p>
                <p><strong>Location:</strong> {analysis.idea_extraction.location}</p>
              </div>

              {/* Demand Analysis */}
              <div className="section">
                <h3>📊 Market Demand</h3>
                <div className="metric">
                  <span>Demand Score:</span>
                  <strong style={{ color: getScoreBadge(analysis.demand_analysis.score).color }}>
                    {analysis.demand_analysis.score}/10
                  </strong>
                </div>
                <p><strong>Market Size:</strong> {analysis.demand_analysis.market_size}</p>
                <p><strong>Competition:</strong> {analysis.demand_analysis.competition}</p>
                <div>
                  <strong>Opportunities:</strong>
                  <ul>
                    {analysis.demand_analysis.opportunities.map((opp, i) => (
                      <li key={i}>✓ {opp}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <strong>Threats:</strong>
                  <ul>
                    {analysis.demand_analysis.threats.map((threat, i) => (
                      <li key={i}>⚠️ {threat}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Regulatory Analysis */}
              <div className="section regulatory">
                <h3>⚖️ Regulatory Landscape</h3>
                <div className="metric">
                  <span>Risk Level:</span>
                  <strong style={{ color: getScoreBadge(10 - analysis.regulatory_analysis.risk_score).color }}>
                    {10 - analysis.regulatory_analysis.risk_score}/10
                  </strong>
                </div>
                <p><strong>Key Regulators:</strong> {analysis.regulatory_analysis.key_regulators.join(', ')}</p>
                <p><strong>Critical Approvals:</strong> {analysis.regulatory_analysis.critical_approvals}</p>
                <p><strong>Timeline:</strong> ~{analysis.regulatory_analysis.estimated_timeline} days</p>
                <p><strong>Estimated Cost:</strong> ৳{analysis.regulatory_analysis.cost_estimate.toLocaleString()}</p>
                <div className="warning">
                  <strong>⚠️ Important:</strong> {analysis.regulatory_analysis.warnings}
                </div>
              </div>

              {/* Business Model Canvas */}
              <div className="section">
                <h3>🎨 Business Model Canvas</h3>
                <div className="canvas-grid">
                  <div className="canvas-block">
                    <h4>Key Partners</h4>
                    <ul>
                      {(analysis.business_canvas.key_partners || []).map((p, i) => (
                        <li key={i}>{p}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="canvas-block">
                    <h4>Key Activities</h4>
                    <ul>
                      {(analysis.business_canvas.key_activities || []).map((a, i) => (
                        <li key={i}>{a}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="canvas-block">
                    <h4>Customer Segments</h4>
                    <ul>
                      {(analysis.business_canvas.customer_segments || []).map((c, i) => (
                        <li key={i}>{c}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="canvas-block">
                    <h4>Value Proposition</h4>
                    <p>{analysis.business_canvas.value_proposition}</p>
                  </div>
                </div>
              </div>

              {/* Investor Questions */}
              <div className="section">
                <h3>❓ Investor Questions (For Your Pitch)</h3>
                <div className="qa-list">
                  {analysis.investor_questions.slice(0, 5).map((q, i) => (
                    <div key={i} className="qa-item">
                      <span className="qa-num">{i + 1}</span>
                      <div>
                        <p><strong>{q.question}</strong></p>
                        <span className="category">{q.category}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </main>

        <footer className="footer">
          <p>🤖 Powered by Claude AI | 🇧🇩 Bangladesh Context | ✅ Data-Driven Analysis</p>
        </footer>
      </div>
    </div>
  )
}

export default App
