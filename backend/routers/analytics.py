"""
Analytics and mutual growth tracking endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Dict, Any
from datetime import datetime, timedelta
import random

from database import get_db, User, Interaction, Feedback, GrowthRecord
from schemas import GrowthMetrics, AIPerformanceMetrics, MutualGrowthAnalysis

router = APIRouter()

@router.get("/user/{user_id}/growth", response_model=GrowthMetrics)
async def get_user_growth_metrics(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get comprehensive growth metrics for a user
    Supports the mutual learning visualization
    """
    # Get user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Total interactions
    interactions_result = await db.execute(
        select(func.count(Interaction.id)).where(Interaction.user_id == user_id)
    )
    total_interactions = interactions_result.scalar()
    
    # Average satisfaction (from feedback ratings)
    satisfaction_result = await db.execute(
        select(func.avg(Feedback.rating))
        .where(Feedback.user_id == user_id)
    )
    avg_satisfaction = satisfaction_result.scalar() or 0.0
    
    # Tasks completed (high quality interactions)
    tasks_result = await db.execute(
        select(func.count(Interaction.id))
        .where(and_(
            Interaction.user_id == user_id,
            Interaction.response_quality >= 0.8
        ))
    )
    tasks_completed = tasks_result.scalar()
    
    return GrowthMetrics(
        user_id=user.id,
        username=user.username,
        skill_level=user.skill_level,
        engagement_score=user.engagement_score,
        learning_progress=user.learning_progress,
        tasks_completed=tasks_completed,
        total_interactions=total_interactions,
        avg_satisfaction=float(avg_satisfaction)
    )

@router.get("/ai/performance", response_model=AIPerformanceMetrics)
async def get_ai_performance_metrics(db: AsyncSession = Depends(get_db)):
    """
    Get AI system performance metrics
    Shows how AI is improving based on user feedback
    """
    # Total interactions
    total_result = await db.execute(select(func.count(Interaction.id)))
    total_interactions = total_result.scalar()
    
    # Average response time
    time_result = await db.execute(select(func.avg(Interaction.processing_time)))
    avg_time = time_result.scalar() or 0.0
    
    # Average user satisfaction
    satisfaction_result = await db.execute(
        select(func.avg(Feedback.rating))
    )
    avg_satisfaction = satisfaction_result.scalar() or 0.0
    
    # Feedback processed
    processed_result = await db.execute(
        select(func.count(Feedback.id)).where(Feedback.is_processed == 1)
    )
    feedback_processed = processed_result.scalar()
    
    # Improvement rate (simulated based on feedback incorporation)
    improvement_result = await db.execute(
        select(func.count(Feedback.id)).where(Feedback.improvement_applied == 1)
    )
    improvements = improvement_result.scalar()
    improvement_rate = (improvements / feedback_processed * 100) if feedback_processed > 0 else 0
    
    return AIPerformanceMetrics(
        total_interactions=total_interactions,
        avg_response_time=float(avg_time),
        avg_user_satisfaction=float(avg_satisfaction),
        feedback_processed=feedback_processed,
        improvement_rate=float(improvement_rate)
    )

@router.post("/user/{user_id}/snapshot")
async def create_growth_snapshot(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Create a growth snapshot for tracking user progress over time
    """
    # Get user
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get current metrics
    metrics = await get_user_growth_metrics(user_id, db)
    
    # Create growth record
    growth_record = GrowthRecord(
        user_id=user_id,
        skill_level=user.skill_level,
        engagement_score=user.engagement_score,
        learning_progress=user.learning_progress,
        tasks_completed=metrics.tasks_completed,
        ai_accuracy=0.85 + random.uniform(0, 0.1),  # Simulated
        ai_response_time=0.3 + random.uniform(-0.1, 0.1),  # Simulated
        user_satisfaction=metrics.avg_satisfaction
    )
    
    db.add(growth_record)
    await db.commit()
    await db.refresh(growth_record)
    
    return {"message": "Growth snapshot created", "snapshot_id": growth_record.id}

@router.get("/user/{user_id}/growth-trend")
async def get_growth_trend(user_id: int, days: int = 30, db: AsyncSession = Depends(get_db)):
    """
    Get growth trend data for visualization
    Shows the mutual growth between user and AI over time
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    result = await db.execute(
        select(GrowthRecord)
        .where(and_(
            GrowthRecord.user_id == user_id,
            GrowthRecord.timestamp >= cutoff_date
        ))
        .order_by(GrowthRecord.timestamp.asc())
    )
    records = result.scalars().all()
    
    trend_data = [
        {
            "timestamp": record.timestamp.isoformat(),
            "skill_level": record.skill_level,
            "engagement_score": record.engagement_score,
            "learning_progress": record.learning_progress,
            "ai_accuracy": record.ai_accuracy,
            "user_satisfaction": record.user_satisfaction
        }
        for record in records
    ]
    
    return {
        "user_id": user_id,
        "period_days": days,
        "data_points": len(trend_data),
        "trend": trend_data
    }

@router.get("/mutual-growth/{user_id}", response_model=MutualGrowthAnalysis)
async def get_mutual_growth_analysis(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Comprehensive mutual growth analysis
    Shows how user and AI are growing together
    """
    user_growth = await get_user_growth_metrics(user_id, db)
    ai_performance = await get_ai_performance_metrics(db)
    
    # Get trend data
    trend_response = await get_growth_trend(user_id, 30, db)
    growth_trend = trend_response["trend"]
    
    # Generate recommendations
    recommendations = []
    
    if user_growth.engagement_score < 50:
        recommendations.append("Increase interaction frequency to boost engagement")
    
    if user_growth.learning_progress < user_growth.engagement_score:
        recommendations.append("Focus on completing tasks to improve learning progress")
    
    if ai_performance.avg_user_satisfaction < 4.0:
        recommendations.append("AI is learning from your feedback - continue providing detailed input")
    
    if len(growth_trend) < 5:
        recommendations.append("Keep using the system to track your growth over time")
    
    if not recommendations:
        recommendations.append("Great progress! You and the AI are growing together effectively")
    
    return MutualGrowthAnalysis(
        user_growth=user_growth,
        ai_performance=ai_performance,
        growth_trend=growth_trend,
        recommendations=recommendations
    )
