"""
API Models for Personal AI Optimization System
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

# Enums for validation
class OptimizationMode(str, Enum):
    BALANCED = "balanced"
    PERFORMANCE = "performance"
    CREATIVITY = "creativity"
    STABILITY = "stability"

class PersonaType(str, Enum):
    SUN_SHIN = "sun-shin"
    KNOW_ENEMY = "know-enemy"
    RAINBOW = "rainbow"
    HWATA = "hwata"
    EINSTEIN = "einstein"
    OMNISCIENT = "omniscient"
    OMEGA = "omega"
    ECHO = "echo"

class QualityGrade(str, Enum):
    GOOD = "GOOD"
    EXCELLENT = "EXCELLENT"
    UNBELIEVABLE = "UNBELIEVABLE"

# Request Models
class WarmupRequest(BaseModel):
    """Request model for Navier-Stokes warmup"""
    viscosity: float = Field(default=0.01, ge=0.001, le=0.1, description="Fluid viscosity (0.001-0.1)")
    pressure: float = Field(default=1.0, ge=0.1, le=5.0, description="System pressure (0.1-5.0)")
    temperature: int = Field(default=300, ge=200, le=500, description="Temperature in Kelvin (200-500)")
    velocity: float = Field(default=1.0, ge=0.1, le=10.0, description="Flow velocity (0.1-10.0)")

class OptimizationRequest(BaseModel):
    """Request model for AI optimization"""
    personas: List[PersonaType] = Field(description="List of personas to activate")
    mode: OptimizationMode = Field(default=OptimizationMode.BALANCED, description="Optimization mode")
    quantum_level: int = Field(default=5, ge=1, le=10, description="Quantum preparation level (1-10)")
    mirror_depth: int = Field(default=3, ge=1, le=7, description="Mirror reflection depth (1-7)")

class QuantumInitRequest(BaseModel):
    """Request model for quantum initialization"""
    level: int = Field(ge=1, le=10, description="Quantum level (1-10)")

class PersonaActivationRequest(BaseModel):
    """Request model for persona activation"""
    persona_id: PersonaType = Field(description="Persona type to activate")

class ReflexTriggerRequest(BaseModel):
    """Request model for manual reflex trigger"""
    reflex_type: str = Field(description="Type of reflex to trigger")
    data: Dict[str, Any] = Field(default_factory=dict, description="Additional data for reflex")

class ConfigurationSaveRequest(BaseModel):
    """Request model for saving configuration"""
    config_name: str = Field(description="Configuration name")
    config_data: Dict[str, Any] = Field(description="Configuration data")

# Response Models
class SystemStatusResponse(BaseModel):
    """Response model for system status"""
    status: str
    timestamp: datetime
    components: Dict[str, str]

class WarmupResponse(BaseModel):
    """Response model for warmup results"""
    status: str
    warmup_id: str
    parameters: Dict[str, Any]
    results: Dict[str, Any]
    timestamp: datetime

class OptimizationResponse(BaseModel):
    """Response model for optimization results"""
    optimization_id: str
    status: str
    activated_personas: int
    mirror_depth: int
    optimization_mode: str
    optimization_results: Dict[str, Any]
    final_metrics: Dict[str, Any]
    quality_grade: QualityGrade
    timestamp: datetime

class PersonaResponse(BaseModel):
    """Response model for persona information"""
    id: str
    name: str
    status: str
    efficiency: float
    specialization: str
    mirror_face: Optional[int] = None

class ActivePersonasResponse(BaseModel):
    """Response model for active personas list"""
    active_personas: List[PersonaResponse]
    total_active: int
    synchronization_level: str

class QuantumStatusResponse(BaseModel):
    """Response model for quantum system status"""
    initialized: bool
    current_level: int
    coherence: str
    entanglement_strength: str
    quantum_gates: int
    superposition_states: int

class MirrorStatusResponse(BaseModel):
    """Response model for mirror system status"""
    status: str
    mirror_type: str
    reflection_quality: QualityGrade
    active_faces: int
    total_reflections: int
    last_calibration: datetime

class MetricsResponse(BaseModel):
    """Response model for system metrics"""
    timestamp: datetime
    performance: Dict[str, float]
    system_load: Dict[str, float]
    ai_metrics: Dict[str, Any]

class DiagnosticsResponse(BaseModel):
    """Response model for system diagnostics"""
    status: str
    diagnostics_id: str
    results: Dict[str, Dict[str, Any]]
    overall_health: QualityGrade
    recommendations: List[str]
    timestamp: datetime

class StorageStatsResponse(BaseModel):
    """Response model for storage statistics"""
    tables: Dict[str, int]
    database_size_mb: float
    data_directory_size_mb: float

# Complex nested models
class CognitiveMetrics(BaseModel):
    """Model for cognitive optimization metrics"""
    processing_speed: float = Field(description="Processing speed percentage")
    creative_turbulence: float = Field(description="Creative turbulence level")
    decision_stability: float = Field(description="Decision stability percentage")
    learning_efficiency: float = Field(description="Learning efficiency percentage")
    overall_cognitive_score: float = Field(description="Overall cognitive score")

class SimulationResults(BaseModel):
    """Model for Navier-Stokes simulation results"""
    reynolds_number: float
    kinetic_energy: float
    max_vorticity: float
    convergence_rate: float
    final_pressure_variance: float
    computation_time: float
    iterations: int
    grid_resolution: int

class PersonaState(BaseModel):
    """Model for persona state information"""
    persona_type: PersonaType
    is_active: bool
    efficiency: float
    specialization: str
    current_task: Optional[str]
    mirror_face_id: Optional[int]
    activation_time: Optional[datetime]
    performance_metrics: Dict[str, float]

class MirrorFaceInfo(BaseModel):
    """Model for mirror face information"""
    face_id: int
    normal_vector: List[float]
    reflection_coefficient: float
    resonance_frequency: float
    active_persona: Optional[PersonaType]
    last_reflection: Optional[datetime]

class ReflexActionInfo(BaseModel):
    """Model for reflex action information"""
    timestamp: datetime
    rule_id: str
    reflex_type: str
    priority: int
    response_time: float
    action_result: Dict[str, Any]
    status: str

class OptimizationHistory(BaseModel):
    """Model for optimization history entry"""
    optimization_id: str
    personas: List[PersonaType]
    configuration: Dict[str, Any]
    results: Dict[str, Any]
    quality_grade: QualityGrade
    created_at: datetime

# Error models
class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

# Success models
class SuccessResponse(BaseModel):
    """Standard success response model"""
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)

# Health check model
class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    version: str
    uptime: str
    components: Dict[str, str]
    timestamp: datetime = Field(default_factory=datetime.now)

# WebSocket message models
class WebSocketMessage(BaseModel):
    """WebSocket message model"""
    type: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class MetricsUpdate(BaseModel):
    """Real-time metrics update model"""
    type: str = "metrics_update"
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)

class SystemAlert(BaseModel):
    """System alert model"""
    type: str = "system_alert"
    level: str  # info, warning, error, critical
    message: str
    component: str
    timestamp: datetime = Field(default_factory=datetime.now)

class PersonaUpdate(BaseModel):
    """Persona status update model"""
    type: str = "persona_update"
    persona_id: PersonaType
    status: str
    efficiency: float
    timestamp: datetime = Field(default_factory=datetime.now)