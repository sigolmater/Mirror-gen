# API Reference - Personal AI Optimization System
# API 참조 문서 - 시골길 개인 AI 최적화 시스템

## Base URL / 기본 URL
```
Development: http://localhost:8000
Production: https://your-domain.com
```

## Authentication / 인증
Currently, the system operates without authentication in development mode. For production deployment, implement JWT token-based authentication.

## Error Handling / 오류 처리

All API endpoints return errors in the following format:
```json
{
  "error": "Error type",
  "detail": "Detailed error message",
  "timestamp": "2024-01-15T14:32:18.123456"
}
```

Common HTTP status codes:
- `200` - Success / 성공
- `201` - Created / 생성됨
- `400` - Bad Request / 잘못된 요청
- `404` - Not Found / 찾을 수 없음
- `500` - Internal Server Error / 내부 서버 오류

## System Endpoints / 시스템 엔드포인트

### Get System Status / 시스템 상태 조회
```http
GET /api/system/status
```

**Response:**
```json
{
  "status": "active",
  "timestamp": "2024-01-15T14:32:18.123456",
  "components": {
    "warmup_engine": "active",
    "quantum_prep": "active",
    "ai_optimizer": "active",
    "reflex_controller": "active",
    "storage": "active"
  }
}
```

### Get System Health / 시스템 건강 상태 조회
```http
GET /api/system/health
```

**Response:**
```json
{
  "overall_health": "good",
  "uptime": "7d 14h 32m",
  "memory_usage": "67%",
  "cpu_usage": "23%",
  "active_processes": 8,
  "error_count": 0
}
```

### Get System Information / 시스템 정보 조회
```http
GET /api/system/info
```

**Response:**
```json
{
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
  ]
}
```

## Navier-Stokes Warmup Endpoints / 나비에-스토크스 웜업 엔드포인트

### Start Navier-Stokes Warmup / 나비에-스토크스 웜업 시작
```http
POST /api/warmup/navier-stokes
Content-Type: application/json
```

**Request Body:**
```json
{
  "viscosity": 0.01,
  "pressure": 1.0,
  "temperature": 300,
  "velocity": 1.0
}
```

**Parameters:**
- `viscosity` (float): Fluid viscosity (0.001-0.1) / 유체 점성도
- `pressure` (float): System pressure (0.1-5.0) / 시스템 압력
- `temperature` (int): Temperature in Kelvin (200-500) / 온도 (켈빈)
- `velocity` (float): Flow velocity (0.1-10.0) / 유속

**Response:**
```json
{
  "status": "completed",
  "warmup_id": "warmup_20240115_143218",
  "parameters": {
    "viscosity": 0.01,
    "pressure": 1.0,
    "temperature": 300,
    "velocity": 1.0
  },
  "results": {
    "processing_speed": "100%",
    "efficiency": "95.5%",
    "stability": "85.0%",
    "temperature_balance": "67%"
  },
  "timestamp": "2024-01-15T14:32:18.123456"
}
```

### Get Warmup Status / 웜업 상태 조회
```http
GET /api/warmup/status
```

**Response:**
```json
{
  "active": false,
  "last_warmup": "2024-01-15T14:30:58Z",
  "total_warmups": 247,
  "average_duration": "5.2s",
  "success_rate": "99.2%"
}
```

## AI Optimization Endpoints / AI 최적화 엔드포인트

### Start AI Optimization / AI 최적화 시작
```http
POST /api/ai-optimization/start
Content-Type: application/json
```

**Request Body:**
```json
{
  "personas": ["sun-shin", "einstein", "omega"],
  "mode": "balanced",
  "quantum_level": 7,
  "mirror_depth": 3
}
```

**Parameters:**
- `personas` (array): List of persona IDs to activate / 활성화할 페르소나 ID 목록
- `mode` (string): Optimization mode ("balanced", "performance", "creativity", "stability")
- `quantum_level` (int): Quantum preparation level (1-10) / 양자 준비 수준
- `mirror_depth` (int): Mirror reflection depth (1-7) / 거울 반사 깊이

**Available Personas / 사용 가능한 페르소나:**
- `sun-shin`: 불멸의 이순신 (Strategic management)
- `know-enemy`: 지피지기 (Environmental analysis)
- `rainbow`: 레인보우 (Creative thinking)
- `hwata`: 화타 (Problem diagnosis)
- `einstein`: 아인슈타인 (Innovation)
- `omniscient`: 만물박사 (Knowledge integration)
- `omega`: 오메가 (Quality verification)
- `echo`: 에코 (Synchronization)

