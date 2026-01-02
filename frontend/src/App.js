import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import FarmerPortal from './components/portals/FarmerPortal';
import BuyerPortal from './components/portals/BuyerPortal';
import VendorPortal from './components/portals/VendorPortal';
import LaborPortal from './components/portals/LaborPortal';
import AdminPortal from './components/portals/AdminPortal';

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing authentication on mount
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    
    if (storedToken && storedUser) {
      try {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
      } catch (error) {
        console.error('Error parsing stored user:', error);
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      }
    }
    setLoading(false);
  }, []);

  const handleLogin = (userData, authToken) => {
    setUser(userData);
    setToken(authToken);
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', authToken);
  };

  const handleLogout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  };

  const ProtectedRoute = ({ children, allowedRoles }) => {
    // Show loading spinner while checking authentication
    if (loading) {
      return (
        <div className="loading">
          <div className="spinner"></div>
          <p className="spinner-text">Loading...</p>
        </div>
      );
    }

    if (!token || !user) {
      return <Navigate to="/login" replace />;
    }
    
    if (allowedRoles && !allowedRoles.includes(user.role)) {
      return <Navigate to="/" replace />;
    }
    
    return children;
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<LandingPage user={user} onLogout={handleLogout} />} />
          <Route 
            path="/login" 
            element={
              user && token ? (
                <Navigate to={`/${user.role}`} replace />
              ) : (
                <Login onLogin={handleLogin} />
              )
            } 
          />
          <Route 
            path="/register" 
            element={
              user && token ? (
                <Navigate to={`/${user.role}`} replace />
              ) : (
                <Register onRegister={handleLogin} />
              )
            } 
          />
          
          <Route
            path="/farmer/*"
            element={
              <ProtectedRoute allowedRoles={['farmer']}>
                <FarmerPortal user={user} onLogout={handleLogout} />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/buyer/*"
            element={
              <ProtectedRoute allowedRoles={['buyer']}>
                <BuyerPortal user={user} onLogout={handleLogout} />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/vendor/*"
            element={
              <ProtectedRoute allowedRoles={['vendor']}>
                <VendorPortal user={user} onLogout={handleLogout} />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/labor/*"
            element={
              <ProtectedRoute allowedRoles={['labor']}>
                <LaborPortal user={user} onLogout={handleLogout} />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/admin/*"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <AdminPortal user={user} onLogout={handleLogout} />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
