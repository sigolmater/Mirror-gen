"""
Simple Storage System for Personal AI Optimization System
Handles data persistence and retrieval for the Mirror-gen system
"""

import asyncio
import json
import logging
import os
import sqlite3
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
import pickle
import hashlib

logger = logging.getLogger(__name__)

class SimpleStorage:
    """
    Simple storage system for persisting system data
    
    Uses SQLite for structured data and file system for large objects
    Implements the storage requirements for the Mirror-gen philosophy
    """
    
    def __init__(self, db_path: str = "personal_ai_system.db"):
        self.db_path = db_path
        self.data_dir = Path("data")
        self.backup_dir = Path("backups")
        self.is_connected = False
        self.connection = None
        
    async def initialize(self):
        """Initialize the storage system"""
        logger.info("💾 Initializing Simple Storage System...")
        
        try:
            # Create directories
            self.data_dir.mkdir(exist_ok=True)
            self.backup_dir.mkdir(exist_ok=True)
            
            # Initialize database
            await self._init_database()
            
            # Start backup scheduler
            asyncio.create_task(self._backup_scheduler())
            
            self.is_connected = True
            logger.info("✅ Simple Storage System initialized")
            
        except Exception as e:
            logger.error(f"❌ Storage initialization failed: {e}")
            raise
    
    async def _init_database(self):
        """Initialize SQLite database with required tables"""
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        
        cursor = self.connection.cursor()
        
        # System configurations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                config_name TEXT UNIQUE NOT NULL,
                config_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Optimization history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS optimization_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                optimization_id TEXT UNIQUE NOT NULL,
                personas TEXT NOT NULL,
                configuration TEXT NOT NULL,
                results TEXT NOT NULL,
                quality_grade TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Warmup sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS warmup_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                warmup_id TEXT UNIQUE NOT NULL,
                parameters TEXT NOT NULL,
                results TEXT NOT NULL,
                duration REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Persona states table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS persona_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                persona_type TEXT NOT NULL,
                state_data TEXT NOT NULL,
                efficiency REAL NOT NULL,
                is_active BOOLEAN NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Mirror reflections table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mirror_reflections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                face_id INTEGER NOT NULL,
                persona_type TEXT,
                intensity REAL NOT NULL,
                frequency REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Quantum measurements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quantum_measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aspect TEXT NOT NULL,
                measured_state INTEGER NOT NULL,
                probability REAL NOT NULL,
                quantum_level INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Reflex actions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reflex_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_id TEXT NOT NULL,
                reflex_type TEXT NOT NULL,
                action_data TEXT NOT NULL,
                response_time REAL NOT NULL,
                status TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # System metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_type TEXT NOT NULL,
                metric_data TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.connection.commit()
        logger.info("📊 Database tables initialized")
    
    async def save_configuration(self, config_name: str, config_data: Dict[str, Any]) -> str:
        """Save system configuration"""
        if not self.is_connected:
            raise RuntimeError("Storage not initialized")
        
        config_json = json.dumps(config_data, default=str)
        
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO system_configs (config_name, config_data, updated_at)
            VALUES (?, ?, ?)
        """, (config_name, config_json, datetime.now()))
        
        self.connection.commit()
        
        logger.info(f"💾 Saved configuration: {config_name}")
        return config_name
    
    async def load_configuration(self, config_name: str) -> Optional[Dict[str, Any]]:
        """Load system configuration"""
        if not self.is_connected:
            raise RuntimeError("Storage not initialized")
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT config_data FROM system_configs WHERE config_name = ?
        """, (config_name,))
        
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
        return None
    
    async def save_optimization_result(self, optimization_data: Dict[str, Any]) -> str:
        """Save optimization results"""
        if not self.is_connected:
            raise RuntimeError("Storage not initialized")
        
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO optimization_history 
            (optimization_id, personas, configuration, results, quality_grade)
            VALUES (?, ?, ?, ?, ?)
        """, (
            optimization_data["optimization_id"],
            json.dumps(optimization_data.get("active_personas", [])),
            json.dumps(optimization_data.get("configuration", {})),
            json.dumps(optimization_data.get("final_metrics", {})),
            optimization_data.get("quality_grade", "GOOD")
        ))
        
        self.connection.commit()
        
        logger.info(f"💾 Saved optimization result: {optimization_data['optimization_id']}")
        return optimization_data["optimization_id"]
    
    async def get_optimization_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get optimization history"""
        if not self.is_connected:
            raise RuntimeError("Storage not initialized")
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT optimization_id, personas, configuration, results, quality_grade, created_at
            FROM optimization_history 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        
        history = []
        for row in rows:
            history.append({
                "optimization_id": row[0],
                "personas": json.loads(row[1]),
                "configuration": json.loads(row[2]),
                "results": json.loads(row[3]),
                "quality_grade": row[4],
                "created_at": row[5]
            })
        
        return history
    
    async def save_warmup_session(self, warmup_data: Dict[str, Any]) -> str:
        """Save warmup session data"""
        if not self.is_connected:
            raise RuntimeError("Storage not initialized")
        
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO warmup_sessions (warmup_id, parameters, results, duration)
            VALUES (?, ?, ?, ?)
        """, (
            warmup_data["warmup_id"],
            json.dumps(warmup_data.get("parameters", {})),
            json.dumps(warmup_data.get("simulation_results", {})),
            warmup_data.get("duration", 0)
        ))
        
        self.connection.commit()
        
        logger.info(f"💾 Saved warmup session: {warmup_data['warmup_id']}")
        return warmup_data["warmup_id"]
    
    async def save_persona_state(self, persona_type: str, state_data: Dict[str, Any]) -> str:
        """Save persona state"""
        if not self.is_connected:
            raise RuntimeError("Storage not initialized")
        
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO persona_states 
            (persona_type, state_data, efficiency, is_active, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            persona_type,
            json.dumps(state_data),
            state_data.get("efficiency", 0.0),
            state_data.get("is_active", False),
            datetime.now()
        ))
        
        self.connection.commit()
        return persona_type
    
    async def get_persona_states(self) -> List[Dict[str, Any]]:
        """Get all persona states"""
        if not self.is_connected:
            raise RuntimeError("Storage not initialized")
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT persona_type, state_data, efficiency, is_active, updated_at
            FROM persona_states
            ORDER BY updated_at DESC
        """)
        
        rows = cursor.fetchall()
        
        states = []
        for row in rows:
            states.append({
                "persona_type": row[0],
                "state_data": json.loads(row[1]),
                "efficiency": row[2],
                "is_active": row[3],
                "updated_at": row[4]
            })
        
        return states
    
    async def save_mirror_reflection(self, reflection_data: Dict[str, Any]) -> int:
        """Save mirror reflection data"""
        if not self.is_connected:
            raise RuntimeError("Storage not initialized")
        
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO mirror_reflections (face_id, persona_type, intensity, frequency)
            VALUES (?, ?, ?, ?)
        """, (
            reflection_data["face_id"],
            reflection_data.get("persona_type"),
            reflection_data["intensity"],
            reflection_data["frequency"]
        ))
        
        self.connection.commit()
        return cursor.lastrowid
    
    async def save_quantum_measurement(self, measurement_data: Dict[str, Any]) -> int:
        """Save quantum measurement data"""
        if not self.is_connected:
            raise RuntimeError("Storage not initialized")
        
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO quantum_measurements 
            (aspect, measured_state, probability, quantum_level)
            VALUES (?, ?, ?, ?)
        """, (
            measurement_data["aspect"],
            measurement_data["measured_state"],
            measurement_data["probability"],
            measurement_data["quantum_level"]
        ))
        
        self.connection.commit()
        return cursor.lastrowid
    
    async def save_reflex_action(self, reflex_data: Dict[str, Any]) -> int:
        """Save reflex action data"""
        if not self.is_connected:
            raise RuntimeError("Storage not initialized")
        
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO reflex_actions 
            (rule_id, reflex_type, action_data, response_time, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            reflex_data["rule_id"],
            reflex_data["reflex_type"],
            json.dumps(reflex_data.get("action_result", {})),
            reflex_data.get("response_time", 0.0),
            reflex_data.get("status", "unknown")
        ))
        
        self.connection.commit()
        return cursor.lastrowid
    
    async def save_system_metrics(self, metric_type: str, metric_data: Dict[str, Any]) -> int:
        """Save system metrics"""
        if not self.is_connected:
            raise RuntimeError("Storage not initialized")
        
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO system_metrics (metric_type, metric_data)
            VALUES (?, ?)
        """, (metric_type, json.dumps(metric_data, default=str)))
        
        self.connection.commit()
        return cursor.lastrowid
    
    async def get_system_metrics(self, metric_type: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get system metrics for the specified time period"""
        if not self.is_connected:
            raise RuntimeError("Storage not initialized")
        
        since = datetime.now() - timedelta(hours=hours)
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT metric_data, timestamp FROM system_metrics 
            WHERE metric_type = ? AND timestamp > ?
            ORDER BY timestamp DESC
        """, (metric_type, since))
        
        rows = cursor.fetchall()
        
        metrics = []
        for row in rows:
            metric_data = json.loads(row[0])
            metric_data["timestamp"] = row[1]
            metrics.append(metric_data)
        
        return metrics
    
    async def save_large_object(self, object_id: str, data: Any) -> str:
        """Save large object to file system"""
        file_path = self.data_dir / f"{object_id}.pkl"
        
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
        
        # Calculate and store hash for integrity
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        hash_path = self.data_dir / f"{object_id}.hash"
        with open(hash_path, 'w') as f:
            f.write(file_hash)
        
        logger.info(f"💾 Saved large object: {object_id}")
        return object_id
    
    async def load_large_object(self, object_id: str) -> Optional[Any]:
        """Load large object from file system"""
        file_path = self.data_dir / f"{object_id}.pkl"
        hash_path = self.data_dir / f"{object_id}.hash"
        
        if not file_path.exists():
            return None
        
        # Verify integrity if hash exists
        if hash_path.exists():
            with open(hash_path, 'r') as f:
                expected_hash = f.read().strip()
            
            with open(file_path, 'rb') as f:
                actual_hash = hashlib.sha256(f.read()).hexdigest()
            
            if expected_hash != actual_hash:
                logger.error(f"❌ Hash mismatch for object {object_id}")
                return None
        
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    
    async def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        if not self.is_connected:
            return {"status": "not_initialized"}
        
        cursor = self.connection.cursor()
        
        # Count records in each table
        tables = [
            "system_configs", "optimization_history", "warmup_sessions",
            "persona_states", "mirror_reflections", "quantum_measurements",
            "reflex_actions", "system_metrics"
        ]
        
        stats = {"tables": {}}
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            stats["tables"][table] = count
        
        # Database size
        db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
        stats["database_size_bytes"] = db_size
        stats["database_size_mb"] = round(db_size / (1024 * 1024), 2)
        
        # Data directory size
        data_size = sum(f.stat().st_size for f in self.data_dir.glob("*") if f.is_file())
        stats["data_directory_size_bytes"] = data_size
        stats["data_directory_size_mb"] = round(data_size / (1024 * 1024), 2)
        
        return stats
    
    async def _backup_scheduler(self):
        """Background task for regular backups"""
        while self.is_connected:
            try:
                await asyncio.sleep(3600)  # Wait 1 hour
                await self._create_backup()
            except Exception as e:
                logger.error(f"Backup scheduler error: {e}")
                await asyncio.sleep(3600)
    
    async def _create_backup(self):
        """Create system backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)
        
        try:
            # Backup database
            if os.path.exists(self.db_path):
                import shutil
                shutil.copy2(self.db_path, backup_path / "database.db")
            
            # Backup data directory
            if self.data_dir.exists():
                shutil.copytree(self.data_dir, backup_path / "data", dirs_exist_ok=True)
            
            logger.info(f"💾 Created backup: {backup_name}")
            
        except Exception as e:
            logger.error(f"❌ Backup creation failed: {e}")
    
    async def cleanup_old_data(self, days: int = 30):
        """Clean up old data"""
        if not self.is_connected:
            raise RuntimeError("Storage not initialized")
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        cursor = self.connection.cursor()
        
        # Clean up old records
        tables_with_timestamp = [
            "mirror_reflections", "quantum_measurements", 
            "reflex_actions", "system_metrics"
        ]
        
        total_cleaned = 0
        
        for table in tables_with_timestamp:
            cursor.execute(f"""
                DELETE FROM {table} WHERE timestamp < ?
            """, (cutoff_date,))
            
            cleaned = cursor.rowcount
            total_cleaned += cleaned
            
            logger.info(f"🧹 Cleaned {cleaned} records from {table}")
        
        self.connection.commit()
        
        logger.info(f"🧹 Total cleanup: {total_cleaned} records older than {days} days")
    
    async def close(self):
        """Close storage connections"""
        if self.connection:
            self.connection.close()
            self.connection = None
        
        self.is_connected = False
        logger.info("💾 Storage connections closed")