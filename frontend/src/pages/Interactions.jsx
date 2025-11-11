import { useState, useEffect } from 'react'
import { interactionService, feedbackService, userService } from '../services/api'
import { Send, Star } from 'lucide-react'

function Interactions() {
  const [users, setUsers] = useState([])
  const [selectedUser, setSelectedUser] = useState(null)
  const [interactions, setInteractions] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })

  // Interaction form
  const [interactionForm, setInteractionForm] = useState({
    interaction_type: 'query',
    content: '',
  })

  // Feedback form
  const [showFeedbackForm, setShowFeedbackForm] = useState(false)
  const [selectedInteraction, setSelectedInteraction] = useState(null)
  const [feedbackForm, setFeedbackForm] = useState({
    feedback_type: 'positive',
    rating: 5,
    comment: '',
  })

  useEffect(() => {
    loadUsers()
  }, [])

  useEffect(() => {
    if (selectedUser) {
      loadUserData(selectedUser)
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

  const loadUserData = async (userId) => {
    setLoading(true)
    try {
      const [interactionsRes, statsRes] = await Promise.all([
        interactionService.getUserInteractions(userId),
        interactionService.getInteractionStats(userId),
      ])
      setInteractions(interactionsRes.data)
      setStats(statsRes.data)
    } catch (error) {
      console.error('Error loading user data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleInteractionSubmit = async (e) => {
    e.preventDefault()
    if (!selectedUser) {
      setMessage({ type: 'error', text: 'Please select a user first' })
      return
    }

    try {
      await interactionService.createInteraction(selectedUser, interactionForm)
      setMessage({ type: 'success', text: 'Interaction created successfully!' })
      setInteractionForm({ interaction_type: 'query', content: '' })
      loadUserData(selectedUser)
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to create interaction' })
    }
  }

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault()
    if (!selectedUser) return

    try {
      await feedbackService.submitFeedback(selectedUser, {
        ...feedbackForm,
        interaction_id: selectedInteraction,
      })
      setMessage({ type: 'success', text: 'Feedback submitted successfully!' })
      setFeedbackForm({ feedback_type: 'positive', rating: 5, comment: '' })
      setShowFeedbackForm(false)
      setSelectedInteraction(null)
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to submit feedback' })
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
        <h2>User Interactions</h2>
        
        {message.text && (
          <div className={message.type}>
            {message.text}
          </div>
        )}

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

        {stats && (
          <div className="grid" style={{ marginTop: '20px' }}>
            <div style={{ background: '#f0f0f0', padding: '16px', borderRadius: '8px' }}>
              <h3>Total Interactions</h3>
              <p style={{ fontSize: '28px', color: '#667eea', fontWeight: 'bold' }}>
                {stats.total_interactions}
              </p>
            </div>
            <div style={{ background: '#f0f0f0', padding: '16px', borderRadius: '8px' }}>
              <h3>Avg Quality</h3>
              <p style={{ fontSize: '28px', color: '#667eea', fontWeight: 'bold' }}>
                {(stats.average_response_quality * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h2>Create New Interaction</h2>
        <form onSubmit={handleInteractionSubmit}>
          <div className="form-group">
            <label>Interaction Type</label>
            <select
              className="input"
              value={interactionForm.interaction_type}
              onChange={(e) =>
                setInteractionForm({ ...interactionForm, interaction_type: e.target.value })
              }
            >
              <option value="query">Query</option>
              <option value="feedback">Feedback</option>
              <option value="task_completion">Task Completion</option>
              <option value="learning">Learning Activity</option>
            </select>
          </div>
          <div className="form-group">
            <label>Content</label>
            <textarea
              className="input"
              value={interactionForm.content}
              onChange={(e) =>
                setInteractionForm({ ...interactionForm, content: e.target.value })
              }
              placeholder="Enter your interaction content..."
              required
            />
          </div>
          <button type="submit" className="btn btn-primary">
            <Send size={16} style={{ verticalAlign: 'middle', marginRight: '8px' }} />
            Submit Interaction
          </button>
        </form>
      </div>

      <div className="card">
        <h2>Recent Interactions</h2>
        {loading ? (
          <div className="loading">Loading interactions...</div>
        ) : interactions.length === 0 ? (
          <p style={{ color: '#888', textAlign: 'center', padding: '20px' }}>
            No interactions yet. Create your first interaction above!
          </p>
        ) : (
          <div className="interaction-list">
            {interactions.map((interaction) => (
              <div key={interaction.id} className="interaction-item">
                <div className="meta">
                  {new Date(interaction.timestamp).toLocaleString()} • {interaction.interaction_type}
                  {interaction.response_quality && (
                    <span style={{ marginLeft: '10px', color: '#667eea' }}>
                      Quality: {(interaction.response_quality * 100).toFixed(0)}%
                    </span>
                  )}
                </div>
                <div className="content">
                  <strong>User:</strong> {interaction.content}
                </div>
                {interaction.ai_response && (
                  <div className="response">
                    <strong>AI:</strong> {interaction.ai_response}
                  </div>
                )}
                <button
                  onClick={() => {
                    setSelectedInteraction(interaction.id)
                    setShowFeedbackForm(true)
                  }}
                  style={{
                    marginTop: '8px',
                    background: '#667eea',
                    color: 'white',
                    border: 'none',
                    padding: '6px 12px',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '14px',
                  }}
                >
                  <Star size={14} style={{ verticalAlign: 'middle', marginRight: '4px' }} />
                  Give Feedback
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {showFeedbackForm && (
        <div className="card">
          <h2>Submit Feedback</h2>
          <form onSubmit={handleFeedbackSubmit}>
            <div className="form-group">
              <label>Feedback Type</label>
              <select
                className="input"
                value={feedbackForm.feedback_type}
                onChange={(e) =>
                  setFeedbackForm({ ...feedbackForm, feedback_type: e.target.value })
                }
              >
                <option value="positive">Positive</option>
                <option value="negative">Negative</option>
                <option value="suggestion">Suggestion</option>
                <option value="bug_report">Bug Report</option>
              </select>
            </div>
            <div className="form-group">
              <label>Rating (1-5)</label>
              <div className="rating-stars">
                {[1, 2, 3, 4, 5].map((star) => (
                  <span
                    key={star}
                    className={feedbackForm.rating >= star ? 'active' : ''}
                    onClick={() => setFeedbackForm({ ...feedbackForm, rating: star })}
                  >
                    ★
                  </span>
                ))}
              </div>
            </div>
            <div className="form-group">
              <label>Comment</label>
              <textarea
                className="input"
                value={feedbackForm.comment}
                onChange={(e) =>
                  setFeedbackForm({ ...feedbackForm, comment: e.target.value })
                }
                placeholder="Share your detailed feedback..."
                required
              />
            </div>
            <div style={{ display: 'flex', gap: '10px' }}>
              <button type="submit" className="btn btn-primary">
                Submit Feedback
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowFeedbackForm(false)
                  setSelectedInteraction(null)
                }}
                className="btn"
                style={{ background: '#ccc' }}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}

export default Interactions
