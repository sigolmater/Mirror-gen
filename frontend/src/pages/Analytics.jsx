import { useState, useEffect } from 'react'
import { analyticsService, userService } from '../services/api'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { TrendingUp, Award, Target } from 'lucide-react'

function Analytics() {
  const [users, setUsers] = useState([])
  const [selectedUser, setSelectedUser] = useState(null)
  const [mutualGrowth, setMutualGrowth] = useState(null)
  const [trendData, setTrendData] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadUsers()
  }, [])

  useEffect(() => {
    if (selectedUser) {
      loadAnalytics(selectedUser)
    }
  }, [selectedUser])

  const loadUsers = async () => {
    try {
      const response = await userService.getUsers()
      setUsers(response.data)
      if (response.data.length > 0 && !selectedUser) {
        setSelectedUser(response.data[0].id)
      }
    } catch (error) {
      console.error('Error loading users:', error)
    }
  }

  const loadAnalytics = async (userId) => {
    setLoading(true)
    try {
      const [mutualRes, trendRes] = await Promise.all([
        analyticsService.getMutualGrowthAnalysis(userId),
        analyticsService.getGrowthTrend(userId, 30),
      ])
      setMutualGrowth(mutualRes.data)
      setTrendData(trendRes.data.trend)
      
      // Create snapshot for tracking
      await analyticsService.createGrowthSnapshot(userId)
    } catch (error) {
      console.error('Error loading analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (users.length === 0) {
    return (
      <div className="card">
        <h2>No Users Found</h2>
        <p style={{ color: '#666' }}>Please create a user first in the User Management page.</p>
      </div>
    )
  }

  return (
    <div>
      <div className="card">
        <h2>Mutual Growth Analytics</h2>
        <p style={{ color: '#666', marginBottom: '20px' }}>
          사용자와 AI의 상호 성장 분석 - Analyze how users and AI grow together
        </p>

        <div className="form-group">
          <label>Select User</label>
          <select
            className="input"
            value={selectedUser || ''}
            onChange={(e) => setSelectedUser(Number(e.target.value))}
          >
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.username} ({user.email})
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="loading">Loading analytics...</div>
      ) : mutualGrowth ? (
        <>
          <h2 style={{ color: 'white', marginTop: '30px', marginBottom: '20px' }}>
            User Growth Metrics
          </h2>
          <div className="grid">
            <div className="stat-card">
              <h3>
                <Award size={20} style={{ verticalAlign: 'middle', marginRight: '8px' }} />
                Skill Level
              </h3>
              <div className="value">{mutualGrowth.user_growth.skill_level.toFixed(1)}</div>
              <div className="label">Current proficiency</div>
            </div>

            <div className="stat-card">
              <h3>
                <TrendingUp size={20} style={{ verticalAlign: 'middle', marginRight: '8px' }} />
                Engagement Score
              </h3>
              <div className="value">{mutualGrowth.user_growth.engagement_score.toFixed(1)}</div>
              <div className="label">Activity level</div>
            </div>

            <div className="stat-card">
              <h3>
                <Target size={20} style={{ verticalAlign: 'middle', marginRight: '8px' }} />
                Learning Progress
              </h3>
              <div className="value">{mutualGrowth.user_growth.learning_progress.toFixed(1)}%</div>
              <div className="label">Educational advancement</div>
            </div>

            <div className="stat-card">
              <h3>Tasks Completed</h3>
              <div className="value">{mutualGrowth.user_growth.tasks_completed}</div>
              <div className="label">High-quality interactions</div>
            </div>
          </div>

          <h2 style={{ color: 'white', marginTop: '30px', marginBottom: '20px' }}>
            AI Performance Metrics
          </h2>
          <div className="grid">
            <div className="stat-card">
              <h3>Total Interactions</h3>
              <div className="value">{mutualGrowth.ai_performance.total_interactions}</div>
              <div className="label">Conversations processed</div>
            </div>

            <div className="stat-card">
              <h3>Response Time</h3>
              <div className="value">{mutualGrowth.ai_performance.avg_response_time.toFixed(2)}s</div>
              <div className="label">Average processing speed</div>
            </div>

            <div className="stat-card">
              <h3>User Satisfaction</h3>
              <div className="value">{mutualGrowth.ai_performance.avg_user_satisfaction.toFixed(1)}/5</div>
              <div className="label">Feedback rating</div>
            </div>

            <div className="stat-card">
              <h3>Improvement Rate</h3>
              <div className="value">{mutualGrowth.ai_performance.improvement_rate.toFixed(1)}%</div>
              <div className="label">AI learning efficiency</div>
            </div>
          </div>

          {trendData.length > 0 && (
            <>
              <div className="card" style={{ marginTop: '30px' }}>
                <h2>Growth Trend - User Metrics</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={trendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="timestamp"
                      tickFormatter={(value) => new Date(value).toLocaleDateString()}
                    />
                    <YAxis />
                    <Tooltip
                      labelFormatter={(value) => new Date(value).toLocaleString()}
                    />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="skill_level"
                      stroke="#8884d8"
                      name="Skill Level"
                    />
                    <Line
                      type="monotone"
                      dataKey="engagement_score"
                      stroke="#82ca9d"
                      name="Engagement"
                    />
                    <Line
                      type="monotone"
                      dataKey="learning_progress"
                      stroke="#ffc658"
                      name="Learning Progress"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="card">
                <h2>AI Performance Trend</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={trendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="timestamp"
                      tickFormatter={(value) => new Date(value).toLocaleDateString()}
                    />
                    <YAxis />
                    <Tooltip
                      labelFormatter={(value) => new Date(value).toLocaleString()}
                    />
                    <Legend />
                    <Bar dataKey="ai_accuracy" fill="#667eea" name="AI Accuracy" />
                    <Bar dataKey="user_satisfaction" fill="#764ba2" name="Satisfaction" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </>
          )}

          <div className="card">
            <h2>Recommendations for Mutual Growth</h2>
            <ul style={{ lineHeight: '2', color: '#666' }}>
              {mutualGrowth.recommendations.map((rec, index) => (
                <li key={index}>
                  <strong style={{ color: '#667eea' }}>→</strong> {rec}
                </li>
              ))}
            </ul>
          </div>

          <div className="card">
            <h2>About Mutual Learning</h2>
            <p style={{ color: '#666', lineHeight: '1.8' }}>
              This system creates a <strong>virtuous cycle</strong> where:
            </p>
            <ul style={{ color: '#666', lineHeight: '2', marginTop: '10px' }}>
              <li>Users interact with the AI, providing valuable usage data</li>
              <li>AI learns from user feedback and improves its responses</li>
              <li>Improved AI performance leads to better user experiences</li>
              <li>Better experiences encourage more user engagement</li>
              <li>More engagement generates more data for AI improvement</li>
            </ul>
            <p style={{ color: '#666', lineHeight: '1.8', marginTop: '10px' }}>
              This creates a <strong>선순환 (virtuous cycle)</strong> where both the user and AI 
              grow together, each benefiting from the other's development.
            </p>
          </div>
        </>
      ) : (
        <div className="card">
          <p style={{ color: '#888', textAlign: 'center', padding: '40px' }}>
            Select a user to view analytics
          </p>
        </div>
      )}
    </div>
  )
}

export default Analytics
