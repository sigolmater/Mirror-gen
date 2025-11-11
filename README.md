# 🪞 Mirror-gen: User-AI Growth System
## 사용자-AI 선순환 성장 시스템

<p align="center">
  <strong>A comprehensive system enabling mutual learning and growth between users and AI through continuous interaction and feedback loops.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
</p>

---

## 🎯 Overview

Mirror-gen implements a **virtuous cycle system (선순환 시스템)** where users and AI grow together through mutual learning. The system tracks user behavior, collects feedback, and uses this data to continuously improve both AI performance and user experience.

### ✨ Key Features

1. **사용자 학습 데이터 동기화** (User Learning Data Synchronization)
   - Real-time data pipeline for user behavior tracking
   - Automatic synchronization of user interactions
   - Comprehensive data storage and retrieval

2. **AI 피드백 루프 강화** (AI Feedback Loop Enhancement)
   - User feedback collection and analysis
   - Continuous AI model optimization
   - Interaction logging and analytics dashboard

3. **사용자 성장 지원 기능** (User Growth Support)
   - Mutual learning interface
   - Educational progress tracking
   - Quantifiable growth metrics visualization

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend runs on: **http://localhost:8000**

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: **http://localhost:5173**

---

## 📁 Project Structure

```
Mirror-gen/
├── backend/          # FastAPI backend
│   ├── main.py       # Application entry point
│   ├── database.py   # Database models
│   ├── schemas.py    # Pydantic schemas
│   └── routers/      # API endpoints
├── frontend/         # React frontend
│   └── src/
│       ├── pages/    # UI pages
│       └── services/ # API integration
└── docs/            # Documentation
```

---

## 🌟 The Virtuous Cycle

```
User Interaction → AI Response → Feedback Collection
      ↓                              ↓
User Growth ←  Mutual Learning  ← AI Improvement
```

1. **Users** interact with the AI system
2. **AI** learns from user feedback
3. **Both** grow together through continuous improvement

---

## 📊 Features

### Dashboard
- Real-time system metrics
- AI performance overview
- User engagement statistics

### User Management
- Create and manage users
- Track growth metrics (skill level, engagement, learning progress)

### Interactions
- Submit queries to AI
- View interaction history
- Provide detailed feedback

### Analytics
- Visualize mutual growth trends
- Compare user and AI performance
- Get personalized recommendations

---

## 📚 Documentation

- [Detailed README](docs/README.md)
- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite, Recharts, TanStack Query
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: SQLite (upgradeable to PostgreSQL)
- **Styling**: Custom CSS with gradient themes

---

## 🔗 API Endpoints

- `/api/users` - User management
- `/api/interactions` - Interaction tracking
- `/api/feedback` - Feedback collection
- `/api/analytics` - Growth analytics

Full API documentation: **http://localhost:8000/docs**

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

---

## 📈 Future Enhancements

- Real AI/ML model integration
- Advanced NLP for sentiment analysis
- Multi-user collaboration
- Mobile application
- Real-time notifications

---

## 📝 License

This project is part of the Mirror-gen repository.

---

<p align="center">
  Built with ❤️ for mutual learning and growth
</p>