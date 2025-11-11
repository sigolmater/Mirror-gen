import { Routes, Route, Link, useLocation } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import UserManagement from './pages/UserManagement'
import Interactions from './pages/Interactions'
import Analytics from './pages/Analytics'

function App() {
  const location = useLocation()

  return (
    <div className="app">
      <div className="header">
        <div className="container">
          <h1>🪞 Mirror-gen: User-AI Growth System</h1>
          <nav className="nav">
            <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
              Dashboard
            </Link>
            <Link to="/users" className={location.pathname === '/users' ? 'active' : ''}>
              Users
            </Link>
            <Link to="/interactions" className={location.pathname === '/interactions' ? 'active' : ''}>
              Interactions
            </Link>
            <Link to="/analytics" className={location.pathname === '/analytics' ? 'active' : ''}>
              Analytics
            </Link>
          </nav>
        </div>
      </div>

      <div className="container">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/users" element={<UserManagement />} />
          <Route path="/interactions" element={<Interactions />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </div>
    </div>
  )
}

export default App
