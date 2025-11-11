# Usage Examples

This guide provides practical examples of using the Mirror-gen User-AI Growth System.

## Quick Start Example

### Step 1: Start the System

**Terminal 1 - Backend:**
```bash
cd backend
./start.sh  # On Windows: start.bat
```

**Terminal 2 - Frontend:**
```bash
cd frontend
./start.sh  # On Windows: start.bat
```

### Step 2: Access the Application

Open your browser and navigate to: **http://localhost:5173**

## Example Workflow

### 1. Create a User

Navigate to the **Users** page and create a new user:

```
Username: alice_learner
Email: alice@example.com
```

### 2. Create Interactions

Go to the **Interactions** page:

1. Select the user you just created
2. Choose interaction type: "Query"
3. Enter content:
   ```
   I want to learn about machine learning. Where should I start?
   ```
4. Submit the interaction
5. The AI will respond and track the interaction

### 3. Provide Feedback

After receiving an AI response:

1. Click "Give Feedback" on the interaction
2. Select feedback type: "Positive"
3. Rate: 5 stars
4. Comment:
   ```
   Great response! The AI provided a clear learning path with specific resources.
   ```
5. Submit feedback

### 4. Track Growth

Go to the **Analytics** page to see:
- User growth metrics (skill level, engagement, learning progress)
- AI performance metrics (response time, accuracy, satisfaction)
- Growth trend visualizations
- Personalized recommendations

## API Usage Examples

### Using cURL

#### Create a User
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com"
  }'
```

#### Create an Interaction
```bash
curl -X POST http://localhost:8000/api/interactions/1 \
  -H "Content-Type: application/json" \
  -d '{
    "interaction_type": "query",
    "content": "How can I improve my programming skills?",
    "context": {"source": "api_test"}
  }'
```

#### Submit Feedback
```bash
curl -X POST http://localhost:8000/api/feedback/1 \
  -H "Content-Type: application/json" \
  -d '{
    "interaction_id": 1,
    "feedback_type": "positive",
    "rating": 5,
    "comment": "Very helpful and practical advice!"
  }'
```

#### Get User Growth Metrics
```bash
curl http://localhost:8000/api/analytics/user/1/growth
```

#### Get Mutual Growth Analysis
```bash
curl http://localhost:8000/api/analytics/mutual-growth/1
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Create a user
user_data = {
    "username": "python_user",
    "email": "python@example.com"
}
response = requests.post(f"{BASE_URL}/users/", json=user_data)
user = response.json()
user_id = user["id"]

# Create an interaction
interaction_data = {
    "interaction_type": "learning",
    "content": "I completed the Python basics tutorial",
    "context": {"tutorial": "python_basics", "score": 95}
}
response = requests.post(
    f"{BASE_URL}/interactions/{user_id}",
    json=interaction_data
)
interaction = response.json()

# Submit feedback
feedback_data = {
    "interaction_id": interaction["id"],
    "feedback_type": "positive",
    "rating": 5,
    "comment": "The tutorial was excellent!"
}
requests.post(f"{BASE_URL}/feedback/{user_id}", json=feedback_data)

# Get mutual growth analysis
response = requests.get(f"{BASE_URL}/analytics/mutual-growth/{user_id}")
analysis = response.json()
print(f"Engagement Score: {analysis['user_growth']['engagement_score']}")
print(f"AI Satisfaction: {analysis['ai_performance']['avg_user_satisfaction']}")
```

### Using JavaScript (Fetch API)

```javascript
const BASE_URL = 'http://localhost:8000/api';

async function example() {
  // Create a user
  const userResponse = await fetch(`${BASE_URL}/users/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'js_user',
      email: 'js@example.com'
    })
  });
  const user = await userResponse.json();
  
  // Create an interaction
  const interactionResponse = await fetch(
    `${BASE_URL}/interactions/${user.id}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        interaction_type: 'query',
        content: 'How do I use async/await in JavaScript?'
      })
    }
  );
  const interaction = await interactionResponse.json();
  
  // Get analytics
  const analyticsResponse = await fetch(
    `${BASE_URL}/analytics/mutual-growth/${user.id}`
  );
  const analytics = await analyticsResponse.json();
  console.log('User Growth:', analytics.user_growth);
  console.log('AI Performance:', analytics.ai_performance);
}

example();
```

## Use Case Scenarios

### Scenario 1: Educational Platform

Track student learning progress and AI tutor effectiveness:

```python
# Student completes a lesson
interaction = create_interaction(
    user_id=student_id,
    interaction_type="task_completion",
    content="Completed Lesson 5: Advanced Functions",
    context={"lesson_id": 5, "score": 92, "time_spent": 45}
)

