#!/usr/bin/env python3
"""
Integration test script for Mirror-gen User-AI Growth System
Tests all major API endpoints and verifies the virtuous cycle functionality
"""

import requests
import time
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api"
COLORS = {
    'green': '\033[92m',
    'red': '\033[91m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'reset': '\033[0m'
}

def print_color(message: str, color: str = 'reset'):
    """Print colored message"""
    print(f"{COLORS.get(color, '')}{message}{COLORS['reset']}")

def test_health_check():
    """Test health check endpoint"""
    print_color("\n🔍 Testing Health Check...", 'blue')
    try:
        response = requests.get("http://localhost:8000/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        print_color("✓ Health check passed", 'green')
        return True
    except Exception as e:
        print_color(f"✗ Health check failed: {e}", 'red')
        return False

def test_create_user():
    """Test user creation"""
    print_color("\n🔍 Testing User Creation...", 'blue')
    try:
        user_data = {
            "username": f"test_user_{int(time.time())}",
            "email": f"test_{int(time.time())}@example.com"
        }
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        assert response.status_code == 200
        user = response.json()
        assert "id" in user
        assert user["username"] == user_data["username"]
        print_color(f"✓ User created: {user['username']} (ID: {user['id']})", 'green')
        return user
    except Exception as e:
        print_color(f"✗ User creation failed: {e}", 'red')
        return None

def test_list_users():
    """Test listing users"""
    print_color("\n🔍 Testing List Users...", 'blue')
    try:
        response = requests.get(f"{BASE_URL}/users/")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        print_color(f"✓ Listed {len(users)} users", 'green')
        return True
    except Exception as e:
        print_color(f"✗ List users failed: {e}", 'red')
        return False

def test_create_interaction(user_id: int):
    """Test interaction creation"""
    print_color("\n🔍 Testing Interaction Creation...", 'blue')
    try:
        interaction_data = {
            "interaction_type": "query",
            "content": "How can I improve my skills with AI and machine learning?",
            "context": {"source": "test_script", "version": "1.0"}
        }
        response = requests.post(
            f"{BASE_URL}/interactions/{user_id}",
            json=interaction_data
        )
        assert response.status_code == 200
        interaction = response.json()
        assert "id" in interaction
        assert "ai_response" in interaction
        assert interaction["user_id"] == user_id
        print_color(f"✓ Interaction created (ID: {interaction['id']})", 'green')
        print_color(f"  AI Response: {interaction['ai_response'][:50]}...", 'yellow')
        return interaction
    except Exception as e:
        print_color(f"✗ Interaction creation failed: {e}", 'red')
        return None

def test_interaction_stats(user_id: int):
    """Test interaction statistics"""
    print_color("\n🔍 Testing Interaction Statistics...", 'blue')
    try:
        response = requests.get(f"{BASE_URL}/interactions/{user_id}/stats")
        assert response.status_code == 200
        stats = response.json()
        assert "total_interactions" in stats
        print_color(f"✓ Stats retrieved: {stats['total_interactions']} interactions", 'green')
        return stats
    except Exception as e:
        print_color(f"✗ Stats retrieval failed: {e}", 'red')
        return None

def test_submit_feedback(user_id: int, interaction_id: int):
    """Test feedback submission"""
    print_color("\n🔍 Testing Feedback Submission...", 'blue')
    try:
        feedback_data = {
            "interaction_id": interaction_id,
            "feedback_type": "positive",
            "rating": 5,
            "comment": "Excellent response! Very helpful and detailed."
        }
        response = requests.post(
            f"{BASE_URL}/feedback/{user_id}",
            json=feedback_data
        )
        assert response.status_code == 200
        feedback = response.json()
        assert "id" in feedback
        assert feedback["rating"] == 5
        print_color(f"✓ Feedback submitted (ID: {feedback['id']})", 'green')
        return feedback
    except Exception as e:
        print_color(f"✗ Feedback submission failed: {e}", 'red')
        return None

def test_feedback_summary():
    """Test feedback summary"""
    print_color("\n🔍 Testing Feedback Summary...", 'blue')
    try:
        response = requests.get(f"{BASE_URL}/feedback/analytics/summary")
        assert response.status_code == 200
        summary = response.json()
        assert "total_feedback" in summary
        print_color(f"✓ Feedback summary: {summary['total_feedback']} total", 'green')
        return summary
    except Exception as e:
        print_color(f"✗ Feedback summary failed: {e}", 'red')
        return None

def test_user_growth(user_id: int):
    """Test user growth metrics"""
    print_color("\n🔍 Testing User Growth Metrics...", 'blue')
    try:
        response = requests.get(f"{BASE_URL}/analytics/user/{user_id}/growth")
        assert response.status_code == 200
        growth = response.json()
        assert "skill_level" in growth
        assert "engagement_score" in growth
        print_color(f"✓ Growth metrics retrieved", 'green')
        print_color(f"  Skill Level: {growth['skill_level']}", 'yellow')
        print_color(f"  Engagement: {growth['engagement_score']}", 'yellow')
        print_color(f"  Learning Progress: {growth['learning_progress']}", 'yellow')
        return growth
    except Exception as e:
        print_color(f"✗ Growth metrics failed: {e}", 'red')
        return None

def test_ai_performance():
    """Test AI performance metrics"""
    print_color("\n🔍 Testing AI Performance Metrics...", 'blue')
    try:
        response = requests.get(f"{BASE_URL}/analytics/ai/performance")
        assert response.status_code == 200
        perf = response.json()
        assert "total_interactions" in perf
        assert "avg_user_satisfaction" in perf
        print_color(f"✓ AI performance retrieved", 'green')
        print_color(f"  Total Interactions: {perf['total_interactions']}", 'yellow')
        print_color(f"  Avg Response Time: {perf['avg_response_time']:.2f}s", 'yellow')
        print_color(f"  User Satisfaction: {perf['avg_user_satisfaction']:.1f}/5.0", 'yellow')
        return perf
    except Exception as e:
        print_color(f"✗ AI performance failed: {e}", 'red')
        return None

def test_mutual_growth(user_id: int):
    """Test mutual growth analysis"""
    print_color("\n🔍 Testing Mutual Growth Analysis...", 'blue')
    try:
        response = requests.get(f"{BASE_URL}/analytics/mutual-growth/{user_id}")
        assert response.status_code == 200
        analysis = response.json()
        assert "user_growth" in analysis
        assert "ai_performance" in analysis
        assert "recommendations" in analysis
        print_color(f"✓ Mutual growth analysis complete", 'green')
        print_color(f"  Recommendations:", 'yellow')
        for rec in analysis["recommendations"]:
            print_color(f"    - {rec}", 'yellow')
        return analysis
    except Exception as e:
        print_color(f"✗ Mutual growth analysis failed: {e}", 'red')
        return None

def test_growth_snapshot(user_id: int):
    """Test growth snapshot creation"""
    print_color("\n🔍 Testing Growth Snapshot...", 'blue')
    try:
        response = requests.post(f"{BASE_URL}/analytics/user/{user_id}/snapshot")
        assert response.status_code == 200
        result = response.json()
        assert "snapshot_id" in result
        print_color(f"✓ Growth snapshot created (ID: {result['snapshot_id']})", 'green')
        return result
    except Exception as e:
        print_color(f"✗ Growth snapshot failed: {e}", 'red')
        return None

def run_all_tests():
    """Run all integration tests"""
    print_color("\n" + "="*60, 'blue')
    print_color("🪞 Mirror-gen Integration Tests", 'blue')
    print_color("="*60, 'blue')
    
    # Health check
    if not test_health_check():
        print_color("\n❌ Backend is not running. Please start it first.", 'red')
        return False
    
    # User tests
    user = test_create_user()
    if not user:
        return False
    
    test_list_users()
    
    # Interaction tests
    interaction = test_create_interaction(user["id"])
    if not interaction:
        return False
    
    test_interaction_stats(user["id"])
    
    # Feedback tests
    feedback = test_submit_feedback(user["id"], interaction["id"])
    if not feedback:
        return False
    
    test_feedback_summary()
    
    # Analytics tests
    test_user_growth(user["id"])
    test_ai_performance()
    test_mutual_growth(user["id"])
    test_growth_snapshot(user["id"])
    
    print_color("\n" + "="*60, 'blue')
    print_color("✅ All tests completed successfully!", 'green')
    print_color("="*60, 'blue')
    
    print_color("\n📊 Test Summary:", 'blue')
    print_color(f"  User ID: {user['id']}", 'yellow')
    print_color(f"  Interaction ID: {interaction['id']}", 'yellow')
    print_color(f"  Feedback ID: {feedback['id']}", 'yellow')
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
