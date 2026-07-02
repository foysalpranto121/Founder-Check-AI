import { useState } from 'react';

const AdvancedAnalyticsDashboard = () => {
  const [activeTab, setActiveTab] = useState<'health' | 'visuals' | 'reports'>('health');

  return (
    <div style={{
      backgroundColor: '#0f2a47',
      color: '#fff',
      borderRadius: '8px',
      overflow: 'hidden',
      border: '1px solid #00ffee',
      padding: '2rem'
    }}>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        borderBottom: '1px solid #00ffee',
        marginBottom: '2rem',
        paddingBottom: '1rem'
      }}>
        {[
          { key: 'health', label: '💚 Health Score' },
          { key: 'visuals', label: '📊 Visualizations' },
          { key: 'reports', label: '📋 Reports' }
        ].map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as typeof activeTab)}
            style={{
              padding: '0.75rem',
              backgroundColor: activeTab === tab.key ? 'rgba(0, 255, 238, 0.2)' : 'transparent',
              color: activeTab === tab.key ? '#00ffee' : '#888',
              border: 'none',
              cursor: 'pointer',
              fontWeight: activeTab === tab.key ? 'bold' : 'normal'
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'health' && (
        <div>
          <h3 style={{ color: '#00ff41', marginTop: 0 }}>Startup Health Score</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
            {['Overall', 'Financial', 'Market', 'Team', 'Product'].map((label, i) => (
              <div key={i} style={{
                backgroundColor: 'rgba(0, 0, 0, 0.3)',
                padding: '1.5rem',
                borderRadius: '8px',
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#00ffee', marginBottom: '0.5rem' }}>
                  {60 + i * 5}
                </div>
                <div style={{ fontSize: '0.9rem', color: '#aaa' }}>{label}</div>
              </div>
            ))}
          </div>
          <div style={{
            backgroundColor: 'rgba(0, 255, 65, 0.1)',
            padding: '1rem',
            borderRadius: '8px',
            marginBottom: '1rem'
          }}>
            <h4 style={{ color: '#00ff41', margin: '0 0 0.5rem 0' }}>🚀 Improvement Opportunities</h4>
            <ul style={{ margin: 0, paddingLeft: '1.5rem', color: '#aaa' }}>
              <li>Expand market reach and competitive positioning</li>
              <li>Strengthen team with key hires or advisors</li>
              <li>Improve user retention rates</li>
            </ul>
          </div>
        </div>
      )}

      {activeTab === 'visuals' && (
        <div>
          <h3 style={{ color: '#00ff41', marginTop: 0 }}>Analytics Visualizations</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1.5rem' }}>
            <div style={{
              backgroundColor: 'rgba(0, 0, 0, 0.3)',
              padding: '1.5rem',
              borderRadius: '8px'
            }}>
              <h4 style={{ color: '#00ffee', marginTop: 0 }}>Strength/Weakness Heatmap</h4>
              <div style={{ fontSize: '0.85rem', color: '#aaa', lineHeight: '1.8' }}>
                <div>✓ Strengths: Financial Planning (85), Team (78), Product (72)</div>
                <div>✗ Weaknesses: Market Reach (45), Brand (38), Differentiation (52)</div>
              </div>
            </div>

            <div style={{
              backgroundColor: 'rgba(0, 0, 0, 0.3)',
              padding: '1.5rem',
              borderRadius: '8px'
            }}>
              <h4 style={{ color: '#00ffee', marginTop: 0 }}>Market Opportunity</h4>
              <div style={{ fontSize: '0.85rem', color: '#aaa', lineHeight: '1.8' }}>
                <div>High Growth, Low Competition: 25% opportunity</div>
                <div>High Growth, High Competition: 35% market size</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'reports' && (
        <div>
          <h3 style={{ color: '#00ff41', marginTop: 0 }}>Custom Reports</h3>
          <div style={{
            backgroundColor: 'rgba(0, 0, 0, 0.3)',
            padding: '1.5rem',
            borderRadius: '8px'
          }}>
            <p style={{ color: '#aaa', marginBottom: '1rem' }}>
              Create scheduled reports with custom metrics, white-label options, and multi-format export (PDF, CSV, JSON)
            </p>
            <button style={{
              padding: '0.75rem 1.5rem',
              backgroundColor: '#0055ff',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}>
              Create New Report
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedAnalyticsDashboard;
