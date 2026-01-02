import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function ProfileEditor({ user, onProfileUpdate }) {
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [profileData, setProfileData] = useState({
    full_name: '',
    phone: '',
    address: '',
    // Role-specific fields
    farm_name: '',
    farm_size: '',
    farm_location: '',
    soil_type: '',
    irrigation_type: '',
    business_name: '',
    business_license: '',
    skills: '',
    experience_years: '',
    daily_wage: '',
    availability: true
  });

  useEffect(() => {
    if (user) {
      setProfileData({
        full_name: user.full_name || '',
        phone: user.phone || '',
        address: user.address || '',
        // Farmer fields
        farm_name: user.farmer_profile?.farm_name || '',
        farm_size: user.farmer_profile?.farm_size || '',
        farm_location: user.farmer_profile?.farm_location || '',
        soil_type: user.farmer_profile?.soil_type || '',
        irrigation_type: user.farmer_profile?.irrigation_type || '',
        // Vendor fields
        business_name: user.vendor_profile?.business_name || '',
        business_license: user.vendor_profile?.business_license || '',
        // Labor fields
        skills: user.labor_profile?.skills || '',
        experience_years: user.labor_profile?.experience_years || '',
        daily_wage: user.labor_profile?.daily_wage || '',
        availability: user.labor_profile?.availability !== undefined ? user.labor_profile.availability : true
      });
    }
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setMessage('Error: No authentication token found. Please log in again.');
        setLoading(false);
        return;
      }

      const response = await axios.put(`${API_URL}/api/auth/profile`, profileData, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.data.success) {
        setMessage('✅ Profile updated successfully!');
        setEditing(false);
        if (onProfileUpdate) {
          onProfileUpdate(response.data.user);
        }
        // Update localStorage
        localStorage.setItem('user', JSON.stringify(response.data.user));
        
        // Clear success message after 3 seconds
        setTimeout(() => setMessage(''), 3000);
      }
    } catch (error) {
      console.error('Profile update error:', error);
      const errorMsg = error.response?.data?.error || error.message || 'Failed to update profile';
      setMessage(`❌ Error: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setProfileData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  if (!editing) {
    return (
      <div className="card">
        <h2 className="card-title">👤 My Profile</h2>
        
        {message && (
          <div style={{
            padding: '1rem',
            marginBottom: '1rem',
            borderRadius: '8px',
            backgroundColor: message.includes('✅') ? '#d1fae5' : '#fee2e2',
            color: message.includes('✅') ? '#065f46' : '#991b1b',
            border: `1px solid ${message.includes('✅') ? '#10b981' : '#ef4444'}`,
            fontWeight: '500'
          }}>
            {message}
          </div>
        )}

        <div className="profile-view">
          <div className="profile-section">
            <h3>Basic Information</h3>
            <div className="profile-field">
              <label>Email:</label>
              <span>{user.email}</span>
              <span className="badge badge-info">Cannot be changed</span>
            </div>
            <div className="profile-field">
              <label>Full Name:</label>
              <span>{user.full_name || 'Not set'}</span>
            </div>
            <div className="profile-field">
              <label>Phone:</label>
              <span>{user.phone || 'Not set'}</span>
            </div>
            <div className="profile-field">
              <label>Address:</label>
              <span>{user.address || 'Not set'}</span>
            </div>
          </div>

          {user.role === 'farmer' && user.farmer_profile && (
            <div className="profile-section">
              <h3>Farm Information</h3>
              <div className="profile-field">
                <label>Farm Name:</label>
                <span>{user.farmer_profile.farm_name || 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Farm Size:</label>
                <span>{user.farmer_profile.farm_size ? `${user.farmer_profile.farm_size} acres` : 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Location:</label>
                <span>{user.farmer_profile.farm_location || 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Soil Type:</label>
                <span>{user.farmer_profile.soil_type || 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Irrigation Type:</label>
                <span>{user.farmer_profile.irrigation_type || 'Not set'}</span>
              </div>
            </div>
          )}

          {user.role === 'vendor' && user.vendor_profile && (
            <div className="profile-section">
              <h3>Business Information</h3>
              <div className="profile-field">
                <label>Business Name:</label>
                <span>{user.vendor_profile.business_name || 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Business License:</label>
                <span>{user.vendor_profile.business_license || 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Rating:</label>
                <span>⭐ {user.vendor_profile.rating || 0}/5</span>
              </div>
              <div className="profile-field">
                <label>Total Sales:</label>
                <span>{user.vendor_profile.total_sales || 0}</span>
              </div>
            </div>
          )}

          {user.role === 'labor' && user.labor_profile && (
            <div className="profile-section">
              <h3>Labor Information</h3>
              <div className="profile-field">
                <label>Skills:</label>
                <span>{user.labor_profile.skills || 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Experience:</label>
                <span>{user.labor_profile.experience_years ? `${user.labor_profile.experience_years} years` : 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Daily Wage:</label>
                <span>{user.labor_profile.daily_wage ? `৳${user.labor_profile.daily_wage}` : 'Not set'}</span>
              </div>
              <div className="profile-field">
                <label>Availability:</label>
                <span className={`badge ${user.labor_profile.availability ? 'badge-success' : 'badge-warning'}`}>
                  {user.labor_profile.availability ? 'Available' : 'Not Available'}
                </span>
              </div>
              <div className="profile-field">
                <label>Rating:</label>
                <span>⭐ {user.labor_profile.rating || 0}/5</span>
              </div>
            </div>
          )}

          <button onClick={() => setEditing(true)} className="btn btn-primary">
            ✏️ Edit Profile
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h2 className="card-title">✏️ Edit Profile</h2>
      
      {message && (
        <div style={{
          padding: '1rem',
          marginBottom: '1rem',
          borderRadius: '8px',
          backgroundColor: message.includes('✅') ? '#d1fae5' : '#fee2e2',
          color: message.includes('✅') ? '#065f46' : '#991b1b',
          border: `1px solid ${message.includes('✅') ? '#10b981' : '#ef4444'}`,
          fontWeight: '500'
        }}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <h3 style={{ marginTop: '1rem', marginBottom: '1rem' }}>Basic Information</h3>
        
        <div className="form-group">
          <label className="form-label">Email (Cannot be changed)</label>
          <input 
            type="email" 
            className="form-input" 
            value={user.email} 
            disabled 
            style={{ backgroundColor: '#f3f4f6', cursor: 'not-allowed' }}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Full Name *</label>
          <input 
            type="text" 
            name="full_name"
            className="form-input" 
            value={profileData.full_name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Phone</label>
          <input 
            type="tel" 
            name="phone"
            className="form-input" 
            value={profileData.phone}
            onChange={handleChange}
            placeholder="+880 1XXX-XXXXXX"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Address</label>
          <textarea 
            name="address"
            className="form-textarea" 
            value={profileData.address}
            onChange={handleChange}
            rows="3"
            placeholder="Your complete address"
          />
        </div>

        {user.role === 'farmer' && (
          <>
            <h3 style={{ marginTop: '1.5rem', marginBottom: '1rem' }}>Farm Information</h3>
            
            <div className="form-group">
              <label className="form-label">Farm Name</label>
              <input 
                type="text" 
                name="farm_name"
                className="form-input" 
                value={profileData.farm_name}
                onChange={handleChange}
                placeholder="Green Valley Farm"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Farm Size (acres)</label>
              <input 
                type="number" 
                name="farm_size"
                className="form-input" 
                value={profileData.farm_size}
                onChange={handleChange}
                step="0.1"
                placeholder="10.5"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Farm Location</label>
              <input 
                type="text" 
                name="farm_location"
                className="form-input" 
                value={profileData.farm_location}
                onChange={handleChange}
                placeholder="District, Division"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Soil Type</label>
              <select 
                name="soil_type"
                className="form-select" 
                value={profileData.soil_type}
                onChange={handleChange}
              >
                <option value="">Select soil type</option>
                <option value="clay">Clay</option>
                <option value="sandy">Sandy</option>
                <option value="loamy">Loamy</option>
                <option value="silty">Silty</option>
                <option value="peaty">Peaty</option>
                <option value="chalky">Chalky</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Irrigation Type</label>
              <select 
                name="irrigation_type"
                className="form-select" 
                value={profileData.irrigation_type}
                onChange={handleChange}
              >
                <option value="">Select irrigation type</option>
                <option value="drip">Drip Irrigation</option>
                <option value="sprinkler">Sprinkler</option>
                <option value="surface">Surface Irrigation</option>
                <option value="subsurface">Subsurface</option>
                <option value="manual">Manual</option>
                <option value="rainfed">Rainfed</option>
              </select>
            </div>
          </>
        )}

        {user.role === 'vendor' && (
          <>
            <h3 style={{ marginTop: '1.5rem', marginBottom: '1rem' }}>Business Information</h3>
            
            <div className="form-group">
              <label className="form-label">Business Name</label>
              <input 
                type="text" 
                name="business_name"
                className="form-input" 
                value={profileData.business_name}
                onChange={handleChange}
                placeholder="Agro Supplies Ltd."
              />
            </div>

            <div className="form-group">
              <label className="form-label">Business License Number</label>
              <input 
                type="text" 
                name="business_license"
                className="form-input" 
                value={profileData.business_license}
                onChange={handleChange}
                placeholder="License #"
              />
            </div>
          </>
        )}

        {user.role === 'labor' && (
          <>
            <h3 style={{ marginTop: '1.5rem', marginBottom: '1rem' }}>Labor Information</h3>
            
            <div className="form-group">
              <label className="form-label">Skills</label>
              <textarea 
                name="skills"
                className="form-textarea" 
                value={profileData.skills}
                onChange={handleChange}
                rows="3"
                placeholder="e.g., Plowing, Harvesting, Irrigation, etc."
              />
            </div>

            <div className="form-group">
              <label className="form-label">Years of Experience</label>
              <input 
                type="number" 
                name="experience_years"
                className="form-input" 
                value={profileData.experience_years}
                onChange={handleChange}
                min="0"
                placeholder="5"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Daily Wage (৳)</label>
              <input 
                type="number" 
                name="daily_wage"
                className="form-input" 
                value={profileData.daily_wage}
                onChange={handleChange}
                min="0"
                step="50"
                placeholder="500"
              />
            </div>

            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <input 
                  type="checkbox" 
                  name="availability"
                  className="form-checkbox" 
                  checked={profileData.availability}
                  onChange={handleChange}
                />
                Available for Work
              </label>
            </div>
          </>
        )}

        <div className="flex gap-2" style={{ marginTop: '1.5rem' }}>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? '💾 Saving...' : '💾 Save Changes'}
          </button>
          <button 
            type="button" 
            onClick={() => {
              setEditing(false);
              setMessage('');
            }} 
            className="btn btn-secondary"
            disabled={loading}
          >
            Cancel
          </button>
        </div>
      </form>

      <style jsx>{`
        .profile-view {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .profile-section {
          padding: 1rem;
          background: var(--gray-50);
          border-radius: var(--radius-lg);
        }

        .profile-section h3 {
          margin-bottom: 1rem;
          color: var(--gray-900);
          font-size: 1.1rem;
          font-weight: 600;
        }

        .profile-field {
          display: grid;
          grid-template-columns: 150px 1fr auto;
          gap: 1rem;
          padding: 0.75rem 0;
          border-bottom: 1px solid var(--gray-200);
          align-items: center;
        }

        .profile-field:last-child {
          border-bottom: none;
        }

        .profile-field label {
          font-weight: 600;
          color: var(--gray-700);
        }

        .profile-field span {
          color: var(--gray-900);
        }

        @media (max-width: 768px) {
          .profile-field {
            grid-template-columns: 1fr;
            gap: 0.25rem;
          }
        }
      `}</style>
    </div>
  );
}

export default ProfileEditor;
