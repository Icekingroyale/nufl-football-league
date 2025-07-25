import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { authAPI } from './services/api';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Fixtures from './components/Fixtures';
import LeagueTable from './components/LeagueTable';
import Teams from './pages/Teams';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Results from './pages/Results';
import Tables from './pages/Tables';
import Stats from './pages/Stats';
import News from './pages/News';
import Players from './pages/Players';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import AdminTeams from './pages/AdminTeams';
import AdminPlayers from './pages/AdminPlayers';
import AdminFixtures from './pages/AdminFixtures';
import AdminNews from './pages/AdminNews';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await authAPI.checkAuth();
      setIsAuthenticated(response.data.authenticated);
      setUser(response.data.user);
    } catch (error) {
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (credentials) => {
    try {
      const response = await authAPI.login(credentials);
      setIsAuthenticated(true);
      setUser(response.data.user);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.message || 'Login failed' };
    }
  };

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      setIsAuthenticated(false);
      setUser(null);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-600"></div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar isAuthenticated={isAuthenticated} onLogout={handleLogout} />
        
        <main className="flex-1">
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Home />} />
            <Route path="/fixtures" element={<Fixtures isAuthenticated={isAuthenticated} />} />
            <Route path="/results" element={<Results />} />
            <Route path="/tables" element={<Tables />} />
            <Route path="/stats" element={<Stats />} />
            <Route path="/news" element={<News />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/players" element={<Players />} />
            
            {/* Admin Routes */}
            <Route 
              path="/admin/login" 
              element={
                isAuthenticated ? 
                <Navigate to="/admin/dashboard" replace /> : 
                <AdminLogin onLogin={handleLogin} />
              } 
            />
            <Route 
              path="/admin/dashboard" 
              element={
                isAuthenticated ? 
                <AdminDashboard /> : 
                <Navigate to="/admin/login" replace />
              } 
            />
            <Route 
              path="/admin/teams" 
              element={
                isAuthenticated ? 
                <AdminTeams /> : 
                <Navigate to="/admin/login" replace />
              } 
            />
            <Route 
              path="/admin/players" 
              element={
                isAuthenticated ? 
                <AdminPlayers /> : 
                <Navigate to="/admin/login" replace />
              } 
            />
            <Route 
              path="/admin/fixtures" 
              element={
                isAuthenticated ? 
                <AdminFixtures /> : 
                <Navigate to="/admin/login" replace />
              } 
            />
            <Route 
              path="/admin/news" 
              element={
                isAuthenticated ? 
                <AdminNews /> : 
                <Navigate to="/admin/login" replace />
              } 
            />
            
            {/* Catch all route */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        
        <Footer />
      </div>
    </Router>
  );
}

export default App; 