**Response:**
```json
{
  "status": "completed",
  "optimization_id": "opt_20240115_143218",
  "active_personas": 3,
  "configuration": {
    "mode": "balanced",
    "quantum_level": 7,
    "mirror_depth": 3
  },
  "metrics": {
    "efficiency": 89,
    "coherence": 95,
    "innovation": 92,
    "stability": 91
  },
  "mirror_reflections": 39,
  "quality_grade": "EXCELLENT",
  "timestamp": "2024-01-15T14:32:18.123456"
}
```

### Get Optimization Status / 최적화 상태 조회
```http
GET /api/ai-optimization/status
```

**Response:**
```json
{
  "active": false,
  "last_optimization": "2024-01-15T14:32:18Z",
  "total_optimizations": 89,
  "active_personas": 5,
  "current_efficiency": 87.3
}
```

## Quantum Preparation Endpoints / 양자 준비 엔드포인트

### Initialize Quantum Preparation / 양자 준비 초기화
```http
POST /api/quantum/init
Content-Type: application/json
```

**Request Body:**
```json
{
  "level": 7
}
```

**Response:**
```json
{
  "status": "initialized",
  "quantum_level": 7,
  "coherence": "94%",
  "entanglement_strength": "70%",
  "timestamp": "2024-01-15T14:32:18.123456"
}
```

### Get Quantum Status / 양자 상태 조회
```http
GET /api/quantum/status
```

**Response:**
```json
{
  "initialized": true,
  "current_level": 7,
  "coherence": "94%",
  "entanglement_strength": "70%",
  "quantum_gates": 42,
  "superposition_states": 128
}
```

## Persona Management Endpoints / 페르소나 관리 엔드포인트

### Get Active Personas / 활성 페르소나 조회
```http
GET /api/personas/active
```

**Response:**
```json
{
  "active_personas": [
    {
      "id": "sun-shin",
      "name": "불멸의 이순신",
      "status": "active",
      "efficiency": 95.2
    },
    {
      "id": "einstein",
      "name": "아인슈타인",
      "status": "active",
      "efficiency": 98.7
    }
  ],
  "total_active": 2,
  "synchronization_level": "EXCELLENT"
}
```

### Activate Persona / 페르소나 활성화
```http
POST /api/personas/{persona_id}/activate
```

**Response:**
```json
{
  "status": "activated",
  "persona": "sun-shin",
  "mirror_face": 5,
  "efficiency": 95.2,
  "specialization": "전략 총괄과 위기 관리"
}
```

### Synchronize Personas / 페르소나 동기화
```http
POST /api/personas/synchronize
```

**Response:**
```json
{
  "status": "synchronized",
  "synchronized_personas": 5,
  "synchronization_level": "EXCELLENT",
  "mirror_coherence": "98.4%",
  "timestamp": "2024-01-15T14:32:18.123456"
}
```

## Mirror System Endpoints / 거울 시스템 엔드포인트

### Get Mirror Reflections / 거울 반사 조회
```http
GET /api/mirror/reflections
```

**Response:**
```json
{
  "total_reflections": 13,
  "active_faces": 13,
  "reflection_depth": 7,
  "coherence_level": "98.7%",
  "amplification_factor": "13x",
  "interference_pattern": "constructive"
}
```

### Get Mirror Status / 거울 상태 조회
```http
GET /api/mirror/status
```

**Response:**
```json
{
  "status": "active",
  "mirror_type": "13-sided polyhedral",
  "reflection_quality": "EXCELLENT",
  "active_faces": 13,
  "total_reflections": 169,
  "last_calibration": "2024-01-15T14:00:00Z"
}
```

## Metrics Endpoints / 지표 엔드포인트

### Get Current Metrics / 현재 지표 조회
```http
GET /api/metrics/current
```

**Response:**
```json
{
  "timestamp": "2024-01-15T14:32:18.123456",
  "performance": {
    "overall": 87.3,
    "efficiency": 89.4,
    "coherence": 94.2,
    "innovation": 82.1,
    "stability": 96.7
  },
  "system_load": {
    "cpu": 23.4,
    "memory": 67.2,
    "network": 12.8,
    "storage": 45.6
  },
  "ai_metrics": {
    "active_personas": 5,
    "optimization_cycles": 1247,
    "quantum_level": 7,
    "mirror_reflections": 13
  }
}
```

### Get Metrics History / 지표 이력 조회
```http
GET /api/metrics/history?timeframe=1h
```

**Query Parameters:**
- `timeframe` (string): Time period ("1h", "6h", "24h", "7d") / 시간 범위

