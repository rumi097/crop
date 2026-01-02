import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import ProfileEditor from '../shared/ProfileEditor';
import axios from 'axios';
import '../../styles/portals/admin.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function AdminPortal({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('analytics');
  const [analytics, setAnalytics] = useState(null);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    if (activeTab === 'analytics') fetchAnalytics();
    if (activeTab === 'users') fetchUsers();
  }, [activeTab]);

  const fetchAnalytics = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/admin/analytics`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAnalytics(response.data.analytics);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/admin/users`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUsers(response.data.users);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const verifyUser = async (userId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API_URL}/api/admin/verify-user/${userId}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('User verified successfully');
      fetchUsers();
    } catch (error) {
      alert('Verification failed');
    }
  };

  return (
    <div>
      <header className="header">
        <div className="header-title">⚙️ Admin Portal</div>
        <div className="header-nav">
          <span className="badge badge-admin">ADMIN</span>
          <span>{user.full_name}</span>
          <Link to="/" className="nav-link">Home</Link>
          <button onClick={onLogout} className="btn btn-secondary">Logout</button>
        </div>
      </header>

      <div className="container">
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
          <button onClick={() => setActiveTab('analytics')} className={`btn ${activeTab === 'analytics' ? 'btn-primary' : 'btn-secondary'}`}>
            Analytics
          </button>
          <button onClick={() => setActiveTab('users')} className={`btn ${activeTab === 'users' ? 'btn-primary' : 'btn-secondary'}`}>
            User Management
          </button>
          <button onClick={() => setActiveTab('profile')} className={`btn ${activeTab === 'profile' ? 'btn-primary' : 'btn-secondary'}`}>
            👤 Profile
          </button>
        </div>

        {activeTab === 'analytics' && analytics && (
          <div>
            <h2 className="card-title">Platform Analytics</h2>
            <div className="grid grid-2">
              <div className="card" style={{ background: '#f0fdf4' }}>
                <h3>Total Users</h3>
                <p style={{ fontSize: '2rem', color: '#10b981' }}>{analytics.total_users}</p>
              </div>
              <div className="card" style={{ background: '#fefce8' }}>
                <h3>Farmers</h3>
                <p style={{ fontSize: '2rem', color: '#f59e0b' }}>{analytics.farmers}</p>
              </div>
              <div className="card" style={{ background: '#dbeafe' }}>
                <h3>Buyers</h3>
                <p style={{ fontSize: '2rem', color: '#3b82f6' }}>{analytics.buyers}</p>
              </div>
              <div className="card" style={{ background: '#fae8ff' }}>
                <h3>Vendors</h3>
                <p style={{ fontSize: '2rem', color: '#a855f7' }}>{analytics.vendors}</p>
              </div>
              <div className="card" style={{ background: '#fce7f3' }}>
                <h3>Total Orders</h3>
                <p style={{ fontSize: '2rem', color: '#ec4899' }}>{analytics.total_orders}</p>
              </div>
              <div className="card" style={{ background: '#f0fdfa' }}>
                <h3>Total Products</h3>
                <p style={{ fontSize: '2rem', color: '#14b8a6' }}>{analytics.total_products}</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'users' && (
          <div className="card">
            <h2 className="card-title">User Management</h2>
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Verified</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {users.map(u => (
                  <tr key={u.id}>
                    <td>{u.id}</td>
                    <td>{u.full_name}</td>
                    <td>{u.email}</td>
                    <td><span className={`badge badge-${u.role}`}>{u.role}</span></td>
                    <td>{u.is_verified ? '✅' : '❌'}</td>
                    <td>
                      {!u.is_verified && (
                        <button onClick={() => verifyUser(u.id)} className="btn btn-success">
                          Verify
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'profile' && (
          <ProfileEditor
            user={user}
            onProfileUpdate={(updatedUser) => {
              localStorage.setItem('user', JSON.stringify(updatedUser));
            }}
          />
        )}
      </div>
    </div>
  );
}

export default AdminPortal;
