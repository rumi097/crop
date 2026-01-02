import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function Register({ onRegister }) {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    phone: '',
    role: 'farmer',
    // Role-specific fields
    farm_name: '',
    business_name: '',
    skills: '',
    daily_wage: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/api/auth/register`, formData);
      onRegister(response.data.user, response.data.token);
      
      // Redirect based on role
      const roleMap = {
        farmer: '/farmer',
        buyer: '/buyer',
        vendor: '/vendor',
        labor: '/labor'
      };
      navigate(roleMap[response.data.user.role] || '/');
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}>
      <div className="card" style={{ maxWidth: '500px', width: '100%' }}>
        <h2 className="card-title" style={{ textAlign: 'center' }}>Register on Smart Farming</h2>
        
        {error && <div className="alert alert-error">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Full Name</label>
            <input
              type="text"
              className="form-input"
              value={formData.full_name}
              onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Email</label>
            <input
              type="email"
              className="form-input"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-input"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Phone</label>
            <input
              type="tel"
              className="form-input"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Register as</label>
            <select
              className="form-select"
              value={formData.role}
              onChange={(e) => setFormData({ ...formData, role: e.target.value })}
              required
            >
              <option value="farmer">Farmer</option>
              <option value="buyer">Buyer</option>
              <option value="vendor">Vendor</option>
              <option value="labor">Labor</option>
            </select>
          </div>

          {/* Role-specific fields */}
          {formData.role === 'farmer' && (
            <div className="form-group">
              <label className="form-label">Farm Name</label>
              <input
                type="text"
                className="form-input"
                value={formData.farm_name}
                onChange={(e) => setFormData({ ...formData, farm_name: e.target.value })}
              />
            </div>
          )}

          {formData.role === 'vendor' && (
            <div className="form-group">
              <label className="form-label">Business Name</label>
              <input
                type="text"
                className="form-input"
                value={formData.business_name}
                onChange={(e) => setFormData({ ...formData, business_name: e.target.value })}
              />
            </div>
          )}

          {formData.role === 'labor' && (
            <>
              <div className="form-group">
                <label className="form-label">Skills</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="e.g., Planting, Harvesting"
                  value={formData.skills}
                  onChange={(e) => setFormData({ ...formData, skills: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Daily Wage (৳)</label>
                <input
                  type="number"
                  className="form-input"
                  value={formData.daily_wage}
                  onChange={(e) => setFormData({ ...formData, daily_wage: e.target.value })}
                />
              </div>
            </>
          )}

          <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Registering...' : 'Register'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '1rem', color: '#666' }}>
          Already have an account? <Link to="/login" style={{ color: '#667eea' }}>Login</Link>
        </p>
        
        <p style={{ textAlign: 'center', marginTop: '0.5rem' }}>
          <Link to="/" style={{ color: '#667eea' }}>← Back to Home</Link>
        </p>
      </div>
    </div>
  );
}

export default Register;
