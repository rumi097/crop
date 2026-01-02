import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './LandingPage.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function LandingPage({ user, onLogout }) {
  const [products, setProducts] = useState({ crops: [], vendor_products: [] });
  const [labor, setLabor] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all');
  const [stats, setStats] = useState({ totalCrops: 0, totalProducts: 0, totalLabor: 0 });
  const [cart, setCart] = useState([]);
  const [showCart, setShowCart] = useState(false);
  const [deliveryAddress, setDeliveryAddress] = useState('');
  const [orderConfirmation, setOrderConfirmation] = useState(null);
  const [showOrders, setShowOrders] = useState(false);
  const [myOrders, setMyOrders] = useState([]);
  const [loadingOrders, setLoadingOrders] = useState(false);

  useEffect(() => {
    fetchPublicData();
  }, []);

  const fetchPublicData = async () => {
    try {
      const [productsRes, laborRes] = await Promise.all([
        axios.get(`${API_URL}/api/public/products`),
        axios.get(`${API_URL}/api/public/labor-listings`)
      ]);
      
      const productsData = productsRes.data;
      const laborData = laborRes.data.labor || [];
      
      setProducts(productsData);
      setLabor(laborData);
      setStats({
        totalCrops: productsData.crops?.length || 0,
        totalProducts: productsData.vendor_products?.length || 0,
        totalLabor: laborData.length
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRoleBasedLink = () => {
    if (!user) return '/register';
    const roleMap = {
      farmer: '/farmer',
      buyer: '/buyer',
      vendor: '/vendor',
      labor: '/labor',
      admin: '/admin'
    };
    return roleMap[user.role] || '/';
  };

  const addToCart = (product, type) => {
    if (!user) {
      alert('Please login to add items to cart');
      return;
    }
    
    const cartItem = {
      id: `${type}-${product.id}`,
      productId: product.id,
      productType: type,
      name: product.crop_name || product.product_name,
      price: product.price_per_unit,
      unit: product.unit,
      maxQuantity: product.quantity || product.quantity_available,
      quantity: 1
    };

    const existingItemIndex = cart.findIndex(item => item.id === cartItem.id);
    if (existingItemIndex >= 0) {
      const newCart = [...cart];
      if (newCart[existingItemIndex].quantity < cartItem.maxQuantity) {
        newCart[existingItemIndex].quantity += 1;
        setCart(newCart);
        alert('Quantity updated in cart!');
      } else {
        alert('Maximum quantity reached!');
      }
    } else {
      setCart([...cart, cartItem]);
      alert('Added to cart!');
    }
  };

  const updateCartQuantity = (itemId, newQuantity) => {
    const newCart = cart.map(item => {
      if (item.id === itemId) {
        return { ...item, quantity: Math.max(1, Math.min(newQuantity, item.maxQuantity)) };
      }
      return item;
    });
    setCart(newCart);
  };

  const removeFromCart = (itemId) => {
    setCart(cart.filter(item => item.id !== itemId));
  };

  const getCartTotal = () => {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const fetchMyOrders = async () => {
    if (!user) return;
    setLoadingOrders(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/buyer/orders`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      console.log('Fetched orders:', response.data.orders);
      setMyOrders(response.data.orders || []);
      return response.data.orders || [];
    } catch (error) {
      console.error('Error fetching orders:', error);
      return [];
    } finally {
      setLoadingOrders(false);
    }
  };

  const handleCheckout = async () => {
    if (cart.length === 0) {
      alert('Your cart is empty!');
      return;
    }

    if (!deliveryAddress.trim()) {
      alert('Please enter a delivery address!');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const orderPromises = cart.map(item => {
        const orderData = {
          quantity: item.quantity,
          delivery_address: deliveryAddress,
          unit_price: item.price
        };

        if (item.productType === 'crop') {
          orderData.order_type = 'crop';
          orderData.crop_listing_id = item.productId;
        } else {
          orderData.order_type = 'vendor_product';
          orderData.vendor_product_id = item.productId;
        }

        return axios.post(`${API_URL}/api/buyer/orders`, orderData, {
          headers: { Authorization: `Bearer ${token}` }
        });
      });

      const responses = await Promise.all(orderPromises);
      const orderIds = responses.map(r => r.data.order_id);
      
      console.log('Orders placed successfully:', orderIds);
      
      // Store cart items for confirmation display
      const orderedItems = [...cart];
      const totalAmount = getCartTotal();
      
      setCart([]);
      setDeliveryAddress('');
      setShowCart(false);
      
      // Wait a moment for database to commit
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Fetch updated orders list
      const updatedOrders = await fetchMyOrders();
      console.log('Updated orders after fetch:', updatedOrders);
      
      // Then show order confirmation
      setOrderConfirmation({
        orderIds,
        items: orderedItems,
        totalAmount: totalAmount
      });
      
      // Refresh product data to show updated quantities
      fetchPublicData();
    } catch (error) {
      console.error('Checkout error:', error);
      alert('Error placing orders: ' + (error.response?.data?.error || error.message || 'Failed to place orders'));
    }
  };

  const features = [
    { icon: '🌾', title: 'Fresh Produce', desc: 'Direct from farmers to your doorstep', color: '#10b981' },
    { icon: '🏪', title: 'Quality Inputs', desc: 'Agricultural supplies from verified vendors', color: '#f59e0b' },
    { icon: '👷', title: 'Skilled Labor', desc: 'Experienced workers when you need them', color: '#8b5cf6' },
    { icon: '📊', title: 'Smart Analytics', desc: 'Track costs and maximize profits', color: '#3b82f6' },
    { icon: '🌱', title: 'Crop Recommendation', desc: 'AI-powered crop suggestions based on soil & climate', color: '#059669' },
    { icon: '🧪', title: 'Fertilizer Recommendation', desc: 'Get optimal fertilizer recommendations for your crops', color: '#dc2626' }
  ];

  return (
    <div className="landing-page">
      {/* Header */}
      <header className="header">
        <div className="header-title">
          Smart Farming Platform
        </div>
        <nav className="header-nav">
          {user ? (
            <>
              <span className={`badge badge-${user.role}`}>{user.role.toUpperCase()}</span>
              <span className="user-name">{user.full_name}</span>
              <button onClick={() => setShowCart(true)} className="nav-link" style={{ position: 'relative', background: 'none', border: 'none', cursor: 'pointer', color: 'inherit' }}>
                <span style={{ fontSize: '1.5rem' }}>🛒</span>
                {cart.length > 0 && (
                  <span style={{
                    position: 'absolute',
                    top: '-5px',
                    right: '-5px',
                    background: '#ef4444',
                    color: 'white',
                    borderRadius: '50%',
                    width: '20px',
                    height: '20px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '0.75rem',
                    fontWeight: 'bold'
                  }}>{cart.length}</span>
                )}
              </button>
              <button onClick={() => { 
                setShowOrders(true); 
                fetchMyOrders(); 
              }} className="nav-link" style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'inherit' }}>
                <span>📦</span> My Orders
              </button>
              <Link to={getRoleBasedLink()} className="nav-link">
                <span>📊</span> Dashboard
              </Link>
              <button onClick={onLogout} className="btn btn-secondary">
                <span>🚪</span> Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link">
                <span>🔑</span> Login
              </Link>
              <Link to="/register" className="nav-link">
                <span>✨</span> Register
              </Link>
            </>
          )}
        </nav>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            <span className="hero-emoji">🌾</span>
            Welcome to Smart Farming
          </h1>
          <p className="hero-subtitle">
            Connecting Farmers, Buyers, Vendors, and Labor in One Intelligent Platform
          </p>
          <div className="hero-stats">
            <div className="hero-stat">
              <div className="hero-stat-value">{stats.totalCrops}+</div>
              <div className="hero-stat-label">Fresh Crops</div>
            </div>
            <div className="hero-stat">
              <div className="hero-stat-value">{stats.totalProducts}+</div>
              <div className="hero-stat-label">Products</div>
            </div>
            <div className="hero-stat">
              <div className="hero-stat-value">{stats.totalLabor}+</div>
              <div className="hero-stat-label">Workers</div>
            </div>
          </div>
          {!user && (
            <div className="hero-actions">
              <Link to="/register" className="btn btn-primary btn-lg hero-btn">
                <span>🚀</span> Get Started Free
              </Link>
              <Link to="/login" className="btn btn-outline btn-lg hero-btn">
                <span>👋</span> Sign In
              </Link>
            </div>
          )}
        </div>
        <div className="hero-decoration"></div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <h2 className="section-title">Why Choose Our Platform?</h2>
          <div className="features-grid">
            {features.map((feature, index) => (
              <div key={index} className="feature-card" style={{ '--accent-color': feature.color }}>
                <div className="feature-icon">{feature.icon}</div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-desc">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Marketplace Section */}
      <section className="marketplace-section">
        <div className="container">
          <h2 className="section-title">Explore Marketplace</h2>
          
          {/* Tabs */}
          <div className="tabs-modern">
            <button 
              onClick={() => setActiveTab('all')} 
              className={`tab-modern ${activeTab === 'all' ? 'active' : ''}`}
            >
              <span>🌐</span> All Products
            </button>
            <button 
              onClick={() => setActiveTab('crops')} 
              className={`tab-modern ${activeTab === 'crops' ? 'active' : ''}`}
            >
              <span>🌾</span> Farmer Crops
            </button>
            <button 
              onClick={() => setActiveTab('inputs')} 
              className={`tab-modern ${activeTab === 'inputs' ? 'active' : ''}`}
            >
              <span>🏪</span> Vendor Products
            </button>
            <button 
              onClick={() => setActiveTab('labor')} 
              className={`tab-modern ${activeTab === 'labor' ? 'active' : ''}`}
            >
              <span>👷</span> Available Labor
            </button>
          </div>

          {loading ? (
            <div className="loading">
              <div className="spinner"></div>
              <p className="spinner-text">Loading marketplace...</p>
            </div>
          ) : (
            <div className="marketplace-content">
              {/* Crops */}
              {(activeTab === 'all' || activeTab === 'crops') && products.crops && products.crops.length > 0 && (
                <div className="marketplace-section-group">
                  <h3 className="marketplace-section-title">
                    <span>🌾</span> Fresh Crops from Farmers
                  </h3>
                  <div className="grid grid-3">
                    {products.crops.map(crop => (
                      <div key={crop.id} className="product-card">
                        <div className="product-image">
                          <div className="product-badge farmer">Farmer</div>
                        </div>
                        <div className="product-info">
                          <h3 className="product-title">{crop.crop_name}</h3>
                          <span className="badge badge-success">{crop.category || 'Crop'}</span>
                          <p className="product-description">{crop.description || 'Fresh and organic produce'}</p>
                          <p className="product-price">৳{crop.price_per_unit}<span className="price-unit">/{crop.unit}</span></p>
                          <div className="product-meta">
                            <span>�‍🌾 {crop.farm_name || crop.farmer_name}</span>
                            <span>📍 {crop.location || crop.farmer_location || 'Location not specified'}</span>
                          </div>
                          <div className="product-meta">
                            <span>📦 {crop.quantity} {crop.unit}</span>
                          </div>
                          {user && (
                            <button 
                              onClick={() => addToCart(crop, 'crop')}
                              className="btn btn-primary"
                              style={{ width: '100%', marginTop: '1rem' }}
                            >
                              🛒 Add to Cart
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Vendor Products */}
              {(activeTab === 'all' || activeTab === 'inputs') && products.vendor_products && products.vendor_products.length > 0 && (
                <div className="marketplace-section-group">
                  <h3 className="marketplace-section-title">
                    <span>🏪</span> Agricultural Inputs from Vendors
                  </h3>
                  <div className="grid grid-3">
                    {products.vendor_products.map(product => (
                      <div key={product.id} className="product-card">
                        <div className="product-image vendor">
                          <div className="product-badge vendor">Vendor</div>
                        </div>
                        <div className="product-info">
                          <h3 className="product-title">{product.product_name}</h3>
                          <span className="badge badge-warning">{product.category}</span>
                          <p className="product-description">{product.description || 'Quality agricultural supplies'}</p>
                          <p className="product-price">৳{product.price_per_unit}<span className="price-unit">/{product.unit}</span></p>
                          <div className="product-meta">
                            <span>📦 {product.quantity_available} {product.unit}</span>
                            <span>✅ In Stock</span>
                          </div>
                          {user && (
                            <button 
                              onClick={() => addToCart(product, 'vendor')}
                              className="btn btn-primary"
                              style={{ width: '100%', marginTop: '1rem' }}
                              disabled={product.quantity_available <= 0}
                            >
                              {product.quantity_available > 0 ? '🛒 Add to Cart' : 'Out of Stock'}
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Labor */}
              {(activeTab === 'all' || activeTab === 'labor') && labor.length > 0 && (
                <div className="marketplace-section-group">
                  <h3 className="marketplace-section-title">
                    <span>👷</span> Skilled Labor Available
                  </h3>
                  <div className="grid grid-3">
                    {labor.map(person => (
                      <div key={person.id} className="product-card labor-card">
                        <div className="product-image labor">
                          <div className="labor-avatar">{person.full_name.charAt(0)}</div>
                        </div>
                        <div className="product-info">
                          <h3 className="product-title">{person.full_name}</h3>
                          <span className="badge badge-labor">Worker</span>
                          <p className="product-description">{person.skills}</p>
                          <p className="product-price">৳{person.daily_wage}<span className="price-unit">/day</span></p>
                          <div className="product-meta">
                            <span>📅 {person.experience_years} years</span>
                            <span>⭐ {person.rating?.toFixed(1) || '5.0'}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Empty State */}
              {((activeTab === 'crops' && (!products.crops || products.crops.length === 0)) ||
                (activeTab === 'inputs' && (!products.vendor_products || products.vendor_products.length === 0)) ||
                (activeTab === 'labor' && labor.length === 0)) && (
                <div className="empty-state">
                  <div className="empty-state-icon">📦</div>
                  <h3 className="empty-state-title">No Items Found</h3>
                  <p className="empty-state-text">Check back later for new listings</p>
                </div>
              )}
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      {!user && (
        <section className="cta-section">
          <div className="cta-content">
            <h2 className="cta-title">Ready to Transform Your Farming Business?</h2>
            <p className="cta-subtitle">Join thousands of farmers, buyers, and vendors already using our platform</p>
            <Link to="/register" className="btn btn-primary btn-lg">
              <span>🚀</span> Start Your Journey Today
            </Link>
          </div>
        </section>
      )}

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-section">
            <h4>🌾 Smart Farming</h4>
            <p>Empowering agriculture through technology</p>
          </div>
          <div className="footer-section">
            <h4>Quick Links</h4>
            <ul>
              <li><Link to="/login">Login</Link></li>
              <li><Link to="/register">Register</Link></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Contact</h4>
            <p>📧 support@smartfarming.com</p>
            <p>📱 +880 1234-567890</p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2026 Smart Farming Platform | Connecting Agriculture Community 🌱</p>
        </div>
      </footer>

      {/* Shopping Cart Modal */}
      {showCart && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.7)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 9999,
          padding: '1rem'
        }} onClick={() => setShowCart(false)}>
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '2rem',
            maxWidth: '600px',
            width: '100%',
            maxHeight: '90vh',
            overflow: 'auto'
          }} onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h2 style={{ fontSize: '1.5rem', margin: 0 }}>
                🛒 Shopping Cart ({cart.length})
              </h2>
              <button onClick={() => setShowCart(false)} style={{
                background: 'none',
                border: 'none',
                fontSize: '1.5rem',
                cursor: 'pointer',
                color: '#64748b'
              }}>✕</button>
            </div>

            {cart.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '3rem 1rem', color: '#64748b' }}>
                <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🛒</div>
                <p style={{ fontSize: '1.1rem' }}>Your cart is empty</p>
                <p>Add some products to get started!</p>
              </div>
            ) : (
              <>
                <div style={{ marginBottom: '1.5rem' }}>
                  {cart.map(item => (
                    <div key={item.id} style={{
                      padding: '1rem',
                      marginBottom: '1rem',
                      background: '#f9fafb',
                      borderRadius: '8px',
                      border: '1px solid #e5e7eb'
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.75rem' }}>
                        <div style={{ flex: 1 }}>
                          <h4 style={{ margin: '0 0 0.25rem 0', fontSize: '1rem' }}>{item.name}</h4>
                          <p style={{ margin: 0, color: '#059669', fontWeight: 'bold' }}>৳{item.price}/{item.unit}</p>
                        </div>
                        <button onClick={() => removeFromCart(item.id)} style={{
                          background: '#fee2e2',
                          color: '#dc2626',
                          border: 'none',
                          padding: '0.5rem 0.75rem',
                          borderRadius: '6px',
                          cursor: 'pointer',
                          fontSize: '0.9rem',
                          fontWeight: '600'
                        }}>Remove</button>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ fontSize: '0.9rem', color: '#64748b' }}>Quantity:</span>
                        <button onClick={() => updateCartQuantity(item.id, item.quantity - 1)} style={{
                          background: '#f3f4f6',
                          border: '1px solid #d1d5db',
                          padding: '0.25rem 0.5rem',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          fontSize: '1rem'
                        }}>−</button>
                        <input
                          type="number"
                          value={item.quantity}
                          onChange={(e) => updateCartQuantity(item.id, parseInt(e.target.value) || 1)}
                          min="1"
                          max={item.maxQuantity}
                          style={{
                            width: '60px',
                            padding: '0.25rem',
                            border: '1px solid #d1d5db',
                            borderRadius: '4px',
                            textAlign: 'center'
                          }}
                        />
                        <button onClick={() => updateCartQuantity(item.id, item.quantity + 1)} style={{
                          background: '#f3f4f6',
                          border: '1px solid #d1d5db',
                          padding: '0.25rem 0.5rem',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          fontSize: '1rem'
                        }}>+</button>
                        <span style={{ marginLeft: 'auto', fontWeight: 'bold', color: '#059669' }}>
                          ৳{(item.price * item.quantity).toFixed(2)}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                    Delivery Address *
                  </label>
                  <textarea
                    value={deliveryAddress}
                    onChange={(e) => setDeliveryAddress(e.target.value)}
                    placeholder="Enter your delivery address"
                    rows="3"
                    style={{
                      width: '100%',
                      padding: '0.75rem',
                      border: '2px solid #e5e7eb',
                      borderRadius: '8px',
                      fontSize: '1rem',
                      resize: 'vertical'
                    }}
                  />
                </div>

                <div style={{
                  padding: '1rem',
                  background: '#ecfdf5',
                  borderRadius: '8px',
                  marginBottom: '1rem',
                  border: '2px solid #10b981'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '1.1rem', fontWeight: '600' }}>Total Amount:</span>
                    <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#059669' }}>
                      ৳{getCartTotal().toFixed(2)}
                    </span>
                  </div>
                  <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.85rem', color: '#64748b' }}>
                    {cart.length} item(s) in cart
                  </p>
                </div>

                <div style={{ display: 'flex', gap: '1rem' }}>
                  <button
                    onClick={handleCheckout}
                    className="btn btn-primary"
                    style={{ flex: 1, padding: '0.75rem', fontSize: '1rem' }}
                  >
                    Checkout
                  </button>
                  <button
                    onClick={() => setShowCart(false)}
                    className="btn btn-secondary"
                    style={{ padding: '0.75rem 1.5rem', fontSize: '1rem' }}
                  >
                    Continue Shopping
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}

      {/* Order Confirmation Modal */}
      {orderConfirmation && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.7)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 10000,
          padding: '1rem'
        }} onClick={() => setOrderConfirmation(null)}>
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '2rem',
            maxWidth: '600px',
            width: '100%',
            maxHeight: '90vh',
            overflow: 'auto'
          }} onClick={(e) => e.stopPropagation()}>
            <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
              <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>✅</div>
              <h2 style={{ color: '#059669', marginBottom: '0.5rem' }}>Order Placed Successfully!</h2>
              <p style={{ color: '#64748b' }}>Your order has been received and is being processed</p>
            </div>

            <div style={{ marginBottom: '2rem', padding: '1rem', background: '#f0fdf4', borderRadius: '8px', border: '2px solid #10b981' }}>
              <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>Order Summary</h3>
              <div style={{ marginBottom: '1rem' }}>
                <p style={{ margin: '0.5rem 0', fontSize: '0.9rem', color: '#64748b' }}>
                  Order IDs: <strong style={{ color: '#059669' }}>{orderConfirmation.orderIds.join(', ')}</strong>
                </p>
                <p style={{ margin: '0.5rem 0', fontSize: '0.9rem', color: '#64748b' }}>
                  Total Items: <strong>{orderConfirmation.items.length}</strong>
                </p>
                <p style={{ margin: '0.5rem 0', fontSize: '1.25rem', color: '#059669' }}>
                  Total Amount: <strong>৳{orderConfirmation.totalAmount.toFixed(2)}</strong>
                </p>
              </div>
            </div>

            <div style={{ marginBottom: '2rem' }}>
              <h4 style={{ marginBottom: '1rem' }}>Ordered Items</h4>
              {orderConfirmation.items.map((item, index) => (
                <div key={index} style={{
                  padding: '0.75rem',
                  marginBottom: '0.5rem',
                  background: '#f9fafb',
                  borderRadius: '6px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}>
                  <div>
                    <p style={{ margin: 0, fontWeight: '600' }}>{item.name}</p>
                    <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.9rem', color: '#64748b' }}>
                      {item.quantity} × ৳{item.price}
                    </p>
                  </div>
                  <p style={{ margin: 0, fontWeight: 'bold', color: '#059669' }}>
                    ৳{(item.quantity * item.price).toFixed(2)}
                  </p>
                </div>
              ))}
            </div>

            <div style={{ padding: '1rem', background: '#fef3c7', borderRadius: '8px', marginBottom: '1.5rem' }}>
              <p style={{ margin: 0, fontSize: '0.9rem' }}>
                <strong>📞 What's Next?</strong><br/>
                The sellers will contact you soon to confirm delivery details. 
                {user && ` You can track your orders in your ${user.role} dashboard.`}
              </p>
            </div>

            <div style={{ display: 'flex', gap: '1rem' }}>
              {user && (
                <Link 
                  to={getRoleBasedLink()} 
                  className="btn btn-primary"
                  style={{ flex: 1, textAlign: 'center', padding: '0.75rem' }}
                  onClick={() => setOrderConfirmation(null)}
                >
                  Go to Dashboard
                </Link>
              )}
              <button
                onClick={() => {
                  setOrderConfirmation(null);
                  setShowOrders(true);
                  // Don't fetch again, we just fetched
                }}
                className="btn btn-success"
                style={{ flex: 1, padding: '0.75rem' }}
              >
                📦 View My Orders
              </button>
              <button
                onClick={() => setOrderConfirmation(null)}
                className="btn btn-secondary"
                style={{ flex: user ? 'none' : 1, padding: '0.75rem' }}
              >
                Continue Shopping
              </button>
            </div>
          </div>
        </div>
      )}

      {/* My Orders Modal */}
      {showOrders && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.7)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 9999,
          padding: '1rem'
        }} onClick={() => setShowOrders(false)}>
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '2rem',
            maxWidth: '900px',
            width: '100%',
            maxHeight: '90vh',
            overflow: 'auto'
          }} onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h2 style={{ fontSize: '1.5rem', margin: 0 }}>
                📦 My Orders ({myOrders.length})
              </h2>
              <button onClick={() => setShowOrders(false)} style={{
                background: 'none',
                border: 'none',
                fontSize: '1.5rem',
                cursor: 'pointer',
                color: '#64748b'
              }}>✕</button>
            </div>

            {loadingOrders ? (
              <div style={{ textAlign: 'center', padding: '3rem', color: '#64748b' }}>
                <div className="spinner" style={{ margin: '0 auto 1rem' }}></div>
                <p>Loading your orders...</p>
              </div>
            ) : myOrders.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '3rem', color: '#64748b' }}>
                <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>📦</div>
                <p style={{ fontSize: '1.1rem' }}>No orders yet</p>
                <p>Start shopping to place your first order!</p>
              </div>
            ) : (
              <div style={{ display: 'grid', gap: '1rem' }}>
                {myOrders.map(order => {
                  const statusConfig = {
                    pending: { color: '#f59e0b', bg: '#fef3c7', icon: '⏳', text: 'Pending' },
                    confirmed: { color: '#3b82f6', bg: '#dbeafe', icon: '✓', text: 'Confirmed' },
                    processing: { color: '#8b5cf6', bg: '#ede9fe', icon: '⚙️', text: 'Processing' },
                    shipped: { color: '#06b6d4', bg: '#cffafe', icon: '🚚', text: 'Shipped' },
                    delivered: { color: '#10b981', bg: '#d1fae5', icon: '✅', text: 'Delivered' },
                    completed: { color: '#10b981', bg: '#d1fae5', icon: '✅', text: 'Completed' },
                    cancelled: { color: '#ef4444', bg: '#fee2e2', icon: '❌', text: 'Cancelled' }
                  };
                  const status = statusConfig[order.status] || statusConfig.pending;

                  return (
                    <div key={order.id} style={{
                      padding: '1.5rem',
                      background: '#f9fafb',
                      borderRadius: '12px',
                      border: '2px solid #e5e7eb'
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
                        <div>
                          <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem' }}>
                            Order #{order.id}
                          </h3>
                          <p style={{ margin: '0.25rem 0', fontSize: '0.9rem', color: '#64748b' }}>
                            📅 {new Date(order.created_at).toLocaleString('en-US', {
                              year: 'numeric',
                              month: 'short',
                              day: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </p>
                        </div>
                        <div style={{
                          padding: '0.5rem 1rem',
                          background: status.bg,
                          color: status.color,
                          borderRadius: '20px',
                          fontWeight: '600',
                          fontSize: '0.9rem',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.5rem'
                        }}>
                          <span>{status.icon}</span>
                          <span>{status.text}</span>
                        </div>
                      </div>

                      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1rem', padding: '1rem', background: 'white', borderRadius: '8px' }}>
                        {order.product_name && (
                          <div>
                            <p style={{ margin: '0 0 0.25rem 0', fontSize: '0.85rem', color: '#64748b' }}>Product</p>
                            <p style={{ margin: 0, fontWeight: '600' }}>{order.product_name}</p>
                          </div>
                        )}
                        <div>
                          <p style={{ margin: '0 0 0.25rem 0', fontSize: '0.85rem', color: '#64748b' }}>Type</p>
                          <p style={{ margin: 0, fontWeight: '600' }}>
                            {order.order_type === 'crop' ? '🌾 Crop' : '🏪 Product'}
                          </p>
                        </div>
                        <div>
                          <p style={{ margin: '0 0 0.25rem 0', fontSize: '0.85rem', color: '#64748b' }}>Quantity</p>
                          <p style={{ margin: 0, fontWeight: '600' }}>{order.quantity} units</p>
                        </div>
                        <div>
                          <p style={{ margin: '0 0 0.25rem 0', fontSize: '0.85rem', color: '#64748b' }}>Total Amount</p>
                          <p style={{ margin: 0, fontWeight: 'bold', fontSize: '1.1rem', color: '#059669' }}>
                            ৳{order.total_price}
                          </p>
                        </div>
                      </div>

                      {order.delivery_address && (
                        <div style={{ padding: '0.75rem', background: 'white', borderRadius: '8px', marginTop: '0.5rem' }}>
                          <p style={{ margin: 0, fontSize: '0.85rem', color: '#64748b' }}>📍 Delivery Address:</p>
                          <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.9rem' }}>{order.delivery_address}</p>
                        </div>
                      )}

                      {order.seller_name && (
                        <div style={{ marginTop: '0.75rem', fontSize: '0.9rem', color: '#64748b' }}>
                          <strong>Seller:</strong> {order.seller_name}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}

            <div style={{ marginTop: '1.5rem', display: 'flex', gap: '1rem' }}>
              <button
                onClick={() => setShowOrders(false)}
                className="btn btn-secondary"
                style={{ flex: 1, padding: '0.75rem' }}
              >
                Close
              </button>
              {user && (
                <Link 
                  to={getRoleBasedLink()} 
                  className="btn btn-primary"
                  style={{ flex: 1, textAlign: 'center', padding: '0.75rem' }}
                  onClick={() => setShowOrders(false)}
                >
                  Go to Dashboard
                </Link>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default LandingPage;
