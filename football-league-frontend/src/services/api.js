import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  withCredentials: true, // Important for session-based auth
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  login: (credentials) => api.post('/login', credentials),
  logout: () => api.post('/logout'),
  checkAuth: () => api.get('/check_auth'),
};

// Data API
export const dataAPI = {
  getLeagueTable: () => api.get('/league_table'),
  getTeams: () => api.get('/teams'),
  getPlayers: () => api.get('/players'),
  getFixtures: () => api.get('/fixtures'),
  getStats: () => api.get('/stats'),
};

// Actions API
export const actionsAPI = {
  addFixture: (fixtureData) => api.post('/add_fixture', fixtureData),
  updateResult: (fixtureId, resultData) => api.post(`/update_result/${fixtureId}`, resultData),
};

export default api; 