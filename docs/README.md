# Mirror-gen: User-AI Growth System
# 사용자-AI 선순환 성장 시스템

A comprehensive system that enables mutual learning and growth between users and AI through continuous interaction and feedback loops.

## 🎯 Overview

Mirror-gen implements a **virtuous cycle system** where users and AI grow together. The system tracks user behavior, collects feedback, and uses this data to continuously improve both AI performance and user experience.

### Key Features

1. **User Learning Data Synchronization** (사용자 학습 데이터 동기화)
   - Real-time data pipeline for user behavior tracking
   - Automatic synchronization of user interactions
   - Comprehensive data storage and retrieval

2. **AI Feedback Loop Enhancement** (AI 피드백 루프 강화)
   - User feedback collection and analysis
   - Continuous AI model optimization
   - Interaction logging and analytics dashboard

3. **User Growth Support** (사용자 성장 지원 기능)
   - Mutual learning interface
   - Educational elements and progress tracking
   - Quantifiable growth metrics visualization

## 🏗️ Architecture

### Technology Stack

- **Frontend**: ReactJS with Vite
  - React Router for navigation
  - Recharts for data visualization
  - Axios for API communication
  - TanStack Query for state management

- **Backend**: FastAPI
  - Async SQLAlchemy for database operations
  - Pydantic for data validation
  - CORS middleware for frontend integration

- **Database**: SQLite (easily upgradeable to PostgreSQL)
  - User profiles and metrics
  - Interaction history
  - Feedback tracking
  - Growth snapshots

## 📁 Project Structure

```
Mirror-gen/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database models and configuration
│   ├── schemas.py           # Pydantic schemas
│   ├── requirements.txt     # Python dependencies
│   └── routers/
│       ├── users.py         # User management endpoints
│       ├── interactions.py  # Interaction tracking endpoints
│       ├── feedback.py      # Feedback collection endpoints
│       └── analytics.py     # Analytics and growth tracking
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx      # Main dashboard
│   │   │   ├── UserManagement.jsx # User CRUD
│   │   │   ├── Interactions.jsx   # Interaction interface
│   │   │   └── Analytics.jsx      # Growth analytics
│   │   ├── services/
│   │   │   └── api.js             # API service layer
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
└── docs/
    └── API.md               # API documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📊 How It Works

### The Virtuous Cycle (선순환)

1. **User Interaction**
   - Users interact with the AI system
   - Each interaction is logged with context and metadata
   - AI generates responses and tracks quality metrics

2. **Feedback Collection**
   - Users provide ratings and detailed feedback
   - Sentiment analysis processes feedback automatically
   - Feedback is categorized and prioritized

3. **AI Learning**
   - System analyzes feedback patterns
   - AI model parameters are adjusted based on user input
   - Performance metrics are continuously monitored

4. **User Growth**
   - System tracks user skill development
   - Engagement scores reflect activity levels
   - Learning progress shows educational advancement

5. **Mutual Improvement**
   - Better AI leads to improved user experiences
   - Enhanced experiences increase user engagement
   - More engagement provides richer data for AI improvement

### Key Metrics

**User Metrics:**
- **Skill Level**: Proficiency and expertise development
- **Engagement Score**: Activity level and participation
- **Learning Progress**: Educational advancement percentage
- **Tasks Completed**: High-quality interactions count

**AI Metrics:**
- **Total Interactions**: Number of conversations processed
- **Response Time**: Average processing speed
- **User Satisfaction**: Average feedback rating
- **Improvement Rate**: Percentage of feedback incorporated

## 🎨 User Interface

The system provides four main interfaces:

1. **Dashboard**: Overview of system performance and metrics
2. **User Management**: Create and manage user profiles
3. **Interactions**: Submit queries and provide feedback
4. **Analytics**: Visualize mutual growth trends

## 🔄 Data Pipeline

```
User Action → Interaction Logging → AI Response → Feedback Collection
      ↓                                                    ↓
Growth Metrics Update ← Performance Analysis ← Sentiment Analysis
      ↓                                                    ↓
Visualization ← Trend Calculation ← Data Aggregation ← Storage
```

## 📈 Analytics Features

- **Real-time Metrics**: Live tracking of user and AI performance
- **Trend Visualization**: Line and bar charts showing growth over time
- **Recommendations**: AI-generated suggestions for improvement
- **Comparative Analysis**: User vs AI performance correlation

## 🔐 API Endpoints

### Users
- `POST /api/users/` - Create user
- `GET /api/users/` - List all users
- `GET /api/users/{id}` - Get user details
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

### Interactions
- `POST /api/interactions/{user_id}` - Create interaction
- `GET /api/interactions/{user_id}` - Get user interactions
- `GET /api/interactions/{user_id}/stats` - Get interaction statistics

### Feedback
- `POST /api/feedback/{user_id}` - Submit feedback
- `GET /api/feedback/{user_id}` - Get user feedback
- `POST /api/feedback/{id}/process` - Process feedback
- `GET /api/feedback/analytics/summary` - Get feedback summary

### Analytics
- `GET /api/analytics/user/{user_id}/growth` - Get user growth metrics
- `GET /api/analytics/ai/performance` - Get AI performance metrics
- `POST /api/analytics/user/{user_id}/snapshot` - Create growth snapshot
- `GET /api/analytics/user/{user_id}/growth-trend` - Get growth trend
- `GET /api/analytics/mutual-growth/{user_id}` - Get mutual growth analysis

## 🌟 Future Enhancements

- Integration with real AI/ML models
- Advanced NLP for sentiment analysis
- Multi-user collaboration features
- Export and reporting capabilities
- Mobile application
- Real-time notifications
- Advanced visualization options

## 📝 License

This project is part of the Mirror-gen repository.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please use the GitHub Issues page.
