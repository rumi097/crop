import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import CropRecommendation from '../CropRecommendation';
import FertilizerRecommendation from '../FertilizerRecommendation';
import ProfileEditor from '../shared/ProfileEditor';
import axios from 'axios';
import '../../styles/portals/farmer.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function FarmerPortal({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [listings, setListings] = useState([]);
  const [farmerOrders, setFarmerOrders] = useState([]);
  const [history, setHistory] = useState([]);
  const [costs, setCosts] = useState([]);
  const [laborPostings, setLaborPostings] = useState([]);
  const [weather, setWeather] = useState(null);
  const [stats, setStats] = useState({ listings: 0, costs: 0, labor: 0, totalRevenue: 0 });
  
  // Form states
  const [showListingForm, setShowListingForm] = useState(false);
  const [showCostForm, setShowCostForm] = useState(false);
  const [showLaborForm, setShowLaborForm] = useState(false);
  const [editingListing, setEditingListing] = useState(null);
  const [editingLaborPosting, setEditingLaborPosting] = useState(null);
  
  const [listingForm, setListingForm] = useState({
    crop_name: '', category: 'vegetables', quantity: '', unit: 'kg',
    price_per_unit: '', harvest_date: '', location: '', description: '', image_url: ''
  });
  
  const [costForm, setCostForm] = useState({
    cost_type: 'seed', crop_name: '', season: '', amount: '', date: '', notes: ''
  });
  
  const [laborForm, setLaborForm] = useState({
    job_title: '', work_type: '', laborers_needed: '', start_date: '', end_date: '',
    wage_type: 'per_day', wage_amount: '', location: '', description: ''
  });

  useEffect(() => {
    // Fetch weather on dashboard load
    if (activeTab === 'dashboard') {
      fetchWeather();
      fetchDashboardStats();
    }
    if (activeTab === 'listings') fetchListings();
    if (activeTab === 'history') fetchHistory();
    if (activeTab === 'costs') fetchCosts();
    if (activeTab === 'labor') fetchLaborPostings();
    if (activeTab === 'orders') fetchFarmerOrders();
  }, [activeTab]);

  const fetchDashboardStats = async () => {
    try {
      const token = localStorage.getItem('token');
      const [listingsRes, costsRes, laborRes] = await Promise.all([
        axios.get(`${API_URL}/api/farmer/crop-listings`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API_URL}/api/farmer/costs`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API_URL}/api/farmer/labor-postings`, { headers: { Authorization: `Bearer ${token}` } })
      ]);
      
      const totalRevenue = costsRes.data.records.reduce((sum, r) => sum + (r.revenue || 0), 0);
      setStats({
        listings: listingsRes.data.listings.length,
        costs: costsRes.data.records.length,
        labor: laborRes.data.postings.length,
        totalRevenue
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const fetchWeather = async () => {
    try {
      const token = localStorage.getItem('token');
      const profileRes = await axios.get(`${API_URL}/api/auth/profile`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      const location = profileRes.data.user.farm_location || 'Delhi';
      const weatherRes = await axios.get(`${API_URL}/api/farmer/weather?location=${location}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setWeather(weatherRes.data.weather);
    } catch (error) {
      console.error('Error fetching weather:', error);
    }
  };

  const fetchListings = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/farmer/crop-listings`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setListings(response.data.listings);
    } catch (error) {
      console.error('Error fetching listings:', error);
    }
  };

  const fetchHistory = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/farmer/recommendation-history`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setHistory(response.data.history);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const fetchCosts = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/farmer/costs`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCosts(response.data.records);
    } catch (error) {
      console.error('Error fetching costs:', error);
    }
  };

  const fetchLaborPostings = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/farmer/labor-postings`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLaborPostings(response.data.postings);
    } catch (error) {
      console.error('Error fetching labor postings:', error);
    }
  };

  const fetchFarmerOrders = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/farmer/orders`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setFarmerOrders(response.data.orders || []);
    } catch (error) {
      console.error('Error fetching farmer orders:', error);
    }
  };

  // Listing handlers
  const handleListingSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      
      if (editingListing) {
        await axios.put(`${API_URL}/api/farmer/crop-listings/${editingListing.id}`, listingForm, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert('Listing updated successfully!');
      } else {
        await axios.post(`${API_URL}/api/farmer/crop-listings`, listingForm, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert('Listing created successfully!');
      }
      
      setShowListingForm(false);
      setEditingListing(null);
      setListingForm({ crop_name: '', category: 'vegetables', quantity: '', unit: 'kg',
        price_per_unit: '', harvest_date: '', location: '', description: '', image_url: '' });
      fetchListings();
    } catch (error) {
      alert('Error: ' + (error.response?.data?.error || 'Failed to save listing'));
    }
  };

  const handleEditListing = (listing) => {
    setEditingListing(listing);
    setListingForm({
      crop_name: listing.crop_name,
      category: listing.category,
      quantity: listing.quantity,
      unit: listing.unit,
      price_per_unit: listing.price_per_unit,
      harvest_date: listing.harvest_date?.split('T')[0] || '',
      location: listing.location || '',
      description: listing.description || '',
      image_url: listing.image_url || ''
    });
    setShowListingForm(true);
  };

  const handleDeleteListing = async (listingId) => {
    if (!window.confirm('Are you sure you want to delete this listing?')) return;
    
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/api/farmer/crop-listings/${listingId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Listing deleted successfully!');
      fetchListings();
    } catch (error) {
      alert('Error: ' + (error.response?.data?.error || 'Failed to delete listing'));
    }
  };

  // Cost handlers
  const handleCostSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      
      // Build cost data based on cost_type
      const costData = {
        crop_name: costForm.crop_name,
        season: costForm.season,
        year: new Date(costForm.date).getFullYear(),
        seed_cost: costForm.cost_type === 'seed' ? parseFloat(costForm.amount) : 0,
        fertilizer_cost: costForm.cost_type === 'fertilizer' ? parseFloat(costForm.amount) : 0,
        pesticide_cost: costForm.cost_type === 'pesticide' ? parseFloat(costForm.amount) : 0,
        labor_cost: costForm.cost_type === 'labor' ? parseFloat(costForm.amount) : 0,
        equipment_cost: costForm.cost_type === 'equipment' ? parseFloat(costForm.amount) : 0,
        irrigation_cost: costForm.cost_type === 'irrigation' ? parseFloat(costForm.amount) : 0,
        other_cost: costForm.cost_type === 'other' ? parseFloat(costForm.amount) : 0,
        revenue: 0,
        notes: `${costForm.cost_type} - ${costForm.notes}`
      };
      
      await axios.post(`${API_URL}/api/farmer/costs`, costData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      alert('Cost entry added successfully!');
      setShowCostForm(false);
      setCostForm({ cost_type: 'seed', crop_name: '', season: '', amount: '', date: '', notes: '' });
      fetchCosts();
    } catch (error) {
      alert('Error: ' + (error.response?.data?.error || 'Failed to add cost'));
    }
  };

  // Labor handlers
  const handleLaborSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      
      const laborData = {
        job_title: laborForm.job_title,
        description: laborForm.description,
        work_type: laborForm.work_type,
        start_date: laborForm.start_date,
        end_date: laborForm.end_date,
        wage_per_day: laborForm.wage_type === 'per_day' ? parseFloat(laborForm.wage_amount) : null,
        total_wage: laborForm.wage_type === 'total' ? parseFloat(laborForm.wage_amount) : null,
        location: laborForm.location,
        laborers_needed: parseInt(laborForm.laborers_needed)
      };

      if (editingLaborPosting) {
        await axios.put(`${API_URL}/api/farmer/labor-postings/${editingLaborPosting.id}`, laborData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert('Labor posting updated successfully!');
      } else {
        await axios.post(`${API_URL}/api/farmer/labor-postings`, laborData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert('Labor posting created successfully!');
      }
      setShowLaborForm(false);
      setEditingLaborPosting(null);
      setLaborForm({ job_title: '', work_type: '', laborers_needed: '', start_date: '', end_date: '',
        wage_type: 'per_day', wage_amount: '', location: '', description: '' });
      fetchLaborPostings();
    } catch (error) {
      alert('Error: ' + (error.response?.data?.error || 'Failed to create labor posting'));
    }
  };

  const handleEditLaborPosting = (posting) => {
    setEditingLaborPosting(posting);
    setLaborForm({
      job_title: posting.job_title || '',
      work_type: posting.work_type || '',
      laborers_needed: posting.laborers_needed || '',
      start_date: posting.start_date ? posting.start_date.split('T')[0] : '',
      end_date: posting.end_date ? posting.end_date.split('T')[0] : '',
      wage_type: posting.wage_per_day ? 'per_day' : 'total',
      wage_amount: posting.wage_per_day || posting.total_wage || '',
      location: posting.location || '',
      description: posting.description || ''
    });
    setShowLaborForm(true);
  };

  const updateLaborStatus = async (postingId, newStatus) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(`${API_URL}/api/farmer/labor-postings/${postingId}`, { status: newStatus }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchLaborPostings();
    } catch (error) {
      alert('Error: ' + (error.response?.data?.error || 'Failed to update status'));
    }
  };

  const updateOrderStatus = async (orderId, newStatus) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(`${API_URL}/api/farmer/orders/${orderId}/status`, { status: newStatus }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchFarmerOrders();
    } catch (error) {
      alert('Error: ' + (error.response?.data?.error || 'Failed to update order status'));
    }
  };

  return (
    <div>
      {/* Header */}
      <header className="header">
        <div className="header-title">🌾 Farmer Portal</div>
        <div className="header-nav">
          <span className="badge badge-farmer">FARMER</span>
          <span>{user.full_name}</span>
          <Link to="/" className="nav-link">Home</Link>
          <button onClick={onLogout} className="btn btn-secondary">Logout</button>
        </div>
      </header>

      <div className="container">
        {/* Navigation Tabs */}
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
          <button onClick={() => setActiveTab('dashboard')} className={`btn ${activeTab === 'dashboard' ? 'btn-primary' : 'btn-secondary'}`}>
            Dashboard
          </button>
          <button onClick={() => setActiveTab('recommend')} className={`btn ${activeTab === 'recommend' ? 'btn-primary' : 'btn-secondary'}`}>
            Recommendations
          </button>
          <button onClick={() => setActiveTab('history')} className={`btn ${activeTab === 'history' ? 'btn-primary' : 'btn-secondary'}`}>
            History
          </button>
          <button onClick={() => setActiveTab('listings')} className={`btn ${activeTab === 'listings' ? 'btn-primary' : 'btn-secondary'}`}>
            My Listings
          </button>
          <button onClick={() => setActiveTab('costs')} className={`btn ${activeTab === 'costs' ? 'btn-primary' : 'btn-secondary'}`}>
            Cost Tracking
          </button>
          <button onClick={() => setActiveTab('labor')} className={`btn ${activeTab === 'labor' ? 'btn-primary' : 'btn-secondary'}`}>
            Labor
          </button>
          <button onClick={() => setActiveTab('orders')} className={`btn ${activeTab === 'orders' ? 'btn-primary' : 'btn-secondary'}`}>
            Orders
          </button>
          <button onClick={() => setActiveTab('profile')} className={`btn ${activeTab === 'profile' ? 'btn-primary' : 'btn-secondary'}`}>
            👤 Profile
          </button>

        </div>

        {/* Content */}
        {activeTab === 'dashboard' && (
          <div>
            <div className="card">
              <h2 className="card-title">Welcome, {user.full_name}! 🌾</h2>
              <p style={{ marginBottom: '2rem' }}>Manage your farm operations from a single dashboard</p>
              
              {/* Quick Actions */}
              <div style={{ marginBottom: '2rem' }}>
                <h3 style={{ marginBottom: '1rem' }}>Quick Actions</h3>
                <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                  <button onClick={() => { setActiveTab('listings'); setShowListingForm(true); }} className="btn btn-primary">
                    + Add Crop Listing
                  </button>
                  <button onClick={() => { setActiveTab('costs'); setShowCostForm(true); }} className="btn btn-primary">
                    + Add Cost Entry
                  </button>
                  <button onClick={() => { setActiveTab('labor'); setShowLaborForm(true); }} className="btn btn-primary">
                    + Post Labor Requirement
                  </button>
                  <button onClick={() => setActiveTab('recommend')} className="btn btn-secondary">
                    Get Recommendations
                  </button>
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-2" style={{ marginTop: '2rem' }}>
                <div className="card" style={{ background: '#f0fdf4', border: '2px solid #22c55e' }}>
                  <h3>📊 Quick Stats</h3>
                  <p><strong>Active Listings:</strong> {stats.listings}</p>
                  <p><strong>Cost Records:</strong> {stats.costs}</p>
                  <p><strong>Labor Postings:</strong> {stats.labor}</p>
                  <p style={{ color: '#10b981', fontWeight: 'bold' }}>
                    <strong>Total Revenue:</strong> ৳{stats.totalRevenue.toFixed(2)}
                  </p>
                </div>
                <div className="card" style={{ background: '#fefce8', border: '2px solid #eab308' }}>
                  <h3>🌤️ Weather Update</h3>
                  {weather ? (
                    <div>
                      <p><strong>Temperature:</strong> {weather.temperature}°C</p>
                      <p><strong>Humidity:</strong> {weather.humidity}%</p>
                      <p><strong>Condition:</strong> {weather.description}</p>
                      <p><strong>Wind Speed:</strong> {weather.wind_speed} m/s</p>
                    </div>
                  ) : (
                    <p>Loading weather data...</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'recommend' && (
          <div>
            <div className="card">
              <h2 className="card-title">Crop Recommendation</h2>
              <CropRecommendation />
            </div>
            <div className="card" style={{ marginTop: '2rem' }}>
              <h2 className="card-title">Fertilizer Recommendation</h2>
              <FertilizerRecommendation />
            </div>
          </div>
        )}

        {activeTab === 'history' && (
          <div className="card">
            <h2 className="card-title">Recommendation History</h2>
            {history.length === 0 ? (
              <p>No history yet</p>
            ) : (
              <div>
                {history.map((item, index) => (
                  <div key={index} style={{ padding: '1rem', borderBottom: '1px solid #e0e0e0' }}>
                    <strong>{item.type === 'crop' ? '🌾 Crop' : '💧 Fertilizer'} Recommendation</strong>
                    <p style={{ color: '#666', fontSize: '0.9rem' }}>{new Date(item.date).toLocaleDateString()}</p>
                    <p>Result: {JSON.stringify(item.result)}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'listings' && (
          <div>
            <div className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h2 className="card-title">My Crop Listings</h2>
                <button onClick={() => { setShowListingForm(true); setEditingListing(null); }} className="btn btn-primary">
                  + Add New Listing
                </button>
              </div>

              {/* Listing Form */}
              {showListingForm && (
                <div className="card" style={{ background: '#f9fafb', padding: '1.5rem', marginBottom: '2rem' }}>
                  <h3>{editingListing ? 'Edit Listing' : 'Create New Listing'}</h3>
                  <form onSubmit={handleListingSubmit}>
                    <div className="grid grid-2" style={{ gap: '1rem' }}>
                      <div className="form-group">
                        <label>Crop Name *</label>
                        <input type="text" required className="form-input" value={listingForm.crop_name}
                          onChange={(e) => setListingForm({...listingForm, crop_name: e.target.value})} />
                      </div>
                      <div className="form-group">
                        <label>Category *</label>
                        <select required className="form-input" value={listingForm.category}
                          onChange={(e) => setListingForm({...listingForm, category: e.target.value})}>
                          <option value="vegetables">Vegetables</option>
                          <option value="fruits">Fruits</option>
                          <option value="grains">Grains</option>
                          <option value="pulses">Pulses</option>
                          <option value="spices">Spices</option>
                          <option value="others">Others</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Quantity *</label>
                        <input type="number" step="0.01" required className="form-input" value={listingForm.quantity}
                          onChange={(e) => setListingForm({...listingForm, quantity: e.target.value})} />
                      </div>
                      <div className="form-group">
                        <label>Unit *</label>
                        <select required className="form-input" value={listingForm.unit}
                          onChange={(e) => setListingForm({...listingForm, unit: e.target.value})}>
                          <option value="kg">Kilogram (kg)</option>
                          <option value="quintal">Quintal</option>
                          <option value="ton">Ton</option>
                          <option value="piece">Piece</option>
                          <option value="dozen">Dozen</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Price per Unit (৳) *</label>
                        <input type="number" step="0.01" required className="form-input" value={listingForm.price_per_unit}
                          onChange={(e) => setListingForm({...listingForm, price_per_unit: e.target.value})} />
                      </div>
                      <div className="form-group">
                        <label>Harvest Date</label>
                        <input type="date" className="form-input" value={listingForm.harvest_date}
                          onChange={(e) => setListingForm({...listingForm, harvest_date: e.target.value})} />
                      </div>
                      <div className="form-group">
                        <label>Farm Location *</label>
                        <input type="text" required className="form-input" value={listingForm.location}
                          onChange={(e) => setListingForm({...listingForm, location: e.target.value})} 
                          placeholder="Village, District, State" />
                      </div>
                      <div className="form-group">
                        <label>Image URL</label>
                        <input type="url" className="form-input" value={listingForm.image_url}
                          onChange={(e) => setListingForm({...listingForm, image_url: e.target.value})}
                          placeholder="https://example.com/crop-image.jpg" />
                      </div>
                    </div>
                    <div className="form-group" style={{ marginTop: '1rem' }}>
                      <label>Description</label>
                      <textarea className="form-input" rows="3" value={listingForm.description}
                        onChange={(e) => setListingForm({...listingForm, description: e.target.value})}
                        placeholder="Describe your crop quality, organic certification, etc."></textarea>
                    </div>
                    <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                      <button type="submit" className="btn btn-primary">
                        {editingListing ? 'Update Listing' : 'Create Listing'}
                      </button>
                      <button type="button" onClick={() => { setShowListingForm(false); setEditingListing(null); }} 
                        className="btn btn-secondary">Cancel</button>
                    </div>
                  </form>
                </div>
              )}

              {/* Listings Grid */}
              {listings.length === 0 ? (
                <p>No listings yet. Create your first listing to sell your crops!</p>
              ) : (
                <div className="grid grid-3" style={{ marginTop: '1rem' }}>
                  {listings.map(listing => (
                    <div key={listing.id} className="product-card">
                      {listing.image_url && (
                        <img src={listing.image_url} alt={listing.crop_name} 
                          style={{ width: '100%', height: '180px', objectFit: 'cover', borderRadius: '8px 8px 0 0' }} />
                      )}
                      <div className="product-info">
                        <h3 className="product-title">{listing.crop_name}</h3>
                        <span className="badge badge-vendor">{listing.category}</span>
                        <p className="product-price">৳{listing.price_per_unit}/{listing.unit}</p>
                        <p>Quantity: {listing.quantity} {listing.unit}</p>
                        {listing.location && <p>📍 {listing.location}</p>}
                        <span className={`badge ${listing.is_available ? 'badge-farmer' : 'badge-admin'}`}>
                          {listing.is_available ? 'Available' : 'Sold Out'}
                        </span>
                        <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
                          <button onClick={() => handleEditListing(listing)} className="btn btn-secondary" style={{ flex: 1 }}>
                            Edit
                          </button>
                          <button onClick={() => handleDeleteListing(listing.id)} className="btn btn-secondary" 
                            style={{ flex: 1, background: '#ef4444', color: 'white' }}>
                            Delete
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'costs' && (
          <div>
            <div className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h2 className="card-title">Cost Tracking & Profit Analysis</h2>
                <button onClick={() => setShowCostForm(true)} className="btn btn-primary">
                  + Add Cost Entry
                </button>
              </div>

              {/* Cost Entry Form */}
              {showCostForm && (
                <div className="card" style={{ background: '#f9fafb', padding: '1.5rem', marginBottom: '2rem' }}>
                  <h3>Add New Cost Entry</h3>
                  <form onSubmit={handleCostSubmit}>
                    <div className="grid grid-2" style={{ gap: '1rem' }}>
                      <div className="form-group">
                        <label>Cost Type *</label>
                        <select required className="form-input" value={costForm.cost_type}
                          onChange={(e) => setCostForm({...costForm, cost_type: e.target.value})}>
                          <option value="seed">Seeds</option>
                          <option value="fertilizer">Fertilizer</option>
                          <option value="pesticide">Pesticide</option>
                          <option value="labor">Labor</option>
                          <option value="equipment">Equipment</option>
                          <option value="irrigation">Irrigation</option>
                          <option value="other">Other</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Crop/Season Name *</label>
                        <input type="text" required className="form-input" value={costForm.crop_name}
                          onChange={(e) => setCostForm({...costForm, crop_name: e.target.value})}
                          placeholder="e.g., Rice - Kharif 2024" />
                      </div>
                      <div className="form-group">
                        <label>Season</label>
                        <select className="form-input" value={costForm.season}
                          onChange={(e) => setCostForm({...costForm, season: e.target.value})}>
                          <option value="">Select season</option>
                          <option value="Kharif">Kharif (June-Oct)</option>
                          <option value="Rabi">Rabi (Nov-March)</option>
                          <option value="Zaid">Zaid (April-June)</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Amount (৳) *</label>
                        <input type="number" step="0.01" required className="form-input" value={costForm.amount}
                          onChange={(e) => setCostForm({...costForm, amount: e.target.value})} />
                      </div>
                      <div className="form-group">
                        <label>Date *</label>
                        <input type="date" required className="form-input" value={costForm.date}
                          onChange={(e) => setCostForm({...costForm, date: e.target.value})} />
                      </div>
                      <div className="form-group">
                        <label>Notes</label>
                        <input type="text" className="form-input" value={costForm.notes}
                          onChange={(e) => setCostForm({...costForm, notes: e.target.value})}
                          placeholder="Additional details" />
                      </div>
                    </div>
                    <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                      <button type="submit" className="btn btn-primary">Add Cost Entry</button>
                      <button type="button" onClick={() => setShowCostForm(false)} className="btn btn-secondary">
                        Cancel
                      </button>
                    </div>
                  </form>
                </div>
              )}

              {/* Cost Summary */}
              {costs.length > 0 && (
                <div className="card" style={{ background: '#f0fdf4', marginBottom: '2rem', padding: '1rem' }}>
                  <h3>Summary</h3>
                  <div className="grid grid-3" style={{ gap: '1rem', marginTop: '1rem' }}>
                    <div>
                      <strong>Total Costs:</strong>
                      <p style={{ fontSize: '1.5rem', color: '#ef4444', fontWeight: 'bold' }}>
                        ৳{costs.reduce((sum, r) => sum + r.costs.total, 0).toFixed(2)}
                      </p>
                    </div>
                    <div>
                      <strong>Total Revenue:</strong>
                      <p style={{ fontSize: '1.5rem', color: '#10b981', fontWeight: 'bold' }}>
                        ৳{costs.reduce((sum, r) => sum + r.revenue, 0).toFixed(2)}
                      </p>
                    </div>
                    <div>
                      <strong>Net Profit/Loss:</strong>
                      <p style={{ 
                        fontSize: '1.5rem', 
                        color: costs.reduce((sum, r) => sum + r.profit_loss, 0) >= 0 ? '#10b981' : '#ef4444',
                        fontWeight: 'bold' 
                      }}>
                        ৳{costs.reduce((sum, r) => sum + r.profit_loss, 0).toFixed(2)}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Cost Records Table */}
              {costs.length === 0 ? (
                <p>No cost records yet. Start tracking your expenses!</p>
              ) : (
                <div style={{ overflowX: 'auto' }}>
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Crop/Season</th>
                        <th>Season</th>
                        <th>Year</th>
                        <th>Seed</th>
                        <th>Fertilizer</th>
                        <th>Labor</th>
                        <th>Equipment</th>
                        <th>Other</th>
                        <th>Total Cost</th>
                        <th>Revenue</th>
                        <th>Profit/Loss</th>
                      </tr>
                    </thead>
                    <tbody>
                      {costs.map(record => (
                        <tr key={record.id}>
                          <td><strong>{record.crop_name}</strong></td>
                          <td>{record.season || '-'}</td>
                          <td>{record.year}</td>
                          <td>৳{record.costs.seed}</td>
                          <td>৳{record.costs.fertilizer}</td>
                          <td>৳{record.costs.labor}</td>
                          <td>৳{record.costs.equipment}</td>
                          <td>৳{record.costs.other}</td>
                          <td><strong>৳{record.costs.total}</strong></td>
                          <td style={{ color: '#10b981' }}>৳{record.revenue}</td>
                          <td style={{ 
                            color: record.profit_loss >= 0 ? '#10b981' : '#ef4444',
                            fontWeight: 'bold' 
                          }}>
                            ৳{record.profit_loss}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'labor' && (
          <div>
            <div className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                <h2 className="card-title">Labor Management</h2>
                <button onClick={() => setShowLaborForm(true)} className="btn btn-primary">
                  + Post Job Requirement
                </button>
              </div>

              {/* Labor Posting Form */}
              {showLaborForm && (
                <div className="card" style={{ background: '#f9fafb', padding: '1.5rem', marginBottom: '2rem' }}>
                  <h3>{editingLaborPosting ? 'Edit Labor Posting' : 'Create Labor Posting'}</h3>
                  <form onSubmit={handleLaborSubmit}>
                    <div className="grid grid-2" style={{ gap: '1rem' }}>
                      <div className="form-group">
                        <label>Job Title *</label>
                        <input type="text" required className="form-input" value={laborForm.job_title}
                          onChange={(e) => setLaborForm({...laborForm, job_title: e.target.value})}
                          placeholder="e.g., Farmhand for Harvest" />
                      </div>
                      <div className="form-group">
                        <label>Work Type *</label>
                        <select required className="form-input" value={laborForm.work_type}
                          onChange={(e) => setLaborForm({...laborForm, work_type: e.target.value})}>
                          <option value="">Select type</option>
                          <option value="planting">Planting</option>
                          <option value="harvesting">Harvesting</option>
                          <option value="weeding">Weeding</option>
                          <option value="irrigation">Irrigation</option>
                          <option value="pesticide_application">Pesticide Application</option>
                          <option value="general">General Farm Work</option>
                          <option value="other">Other</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Number of Laborers Needed *</label>
                        <input type="number" required min="1" className="form-input" value={laborForm.laborers_needed}
                          onChange={(e) => setLaborForm({...laborForm, laborers_needed: e.target.value})} />
                      </div>
                      <div className="form-group">
                        <label>Start Date *</label>
                        <input type="date" required className="form-input" value={laborForm.start_date}
                          onChange={(e) => setLaborForm({...laborForm, start_date: e.target.value})} />
                      </div>
                      <div className="form-group">
                        <label>End Date *</label>
                        <input type="date" required className="form-input" value={laborForm.end_date}
                          onChange={(e) => setLaborForm({...laborForm, end_date: e.target.value})} />
                      </div>
                      <div className="form-group">
                        <label>Wage Type *</label>
                        <select required className="form-input" value={laborForm.wage_type}
                          onChange={(e) => setLaborForm({...laborForm, wage_type: e.target.value})}>
                          <option value="per_day">Per Day</option>
                          <option value="total">Total Contract</option>
                        </select>
                      </div>
                      <div className="form-group">
                        <label>Wage Amount (৳) *</label>
                        <input type="number" step="0.01" required className="form-input" value={laborForm.wage_amount}
                          onChange={(e) => setLaborForm({...laborForm, wage_amount: e.target.value})}
                          placeholder={laborForm.wage_type === 'per_day' ? 'Amount per day' : 'Total amount'} />
                      </div>
                      <div className="form-group">
                        <label>Work Location *</label>
                        <input type="text" required className="form-input" value={laborForm.location}
                          onChange={(e) => setLaborForm({...laborForm, location: e.target.value})}
                          placeholder="Village, District" />
                      </div>
                    </div>
                    <div className="form-group" style={{ marginTop: '1rem' }}>
                      <label>Job Description *</label>
                      <textarea required className="form-input" rows="3" value={laborForm.description}
                        onChange={(e) => setLaborForm({...laborForm, description: e.target.value})}
                        placeholder="Describe the work requirements, skills needed, working hours, etc."></textarea>
                    </div>
                    <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                      <button type="submit" className="btn btn-primary">{editingLaborPosting ? 'Update Job Posting' : 'Create Job Posting'}</button>
                      <button type="button" onClick={() => { setShowLaborForm(false); setEditingLaborPosting(null); }} className="btn btn-secondary">
                        Cancel
                      </button>
                    </div>
                  </form>
                </div>
              )}

              {/* Labor Postings List */}
              {laborPostings.length === 0 ? (
                <p>No labor postings yet. Create your first job posting!</p>
              ) : (
                <div style={{ display: 'grid', gap: '1rem' }}>
                  {laborPostings.map(posting => (
                    <div key={posting.id} className="card" style={{ background: '#fefce8', border: '2px solid #eab308' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                        <div style={{ flex: 1 }}>
                          <h3 style={{ marginBottom: '0.5rem' }}>{posting.job_title}</h3>
                          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
                            <span className="badge badge-vendor">{posting.work_type}</span>
                            <span className={`badge ${posting.status === 'open' ? 'badge-farmer' : 'badge-admin'}`}>
                              {posting.status}
                            </span>
                          </div>
                          <p style={{ marginBottom: '0.5rem' }}><strong>Description:</strong> {posting.description}</p>
                          <p style={{ marginBottom: '0.5rem' }}>
                            <strong>Laborers Needed:</strong> {posting.laborers_needed || 'Not specified'}
                          </p>
                          <p style={{ marginBottom: '0.5rem' }}>
                            <strong>Duration:</strong> {new Date(posting.start_date).toLocaleDateString()} - {new Date(posting.end_date).toLocaleDateString()}
                          </p>
                          <p style={{ marginBottom: '0.5rem' }}>
                            <strong>Wage:</strong> ৳{posting.wage_per_day || posting.total_wage} 
                            {posting.wage_per_day ? ' per day' : ' (total)'}
                          </p>
                          <p style={{ marginBottom: '0.5rem' }}>
                            <strong>Location:</strong> 📍 {posting.location || 'Not specified'}
                          </p>
                          {posting.labor_name && (
                            <p style={{ marginTop: '1rem', padding: '0.5rem', background: '#fff', borderRadius: '4px' }}>
                              <strong>Hired:</strong> {posting.labor_name} ({posting.labor_phone})
                            </p>
                          )}
                          <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem', flexWrap: 'wrap' }}>
                            <button onClick={() => handleEditLaborPosting(posting)} className="btn btn-secondary">
                              Edit
                            </button>
                            {posting.status !== 'completed' && posting.status !== 'cancelled' && (
                              <>
                                <button onClick={() => updateLaborStatus(posting.id, 'active')} className="btn btn-primary">
                                  Mark Active
                                </button>
                                <button onClick={() => updateLaborStatus(posting.id, 'completed')} className="btn btn-secondary">
                                  End Posting
                                </button>
                              </>
                            )}
                            {posting.status !== 'cancelled' && (
                              <button onClick={() => updateLaborStatus(posting.id, 'cancelled')} className="btn btn-secondary" style={{ background: '#ef4444', color: 'white' }}>
                                Cancel Posting
                              </button>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'orders' && (
          <div>
            <div className="card">
              <h2 className="card-title">Order Management</h2>
              {farmerOrders.length === 0 ? (
                <p>No orders yet for your listings.</p>
              ) : (
                <div style={{ display: 'grid', gap: '1rem', marginTop: '1rem' }}>
                  {farmerOrders.map(order => (
                    <div key={order.id} className="card" style={{ background: '#f9fafb', border: '2px solid #e5e7eb' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                        <div>
                          <h3 style={{ margin: 0 }}>Order #{order.id}</h3>
                          <p style={{ margin: '0.25rem 0', color: '#64748b' }}>
                            📅 {new Date(order.created_at).toLocaleString()}
                          </p>
                          <p style={{ margin: '0.25rem 0' }}>
                            <strong>Product:</strong> {order.product_name || 'Crop Listing'}
                          </p>
                          <p style={{ margin: '0.25rem 0' }}>
                            <strong>Buyer:</strong> {order.buyer_name} ({order.buyer_email})
                          </p>
                        </div>
                        <div style={{ textAlign: 'right' }}>
                          <p style={{ margin: '0.25rem 0' }}>
                            <strong>Qty:</strong> {order.quantity}
                          </p>
                          <p style={{ margin: '0.25rem 0' }}>
                            <strong>Total:</strong> ৳{order.total_price}
                          </p>
                          <span className={`badge ${
                            order.status === 'completed' ? 'badge-success' :
                            order.status === 'cancelled' ? 'badge-danger' :
                            'badge-farmer'
                          }`}>
                            {order.status.toUpperCase()}
                          </span>
                        </div>
                      </div>
                      <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
                        <span style={{ fontSize: '0.9rem', color: '#64748b' }}>Update Status:</span>
                        <button onClick={() => updateOrderStatus(order.id, 'pending')} className="btn btn-secondary">Pending</button>
                        <button onClick={() => updateOrderStatus(order.id, 'confirmed')} className="btn btn-secondary">Confirmed</button>
                        <button onClick={() => updateOrderStatus(order.id, 'in_progress')} className="btn btn-secondary">In Progress</button>
                        <button onClick={() => updateOrderStatus(order.id, 'completed')} className="btn btn-primary">Delivered</button>
                        <button onClick={() => updateOrderStatus(order.id, 'cancelled')} className="btn btn-secondary" style={{ background: '#ef4444', color: 'white' }}>Cancel</button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'profile' && (
          <ProfileEditor user={user} onProfileUpdate={(updatedUser) => {
            // Update local user state if needed
            localStorage.setItem('user', JSON.stringify(updatedUser));
          }} />
        )}
      </div>
    </div>
  );
}

export default FarmerPortal;
