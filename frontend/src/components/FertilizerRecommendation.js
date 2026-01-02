import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function FertilizerRecommendation() {
  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    crop: 'wheat',
    soil_type: 'loamy'
  });
  
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [availableCrops, setAvailableCrops] = useState([]);
  const [soilTypes, setSoilTypes] = useState([]);

  // Fetch available crops and soil types on component mount
  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const [cropsRes, soilRes] = await Promise.all([
          axios.get(`${API_URL}/api/available-crops`),
          axios.get(`${API_URL}/api/soil-types`)
        ]);
        
        if (cropsRes.data.crops) {
          setAvailableCrops(cropsRes.data.crops);
        }
        if (soilRes.data.soil_types) {
          setSoilTypes(soilRes.data.soil_types);
        }
      } catch (err) {
        console.error('Error fetching options:', err);
      }
    };

    fetchOptions();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = {
        N: parseFloat(formData.N),
        P: parseFloat(formData.P),
        K: parseFloat(formData.K),
        crop: formData.crop,
        soil_type: formData.soil_type
      };

      if (isNaN(data.N) || isNaN(data.P) || isNaN(data.K)) {
        throw new Error('Please fill in all nutrient fields with valid numbers');
      }

      const token = localStorage.getItem('token');
      const fertData = {
        soil_type: data.soil_type,
        crop_type: data.crop,
        N: data.N,
        P: data.P,
        K: data.K
      };
      
      const response = await axios.post(`${API_URL}/api/farmer/fertilizer-recommendation`, fertData, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });
      
      if (response.data.success) {
        setResult(response.data);
      } else {
        setError(response.data.error || 'An error occurred');
      }
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.error || err.message || 'Failed to get recommendation');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      N: '',
      P: '',
      K: '',
      crop: 'wheat',
      soil_type: 'loamy'
    });
    setResult(null);
    setError(null);
  };

  const getNutrientStatus = (status) => {
    const statusColors = {
      'Adequate': '#27ae60',
      'Deficient': '#e74c3c',
      'Excess': '#f39c12'
    };
    return statusColors[status] || '#95a5a6';
  };

  return (
    <div className="content-card">
      <div className="card-header">
        <h2 className="card-title">💧 Fertilizer Recommendation</h2>
        <p className="card-description">
          Get personalized fertilizer recommendations based on soil nutrient analysis
        </p>
      </div>

      <form className="input-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          {/* Nitrogen */}
          <div className="form-group">
            <label className="form-label">Current Nitrogen (N) - kg/ha</label>
            <input
              type="number"
              name="N"
              className="form-input"
              value={formData.N}
              onChange={handleInputChange}
              placeholder="e.g., 30"
              min="0"
              max="300"
              step="0.1"
              required
            />
            <span className="form-help">Current soil nitrogen level</span>
          </div>

          {/* Phosphorus */}
          <div className="form-group">
            <label className="form-label">Current Phosphorus (P) - kg/ha</label>
            <input
              type="number"
              name="P"
              className="form-input"
              value={formData.P}
              onChange={handleInputChange}
              placeholder="e.g., 20"
              min="0"
              max="200"
              step="0.1"
              required
            />
            <span className="form-help">Current soil phosphorus level</span>
          </div>

          {/* Potassium */}
          <div className="form-group">
            <label className="form-label">Current Potassium (K) - kg/ha</label>
            <input
              type="number"
              name="K"
              className="form-input"
              value={formData.K}
              onChange={handleInputChange}
              placeholder="e.g., 25"
              min="0"
              max="300"
              step="0.1"
              required
            />
            <span className="form-help">Current soil potassium level</span>
          </div>

          {/* Crop Type */}
          <div className="form-group">
            <label className="form-label">Crop Type</label>
            <select
              name="crop"
              className="form-select"
              value={formData.crop}
              onChange={handleInputChange}
              required
            >
              {availableCrops.length > 0 ? (
                availableCrops.map(crop => (
                  <option key={crop} value={crop}>
                    {crop.charAt(0).toUpperCase() + crop.slice(1)}
                  </option>
                ))
              ) : (
                <>
                  <option value="wheat">Wheat</option>
                  <option value="rice">Rice</option>
                  <option value="maize">Maize</option>
                  <option value="cotton">Cotton</option>
                  <option value="sugarcane">Sugarcane</option>
                  <option value="groundnut">Groundnut</option>
                  <option value="pulses">Pulses</option>
                  <option value="vegetables">Vegetables</option>
                  <option value="fruits">Fruits</option>
                </>
              )}
            </select>
            <span className="form-help">Select the crop you want to grow</span>
          </div>

          {/* Soil Type */}
          <div className="form-group">
            <label className="form-label">Soil Type</label>
            <select
              name="soil_type"
              className="form-select"
              value={formData.soil_type}
              onChange={handleInputChange}
              required
            >
              {soilTypes.length > 0 ? (
                soilTypes.map(soil => (
                  <option key={soil} value={soil}>
                    {soil.charAt(0).toUpperCase() + soil.slice(1)}
                  </option>
                ))
              ) : (
                <>
                  <option value="sandy">Sandy</option>
                  <option value="loamy">Loamy</option>
                  <option value="clayey">Clayey</option>
                  <option value="silty">Silty</option>
                  <option value="peaty">Peaty</option>
                </>
              )}
            </select>
            <span className="form-help">Your soil type</span>
          </div>
        </div>

        <button 
          type="submit" 
          className="submit-button"
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Get Fertilizer Recommendation'}
        </button>

        {result && (
          <button 
            type="button" 
            onClick={resetForm}
            className="submit-button"
            style={{ marginTop: '10px', background: '#95a5a6' }}
          >
            Reset Form
          </button>
        )}
      </form>

      {/* Loading State */}
      {loading && (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Analyzing soil nutrient levels...</p>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Result Display */}
      {result && (
        <div className="result-card">
          <div className="result-header">
            <div className="result-icon">🌿</div>
            <h3 className="result-title">Recommended Fertilizer</h3>
            <div className="result-value">
              {result.recommendation.fertilizer}
            </div>
            {result.recommendation.amount && (
              <div className="result-confidence" style={{ background: '#3498db' }}>
                Amount: {result.recommendation.amount}
              </div>
            )}
          </div>

          {/* Recommendation Details */}
          <div className="top-predictions" style={{ marginTop: '25px' }}>
            <h4 className="predictions-title">Recommendation Details</h4>
            <div style={{
              background: 'white',
              padding: '20px',
              borderRadius: '10px',
              marginBottom: '15px'
            }}>
              <p style={{ fontSize: '1.1rem', lineHeight: '1.6', color: '#2c3e50' }}>
                <strong>Reason:</strong> {result.recommendation.reason}
              </p>
              {result.recommendation.application && (
                <p style={{ 
                  fontSize: '1rem', 
                  lineHeight: '1.6', 
                  color: '#34495e',
                  marginTop: '15px',
                  paddingTop: '15px',
                  borderTop: '1px solid #ecf0f1'
                }}>
                  <strong>📋 Application Method:</strong> {result.recommendation.application}
                </p>
              )}
              {result.recommendation.note && (
                <p style={{ 
                  fontSize: '0.95rem', 
                  lineHeight: '1.6', 
                  color: '#7f8c8d',
                  marginTop: '15px',
                  paddingTop: '15px',
                  borderTop: '1px solid #ecf0f1',
                  fontStyle: 'italic'
                }}>
                  <strong>ℹ️ Note:</strong> {result.recommendation.note}
                </p>
              )}
            </div>
          </div>

          {/* Nutrient Analysis */}
          {result.nutrient_analysis && (
            <div className="top-predictions">
              <h4 className="predictions-title">Soil Nutrient Analysis</h4>
              
              {/* Current vs Required */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '15px',
                marginBottom: '20px'
              }}>
                {['N', 'P', 'K'].map(nutrient => (
                  <div key={nutrient} style={{
                    background: 'white',
                    padding: '20px',
                    borderRadius: '10px',
                    textAlign: 'center'
                  }}>
                    <h5 style={{ 
                      color: '#2c3e50', 
                      marginBottom: '10px',
                      fontSize: '1.2rem'
                    }}>
                      {nutrient === 'N' ? 'Nitrogen' : nutrient === 'P' ? 'Phosphorus' : 'Potassium'}
                    </h5>
                    <div style={{ marginBottom: '15px' }}>
                      <div style={{ fontSize: '0.9rem', color: '#7f8c8d' }}>Current</div>
                      <div style={{ 
                        fontSize: '1.5rem', 
                        fontWeight: 'bold',
                        color: getNutrientStatus(result.nutrient_analysis.status[nutrient])
                      }}>
                        {result.nutrient_analysis.current_levels[nutrient]} kg/ha
                      </div>
                    </div>
                    <div style={{ marginBottom: '10px' }}>
                      <div style={{ fontSize: '0.9rem', color: '#7f8c8d' }}>Required</div>
                      <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#34495e' }}>
                        {result.nutrient_analysis.required_levels[nutrient]} kg/ha
                      </div>
                    </div>
                    <div style={{
                      padding: '8px 15px',
                      borderRadius: '20px',
                      fontSize: '0.9rem',
                      fontWeight: '600',
                      color: 'white',
                      background: getNutrientStatus(result.nutrient_analysis.status[nutrient])
                    }}>
                      {result.nutrient_analysis.status[nutrient]}
                    </div>
                    {result.nutrient_analysis.deficit[nutrient] > 0 && (
                      <div style={{ 
                        marginTop: '10px', 
                        fontSize: '0.85rem', 
                        color: '#e74c3c',
                        fontWeight: '600'
                      }}>
                        Deficit: {result.nutrient_analysis.deficit[nutrient].toFixed(1)} kg/ha
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Deficiency Summary */}
              {result.recommendation.deficiencies && (
                <div style={{
                  background: 'white',
                  padding: '20px',
                  borderRadius: '10px'
                }}>
                  <h5 style={{ marginBottom: '15px', color: '#2c3e50' }}>
                    Nutrient Deficiencies (kg/ha)
                  </h5>
                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(3, 1fr)',
                    gap: '15px',
                    textAlign: 'center'
                  }}>
                    <div>
                      <div style={{ fontSize: '0.9rem', color: '#7f8c8d' }}>N Deficit</div>
                      <div style={{ fontSize: '1.3rem', fontWeight: 'bold', color: '#e67e22' }}>
                        {result.recommendation.deficiencies.N.toFixed(1)}
                      </div>
                    </div>
                    <div>
                      <div style={{ fontSize: '0.9rem', color: '#7f8c8d' }}>P Deficit</div>
                      <div style={{ fontSize: '1.3rem', fontWeight: 'bold', color: '#e67e22' }}>
                        {result.recommendation.deficiencies.P.toFixed(1)}
                      </div>
                    </div>
                    <div>
                      <div style={{ fontSize: '0.9rem', color: '#7f8c8d' }}>K Deficit</div>
                      <div style={{ fontSize: '1.3rem', fontWeight: 'bold', color: '#e67e22' }}>
                        {result.recommendation.deficiencies.K.toFixed(1)}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default FertilizerRecommendation;
