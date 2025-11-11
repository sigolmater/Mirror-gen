"""
Feedback collection and processing endpoints
AI Feedback Loop Enhancement
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List
from datetime import datetime
import random

from database import get_db, Feedback, User, GrowthRecord
from schemas import FeedbackCreate, FeedbackResponse

router = APIRouter()

def calculate_sentiment(comment: str, rating: int) -> float:
    """
    Simple sentiment calculation
    In production, this would use NLP/ML models
    """
    # Sentiment based on rating and comment length
    base_sentiment = (rating - 3) / 2  # -1 to 1 scale
    comment_boost = min(0.2, len(comment) / 1000)
    return max(-1.0, min(1.0, base_sentiment + comment_boost))

@router.post("/{user_id}", response_model=FeedbackResponse)
async def submit_feedback(
    user_id: int,
    feedback: FeedbackCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit user feedback for AI improvement
    This is a key component of the feedback loop
    """
    # Verify user exists
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate sentiment
    sentiment = calculate_sentiment(feedback.comment, feedback.rating)
    
    # Create feedback record
    db_feedback = Feedback(
        user_id=user_id,
        interaction_id=feedback.interaction_id,
        feedback_type=feedback.feedback_type,
        rating=feedback.rating,
        comment=feedback.comment,
        sentiment_score=sentiment
    )
    
    db.add(db_feedback)
    
    # Update user learning progress based on feedback quality
    if len(feedback.comment) > 50:  # Detailed feedback shows engagement
        user.learning_progress = min(100.0, user.learning_progress + 2.0)
    
    await db.commit()
    await db.refresh(db_feedback)
    
    return db_feedback

@router.get("/{user_id}", response_model=List[FeedbackResponse])
async def get_user_feedback(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get all feedback from a specific user"""
    result = await db.execute(
        select(Feedback)
        .where(Feedback.user_id == user_id)
        .order_by(Feedback.timestamp.desc())
        .offset(skip)
        .limit(limit)
    )
    feedbacks = result.scalars().all()
    return feedbacks

@router.post("/{feedback_id}/process")
async def process_feedback(feedback_id: int, db: AsyncSession = Depends(get_db)):
    """
    Mark feedback as processed and apply improvements
    Simulates the AI learning from user feedback
    """
    result = await db.execute(select(Feedback).where(Feedback.id == feedback_id))
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    # Mark as processed
    feedback.is_processed = 1
    
    # Simulate improvement application based on feedback quality
    if feedback.rating >= 4 or feedback.sentiment_score > 0.5:
        feedback.improvement_applied = 1
    
    await db.commit()
    await db.refresh(feedback)
    
    return {
        "message": "Feedback processed successfully",
        "improvement_applied": bool(feedback.improvement_applied)
    }

@router.get("/analytics/summary")
async def get_feedback_summary(db: AsyncSession = Depends(get_db)):
    """Get overall feedback analytics"""
    # Total feedback count
    total_result = await db.execute(select(func.count(Feedback.id)))
    total = total_result.scalar()
    
    # Average rating
    avg_rating_result = await db.execute(select(func.avg(Feedback.rating)))
    avg_rating = avg_rating_result.scalar() or 0.0
    
    # Processed count
    processed_result = await db.execute(
        select(func.count(Feedback.id)).where(Feedback.is_processed == 1)
    )
    processed = processed_result.scalar()
    
    # Feedback by type
    type_result = await db.execute(
        select(Feedback.feedback_type, func.count(Feedback.id))
        .group_by(Feedback.feedback_type)
    )
    by_type = {row[0]: row[1] for row in type_result.all()}
    
    return {
        "total_feedback": total,
        "average_rating": float(avg_rating),
        "processed_count": processed,
        "processing_rate": (processed / total * 100) if total > 0 else 0,
        "feedback_by_type": by_type
    }
