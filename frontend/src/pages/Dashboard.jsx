import { useState, useEffect } from 'react'
import { analyticsService, feedbackService } from '../services/api'
import { Activity, TrendingUp, Users, MessageSquare } from 'lucide-react'

function Dashboard() {
  const [aiMetrics, setAIMetrics] = useState(null)
  const [feedbackSummary, setFeedbackSummary] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const [aiResponse, feedbackResponse] = await Promise.all([
        analyticsService.getAIPerformanceMetrics(),
        feedbackService.getFeedbackSummary(),
      ])
      setAIMetrics(aiResponse.data)
      setFeedbackSummary(feedbackResponse.data)
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading dashboard...</div>
  }

  return (
    <div>
      <div className="card">
        <h2>Welcome to Mirror-gen</h2>
        <p style={{ color: '#666', marginBottom: '20px' }}>
          사용자와 AI가 함께 성장하며 선순환하는 시스템
        </p>
        <p style={{ color: '#666' }}>
          This system enables mutual learning between users and AI, creating a virtuous cycle 
          where both grow together through continuous interaction and feedback.
        </p>
      </div>

      <h2 style={{ color: 'white', marginBottom: '20px' }}>AI Performance Metrics</h2>
      <div className="grid">
        <div className="stat-card">
          <h3>
            <Activity size={20} style={{ verticalAlign: 'middle', marginRight: '8px' }} />
            Total Interactions
          </h3>
          <div className="value">{aiMetrics?.total_interactions || 0}</div>
          <div className="label">User-AI conversations</div>
        </div>

        <div className="stat-card">
          <h3>
            <TrendingUp size={20} style={{ verticalAlign: 'middle', marginRight: '8px' }} />
            Avg Response Time
          </h3>
          <div className="value">{(aiMetrics?.avg_response_time || 0).toFixed(2)}s</div>
          <div className="label">AI processing speed</div>
        </div>

        <div className="stat-card">
          <h3>
            <Users size={20} style={{ verticalAlign: 'middle', marginRight: '8px' }} />
            User Satisfaction
          </h3>
          <div className="value">{(aiMetrics?.avg_user_satisfaction || 0).toFixed(1)}/5.0</div>
          <div className="label">Average rating</div>
        </div>

        <div className="stat-card">
          <h3>
            <MessageSquare size={20} style={{ verticalAlign: 'middle', marginRight: '8px' }} />
            Feedback Processed
          </h3>
          <div className="value">{aiMetrics?.feedback_processed || 0}</div>
          <div className="label">AI improvements applied</div>
        </div>
      </div>

      <h2 style={{ color: 'white', marginTop: '30px', marginBottom: '20px' }}>Feedback Summary</h2>
      <div className="card">
        <div className="grid">
          <div>
            <h3>Total Feedback</h3>
            <p style={{ fontSize: '32px', color: '#667eea', fontWeight: 'bold' }}>
              {feedbackSummary?.total_feedback || 0}
            </p>
          </div>
          <div>
            <h3>Average Rating</h3>
            <p style={{ fontSize: '32px', color: '#667eea', fontWeight: 'bold' }}>
              {(feedbackSummary?.average_rating || 0).toFixed(1)}/5.0
            </p>
          </div>
          <div>
            <h3>Processing Rate</h3>
            <p style={{ fontSize: '32px', color: '#667eea', fontWeight: 'bold' }}>
              {(feedbackSummary?.processing_rate || 0).toFixed(1)}%
            </p>
          </div>
        </div>

        {feedbackSummary?.feedback_by_type && (
          <div style={{ marginTop: '20px' }}>
            <h3>Feedback by Type</h3>
            <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginTop: '10px' }}>
              {Object.entries(feedbackSummary.feedback_by_type).map(([type, count]) => (
                <div key={type} style={{ 
                  background: '#f0f0f0', 
                  padding: '8px 16px', 
                  borderRadius: '20px',
                  fontSize: '14px'
                }}>
                  <strong>{type}:</strong> {count}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h2>System Features</h2>
        <ul style={{ lineHeight: '2', color: '#666' }}>
          <li>✅ User learning data synchronization pipeline</li>
          <li>✅ AI feedback loop with continuous improvement</li>
          <li>✅ User interaction logging and analytics</li>
          <li>✅ Mutual learning experience tracking</li>
          <li>✅ Quantifiable user growth visualization</li>
          <li>✅ Real-time performance metrics</li>
        </ul>
      </div>
    </div>
  )
}

export default Dashboard
