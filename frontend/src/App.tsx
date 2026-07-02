import { useState } from 'react'
import './App.css'

interface BackendResponse {
  message: string
  idea_received: string
  backend_status: string
}

function App() {
  const [idea, setIdea] = useState('')
  const [response, setResponse] = useState<BackendResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [backendHealth, setBackendHealth] = useState<string | null>(null)

  // Check backend health on mount
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

    try {
      const res = await fetch('http://localhost:8000/api/v1/hello', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idea }),
      })

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`)
      }

      const data: BackendResponse = await res.json()
      setResponse(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to connect to backend')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🚀 FounderCheck</h1>
          <p>Bangladesh Startup Validator (Hello World Phase)</p>
          <div className="status">
            Backend: <span className={backendHealth?.includes('✓') ? 'connected' : 'disconnected'}>
              {backendHealth || 'Checking...'}
            </span>
          </div>
        </header>

        <main className="main">
          <form onSubmit={handleSubmit} className="form">
            <label htmlFor="idea">Enter your startup idea:</label>
            <textarea
              id="idea"
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              placeholder="E.g., A cloud kitchen in Mirpur..."
              rows={4}
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Analyzing...' : 'Send to Backend'}
            </button>
          </form>

          {error && (
            <div className="error">
              <strong>Error:</strong> {error}
            </div>
          )}

          {response && (
            <div className="response">
              <h2>✓ Backend Response</h2>
              <p><strong>Message:</strong> {response.message}</p>
              <p><strong>Idea Received:</strong> {response.idea_received}</p>
              <p><strong>Status:</strong> {response.backend_status}</p>
            </div>
          )}
        </main>

        <footer className="footer">
          <p>Phase 0: Setup & Scoping | End-to-End Connection Verified ✓</p>
        </footer>
      </div>
    </div>
  )
}

export default App
