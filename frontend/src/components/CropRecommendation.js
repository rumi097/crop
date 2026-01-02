import React, { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function CropRecommendation() {
  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    temperature: '',
    humidity: '',
    pH: '',
    rainfall: ''
  });
  
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
      // Validate inputs
      const data = {
        N: parseFloat(formData.N),
        P: parseFloat(formData.P),
        K: parseFloat(formData.K),
        temperature: parseFloat(formData.temperature),
        humidity: parseFloat(formData.humidity),
        pH: parseFloat(formData.pH),
        rainfall: parseFloat(formData.rainfall)
      };

      // Check for NaN values
      if (Object.values(data).some(val => isNaN(val))) {
        throw new Error('Please fill in all fields with valid numbers');
      }

      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_URL}/api/farmer/crop-recommendation`, data, {
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
      temperature: '',
      humidity: '',
      pH: '',
      rainfall: ''
    });
    setResult(null);
    setError(null);
  };

  return (
    <div className="content-card">
      <div className="card-header">
        <h2 className="card-title">🌱 Crop Recommendation</h2>
        <p className="card-description">
          Get AI-powered crop recommendations based on soil and climate parameters
        </p>
      </div>

      <form className="input-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          {/* Nitrogen */}
          <div className="form-group">
            <label className="form-label">Nitrogen (N) - kg/ha</label>
            <input
              type="number"
              name="N"
              className="form-input"
              value={formData.N}
              onChange={handleInputChange}
              placeholder="e.g., 90"
              min="0"
              max="300"
              step="0.1"
              required
            />
            <span className="form-help">Range: 0-300</span>
          </div>

          {/* Phosphorus */}
          <div className="form-group">
            <label className="form-label">Phosphorus (P) - kg/ha</label>
            <input
              type="number"
              name="P"
              className="form-input"
              value={formData.P}
              onChange={handleInputChange}
              placeholder="e.g., 42"
              min="0"
              max="200"
              step="0.1"
              required
            />
            <span className="form-help">Range: 0-200</span>
          </div>

          {/* Potassium */}
          <div className="form-group">
            <label className="form-label">Potassium (K) - kg/ha</label>
            <input
              type="number"
              name="K"
              className="form-input"
              value={formData.K}
              onChange={handleInputChange}
              placeholder="e.g., 43"
              min="0"
              max="300"
              step="0.1"
              required
            />
            <span className="form-help">Range: 0-300</span>
          </div>

          {/* Temperature */}
          <div className="form-group">
            <label className="form-label">Temperature - °C</label>
            <input
              type="number"
              name="temperature"
              className="form-input"
              value={formData.temperature}
              onChange={handleInputChange}
              placeholder="e.g., 20.87"
              min="0"
              max="50"
              step="0.01"
              required
            />
            <span className="form-help">Average temperature</span>
          </div>

          {/* Humidity */}
          <div className="form-group">
            <label className="form-label">Humidity - %</label>
            <input
              type="number"
              name="humidity"
              className="form-input"
              value={formData.humidity}
              onChange={handleInputChange}
              placeholder="e.g., 82.0"
              min="0"
              max="100"
              step="0.1"
              required
            />
            <span className="form-help">Relative humidity</span>
          </div>

          {/* pH */}
          <div className="form-group">
            <label className="form-label">pH Value</label>
            <input
              type="number"
              name="pH"
              className="form-input"
              value={formData.pH}
              onChange={handleInputChange}
              placeholder="e.g., 6.5"
              min="0"
              max="14"
              step="0.1"
              required
            />
            <span className="form-help">Soil pH level</span>
          </div>

          {/* Rainfall */}
          <div className="form-group">
            <label className="form-label">Rainfall - mm</label>
            <input
              type="number"
              name="rainfall"
              className="form-input"
              value={formData.rainfall}
              onChange={handleInputChange}
              placeholder="e.g., 202.9"
              min="0"
              max="500"
              step="0.1"
              required
            />
            <span className="form-help">Annual rainfall</span>
          </div>
        </div>

        <button 
          type="submit" 
          className="submit-button"
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Get Crop Recommendation'}
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
          <p>Analyzing soil and climate parameters...</p>
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
            <div className="result-icon">🌾</div>
            <h3 className="result-title">Recommended Crop</h3>
            <div className="result-value">
              {result.prediction.charAt(0).toUpperCase() + result.prediction.slice(1)}
            </div>
            <div className="result-confidence">
              Confidence: {(result.confidence * 100).toFixed(2)}%
            </div>
            <div className="confidence-bar">
              <div 
                className="confidence-fill" 
                style={{ width: `${result.confidence * 100}%` }}
              >
                {(result.confidence * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          {/* Top 3 Predictions */}
          {result.top_3_predictions && (
            <div className="top-predictions">
              <h4 className="predictions-title">Top 3 Suitable Crops</h4>
              {result.top_3_predictions.map((pred, index) => (
                <div key={index} className="prediction-item">
                  <span className="prediction-name">
                    {index + 1}. {pred.crop.charAt(0).toUpperCase() + pred.crop.slice(1)}
                  </span>
                  <span className="prediction-confidence">
                    {(pred.confidence * 100).toFixed(2)}%
                  </span>
                </div>
              ))}
            </div>
          )}

          {/* Input Summary */}
          <div className="top-predictions" style={{ marginTop: '25px' }}>
            <h4 className="predictions-title">Input Parameters</h4>
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '15px',
              background: 'white',
              padding: '20px',
              borderRadius: '10px'
            }}>
              <div>
                <strong>Nitrogen:</strong> {result.input_parameters.N} kg/ha
              </div>
              <div>
                <strong>Phosphorus:</strong> {result.input_parameters.P} kg/ha
              </div>
              <div>
                <strong>Potassium:</strong> {result.input_parameters.K} kg/ha
              </div>
              <div>
                <strong>Temperature:</strong> {result.input_parameters.temperature}°C
              </div>
              <div>
                <strong>Humidity:</strong> {result.input_parameters.humidity}%
              </div>
              <div>
                <strong>pH:</strong> {result.input_parameters.pH}
              </div>
              <div>
                <strong>Rainfall:</strong> {result.input_parameters.rainfall} mm
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default CropRecommendation;