# Student provides feedback on AI explanations
submit_feedback(
    user_id=student_id,
    interaction_id=interaction["id"],
    rating=5,
    comment="The AI examples were very clear and helpful"
)

# Teacher reviews progress
growth = get_growth_metrics(student_id)
# Shows: skill_level increasing, learning_progress tracking
```

### Scenario 2: Customer Support

Monitor customer satisfaction and AI assistant quality:

```python
# Customer asks a question
interaction = create_interaction(
    user_id=customer_id,
    interaction_type="query",
    content="How do I reset my password?"
)

# Customer rates the AI response
submit_feedback(
    user_id=customer_id,
    rating=4,
    feedback_type="suggestion",
    comment="Answer was correct but could be more detailed"
)

# Analyze overall performance
ai_metrics = get_ai_performance_metrics()
# Shows: avg_satisfaction, improvement_rate
```

### Scenario 3: Personal Growth Tracking

Individual learning journey:

```python
# Daily learning session
create_interaction(
    user_id=my_id,
    interaction_type="learning",
    content="Studied React hooks for 2 hours"
)

# Weekly review
growth_trend = get_growth_trend(my_id, days=7)
# Visualize: skill_level, engagement_score over time

# Get personalized recommendations
analysis = get_mutual_growth_analysis(my_id)
print(analysis["recommendations"])
# Output: ["Increase interaction frequency to boost engagement"]
```

## Data Analysis Examples

### Tracking Progress Over Time

```python
import pandas as pd
import matplotlib.pyplot as plt

# Get growth trend
trend = requests.get(
    f"{BASE_URL}/analytics/user/{user_id}/growth-trend?days=30"
).json()

# Convert to DataFrame
df = pd.DataFrame(trend["trend"])
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Plot growth metrics
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["skill_level"], label="Skill Level")
plt.plot(df["timestamp"], df["engagement_score"], label="Engagement")
plt.plot(df["timestamp"], df["learning_progress"], label="Learning Progress")
plt.xlabel("Date")
plt.ylabel("Score")
plt.title("User Growth Over Time")
plt.legend()
plt.show()
```

### Analyzing AI Performance

```python
# Get AI metrics
ai_perf = requests.get(f"{BASE_URL}/analytics/ai/performance").json()

# Get feedback summary
feedback = requests.get(f"{BASE_URL}/feedback/analytics/summary").json()

# Calculate improvement rate
improvement_rate = (
    feedback["processed_count"] / feedback["total_feedback"] * 100
)

print(f"AI Response Time: {ai_perf['avg_response_time']:.2f}s")
print(f"User Satisfaction: {ai_perf['avg_user_satisfaction']:.1f}/5.0")
print(f"Feedback Processing: {improvement_rate:.1f}%")
```

## Testing the Virtuous Cycle

### Simulating User Growth

```python
# Week 1: Basic interactions
for i in range(5):
    create_interaction(user_id, "query", f"Question {i}")
    submit_feedback(user_id, rating=3, comment="Okay response")

# Week 2: More engagement
for i in range(10):
    create_interaction(user_id, "learning", f"Lesson {i}")
    submit_feedback(user_id, rating=4, comment="Good, improving!")

# Week 3: Advanced usage
for i in range(15):
    create_interaction(user_id, "task_completion", f"Task {i}")
    submit_feedback(user_id, rating=5, comment="Excellent!")

# Analyze the growth
analysis = get_mutual_growth_analysis(user_id)
print(f"Engagement: {analysis['user_growth']['engagement_score']}")
print(f"AI Improvement: {analysis['ai_performance']['improvement_rate']}")
```

## Troubleshooting

### Common Issues

**Issue: Cannot connect to backend**
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not, start backend
cd backend && ./start.sh
```

**Issue: Frontend shows API errors**
```bash
# Verify CORS settings in backend/main.py
# Check browser console for specific errors
# Ensure both frontend and backend are running
```

**Issue: Database not found**
```bash
# The database is auto-created on first run
# If issues persist, delete and restart:
cd backend
rm mirror_gen.db
python main.py
```

## Next Steps

1. Explore the **Interactive API Documentation**: http://localhost:8000/docs
2. Try creating multiple users to compare growth patterns
3. Experiment with different interaction types and feedback
4. Review the analytics dashboard to see the virtuous cycle in action
5. Customize the system for your specific use case

## Support

For more information, see:
- [API Documentation](API.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Main README](README.md)
