import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// User services
export const userService = {
  createUser: (userData) => api.post('/users/', userData),
  getUsers: () => api.get('/users/'),
  getUser: (userId) => api.get(`/users/${userId}`),
  updateUser: (userId, userData) => api.put(`/users/${userId}`, userData),
  deleteUser: (userId) => api.delete(`/users/${userId}`),
};

// Interaction services
export const interactionService = {
  createInteraction: (userId, interactionData) => 
    api.post(`/interactions/${userId}`, interactionData),
  getUserInteractions: (userId, skip = 0, limit = 50) => 
    api.get(`/interactions/${userId}?skip=${skip}&limit=${limit}`),
  getInteractionStats: (userId) => 
    api.get(`/interactions/${userId}/stats`),
};

// Feedback services
export const feedbackService = {
  submitFeedback: (userId, feedbackData) => 
    api.post(`/feedback/${userId}`, feedbackData),
  getUserFeedback: (userId, skip = 0, limit = 50) => 
    api.get(`/feedback/${userId}?skip=${skip}&limit=${limit}`),
  processFeedback: (feedbackId) => 
    api.post(`/feedback/${feedbackId}/process`),
  getFeedbackSummary: () => 
    api.get('/feedback/analytics/summary'),
};

// Analytics services
export const analyticsService = {
  getUserGrowthMetrics: (userId) => 
    api.get(`/analytics/user/${userId}/growth`),
  getAIPerformanceMetrics: () => 
    api.get('/analytics/ai/performance'),
  createGrowthSnapshot: (userId) => 
    api.post(`/analytics/user/${userId}/snapshot`),
  getGrowthTrend: (userId, days = 30) => 
    api.get(`/analytics/user/${userId}/growth-trend?days=${days}`),
  getMutualGrowthAnalysis: (userId) => 
    api.get(`/analytics/mutual-growth/${userId}`),
};

export default api;
