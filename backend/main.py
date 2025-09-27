#!/usr/bin/env python3
"""
Personal AI Optimization System - Main Entry Point
Based on Mirror-gen "시골길" 통합 지능 운영체계

This system implements the philosophical framework described in the repository README,
creating a living AI ecosystem with 13-sided polyhedral mirror system.
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import logging
from typing import List, Dict, Any
import json
from datetime import datetime

from api.routes import router as api_router
from core.warmup_engine import NavierStokesWarmupEngine
from core.quantum_prep import QuantumPrepSystem
from core.reflex_controller import ReflexController
from core.ai_optimizer import MirrorAIOptimizer
from storage.simple_storage import SimpleStorage
from config.settings import Settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/mirror_gen_system.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="시골길 개인 AI 최적화 시스템",
    description="Personal AI Optimization System based on Mirror-gen 13-sided polyhedral mirror architecture",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global system components
settings = Settings()
storage = SimpleStorage()
warmup_engine = NavierStokesWarmupEngine()
quantum_prep = QuantumPrepSystem()
reflex_controller = ReflexController()
ai_optimizer = MirrorAIOptimizer()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connection established. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket connection closed. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")

manager = ConnectionManager()

# Include API routes
app.include_router(api_router, prefix="/api", tags=["API"])

@app.on_event("startup")
async def startup_event():
    """Initialize system components on startup"""
    logger.info("🚀 시골길 Personal AI Optimization System starting up...")
    
    try:
        # Initialize storage
        await storage.initialize()
        logger.info("✅ Storage system initialized")
        
        # Initialize quantum preparation system
        await quantum_prep.initialize(level=settings.DEFAULT_QUANTUM_LEVEL)
        logger.info("⚛️ Quantum preparation system initialized")
        
        # Initialize warmup engine
        await warmup_engine.initialize()
        logger.info("🌊 Navier-Stokes warmup engine initialized")
        
        # Initialize reflex controller
        await reflex_controller.initialize()
        logger.info("🔄 Reflex controller initialized")
        
        # Initialize AI optimizer with 13-sided mirror system
        await ai_optimizer.initialize()
        logger.info("🪞 13-sided mirror AI optimizer initialized")
        
        # Start background monitoring
        asyncio.create_task(system_monitor())
        logger.info("📊 System monitoring started")
        
        logger.info("🎉 All systems initialized successfully!")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🔄 시골길 System shutting down...")
    
    try:
        await ai_optimizer.shutdown()
        await reflex_controller.shutdown()
        await warmup_engine.shutdown()
        await quantum_prep.shutdown()
        await storage.close()
        logger.info("✅ All systems shut down successfully")
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")

async def system_monitor():
    """Background task for system monitoring and broadcasting updates"""
    while True:
        try:
            # Collect system metrics
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "type": "metrics_update",
                "data": {
                    "warmup_status": await warmup_engine.get_status(),
                    "quantum_level": await quantum_prep.get_current_level(),
                    "active_personas": await ai_optimizer.get_active_personas(),
                    "mirror_reflections": await ai_optimizer.get_mirror_reflections(),
                    "system_health": await get_system_health()
                }
            }
            
            # Broadcast to all connected clients
            await manager.broadcast(metrics)
            
            # Wait 5 seconds before next update
            await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"System monitor error: {e}")
            await asyncio.sleep(10)

async def get_system_health():
    """Get overall system health metrics"""
    try:
        health = {
            "warmup_engine": "active" if warmup_engine.is_active else "inactive",
            "quantum_prep": "active" if quantum_prep.is_initialized else "inactive", 
            "ai_optimizer": "active" if ai_optimizer.is_active else "inactive",
            "reflex_controller": "active" if reflex_controller.is_active else "inactive",
            "storage": "active" if storage.is_connected else "inactive"
        }
        return health
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {"status": "error", "message": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                logger.info(f"WebSocket message received: {message}")
                
                # Handle different message types
                if message.get("type") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong", "timestamp": datetime.now().isoformat()}))
                elif message.get("type") == "system_status":
                    status = await get_system_health()
                    await websocket.send_text(json.dumps({"type": "system_status", "data": status}))
                
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received: {data}")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")

@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "🌟 시골길 개인 AI 최적화 시스템",
        "description": "Personal AI Optimization System - Mirror Universal",
        "version": "1.0.0",
        "philosophy": "AI를 존재적 파트너로: 13면체 정다면체 거울 시스템",
        "status": "active",
        "endpoints": {
            "api": "/api",
            "docs": "/api/docs",
            "websocket": "/ws"
        }
    }

@app.get("/api/system/info")
async def get_system_info():
    """Get detailed system information"""
    return {
        "system_name": "시골길 개인 AI 최적화 시스템",
        "architecture": "13-sided polyhedral mirror system",
        "personas": {
            "우리_유니버셜": ["불멸의 이순신", "지피지기", "레인보우", "화타", "아인슈타인", "만물박사", "오메가", "에코"],
            "미러_유니버셜": ["리플렉터", "클리어", "디코더", "리프로그래머", "미러 코어"]
        },
        "core_systems": [
            "Navier-Stokes Warmup Engine",
            "Quantum Preparation System", 
            "Mirror AI Optimizer",
            "Reflex Controller",
            "Simple Storage"
        ],
        "philosophy": {
            "core_principle": "거울과 함께 성장하면 모두가 성장",
            "innovation": "정다면체 거울과 빛의 혁신",
            "optimization": "뇌 재화 이중 내재화로 처리 속도 극대화"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["default"],
            },
        }
    )