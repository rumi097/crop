import React, { useState, useRef } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5001';

function DiseaseRecognition() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    processFile(file);
  };

  const processFile = (file) => {
    if (file) {
      // Validate file type
      const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp'];
      if (!validTypes.includes(file.type)) {
        setError('Please upload a valid image file (JPG, PNG, or BMP)');
        return;
      }

      // Validate file size (max 16MB)
      if (file.size > 16 * 1024 * 1024) {
        setError('File size must be less than 16MB');
        return;
      }

      setSelectedFile(file);
      setError(null);
      setResult(null);

      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    
    const file = e.dataTransfer.files[0];
    processFile(file);
  };

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
      setError('Please select an image file');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('image', selectedFile);

      const response = await axios.post(
        `${API_URL}/api/disease-recognition`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      if (response.data.status === 'success') {
        setResult(response.data);
      } else {
        setError(response.data.error || 'An error occurred');
      }
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.error || err.message || 'Failed to analyze image');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const getConditionIcon = (condition) => {
    const icons = {
      'Healthy': '✅',
      'Contaminated': '⚠️',
      'Expired': '⏰',
      'Fake': '🚫',
      'Damaged': '💔'
    };
    return icons[condition] || '❓';
  };

  const getConditionColor = (condition) => {
    const colors = {
      'Healthy': '#27ae60',
      'Contaminated': '#f39c12',
      'Expired': '#e74c3c',
      'Fake': '#9b59b6',
      'Damaged': '#e67e22'
    };
    return colors[condition] || '#95a5a6';
  };

  const getConditionDescription = (condition) => {
    const descriptions = {
      'Healthy': 'The fertilizer is in good condition and safe to use.',
      'Contaminated': 'The fertilizer may be mixed with impurities. Use with caution.',
      'Expired': 'The fertilizer has likely expired or degraded. Not recommended for use.',
      'Fake': 'This appears to be counterfeit fertilizer. Do not use.',
      'Damaged': 'The fertilizer shows physical damage or moisture exposure. Quality may be compromised.'
    };
    return descriptions[condition] || 'Unable to determine condition.';
  };

  return (
    <div className="content-card">
      <div className="card-header">
        <h2 className="card-title">🔬 Fertilizer Quality Recognition</h2>
        <p className="card-description">
          Upload an image of fertilizer to detect its condition using AI
        </p>
      </div>

      <form className="input-form" onSubmit={handleSubmit}>
        {/* File Upload Area */}
        {!previewUrl ? (
          <div
            className={`upload-area ${dragOver ? 'dragover' : ''}`}
            onClick={handleUploadClick}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <div className="upload-icon">📸</div>
            <div className="upload-text">
              Click to upload or drag and drop
            </div>
            <div className="upload-hint">
              Supported formats: JPG, PNG, BMP (Max 16MB)
            </div>
            <input
              ref={fileInputRef}
              type="file"
              className="file-input"
              accept="image/jpeg,image/jpg,image/png,image/bmp"
              onChange={handleFileSelect}
            />
          </div>
        ) : (
          <div className="image-preview">
            <img 
              src={previewUrl} 
              alt="Preview" 
              className="preview-image"
            />
            <div style={{ marginTop: '15px' }}>
              <button
                type="button"
                className="remove-image"
                onClick={resetForm}
              >
                Remove Image
              </button>
            </div>
          </div>
        )}

        {/* Submit Button */}
        {selectedFile && !result && (
          <button 
            type="submit" 
            className="submit-button"
            style={{ marginTop: '20px' }}
            disabled={loading}
          >
            {loading ? 'Analyzing Image...' : 'Analyze Fertilizer Quality'}
          </button>
        )}
      </form>

      {/* Loading State */}
      {loading && (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Analyzing fertilizer image using CNN model...</p>
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
            <div className="result-icon" style={{ fontSize: '5rem' }}>
              {result.disease && result.disease.toLowerCase().includes('healthy') ? '✅' : '🌿'}
            </div>
            <h3 className="result-title">Plant Disease Detection</h3>
            
            {result.crop && (
              <div style={{
                background: '#3498db',
                color: 'white',
                padding: '8px 20px',
                borderRadius: '20px',
                display: 'inline-block',
                marginBottom: '10px',
                fontSize: '0.9rem',
                fontWeight: '600'
              }}>
                Crop: {result.crop}
              </div>
            )}
            
            <div 
              className="result-value"
              style={{ color: result.disease && result.disease.toLowerCase().includes('healthy') ? '#27ae60' : '#e74c3c' }}
            >
              {result.disease || result.prediction}
            </div>
            <div 
              className="result-confidence"
              style={{ background: result.disease && result.disease.toLowerCase().includes('healthy') ? '#27ae60' : '#e74c3c' }}
            >
              Confidence: {(result.confidence * 100).toFixed(2)}%
            </div>
            <div className="confidence-bar">
              <div 
                className="confidence-fill"
                style={{ 
                  width: `${result.confidence * 100}%`,
                  background: result.disease && result.disease.toLowerCase().includes('healthy') ? '#27ae60' : '#e74c3c'
                }}
              >
                {(result.confidence * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          {/* Condition Description */}
          <div style={{
            background: 'white',
            padding: '20px',
            borderRadius: '10px',
            marginTop: '20px',
            textAlign: 'center'
          }}>
            <p style={{ 
              fontSize: '1.1rem', 
              lineHeight: '1.6', 
              color: '#2c3e50' 
            }}>
              {getConditionDescription(result.prediction)}
            </p>
          </div>

          {/* All Predictions */}
          {result.all_predictions && (
            <div className="top-predictions">
              <h4 className="predictions-title">All Predictions</h4>
              {Object.entries(result.all_predictions)
                .sort((a, b) => b[1] - a[1])
                .map(([condition, confidence], index) => (
                  <div key={index} className="prediction-item">
                    <span className="prediction-name">
                      {getConditionIcon(condition)} {condition}
                    </span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                      <div style={{ 
                        width: '150px', 
                        height: '8px', 
                        background: '#ecf0f1',
                        borderRadius: '4px',
                        overflow: 'hidden'
                      }}>
                        <div style={{
                          width: `${confidence * 100}%`,
                          height: '100%',
                          background: getConditionColor(condition),
                          transition: 'width 0.5s ease'
                        }}></div>
                      </div>
                      <span 
                        className="prediction-confidence"
                        style={{ color: getConditionColor(condition) }}
                      >
                        {(confidence * 100).toFixed(2)}%
                      </span>
                    </div>
                  </div>
                ))}
            </div>
          )}

          {/* Recommendations */}
          <div style={{
            marginTop: '25px',
            padding: '20px',
            background: '#fff3cd',
            border: '2px solid #ffc107',
            borderRadius: '10px'
          }}>
            <h4 style={{ 
              color: '#856404', 
              marginBottom: '15px',
              fontSize: '1.2rem'
            }}>
              💡 Recommendations
            </h4>
            {result.prediction === 'Healthy' && (
              <ul style={{ 
                color: '#856404', 
                lineHeight: '1.8',
                paddingLeft: '20px'
              }}>
                <li>This fertilizer is safe to use as per guidelines</li>
                <li>Store in a cool, dry place away from direct sunlight</li>
                <li>Keep away from moisture and water</li>
              </ul>
            )}
            {result.prediction === 'Contaminated' && (
              <ul style={{ 
                color: '#856404', 
                lineHeight: '1.8',
                paddingLeft: '20px'
              }}>
                <li>Check for visible impurities or foreign materials</li>
                <li>Consider testing at an agricultural lab</li>
                <li>Use with caution or consult an agricultural expert</li>
              </ul>
            )}
            {(result.prediction === 'Expired' || result.prediction === 'Damaged') && (
              <ul style={{ 
                color: '#856404', 
                lineHeight: '1.8',
                paddingLeft: '20px'
              }}>
                <li>Do not use this fertilizer</li>
                <li>Dispose of according to local regulations</li>
                <li>Purchase fresh, properly stored fertilizer</li>
              </ul>
            )}
            {result.prediction === 'Fake' && (
              <ul style={{ 
                color: '#856404', 
                lineHeight: '1.8',
                paddingLeft: '20px'
              }}>
                <li>Do not use this product</li>
                <li>Report to local agricultural authorities</li>
                <li>Purchase from authorized dealers only</li>
                <li>Check for proper labeling and certifications</li>
              </ul>
            )}
          </div>

          {/* Action Buttons */}
          <div style={{ marginTop: '25px', display: 'flex', gap: '15px' }}>
            <button
              onClick={resetForm}
              className="submit-button"
              style={{ background: '#3498db' }}
            >
              Analyze Another Image
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default DiseaseRecognition;
