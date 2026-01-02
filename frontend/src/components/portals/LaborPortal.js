import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import ProfileEditor from '../shared/ProfileEditor';
import axios from 'axios';
import '../../styles/portals/labor.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function LaborPortal({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('jobs');
  const [jobPostings, setJobPostings] = useState([]);
  const [myJobs, setMyJobs] = useState([]);
  const [earnings, setEarnings] = useState({ total: 0, thisMonth: 0, completed: 0 });

  const calculateEarnings = useCallback(() => {
    const completedJobs = myJobs.filter(j => j.status === 'completed');
    const totalEarnings = completedJobs.reduce((sum, j) => sum + (j.total_wage || j.daily_wage * j.total_days || 0), 0);
    
    const currentMonth = new Date().getMonth();
    const thisMonthEarnings = completedJobs
      .filter(j => new Date(j.created_at).getMonth() === currentMonth)
      .reduce((sum, j) => sum + (j.total_wage || j.daily_wage * j.total_days || 0), 0);

    setEarnings({
      total: totalEarnings,
      thisMonth: thisMonthEarnings,
      completed: completedJobs.length
    });
  }, [myJobs]);

  useEffect(() => {
    if (activeTab === 'jobs') fetchJobPostings();
    if (activeTab === 'myjobs') fetchMyJobs();
    if (activeTab === 'earnings') {
      fetchMyJobs();
      calculateEarnings();
    }
  }, [activeTab, calculateEarnings]);

  const fetchJobPostings = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/labor/job-postings`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setJobPostings(response.data.postings || []);
    } catch (error) {
      console.error('Error fetching job postings:', error);
    }
  };

  const fetchMyJobs = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/labor/my-jobs`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMyJobs(response.data.jobs || []);
    } catch (error) {
      console.error('Error fetching my jobs:', error);
    }
  };

  const applyForJob = async (postingId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`${API_URL}/api/labor/apply/${postingId}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Application submitted successfully!');
      fetchJobPostings();
    } catch (error) {
      alert('Application failed: ' + (error.response?.data?.error || 'Unknown error'));
    }
  };

  return (
    <div>
      <header className="header">
        <div className="header-title">👷 Labor Portal</div>
        <div className="header-nav">
          <span className="badge badge-labor">LABOR</span>
          <span>{user.full_name}</span>
          <Link to="/" className="nav-link">Home</Link>
          <button onClick={onLogout} className="btn btn-secondary">Logout</button>
        </div>
      </header>

      <div className="container">
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
          <button onClick={() => setActiveTab('jobs')} 
            className={`btn ${activeTab === 'jobs' ? 'btn-primary' : 'btn-secondary'}`}>
            💼 Available Jobs
          </button>
          <button onClick={() => setActiveTab('myjobs')} 
            className={`btn ${activeTab === 'myjobs' ? 'btn-primary' : 'btn-secondary'}`}>
            📋 My Jobs
          </button>
          <button onClick={() => setActiveTab('earnings')} 
            className={`btn ${activeTab === 'earnings' ? 'btn-primary' : 'btn-secondary'}`}>
            💰 Earnings & History
          </button>
          <button onClick={() => setActiveTab('profile')} 
            className={`btn ${activeTab === 'profile' ? 'btn-primary' : 'btn-secondary'}`}>
            👤 Profile
          </button>
        </div>

        {activeTab === 'jobs' && (
          <div>
            <div className="card" style={{ marginBottom: '1rem', background: '#eff6ff' }}>
              <h3 style={{ marginBottom: '0.5rem' }}>🔍 Find Work Opportunities</h3>
              <p style={{ margin: 0 }}>
                Browse available job postings from farmers in your area. Apply to jobs that match your skills and availability.
              </p>
            </div>

            <div className="card">
              <h2 className="card-title">💼 Available Job Postings</h2>
              {jobPostings.length === 0 ? (
                <p>No job postings available at the moment. Check back later!</p>
              ) : (
                <div className="grid grid-2">
                  {jobPostings.map(job => (
                    <div key={job.id} className="card" style={{ background: '#f9fafb' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
                        <h3 style={{ margin: 0 }}>{job.job_title}</h3>
                        <span className="badge badge-success">{job.status || 'Open'}</span>
                      </div>
                      
                      <div style={{ marginBottom: '1rem' }}>
                        <p><strong>👨‍🌾 Farmer:</strong> {job.farmer_name}</p>
                        <p><strong>📍 Location:</strong> {job.location || job.farmer_location}</p>
                        <p><strong>🔨 Work Type:</strong> {job.work_type}</p>
                        <p><strong>📅 Start Date:</strong> {new Date(job.start_date).toLocaleDateString()}</p>
                        {job.end_date && (
                          <p><strong>📅 End Date:</strong> {new Date(job.end_date).toLocaleDateString()}</p>
                        )}
                        {job.laborers_needed && (
                          <p><strong>👥 Workers Needed:</strong> {job.laborers_needed}</p>
                        )}
                        <p style={{ 
                          fontSize: '1.25rem', 
                          fontWeight: 'bold', 
                          color: '#059669', 
                          margin: '0.5rem 0' 
                        }}>
                          💵 ৳{job.daily_wage}/day
                        </p>
                      </div>
                      
                      {job.description && (
                        <p style={{ 
                          padding: '0.5rem', 
                          background: 'white', 
                          borderRadius: '4px',
                          fontSize: '0.9rem',
                          marginBottom: '1rem'
                        }}>
                          {job.description}
                        </p>
                      )}
                      
                      <button 
                        onClick={() => applyForJob(job.id)} 
                        className="btn btn-success" 
                        style={{ width: '100%' }}
                      >
                        Apply Now
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'myjobs' && (
          <div className="card">
            <h2 className="card-title">📋 My Jobs</h2>
            <p>Track your ongoing and completed work assignments</p>
            {myJobs.length === 0 ? (
              <p>No jobs yet. Start applying to available postings!</p>
            ) : (
              <table className="table">
                <thead>
                  <tr>
                    <th>Farmer</th>
                    <th>Job Title</th>
                    <th>Work Type</th>
                    <th>Location</th>
                    <th>Start Date</th>
                    <th>Duration</th>
                    <th>Daily Wage</th>
                    <th>Total Wage</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {myJobs.map(job => (
                    <tr key={job.id}>
                      <td>{job.farmer_name}</td>
                      <td>{job.job_title}</td>
                      <td><span className="badge badge-labor">{job.work_type}</span></td>
                      <td>{job.location || 'N/A'}</td>
                      <td>{new Date(job.start_date).toLocaleDateString()}</td>
                      <td>{job.total_days || 'TBD'} days</td>
                      <td>৳{job.daily_wage}</td>
                      <td>
                        <strong style={{ color: '#059669' }}>
                          ৳{job.total_wage || (job.daily_wage * (job.total_days || 0))}
                        </strong>
                      </td>
                      <td>
                        <span className={`badge ${
                          job.status === 'completed' ? 'badge-success' : 
                          job.status === 'active' ? 'badge-primary' : 'badge-labor'
                        }`}>
                          {job.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}

        {activeTab === 'earnings' && (
          <div>
            <div className="card" style={{ marginBottom: '2rem' }}>
              <h2 className="card-title">💰 Earnings Summary</h2>
              <div className="grid grid-3">
                <div style={{ 
                  padding: '1.5rem', 
                  background: 'linear-gradient(135deg, #059669 0%, #047857 100%)', 
                  color: 'white',
                  borderRadius: '12px',
                  textAlign: 'center'
                }}>
                  <h3 style={{ fontSize: '2rem', margin: '0.5rem 0' }}>৳{earnings.total.toFixed(2)}</h3>
                  <p style={{ margin: 0 }}>Total Earnings</p>
                </div>
                <div style={{ 
                  padding: '1.5rem', 
                  background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)', 
                  color: 'white',
                  borderRadius: '12px',
                  textAlign: 'center'
                }}>
                  <h3 style={{ fontSize: '2rem', margin: '0.5rem 0' }}>৳{earnings.thisMonth.toFixed(2)}</h3>
                  <p style={{ margin: 0 }}>This Month</p>
                </div>
                <div style={{ 
                  padding: '1.5rem', 
                  background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', 
                  color: 'white',
                  borderRadius: '12px',
                  textAlign: 'center'
                }}>
                  <h3 style={{ fontSize: '2rem', margin: '0.5rem 0' }}>{earnings.completed}</h3>
                  <p style={{ margin: 0 }}>Jobs Completed</p>
                </div>
              </div>
            </div>

            <div className="card">
              <h2 className="card-title">📊 Work History</h2>
              {myJobs.length === 0 ? (
                <p>No work history yet</p>
              ) : (
                <table className="table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Farmer</th>
                      <th>Job</th>
                      <th>Work Type</th>
                      <th>Location</th>
                      <th>Duration</th>
                      <th>Wage/Day</th>
                      <th>Total Earned</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {myJobs.map(job => (
                      <tr key={job.id}>
                        <td>{new Date(job.start_date).toLocaleDateString()}</td>
                        <td>{job.farmer_name}</td>
                        <td>{job.job_title}</td>
                        <td><span className="badge badge-labor">{job.work_type}</span></td>
                        <td>{job.location || 'N/A'}</td>
                        <td>{job.total_days || 'TBD'} days</td>
                        <td>৳{job.daily_wage}</td>
                        <td>
                          <strong style={{ 
                            color: job.status === 'completed' ? '#059669' : '#6b7280' 
                          }}>
                            ৳{job.total_wage || (job.daily_wage * (job.total_days || 0))}
                          </strong>
                        </td>
                        <td>
                          <span className={`badge ${
                            job.status === 'completed' ? 'badge-success' : 
                            job.status === 'active' ? 'badge-primary' : 
                            job.status === 'cancelled' ? 'badge-danger' : 'badge-labor'
                          }`}>
                            {job.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>

            <div className="card" style={{ background: '#fffbeb', border: '1px solid #fbbf24' }}>
              <h3 style={{ color: '#92400e', marginBottom: '0.5rem' }}>💡 Earnings Tip</h3>
              <p style={{ margin: 0, color: '#78350f' }}>
                Complete jobs on time and maintain good relationships with farmers to get more work opportunities 
                and potentially higher wages. Your reputation as a reliable worker will help you earn more!
              </p>
            </div>
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

export default LaborPortal;
