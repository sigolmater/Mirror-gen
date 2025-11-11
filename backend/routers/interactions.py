"""
User interaction tracking endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from datetime import datetime
import random

from database import get_db, Interaction, User
from schemas import InteractionCreate, InteractionResponse

router = APIRouter()

@router.post("/{user_id}", response_model=InteractionResponse)
async def create_interaction(
    user_id: int,
    interaction: InteractionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user interaction and generate AI response
    This is where the user-AI feedback loop begins
    """
    # Verify user exists
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Simulate AI response (in real implementation, this would call an AI model)
    ai_response = f"AI response to: {interaction.content}"
    response_quality = random.uniform(0.7, 1.0)  # Simulated quality score
    processing_time = random.uniform(0.1, 0.5)
    
    # Create interaction record
    db_interaction = Interaction(
        user_id=user_id,
        interaction_type=interaction.interaction_type,
        content=interaction.content,
        context=interaction.context,
        ai_response=ai_response,
        response_quality=response_quality,
        processing_time=processing_time
    )
    
    db.add(db_interaction)
    
    # Update user engagement score
    user.engagement_score = min(100.0, user.engagement_score + 1.0)
    
    await db.commit()
    await db.refresh(db_interaction)
    
    return db_interaction

@router.get("/{user_id}", response_model=List[InteractionResponse])
async def get_user_interactions(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get all interactions for a specific user"""
    result = await db.execute(
        select(Interaction)
        .where(Interaction.user_id == user_id)
        .order_by(Interaction.timestamp.desc())
        .offset(skip)
        .limit(limit)
    )
    interactions = result.scalars().all()
    return interactions

@router.get("/{user_id}/stats")
async def get_interaction_stats(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get interaction statistics for a user"""
    # Total interactions
    total_result = await db.execute(
        select(func.count(Interaction.id))
        .where(Interaction.user_id == user_id)
    )
    total_interactions = total_result.scalar()
    
    # Average response quality
    avg_quality_result = await db.execute(
        select(func.avg(Interaction.response_quality))
        .where(Interaction.user_id == user_id)
    )
    avg_quality = avg_quality_result.scalar() or 0.0
    
    # Interactions by type
    type_result = await db.execute(
        select(Interaction.interaction_type, func.count(Interaction.id))
        .where(Interaction.user_id == user_id)
        .group_by(Interaction.interaction_type)
    )
    interactions_by_type = {row[0]: row[1] for row in type_result.all()}
    
    return {
        "user_id": user_id,
        "total_interactions": total_interactions,
        "average_response_quality": float(avg_quality),
        "interactions_by_type": interactions_by_type
    }
