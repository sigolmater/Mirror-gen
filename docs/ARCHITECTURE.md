# System Architecture

## Overview

Mirror-gen implements a three-tier architecture with frontend, backend, and data layers working together to create a virtuous cycle of user-AI growth.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                          │
│                      (React + Vite + Recharts)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Dashboard   │  │    Users     │  │ Interactions │         │
│  │              │  │              │  │              │         │
│  │ - Metrics    │  │ - Create     │  │ - Submit     │         │
│  │ - Overview   │  │ - List       │  │ - View       │         │
│  │ - Summary    │  │ - Edit       │  │ - Feedback   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │            Analytics & Visualization              │          │
│  │                                                   │          │
│  │  - Growth Trends (Line Charts)                   │          │
│  │  - Performance Metrics (Bar Charts)              │          │
│  │  - Recommendations                               │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ HTTP/REST API
                              │ (axios)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Backend Layer                           │
│                     (FastAPI + SQLAlchemy)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Users Router │  │ Interactions │  │  Feedback    │         │
│  │              │  │    Router    │  │   Router     │         │
│  │ - CRUD ops   │  │              │  │              │         │
│  │ - Validation │  │ - Create     │  │ - Submit     │         │
│  │              │  │ - Track      │  │ - Process    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │         Analytics Router                         │          │
│  │                                                   │          │
│  │  - User Growth Calculation                       │          │
│  │  - AI Performance Tracking                       │          │
│  │  - Mutual Growth Analysis                        │          │
│  │  - Trend Data Generation                         │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │            Pydantic Schemas                       │          │
│  │  (Request/Response Validation)                   │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ SQLAlchemy ORM
                              │ (Async)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Data Layer                             │
│                       (SQLite Database)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │   Users    │  │Interactions│  │  Feedback  │               │
│  │            │  │            │  │            │               │
│  │ - id       │  │ - id       │  │ - id       │               │
│  │ - username │  │ - user_id  │  │ - user_id  │               │
│  │ - email    │  │ - type     │  │ - rating   │               │
│  │ - metrics  │  │ - content  │  │ - comment  │               │
│  └────────────┘  └────────────┘  └────────────┘               │
│                                                                 │
│  ┌────────────┐  ┌────────────┐                                │
│  │   Growth   │  │ AI Models  │                                │
│  │  Records   │  │            │                                │
│  │            │  │ - version  │                                │
│  │ - user_id  │  │ - metrics  │                                │
│  │ - snapshot │  │ - training │                                │
│  └────────────┘  └────────────┘                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow: The Virtuous Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interaction                        │
│                                                             │
│  User submits query/task → System logs interaction         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI Processing                            │
│                                                             │
│  AI generates response → Quality score calculated           │
│  Response time tracked → User engagement updated            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Feedback Collection                        │
│                                                             │
│  User rates response → Sentiment analysis                   │
│  Detailed comment → Feedback categorization                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Analysis                             │
│                                                             │
│  Aggregate feedback → Identify patterns                     │
│  Calculate metrics → Generate insights                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Mutual Improvement                         │
│                                                             │
│  User: Skill ↑, Engagement ↑, Progress ↑                   │
│  AI: Accuracy ↑, Response time ↓, Satisfaction ↑           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      └──────────┐
                                 │
                      ┌──────────┘
                      │
                      ▼
            Better Experience → More Engagement
                      │
                      └─────→ (Cycle continues)
```

## Component Responsibilities

### Frontend Components

1. **Dashboard**
   - Display real-time metrics
   - Show AI performance overview
   - Present feedback summary

2. **User Management**
   - CRUD operations for users
   - Display user growth metrics
   - Track individual progress

3. **Interactions**
   - Submit user queries
   - View interaction history
   - Provide detailed feedback

4. **Analytics**
   - Visualize growth trends
   - Compare user vs AI metrics
   - Generate recommendations

### Backend Routers

1. **Users Router**
   - User CRUD operations
   - Profile management
   - Metrics updates

2. **Interactions Router**
   - Log user interactions
   - Generate AI responses
   - Track quality metrics

3. **Feedback Router**
   - Collect user feedback
   - Sentiment analysis
   - Feedback processing

4. **Analytics Router**
   - Calculate growth metrics
   - Generate trend data
   - Provide insights

### Database Models

1. **User**
   - Profile information
   - Growth metrics (skill, engagement, progress)
   - Timestamps

2. **Interaction**
   - User ID reference
   - Interaction type and content
   - AI response and quality

3. **Feedback**
   - User ID reference
   - Rating and comment
   - Processing status

4. **GrowthRecord**
   - Historical snapshots
   - Trend tracking
   - Performance correlation

5. **AIModel**
   - Version tracking
   - Performance metrics
   - Training information

## API Communication

### Request Flow

```
Frontend → HTTP Request → FastAPI Router
                              ↓
                    Pydantic Validation
                              ↓
                    Business Logic
                              ↓
                    SQLAlchemy ORM
                              ↓
                    Database Query
                              ↓
                    Response Model
                              ↓
Frontend ← HTTP Response ← Pydantic Schema
```

### Key Endpoints

- **GET /api/users/** - List users
- **POST /api/interactions/{user_id}** - Create interaction
- **POST /api/feedback/{user_id}** - Submit feedback
- **GET /api/analytics/mutual-growth/{user_id}** - Get analysis

## Security Considerations

1. **Input Validation**: Pydantic schemas validate all inputs
2. **CORS**: Configured for specific origins
3. **Database**: SQLAlchemy prevents SQL injection
4. **Future**: Add authentication, rate limiting, encryption

## Scalability

### Current Design
- Single-server deployment
- SQLite database
- Synchronous frontend

### Future Enhancements
- Horizontal scaling with load balancer
- PostgreSQL with connection pooling
- Redis caching layer
- Message queue for async tasks
- Microservices architecture

## Monitoring Points

1. **API Performance**
   - Response times
   - Error rates
   - Request counts

2. **Database Health**
   - Query performance
   - Connection pool usage
   - Storage capacity

3. **User Metrics**
   - Active users
   - Engagement rates
   - Satisfaction scores

4. **AI Performance**
   - Response quality
   - Processing time
   - Improvement rate

## Development Workflow

```
1. Code Changes
   ↓
2. Local Testing
   ↓
3. Integration Tests
   ↓
4. Build Frontend
   ↓
5. Deploy Backend
   ↓
6. Monitor Metrics
```

## Technology Choices Rationale

### FastAPI
- Async support for better performance
- Automatic API documentation
- Type hints and validation
- Modern Python framework

### React + Vite
- Fast development experience
- Component-based architecture
- Rich ecosystem
- Excellent performance

### SQLite → PostgreSQL
- SQLite: Easy development setup
- PostgreSQL: Production-ready
- Easy migration path
- Same SQLAlchemy code

### Recharts
- Declarative API
- React integration
- Customizable
- Good documentation

## Deployment Architecture

### Development
```
localhost:5173 (Frontend) → localhost:8000 (Backend) → SQLite DB
```

### Production
```
nginx (80/443) → React (static) → nginx reverse proxy
                                        ↓
                                 FastAPI (8000)
                                        ↓
                                 PostgreSQL (5432)
```

## Configuration Management

1. **Environment Variables**
   - Database URL
   - CORS origins
   - API keys (future)

2. **Build Configuration**
   - Vite config for frontend
   - Uvicorn config for backend
   - Docker compose for containers

3. **Feature Flags**
   - Enable/disable features
   - A/B testing capability
   - Gradual rollout support
