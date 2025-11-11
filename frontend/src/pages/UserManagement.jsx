import { useState, useEffect } from 'react'
import { userService } from '../services/api'
import { UserPlus, Trash2, Edit } from 'lucide-react'

function UserManagement() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
  })
  const [message, setMessage] = useState({ type: '', text: '' })

  useEffect(() => {
    loadUsers()
  }, [])

  const loadUsers = async () => {
    try {
      const response = await userService.getUsers()
      setUsers(response.data)
    } catch (error) {
      console.error('Error loading users:', error)
      setMessage({ type: 'error', text: 'Failed to load users' })
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await userService.createUser(formData)
      setMessage({ type: 'success', text: 'User created successfully!' })
      setFormData({ username: '', email: '' })
      setShowCreateForm(false)
      loadUsers()
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || 'Failed to create user' 
      })
    }
  }

  const handleDelete = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        await userService.deleteUser(userId)
        setMessage({ type: 'success', text: 'User deleted successfully!' })
        loadUsers()
      } catch (error) {
        setMessage({ type: 'error', text: 'Failed to delete user' })
      }
    }
  }

  if (loading) {
    return <div className="loading">Loading users...</div>
  }

  return (
    <div>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2>User Management</h2>
          <button 
            className="btn btn-primary" 
            onClick={() => setShowCreateForm(!showCreateForm)}
          >
            <UserPlus size={20} style={{ verticalAlign: 'middle', marginRight: '8px' }} />
            {showCreateForm ? 'Cancel' : 'Create User'}
          </button>
        </div>

        {message.text && (
          <div className={message.type}>
            {message.text}
          </div>
        )}

        {showCreateForm && (
          <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                className="input"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                className="input"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary">
              Create User
            </button>
          </form>
        )}

        {users.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#888', padding: '40px' }}>
            No users found. Create your first user to get started!
          </p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #e0e0e0' }}>
                  <th style={{ padding: '12px', textAlign: 'left' }}>ID</th>
                  <th style={{ padding: '12px', textAlign: 'left' }}>Username</th>
                  <th style={{ padding: '12px', textAlign: 'left' }}>Email</th>
                  <th style={{ padding: '12px', textAlign: 'left' }}>Skill Level</th>
                  <th style={{ padding: '12px', textAlign: 'left' }}>Engagement</th>
                  <th style={{ padding: '12px', textAlign: 'left' }}>Learning Progress</th>
                  <th style={{ padding: '12px', textAlign: 'left' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id} style={{ borderBottom: '1px solid #f0f0f0' }}>
                    <td style={{ padding: '12px' }}>{user.id}</td>
                    <td style={{ padding: '12px' }}>{user.username}</td>
                    <td style={{ padding: '12px' }}>{user.email}</td>
                    <td style={{ padding: '12px' }}>{user.skill_level.toFixed(1)}</td>
                    <td style={{ padding: '12px' }}>{user.engagement_score.toFixed(1)}</td>
                    <td style={{ padding: '12px' }}>{user.learning_progress.toFixed(1)}</td>
                    <td style={{ padding: '12px' }}>
                      <button
                        onClick={() => handleDelete(user.id)}
                        style={{
                          background: '#f44336',
                          color: 'white',
                          border: 'none',
                          padding: '6px 12px',
                          borderRadius: '4px',
                          cursor: 'pointer',
                        }}
                      >
                        <Trash2 size={16} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="card">
        <h3>About User Growth Tracking</h3>
        <p style={{ color: '#666', lineHeight: '1.6' }}>
          This system tracks three key metrics for each user:
        </p>
        <ul style={{ color: '#666', lineHeight: '2', marginTop: '10px' }}>
          <li><strong>Skill Level:</strong> Measures user proficiency and expertise development</li>
          <li><strong>Engagement Score:</strong> Tracks active participation and interaction frequency</li>
          <li><strong>Learning Progress:</strong> Monitors educational advancement and task completion</li>
        </ul>
        <p style={{ color: '#666', lineHeight: '1.6', marginTop: '10px' }}>
          These metrics automatically update based on user interactions and feedback, creating a 
          comprehensive view of user-AI mutual growth.
        </p>
      </div>
    </div>
  )
}

export default UserManagement
