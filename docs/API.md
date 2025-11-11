# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, the API does not require authentication. In production, implement proper authentication mechanisms.

## Endpoints

### Health Check

#### GET `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Users

### Create User

#### POST `/users/`

Create a new user in the system.

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com"
}
```

**Response (201):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2025-01-01T00:00:00",
  "skill_level": 0.0,
  "engagement_score": 0.0,
  "learning_progress": 0.0
}
```

### List Users

#### GET `/users/`

Get all users with pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum records to return (default: 100)

**Response (200):**
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2025-01-01T00:00:00",
    "skill_level": 25.5,
    "engagement_score": 45.0,
    "learning_progress": 30.0
  }
]
```

### Get User

#### GET `/users/{user_id}`

Get a specific user by ID.

**Response (200):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2025-01-01T00:00:00",
  "skill_level": 25.5,
  "engagement_score": 45.0,
  "learning_progress": 30.0
}
```

### Update User

#### PUT `/users/{user_id}`

Update user information.

**Request Body:**
```json
{
  "username": "john_updated",
  "skill_level": 30.0
}
```

**Response (200):**
```json
{
  "id": 1,
  "username": "john_updated",
  "email": "john@example.com",
  "created_at": "2025-01-01T00:00:00",
  "skill_level": 30.0,
  "engagement_score": 45.0,
  "learning_progress": 30.0
}
```

### Delete User

#### DELETE `/users/{user_id}`

Delete a user and all associated data.

**Response (200):**
```json
{
  "message": "User deleted successfully"
}
```

---

## Interactions

### Create Interaction

#### POST `/interactions/{user_id}`

Create a new interaction for a user.

**Request Body:**
```json
{
  "interaction_type": "query",
  "content": "How do I improve my skills?",
  "context": {
    "source": "web_interface",
    "session_id": "abc123"
  }
}
```

**Interaction Types:**
- `query`: User question or request
- `feedback`: User feedback on AI response
- `task_completion`: Completed task or exercise
- `learning`: Educational activity

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "timestamp": "2025-01-01T00:00:00",
  "interaction_type": "query",
  "content": "How do I improve my skills?",
  "ai_response": "AI response to: How do I improve my skills?",
  "response_quality": 0.85
}
```

### Get User Interactions

#### GET `/interactions/{user_id}`

Get all interactions for a specific user.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Maximum records to return (default: 50)

**Response (200):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "timestamp": "2025-01-01T00:00:00",
    "interaction_type": "query",
    "content": "How do I improve my skills?",
    "ai_response": "AI response...",
    "response_quality": 0.85
  }
]
```

### Get Interaction Statistics

#### GET `/interactions/{user_id}/stats`

Get interaction statistics for a user.

**Response (200):**
```json
{
  "user_id": 1,
  "total_interactions": 25,
  "average_response_quality": 0.82,
  "interactions_by_type": {
    "query": 15,
    "feedback": 5,
    "task_completion": 5
  }
}
```

---

## Feedback

### Submit Feedback

#### POST `/feedback/{user_id}`

Submit user feedback on an interaction.

**Request Body:**
```json
{
  "interaction_id": 1,
  "feedback_type": "positive",
  "rating": 5,
  "comment": "Very helpful response!"
}
```

**Feedback Types:**
- `positive`: Positive feedback
- `negative`: Negative feedback
- `suggestion`: Improvement suggestion
- `bug_report`: Bug or issue report

**Rating:** Integer from 1 to 5

**Response (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "timestamp": "2025-01-01T00:00:00",
  "feedback_type": "positive",
  "rating": 5,
  "comment": "Very helpful response!",
  "is_processed": false
}
```

### Get User Feedback

#### GET `/feedback/{user_id}`

Get all feedback from a specific user.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Maximum records to return (default: 50)

**Response (200):**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "timestamp": "2025-01-01T00:00:00",
    "feedback_type": "positive",
    "rating": 5,
    "comment": "Very helpful response!",
    "is_processed": true
  }
]
```

### Process Feedback

#### POST `/feedback/{feedback_id}/process`

Mark feedback as processed and apply improvements.

**Response (200):**
```json
{
  "message": "Feedback processed successfully",
  "improvement_applied": true
}
```

### Get Feedback Summary

#### GET `/feedback/analytics/summary`

Get overall feedback analytics.

**Response (200):**
```json
{
  "total_feedback": 100,
  "average_rating": 4.2,
  "processed_count": 85,
  "processing_rate": 85.0,
  "feedback_by_type": {
    "positive": 60,
    "negative": 20,
    "suggestion": 15,
    "bug_report": 5
  }
}
```

---

## Analytics

### Get User Growth Metrics

#### GET `/analytics/user/{user_id}/growth`

Get comprehensive growth metrics for a user.

**Response (200):**
```json
{
  "user_id": 1,
  "username": "john_doe",
  "skill_level": 35.5,
  "engagement_score": 67.0,
  "learning_progress": 45.0,
  "tasks_completed": 12,
  "total_interactions": 50,
  "avg_satisfaction": 4.3
}
```

### Get AI Performance Metrics

#### GET `/analytics/ai/performance`

Get AI system performance metrics.

**Response (200):**
```json
{
  "total_interactions": 500,
  "avg_response_time": 0.35,
  "avg_user_satisfaction": 4.2,
  "feedback_processed": 150,
  "improvement_rate": 78.5
}
```

### Create Growth Snapshot

#### POST `/analytics/user/{user_id}/snapshot`

Create a snapshot of current user growth for historical tracking.

**Response (200):**
```json
{
  "message": "Growth snapshot created",
  "snapshot_id": 42
}
```

### Get Growth Trend

#### GET `/analytics/user/{user_id}/growth-trend`

Get user growth trend data over time.

**Query Parameters:**
- `days` (int, optional): Number of days to look back (default: 30)

**Response (200):**
```json
{
  "user_id": 1,
  "period_days": 30,
  "data_points": 15,
  "trend": [
    {
      "timestamp": "2025-01-01T00:00:00",
      "skill_level": 25.0,
      "engagement_score": 40.0,
      "learning_progress": 30.0,
      "ai_accuracy": 0.85,
      "user_satisfaction": 4.0
    }
  ]
}
```

### Get Mutual Growth Analysis

#### GET `/analytics/mutual-growth/{user_id}`

Get comprehensive mutual growth analysis showing how user and AI grow together.

**Response (200):**
```json
{
  "user_growth": {
    "user_id": 1,
    "username": "john_doe",
    "skill_level": 35.5,
    "engagement_score": 67.0,
    "learning_progress": 45.0,
    "tasks_completed": 12,
    "total_interactions": 50,
    "avg_satisfaction": 4.3
  },
  "ai_performance": {
    "total_interactions": 500,
    "avg_response_time": 0.35,
    "avg_user_satisfaction": 4.2,
    "feedback_processed": 150,
    "improvement_rate": 78.5
  },
  "growth_trend": [...],
  "recommendations": [
    "Increase interaction frequency to boost engagement",
    "Focus on completing tasks to improve learning progress"
  ]
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Error message describing the issue"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently not implemented. Consider adding rate limiting in production.

## CORS

The API allows CORS from:
- `http://localhost:3000`
- `http://localhost:5173`

Additional origins can be configured in the backend `main.py` file.
