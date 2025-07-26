import axios from 'axios';


// Add this at the top of your api.js file, right after the imports
console.log('=== API Configuration Debug ===');
console.log('VITE_API_URL:', import.meta.env.VITE_API_URL);
console.log('Mode:', import.meta.env.MODE);
console.log('All env vars:', import.meta.env);
console.log('Final baseURL will be:', import.meta.env.VITE_API_URL || '/api');


// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  withCredentials: true, // Enable credentials for admin authentication
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Don't redirect for check_auth endpoint as 401 is expected when not authenticated
    if (error.response?.status === 401 && !error.config.url.includes('/check_auth')) {
      // Unauthorized - redirect to login
      localStorage.removeItem('authToken');
      window.location.href = '/admin/login';
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

// Teams API
export const teamsAPI = {
  getAllTeams: () => api.get('/teams'),
  getTeam: (id) => api.get(`/teams/${id}`),
  createTeam: (teamData) => api.post('/teams', teamData),
  updateTeam: (id, teamData) => api.put(`/teams/${id}`, teamData),
  deleteTeam: (id) => api.delete(`/teams/${id}`),
};

// Players API
export const playersAPI = {
  getAllPlayers: () => api.get('/players'),
  getPlayer: (id) => api.get(`/players/${id}`),
  createPlayer: (playerData) => api.post('/players', playerData),
  updatePlayer: (id, playerData) => api.put(`/players/${id}`, playerData),
  deletePlayer: (id) => api.delete(`/players/${id}`),
  getPlayersByTeam: (teamId) => api.get(`/teams/${teamId}/players`),
};

// Fixtures API
export const fixturesAPI = {
  getAllFixtures: () => api.get('/fixtures'),
  getFixture: (id) => api.get(`/fixtures/${id}`),
  createFixture: (fixtureData) => api.post('/fixtures', fixtureData),
  updateFixture: (id, fixtureData) => api.put(`/fixtures/${id}`, fixtureData),
  deleteFixture: (id) => api.delete(`/fixtures/${id}`),
  updateResult: (id, resultData) => api.post(`/fixtures/${id}/result`, resultData),
};

// News API
export const newsAPI = {
  getAllNews: () => api.get('/news'),
  getNews: (id) => api.get(`/news/${id}`),
  createNews: (newsData) => api.post('/news', newsData),
  updateNews: (id, newsData) => api.put(`/news/${id}`, newsData),
  deleteNews: (id) => api.delete(`/news/${id}`),
};

// Data API (for public pages)
export const dataAPI = {
  getLeagueTable: () => api.get('/league_table'),
  getTeams: () => api.get('/teams'),
  getPlayers: () => api.get('/players'),
  getFixtures: () => api.get('/fixtures'),
  getStats: () => api.get('/stats'),
  getNews: () => api.get('/news'),
};

// Actions API (legacy - keeping for compatibility)
export const actionsAPI = {
  addFixture: (fixtureData) => api.post('/add_fixture', fixtureData),
  updateResult: (fixtureId, resultData) => api.post(`/update_result/${fixtureId}`, resultData),
};

export default api; 