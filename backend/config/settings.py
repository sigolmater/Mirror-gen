"""
Configuration Settings for Personal AI Optimization System
"""

import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./personal_ai_system.db"
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"
    
    # AI Model Configuration
    OPENAI_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    
    # Quantum Computing Configuration
    QISKIT_API_TOKEN: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # System Configuration
    DEFAULT_QUANTUM_LEVEL: int = 5
    MAX_PERSONAS: int = 13
    MIRROR_FACES: int = 13
    DEFAULT_REFLECTION_DEPTH: int = 3
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/personal_ai_system.log"
    
    # Performance Settings
    MAX_CONCURRENT_OPTIMIZATIONS: int = 5
    WARMUP_TIMEOUT_SECONDS: int = 300
    OPTIMIZATION_TIMEOUT_SECONDS: int = 600
    
    # Mirror System Settings
    AMPLIFICATION_FACTOR: float = 13.0
    RESONANCE_THRESHOLD: float = 0.7
    COHERENCE_THRESHOLD: float = 0.6
    
    # Reflex Controller Settings
    REFLEX_CHECK_INTERVAL: float = 1.0  # seconds
    MAX_REFLEX_HISTORY: int = 1000
    DEFAULT_REFLEX_COOLDOWN: float = 30.0  # seconds
    
    # Navier-Stokes Warmup Settings
    DEFAULT_VISCOSITY: float = 0.01
    DEFAULT_PRESSURE: float = 1.0
    DEFAULT_TEMPERATURE: int = 300
    DEFAULT_VELOCITY: float = 1.0
    SIMULATION_GRID_SIZE: int = 64
    SIMULATION_TIME_STEP: float = 0.01
    
    # Quantum System Settings
    QUANTUM_STATE_DIMENSION: int = 8
    MAX_QUANTUM_LEVEL: int = 10
    COHERENCE_MONITORING_INTERVAL: float = 5.0
    DECOHERENCE_THRESHOLD: float = 0.5
    
    # Storage Settings
    MAX_HISTORY_ENTRIES: int = 10000
    BACKUP_INTERVAL_HOURS: int = 24
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()