**Response:**
```json
{
  "timeframe": "1h",
  "data_points": [
    {
      "timestamp": "2024-01-15T14:32:18.123456",
      "performance": 87.3,
      "efficiency": 89.4,
      "coherence": 94.2
    }
  ]
}
```

## Diagnostics Endpoints / 진단 엔드포인트

### Run System Diagnostics / 시스템 진단 실행
```http
POST /api/system/diagnostics
```

**Response:**
```json
{
  "status": "completed",
  "diagnostics_id": "diag_20240115_143218",
  "results": {
    "warmup_engine": {
      "status": "healthy",
      "response_time": "120ms"
    },
    "quantum_prep": {
      "status": "healthy",
      "coherence": "94%"
    },
    "ai_optimizer": {
      "status": "healthy",
      "efficiency": "87%"
    },
    "mirror_system": {
      "status": "healthy",
      "reflections": 13
    },
    "storage": {
      "status": "healthy",
      "available_space": "78%"
    }
  },
  "overall_health": "EXCELLENT",
  "recommendations": [
    "All systems operating within normal parameters",
    "Mirror coherence excellent at 98.7%",
    "Quantum preparation stable at level 7"
  ],
  "timestamp": "2024-01-15T14:32:18.123456"
}
```

## WebSocket API / WebSocket API

### Connection / 연결
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

### Message Types / 메시지 유형

#### Ping/Pong / 핑/퐁
```javascript
// Send ping
ws.send(JSON.stringify({ type: "ping" }));

// Receive pong
{
  "type": "pong",
  "timestamp": "2024-01-15T14:32:18.123456"
}
```

#### System Status Request / 시스템 상태 요청
```javascript
ws.send(JSON.stringify({ type: "system_status" }));
```

#### Real-time Metrics Updates / 실시간 지표 업데이트
```javascript
{
  "type": "metrics_update",
  "timestamp": "2024-01-15T14:32:18.123456",
  "data": {
    "warmup_status": { ... },
    "quantum_level": 7,
    "active_personas": 5,
    "mirror_reflections": 13,
    "system_health": { ... }
  }
}
```

## Rate Limits / 속도 제한

- **API Requests**: 1000 requests per minute per IP
- **WebSocket Connections**: 10 concurrent connections per IP
- **Heavy Operations**: 10 per minute (warmup, optimization)

## SDK Examples / SDK 예제

### JavaScript/Node.js
```javascript
const axios = require('axios');

// Start AI optimization
const response = await axios.post('http://localhost:8000/api/ai-optimization/start', {
  personas: ['sun-shin', 'einstein'],
  mode: 'balanced',
  quantum_level: 7,
  mirror_depth: 3
});

console.log('Optimization result:', response.data);
```

### Python
```python
import requests

# Start AI optimization
response = requests.post('http://localhost:8000/api/ai-optimization/start', json={
    'personas': ['sun-shin', 'einstein'],
    'mode': 'balanced',
    'quantum_level': 7,
    'mirror_depth': 3
})

print('Optimization result:', response.json())
```

### cURL
```bash
# Start AI optimization
curl -X POST http://localhost:8000/api/ai-optimization/start \
  -H "Content-Type: application/json" \
  -d '{
    "personas": ["sun-shin", "einstein"],
    "mode": "balanced",
    "quantum_level": 7,
    "mirror_depth": 3
  }'
```

## Error Codes / 오류 코드

| Code | Description | Korean |
|------|-------------|---------|
| `INVALID_PERSONA` | Invalid persona ID specified | 유효하지 않은 페르소나 ID |
| `QUANTUM_LEVEL_OUT_OF_RANGE` | Quantum level must be 1-10 | 양자 레벨은 1-10 사이여야 함 |
| `OPTIMIZATION_IN_PROGRESS` | Another optimization is running | 다른 최적화가 진행 중 |
| `WARMUP_FAILED` | Navier-Stokes warmup failed | 나비에-스토크스 웜업 실패 |
| `STORAGE_ERROR` | Database or storage error | 데이터베이스 또는 저장소 오류 |
| `SYSTEM_OVERLOADED` | System resources exhausted | 시스템 리소스 고갈 |

## Best Practices / 모범 사례

1. **Always check system status before starting operations** / 작업 시작 전 항상 시스템 상태 확인
2. **Use appropriate quantum levels for your use case** / 사용 사례에 적합한 양자 레벨 사용
3. **Monitor system metrics during long operations** / 긴 작업 중 시스템 지표 모니터링
4. **Handle WebSocket disconnections gracefully** / WebSocket 연결 끊김을 우아하게 처리
5. **Implement exponential backoff for retries** / 재시도에 지수 백오프 구현

For more detailed information, visit the interactive API documentation at `/api/docs` when the system is running.