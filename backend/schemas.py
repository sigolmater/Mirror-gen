"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    skill_level: Optional[float] = None
    engagement_score: Optional[float] = None
    learning_progress: Optional[float] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    skill_level: float
    engagement_score: float
    learning_progress: float
    
    class Config:
        from_attributes = True

# Interaction schemas
class InteractionCreate(BaseModel):
    interaction_type: str
    content: str
    context: Optional[Dict[str, Any]] = None

class InteractionResponse(BaseModel):
    id: int
    user_id: int
    timestamp: datetime
    interaction_type: str
    content: str
    ai_response: Optional[str]
    response_quality: Optional[float]
    
    class Config:
        from_attributes = True

# Feedback schemas
class FeedbackCreate(BaseModel):
    interaction_id: Optional[int] = None
    feedback_type: str
    rating: int = Field(ge=1, le=5)
    comment: str

class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    timestamp: datetime
    feedback_type: str
    rating: int
    comment: str
    is_processed: bool
    
    class Config:
        from_attributes = True

# Analytics schemas
class GrowthMetrics(BaseModel):
    user_id: int
    username: str
    skill_level: float
    engagement_score: float
    learning_progress: float
    tasks_completed: int
    total_interactions: int
    avg_satisfaction: float

class AIPerformanceMetrics(BaseModel):
    total_interactions: int
    avg_response_time: float
    avg_user_satisfaction: float
    feedback_processed: int
    improvement_rate: float

class MutualGrowthAnalysis(BaseModel):
    user_growth: GrowthMetrics
    ai_performance: AIPerformanceMetrics
    growth_trend: List[Dict[str, Any]]
    recommendations: List[str]
