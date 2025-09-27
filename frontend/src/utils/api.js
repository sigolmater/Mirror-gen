import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API endpoints
export const mirrorGenAPI = {
  // System status
  getSystemStatus: () => api.get('/api/system/status'),
  
  // Navier-Stokes Warmup
  startNavierStokesWarmup: (params) => 
    api.post('/api/warmup/navier-stokes', params),
  getWarmupStatus: () => 
    api.get('/api/warmup/status'),
  stopWarmup: () => 
    api.post('/api/warmup/stop'),
    
  // AI Optimization
  startOptimization: (config) => 
    api.post('/api/ai-optimization/start', config),
  getOptimizationStatus: () => 
    api.get('/api/ai-optimization/status'),
  stopOptimization: () => 
    api.post('/api/ai-optimization/stop'),
  getOptimizationHistory: () => 
    api.get('/api/ai-optimization/history'),
    
  // Quantum Preparation
  initQuantumPrep: (level) => 
    api.post('/api/quantum/init', { level }),
  getQuantumStatus: () => 
    api.get('/api/quantum/status'),
  adjustQuantumLevel: (level) => 
    api.put('/api/quantum/level', { level }),
    
  // Persona Management
  getActivePersonas: () => 
    api.get('/api/personas/active'),
  activatePersona: (personaId) => 
    api.post(`/api/personas/${personaId}/activate`),
  deactivatePersona: (personaId) => 
    api.post(`/api/personas/${personaId}/deactivate`),
  getPersonaStatus: (personaId) => 
    api.get(`/api/personas/${personaId}/status`),
  synchronizePersonas: () => 
    api.post('/api/personas/synchronize'),
    
  // Mirror System
  getMirrorReflections: () => 
    api.get('/api/mirror/reflections'),
  adjustMirrorDepth: (depth) => 
    api.put('/api/mirror/depth', { depth }),
  getMirrorStatus: () => 
    api.get('/api/mirror/status'),
    
  // Reflex Controller
  getReflexStatus: () => 
    api.get('/api/reflex/status'),
  triggerReflex: (type, data) => 
    api.post('/api/reflex/trigger', { type, data }),
    
  // Storage
  saveConfiguration: (config) => 
    api.post('/api/storage/config', config),
  loadConfiguration: (configId) => 
    api.get(`/api/storage/config/${configId}`),
  getStorageStats: () => 
    api.get('/api/storage/stats'),
    
  // Real-time metrics
  getMetrics: () => 
    api.get('/api/metrics/current'),
  getMetricsHistory: (timeframe = '1h') => 
    api.get(`/api/metrics/history?timeframe=${timeframe}`),
    
  // System diagnostics
  runDiagnostics: () => 
    api.post('/api/system/diagnostics'),
  getSystemHealth: () => 
    api.get('/api/system/health'),
  getLogs: (level = 'INFO', limit = 100) => 
    api.get(`/api/system/logs?level=${level}&limit=${limit}`)
};

// WebSocket connection for real-time updates
export class MirrorGenWebSocket {
  constructor(url) {
    this.url = url || process.env.REACT_APP_WEBSOCKET_URL || 'ws://localhost:8000/ws';
    this.socket = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectInterval = 3000;
    this.listeners = new Map();
  }

  connect() {
    try {
      this.socket = new WebSocket(this.url);
      
      this.socket.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        this.emit('connected');
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.emit(data.type || 'message', data);
        } catch (error) {
          console.error('WebSocket message parse error:', error);
        }
      };

      this.socket.onclose = () => {
        console.log('WebSocket disconnected');
        this.emit('disconnected');
        this.attemptReconnect();
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.emit('error', error);
      };
    } catch (error) {
      console.error('WebSocket connection failed:', error);
      this.attemptReconnect();
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        this.connect();
      }, this.reconnectInterval);
    } else {
      console.error('Max reconnection attempts reached');
      this.emit('maxReconnectAttemptsReached');
    }
  }

  send(message) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message));
    } else {
      console.error('WebSocket is not connected');
    }
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  off(event, callback) {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      const index = eventListeners.indexOf(callback);
      if (index > -1) {
        eventListeners.splice(index, 1);
      }
    }
  }

  emit(event, data) {
    const eventListeners = this.listeners.get(event);
    if (eventListeners) {
      eventListeners.forEach(callback => callback(data));
    }
  }
}

// Utility functions
export const formatTimestamp = (timestamp) => {
  return new Date(timestamp).toLocaleString();
};

export const formatDuration = (milliseconds) => {
  const seconds = Math.floor(milliseconds / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 0) return `${days}d ${hours % 24}h ${minutes % 60}m`;
  if (hours > 0) return `${hours}h ${minutes % 60}m`;
  if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
  return `${seconds}s`;
};

export const formatPercentage = (value, decimals = 1) => {
  return `${value.toFixed(decimals)}%`;
};

export const getPersonaIcon = (personaId) => {
  const icons = {
    'sun-shin': '⚓',
    'know-enemy': '🔍',
    'rainbow': '🌈',
    'hwata': '💉',
    'einstein': '⚛️',
    'omniscient': '📚',
    'omega': '✅',
    'echo': '🔄'
  };
  return icons[personaId] || '🎭';
};

export const getStatusColor = (status) => {
  const colors = {
    'active': '#00ff00',
    'warning': '#ffff00',
    'error': '#ff0000',
    'inactive': '#888888',
    'optimizing': '#00ffff'
  };
  return colors[status] || '#ffffff';
};

export default api;