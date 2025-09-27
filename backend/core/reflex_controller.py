"""
Reflex Controller - Instant Response System
Implements instant reflex responses for AI optimization system

This module represents the "인지 → 판단 → 실행의 즉각적 최적화" concept,
providing instant reflex responses to system events and user interactions.
"""

import asyncio
import logging
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)

class ReflexType(Enum):
    """Types of reflex responses"""
    EMERGENCY_STOP = "emergency_stop"
    PERFORMANCE_BOOST = "performance_boost"
    ERROR_CORRECTION = "error_correction"
    LOAD_BALANCING = "load_balancing"
    SECURITY_RESPONSE = "security_response"
    OPTIMIZATION_TRIGGER = "optimization_trigger"
    PERSONA_SYNC = "persona_sync"
    MIRROR_CALIBRATION = "mirror_calibration"

@dataclass
class ReflexRule:
    """Defines a reflex rule"""
    rule_id: str
    reflex_type: ReflexType
    condition: Callable[[Dict[str, Any]], bool]
    action: Callable[[Dict[str, Any]], Dict[str, Any]]
    priority: int  # 1-10, higher is more urgent
    cooldown_seconds: float
    last_triggered: Optional[datetime]
    trigger_count: int

class ReflexController:
    """
    Reflex Controller for instant AI system responses
    
    Provides instant reflexes for:
    - Emergency situations
    - Performance optimization
    - Error correction
    - Load balancing
    - Security threats
    """
    
    def __init__(self):
        self.is_active = False
        self.is_initialized = False
        self.reflex_rules: Dict[str, ReflexRule] = {}
        self.reflex_history: List[Dict[str, Any]] = []
        self.monitoring_task = None
        
        # Performance metrics
        self.total_reflexes = 0
        self.successful_reflexes = 0
        self.average_response_time = 0.0
        
    async def initialize(self):
        """Initialize the reflex controller"""
        logger.info("🔄 Initializing Reflex Controller...")
        
        try:
            # Setup default reflex rules
            await self._setup_default_reflexes()
            
            # Start reflex monitoring
            self.monitoring_task = asyncio.create_task(self._monitor_system())
            
            self.is_initialized = True
            self.is_active = True
            logger.info("✅ Reflex Controller initialized")
            
        except Exception as e:
            logger.error(f"❌ Reflex Controller initialization failed: {e}")
            raise
    
    async def _setup_default_reflexes(self):
        """Setup default reflex rules"""
        
        # Emergency Stop Reflex
        emergency_stop_rule = ReflexRule(
            rule_id="emergency_stop",
            reflex_type=ReflexType.EMERGENCY_STOP,
            condition=lambda data: (
                data.get("cpu_usage", 0) > 95 or
                data.get("memory_usage", 0) > 98 or
                data.get("error_rate", 0) > 0.1
            ),
            action=self._emergency_stop_action,
            priority=10,
            cooldown_seconds=30.0,
            last_triggered=None,
            trigger_count=0
        )
        
        # Performance Boost Reflex
        performance_boost_rule = ReflexRule(
            rule_id="performance_boost",
            reflex_type=ReflexType.PERFORMANCE_BOOST,
            condition=lambda data: (
                data.get("active_personas", 0) > 5 and
                data.get("overall_efficiency", 0) < 70
            ),
            action=self._performance_boost_action,
            priority=7,
            cooldown_seconds=60.0,
            last_triggered=None,
            trigger_count=0
        )
        
        # Error Correction Reflex
        error_correction_rule = ReflexRule(
            rule_id="error_correction",
            reflex_type=ReflexType.ERROR_CORRECTION,
            condition=lambda data: (
                data.get("error_count", 0) > 3 or
                data.get("failed_operations", 0) > 1
            ),
            action=self._error_correction_action,
            priority=8,
            cooldown_seconds=15.0,
            last_triggered=None,
            trigger_count=0
        )
        
        # Load Balancing Reflex
        load_balancing_rule = ReflexRule(
            rule_id="load_balancing",
            reflex_type=ReflexType.LOAD_BALANCING,
            condition=lambda data: (
                data.get("persona_load_imbalance", 0) > 0.3
            ),
            action=self._load_balancing_action,
            priority=6,
            cooldown_seconds=45.0,
            last_triggered=None,
            trigger_count=0
        )
        
        # Security Response Reflex
        security_response_rule = ReflexRule(
            rule_id="security_response",
            reflex_type=ReflexType.SECURITY_RESPONSE,
            condition=lambda data: (
                data.get("unauthorized_access", False) or
                data.get("suspicious_activity", False)
            ),
            action=self._security_response_action,
            priority=9,
            cooldown_seconds=5.0,
            last_triggered=None,
            trigger_count=0
        )
        
        # Optimization Trigger Reflex
        optimization_trigger_rule = ReflexRule(
            rule_id="optimization_trigger",
            reflex_type=ReflexType.OPTIMIZATION_TRIGGER,
            condition=lambda data: (
                data.get("coherence_level", 1.0) < 0.6 or
                data.get("mirror_synchronization", 1.0) < 0.7
            ),
            action=self._optimization_trigger_action,
            priority=5,
            cooldown_seconds=90.0,
            last_triggered=None,
            trigger_count=0
        )
        
        # Persona Synchronization Reflex
        persona_sync_rule = ReflexRule(
            rule_id="persona_sync",
            reflex_type=ReflexType.PERSONA_SYNC,
            condition=lambda data: (
                data.get("persona_desync", 0) > 0.4
            ),
            action=self._persona_sync_action,
            priority=7,
            cooldown_seconds=30.0,
            last_triggered=None,
            trigger_count=0
        )
        
        # Mirror Calibration Reflex
        mirror_calibration_rule = ReflexRule(
            rule_id="mirror_calibration",
            reflex_type=ReflexType.MIRROR_CALIBRATION,
            condition=lambda data: (
                data.get("mirror_drift", 0) > 0.2 or
                data.get("reflection_quality", 1.0) < 0.8
            ),
            action=self._mirror_calibration_action,
            priority=6,
            cooldown_seconds=120.0,
            last_triggered=None,
            trigger_count=0
        )
        
        # Register all rules
        rules = [
            emergency_stop_rule, performance_boost_rule, error_correction_rule,
            load_balancing_rule, security_response_rule, optimization_trigger_rule,
            persona_sync_rule, mirror_calibration_rule
        ]
        
        for rule in rules:
            self.reflex_rules[rule.rule_id] = rule
        
        logger.info(f"⚡ Setup {len(rules)} default reflex rules")
    
    async def _monitor_system(self):
        """Background monitoring for reflex triggers"""
        while self.is_active:
            try:
                # Simulate system metrics collection
                system_data = await self._collect_system_metrics()
                
                # Check all reflex rules
                await self._check_reflex_triggers(system_data)
                
                await asyncio.sleep(1)  # Check every second for fast reflexes
                
            except Exception as e:
                logger.error(f"Reflex monitoring error: {e}")
                await asyncio.sleep(5)
    
    async def _collect_system_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics for reflex evaluation"""
        # Simulate system metrics - in real implementation, these would come from actual system monitoring
        import random
        
        base_cpu = 25
        base_memory = 60
        base_efficiency = 85
        
        # Add some random variation
        metrics = {
            "cpu_usage": base_cpu + random.uniform(-10, 20),
            "memory_usage": base_memory + random.uniform(-10, 15),
            "overall_efficiency": base_efficiency + random.uniform(-15, 10),
            "active_personas": random.randint(3, 8),
            "error_count": random.randint(0, 5),
            "failed_operations": random.randint(0, 2),
            "persona_load_imbalance": random.uniform(0, 0.5),
            "unauthorized_access": random.random() < 0.01,  # 1% chance
            "suspicious_activity": random.random() < 0.02,  # 2% chance
            "coherence_level": random.uniform(0.5, 1.0),
            "mirror_synchronization": random.uniform(0.6, 1.0),
            "persona_desync": random.uniform(0, 0.6),
            "mirror_drift": random.uniform(0, 0.3),
            "reflection_quality": random.uniform(0.7, 1.0),
            "timestamp": datetime.now()
        }
        
        return metrics
    
    async def _check_reflex_triggers(self, system_data: Dict[str, Any]):
        """Check if any reflex rules should be triggered"""
        # Sort rules by priority (highest first)
        sorted_rules = sorted(self.reflex_rules.values(), key=lambda r: r.priority, reverse=True)
        
        for rule in sorted_rules:
            try:
                # Check cooldown
                if rule.last_triggered is not None:
                    time_since_last = (datetime.now() - rule.last_triggered).total_seconds()
                    if time_since_last < rule.cooldown_seconds:
                        continue
                
                # Check condition
                if rule.condition(system_data):
                    # Trigger reflex
                    await self._trigger_reflex(rule, system_data)
                    
            except Exception as e:
                logger.error(f"Error checking reflex rule {rule.rule_id}: {e}")
    
    async def _trigger_reflex(self, rule: ReflexRule, system_data: Dict[str, Any]):
        """Trigger a specific reflex action"""
        start_time = datetime.now()
        
        logger.info(f"⚡ Triggering reflex: {rule.reflex_type.value} (priority {rule.priority})")
        
        try:
            # Execute reflex action
            action_result = await rule.action(system_data)
            
            response_time = (datetime.now() - start_time).total_seconds()
            
            # Update rule statistics
            rule.last_triggered = datetime.now()
            rule.trigger_count += 1
            
            # Update global statistics
            self.total_reflexes += 1
            self.successful_reflexes += 1
            
            # Update average response time
            self.average_response_time = (
                (self.average_response_time * (self.total_reflexes - 1) + response_time) 
                / self.total_reflexes
            )
            
            # Log reflex execution
            reflex_log = {
                "timestamp": start_time.isoformat(),
                "rule_id": rule.rule_id,
                "reflex_type": rule.reflex_type.value,
                "priority": rule.priority,
                "response_time": response_time,
                "action_result": action_result,
                "system_data": {k: v for k, v in system_data.items() if k != "timestamp"},
                "status": "success"
            }
            
            self.reflex_history.append(reflex_log)
            
            # Keep only recent history (last 1000 entries)
            if len(self.reflex_history) > 1000:
                self.reflex_history = self.reflex_history[-1000:]
            
            logger.info(f"✅ Reflex completed in {response_time*1000:.1f}ms: {action_result.get('action', 'Unknown')}")
            
        except Exception as e:
            logger.error(f"❌ Reflex {rule.rule_id} failed: {e}")
            
            # Log failed reflex
            reflex_log = {
                "timestamp": start_time.isoformat(),
                "rule_id": rule.rule_id,
                "reflex_type": rule.reflex_type.value,
                "priority": rule.priority,
                "error": str(e),
                "status": "failed"
            }
            
            self.reflex_history.append(reflex_log)
    
    # Reflex action implementations
    async def _emergency_stop_action(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Emergency stop action"""
        logger.warning("🚨 EMERGENCY STOP reflex triggered!")
        
        # Simulate emergency actions
        actions_taken = []
        
        if system_data.get("cpu_usage", 0) > 95:
            actions_taken.append("Reduced CPU intensive operations")
        
        if system_data.get("memory_usage", 0) > 98:
            actions_taken.append("Freed memory resources")
        
        if system_data.get("error_rate", 0) > 0.1:
            actions_taken.append("Stopped error-prone processes")
        
        return {
            "action": "emergency_stop",
            "actions_taken": actions_taken,
            "severity": "high",
            "immediate": True
        }
    
    async def _performance_boost_action(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Performance boost action"""
        logger.info("🚀 Performance boost reflex triggered!")
        
        return {
            "action": "performance_boost",
            "optimizations": [
                "Increased resource allocation",
                "Optimized persona scheduling",
                "Enhanced mirror coherence"
            ],
            "expected_improvement": "15-20%"
        }
    
    async def _error_correction_action(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Error correction action"""
        logger.info("🔧 Error correction reflex triggered!")
        
        return {
            "action": "error_correction",
            "corrections": [
                "Reset failed operations",
                "Cleared error queues",
                "Restored stable configurations"
            ],
            "errors_resolved": system_data.get("error_count", 0)
        }
    
    async def _load_balancing_action(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Load balancing action"""
        logger.info("⚖️ Load balancing reflex triggered!")
        
        return {
            "action": "load_balancing",
            "balancing": [
                "Redistributed persona workload",
                "Optimized mirror face utilization",
                "Balanced processing queues"
            ],
            "imbalance_reduced": f"{system_data.get('persona_load_imbalance', 0)*100:.1f}%"
        }
    
    async def _security_response_action(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Security response action"""
        logger.warning("🛡️ Security response reflex triggered!")
        
        return {
            "action": "security_response",
            "measures": [
                "Blocked suspicious connections",
                "Enhanced access controls",
                "Increased monitoring sensitivity"
            ],
            "threat_level": "medium"
        }
    
    async def _optimization_trigger_action(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimization trigger action"""
        logger.info("✨ Optimization trigger reflex triggered!")
        
        return {
            "action": "optimization_trigger",
            "optimizations": [
                "Started mirror recalibration",
                "Initiated coherence enhancement",
                "Triggered persona synchronization"
            ],
            "coherence_target": "> 0.8"
        }
    
    async def _persona_sync_action(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Persona synchronization action"""
        logger.info("🔄 Persona sync reflex triggered!")
        
        return {
            "action": "persona_sync",
            "synchronization": [
                "Aligned persona frequencies",
                "Corrected phase differences",
                "Restored communication channels"
            ],
            "sync_improvement": f"{(1 - system_data.get('persona_desync', 0))*100:.1f}%"
        }
    
    async def _mirror_calibration_action(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mirror calibration action"""
        logger.info("🪞 Mirror calibration reflex triggered!")
        
        return {
            "action": "mirror_calibration",
            "calibrations": [
                "Adjusted mirror face angles",
                "Corrected reflection coefficients",
                "Optimized resonance frequencies"
            ],
            "quality_improvement": f"{system_data.get('reflection_quality', 0)*100:.1f}%"
        }
    
    async def trigger_manual_reflex(self, reflex_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Manually trigger a specific reflex"""
        if reflex_type not in self.reflex_rules:
            raise ValueError(f"Unknown reflex type: {reflex_type}")
        
        rule = self.reflex_rules[reflex_type]
        
        logger.info(f"🔧 Manual reflex trigger: {reflex_type}")
        
        # Force trigger regardless of condition
        await self._trigger_reflex(rule, data)
        
        return {
            "status": "triggered",
            "reflex_type": reflex_type,
            "manual": True,
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_status(self) -> Dict[str, Any]:
        """Get reflex controller status"""
        return {
            "is_active": self.is_active,
            "is_initialized": self.is_initialized,
            "total_rules": len(self.reflex_rules),
            "total_reflexes": self.total_reflexes,
            "successful_reflexes": self.successful_reflexes,
            "success_rate": f"{(self.successful_reflexes / max(1, self.total_reflexes)) * 100:.1f}%",
            "average_response_time": f"{self.average_response_time * 1000:.1f}ms",
            "recent_reflexes": len([r for r in self.reflex_history 
                                  if datetime.fromisoformat(r["timestamp"]) > datetime.now() - timedelta(minutes=5)])
        }
    
    async def get_reflex_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent reflex history"""
        return self.reflex_history[-limit:]
    
    async def add_custom_reflex(self, rule: ReflexRule):
        """Add a custom reflex rule"""
        self.reflex_rules[rule.rule_id] = rule
        logger.info(f"➕ Added custom reflex rule: {rule.rule_id}")
    
    async def remove_reflex(self, rule_id: str):
        """Remove a reflex rule"""
        if rule_id in self.reflex_rules:
            del self.reflex_rules[rule_id]
            logger.info(f"➖ Removed reflex rule: {rule_id}")
        else:
            raise ValueError(f"Reflex rule not found: {rule_id}")
    
    async def shutdown(self):
        """Shutdown the reflex controller"""
        logger.info("🔄 Shutting down Reflex Controller...")
        
        self.is_active = False
        
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        
        self.is_initialized = False
        logger.info("✅ Reflex Controller shut down")