"""
Database configuration and models
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///./mirror_gen.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

class User(Base):
    """User model for tracking individual users"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Growth metrics
    skill_level = Column(Float, default=0.0)
    engagement_score = Column(Float, default=0.0)
    learning_progress = Column(Float, default=0.0)
    
    # Relationships
    interactions = relationship("Interaction", back_populates="user", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")
    growth_records = relationship("GrowthRecord", back_populates="user", cascade="all, delete-orphan")

class Interaction(Base):
    """User interaction tracking for AI learning"""
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Interaction details
    interaction_type = Column(String)  # query, feedback, task_completion, etc.
    content = Column(Text)
    context = Column(JSON)  # Additional context as JSON
    
    # AI response tracking
    ai_response = Column(Text)
    response_quality = Column(Float)  # User-rated or calculated
    processing_time = Column(Float)
    
    # Relationships
    user = relationship("User", back_populates="interactions")

class Feedback(Base):
    """User feedback for AI improvement"""
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    interaction_id = Column(Integer, ForeignKey("interactions.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Feedback details
    feedback_type = Column(String)  # positive, negative, suggestion, bug_report
    rating = Column(Integer)  # 1-5 rating
    comment = Column(Text)
    sentiment_score = Column(Float)  # Calculated sentiment
    
    # Status
    is_processed = Column(Integer, default=0)  # Boolean as int for SQLite
    improvement_applied = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="feedbacks")

class GrowthRecord(Base):
    """Track user growth over time"""
    __tablename__ = "growth_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Growth metrics snapshot
    skill_level = Column(Float)
    engagement_score = Column(Float)
    learning_progress = Column(Float)
    tasks_completed = Column(Integer, default=0)
    
    # AI performance metrics
    ai_accuracy = Column(Float)
    ai_response_time = Column(Float)
    user_satisfaction = Column(Float)
    
    # Relationships
    user = relationship("User", back_populates="growth_records")

class AIModel(Base):
    """Track AI model versions and performance"""
    __tablename__ = "ai_models"
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Performance metrics
    accuracy = Column(Float)
    avg_response_time = Column(Float)
    user_satisfaction = Column(Float)
    
    # Training info
    training_data_size = Column(Integer)
    feedback_incorporated = Column(Integer)
    improvements = Column(JSON)

# Dependency for getting database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
