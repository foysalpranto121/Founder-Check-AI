import { useState } from 'react';

const ContinuousMonitoringDashboard = () => {
  const [activeTab, setActiveTab] = useState<'milestones' | 'alerts' | 'insights'>('milestones');

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
          { key: 'milestones', label: 'Milestones' },
          { key: 'alerts', label: 'Live Alerts' },
          { key: 'insights', label: 'Daily Insights' }
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

      {activeTab === 'milestones' && (
        <div>
          <h3 style={{ color: '#00ff41', marginTop: 0 }}>Milestone Tracking</h3>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(5, 1fr)',
            gap: '1rem',
            marginBottom: '2rem'
          }}>
            {[
              { label: 'Total', value: '5', icon: '' },
              { label: 'Completed', value: '1', icon: '' },
              { label: 'In Progress', value: '2', icon: '' },
              { label: 'Delayed', value: '0', icon: '' },
              { label: 'Overall', value: '44%', icon: '' }
            ].map((stat, i) => (
              <div key={i} style={{
                backgroundColor: 'rgba(0, 0, 0, 0.3)',
                padding: '1rem',
                borderRadius: '8px',
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>{stat.icon}</div>
                <div style={{ fontSize: '1.3rem', fontWeight: 'bold', color: '#00ffee', marginBottom: '0.25rem' }}>
                  {stat.value}
                </div>
                <div style={{ fontSize: '0.8rem', color: '#aaa' }}>{stat.label}</div>
              </div>
            ))}
          </div>

          <div style={{
            backgroundColor: 'rgba(0, 0, 0, 0.3)',
            borderRadius: '8px',
            overflow: 'hidden'
          }}>
            <div style={{ padding: '1rem', borderBottom: '1px solid rgba(0, 255, 238, 0.2)' }}>
              <h4 style={{ margin: 0, color: '#00ff41' }}>Upcoming Milestones</h4>
            </div>
            {[
              { name: 'First 1000 Users', date: 'Jun 30, 2024', progress: 60, status: '' },
              { name: 'Series A Fundraising', date: 'Sep 30, 2024', progress: 0, status: '⏳' },
              { name: 'Market Expansion', date: 'Aug 31, 2024', progress: 0, status: '⏳' }
            ].map((m, i) => (
              <div key={i} style={{
                padding: '1rem',
                borderBottom: i < 2 ? '1px solid rgba(0, 255, 238, 0.1)' : 'none'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span style={{ fontSize: '1rem' }}>{m.status}</span>
                    <span style={{ fontWeight: 'bold', color: '#00ffee' }}>{m.name}</span>
                  </div>
                  <span style={{ fontSize: '0.85rem', color: '#888' }}>{m.date}</span>
                </div>
                <div style={{
                  height: '6px',
                  backgroundColor: 'rgba(0, 255, 238, 0.1)',
                  borderRadius: '3px',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    height: '100%',
                    backgroundColor: m.progress === 100 ? '#00ff41' : '#0055ff',
                    width: `${m.progress}%`,
                    transition: 'width 0.3s ease'
                  }} />
                </div>
                <div style={{ fontSize: '0.75rem', color: '#888', marginTop: '0.25rem' }}>
                  {m.progress}% complete
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'alerts' && (
        <div>
          <h3 style={{ color: '#00ff41', marginTop: 0 }}>Live Alerts & News</h3>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: '1rem',
            marginBottom: '2rem'
          }}>
            {[
              { icon: '', label: 'Critical', count: '2', color: '#ff5555' },
              { icon: '', label: 'High', count: '5', color: '#ffaa00' },
              { icon: '', label: 'Medium', count: '8', color: '#ffff00' },
              { icon: '', label: 'Low', count: '3', color: '#00ff41' }
            ].map((priority, i) => (
              <div key={i} style={{
                backgroundColor: 'rgba(0, 0, 0, 0.3)',
                padding: '1rem',
                borderRadius: '8px',
                textAlign: 'center',
                borderLeft: `4px solid ${priority.color}`
              }}>
                <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>{priority.icon}</div>
                <div style={{ fontSize: '0.9rem', color: '#aaa', marginBottom: '0.25rem' }}>{priority.label}</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#00ffee' }}>{priority.count}</div>
              </div>
            ))}
          </div>

          <div style={{
            backgroundColor: 'rgba(0, 0, 0, 0.3)',
            borderRadius: '8px',
            overflow: 'hidden',
            marginBottom: '2rem'
          }}>
            <div style={{ padding: '1rem', borderBottom: '1px solid rgba(0, 255, 238, 0.2)' }}>
              <h4 style={{ margin: 0, color: '#00ff41' }}>Recent Alerts</h4>
            </div>
            {[
              { type: '', title: 'Competitor Alert: GrowthX acquired StrategyBD', time: '2 hours ago', priority: 'high' },
              { type: '', title: 'Funding News: Series B rounds up 40% in region', time: '4 hours ago', priority: 'medium' },
              { type: '', title: 'Market Trend: EdTech adoption accelerating', time: '1 day ago', priority: 'medium' }
            ].map((alert, i) => (
              <div key={i} style={{
                padding: '1rem',
                borderBottom: i < 2 ? '1px solid rgba(0, 255, 238, 0.1)' : 'none',
                display: 'flex',
                gap: '1rem',
                alignItems: 'flex-start'
              }}>
                <div style={{ fontSize: '1.2rem' }}>{alert.type}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ color: '#fff', fontWeight: 'bold', marginBottom: '0.25rem' }}>{alert.title}</div>
                  <div style={{ fontSize: '0.85rem', color: '#888' }}>{alert.time}</div>
                </div>
                <div style={{
                  padding: '0.25rem 0.75rem',
                  backgroundColor: alert.priority === 'high' ? 'rgba(255, 85, 85, 0.2)' : 'rgba(255, 170, 0, 0.2)',
                  color: alert.priority === 'high' ? '#ff5555' : '#ffaa00',
                  borderRadius: '4px',
                  fontSize: '0.75rem',
                  fontWeight: 'bold'
                }}>
                  {alert.priority.toUpperCase()}
                </div>
              </div>
            ))}
          </div>

          <div style={{
            backgroundColor: 'rgba(0, 0, 0, 0.3)',
            borderRadius: '8px',
            overflow: 'hidden'
          }}>
            <div style={{ padding: '1rem', borderBottom: '1px solid rgba(0, 255, 238, 0.2)' }}>
              <h4 style={{ margin: 0, color: '#00ff41' }}>Trending Categories</h4>
            </div>
            <div style={{ padding: '1rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
              {[
                { name: 'FinTech', articles: 24 },
                { name: 'EdTech', articles: 18 },
                { name: 'HealthTech', articles: 12 },
                { name: 'Logistics', articles: 8 }
              ].map((cat, i) => (
                <div key={i} style={{
                  backgroundColor: 'rgba(0, 255, 238, 0.1)',
                  border: '1px solid rgba(0, 255, 238, 0.3)',
                  padding: '0.75rem 1rem',
                  borderRadius: '6px',
                  cursor: 'pointer'
                }}>
                  <div style={{ fontSize: '0.9rem', fontWeight: 'bold', color: '#00ffee' }}>{cat.name}</div>
                  <div style={{ fontSize: '0.75rem', color: '#888' }}>{cat.articles} articles</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'insights' && (
        <div>
          <h3 style={{ color: '#00ff41', marginTop: 0 }}>Daily Insights</h3>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1.5rem', marginBottom: '2rem' }}>
            <div style={{
              backgroundColor: 'rgba(0, 0, 0, 0.3)',
              padding: '1.5rem',
              borderRadius: '8px'
            }}>
              <h4 style={{ color: '#00ffee', marginTop: 0 }}>Market Insights</h4>
              <ul style={{ margin: 0, paddingLeft: '1.5rem', color: '#aaa', lineHeight: '1.8', fontSize: '0.9rem' }}>
                <li>EdTech market growing 35% YoY</li>
                <li>Regulatory uncertainty in FinTech</li>
                <li>Mobile adoption at 65% in Bangladesh</li>
              </ul>
            </div>

            <div style={{
              backgroundColor: 'rgba(0, 0, 0, 0.3)',
              padding: '1.5rem',
              borderRadius: '8px'
            }}>
              <h4 style={{ color: '#00ffee', marginTop: 0 }}>Opportunities</h4>
              <div style={{ color: '#aaa', lineHeight: '1.8', fontSize: '0.9rem' }}>
                <div>High-growth sectors (EdTech, HealthTech)</div>
                <div>Government incentives for tech startups</div>
                <div>Rising venture capital activity</div>
              </div>
            </div>

            <div style={{
              backgroundColor: 'rgba(0, 0, 0, 0.3)',
              padding: '1.5rem',
              borderRadius: '8px'
            }}>
              <h4 style={{ color: '#00ffee', marginTop: 0 }}>Competitor Moves</h4>
              <ul style={{ margin: 0, paddingLeft: '1.5rem', color: '#aaa', lineHeight: '1.8', fontSize: '0.9rem' }}>
                <li>Competitor A launched AI feature</li>
                <li>Competitor B raised Series B ($5M)</li>
                <li>Competitor C expanded to Pakistan</li>
              </ul>
            </div>

            <div style={{
              backgroundColor: 'rgba(0, 0, 0, 0.3)',
              padding: '1.5rem',
              borderRadius: '8px'
            }}>
              <h4 style={{ color: '#00ffee', marginTop: 0 }}>Funding Updates</h4>
              <ul style={{ margin: 0, paddingLeft: '1.5rem', color: '#aaa', lineHeight: '1.8', fontSize: '0.9rem' }}>
                <li>TechBD raised $5M Series A</li>
                <li>StartupX raised $2M Seed Round</li>
                <li>Regional VC activity +30% YoY</li>
              </ul>
            </div>
          </div>

          <div style={{
            backgroundColor: 'rgba(0, 255, 65, 0.1)',
            border: '1px solid rgba(0, 255, 65, 0.3)',
            padding: '1.5rem',
            borderRadius: '8px'
          }}>
            <h4 style={{ color: '#00ff41', margin: '0 0 1rem 0' }}>Pivot Detection Analysis</h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem' }}>
              <div>
                <div style={{ color: '#aaa', marginBottom: '0.5rem' }}>Status</div>
                <div style={{ color: '#00ff41', fontWeight: 'bold', fontSize: '1.1rem' }}>On Track</div>
                <div style={{ fontSize: '0.85rem', color: '#888', marginTop: '0.25rem' }}>Confidence: 78%</div>
              </div>
              <div>
                <div style={{ color: '#aaa', marginBottom: '0.5rem' }}>Key Metrics</div>
                <div style={{ fontSize: '0.9rem', color: '#aaa' }}>
                  <div>• Retention: 68% (Healthy)</div>
                  <div>• Growth: 18% MoM (Good)</div>
                  <div>• NPS: 52 (Solid)</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ContinuousMonitoringDashboard;
