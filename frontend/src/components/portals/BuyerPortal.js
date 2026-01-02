import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import ProfileEditor from '../shared/ProfileEditor';
import axios from 'axios';
import '../../styles/portals/buyer.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function BuyerPortal({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('marketplace');
  const [marketplace, setMarketplace] = useState({ crops: [], products: [] });
  const [orders, setOrders] = useState([]);
  const [cart, setCart] = useState([]);
  const [showCheckout, setShowCheckout] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [checkoutForm, setCheckoutForm] = useState({
    delivery_address: '', payment_method: 'Cash', notes: ''
  });

  useEffect(() => {
    if (activeTab === 'marketplace') fetchMarketplace();
    if (activeTab === 'orders' || activeTab === 'history' || activeTab === 'tracking') fetchOrders();
  }, [activeTab]);

  const fetchMarketplace = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/buyer/marketplace`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMarketplace(response.data);
    } catch (error) {
      console.error('Error fetching marketplace:', error);
    }
  };

  const fetchOrders = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/buyer/orders`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOrders(response.data.orders);
    } catch (error) {
      console.error('Error fetching orders:', error);
    }
  };

  const addToCart = (item, type) => {
    const existingItem = cart.find(i => i.id === item.id && i.type === type);
    if (existingItem) {
      setCart(cart.map(i => 
        i.id === item.id && i.type === type 
          ? {...i, quantity: i.quantity + 1} 
          : i
      ));
    } else {
      setCart([...cart, { ...item, type, quantity: 1 }]);
    }
    alert('Added to cart!');
  };

  const updateCartQuantity = (itemId, type, newQuantity) => {
    if (newQuantity <= 0) {
      setCart(cart.filter(i => !(i.id === itemId && i.type === type)));
    } else {
      setCart(cart.map(i => 
        i.id === itemId && i.type === type 
          ? {...i, quantity: newQuantity} 
          : i
      ));
    }
  };

  const removeFromCart = (itemId, type) => {
    setCart(cart.filter(i => !(i.id === itemId && i.type === type)));
  };

  const getCartTotal = () => {
    return cart.reduce((total, item) => {
      const price = item.type === 'crop' ? item.price_per_unit : item.price_per_unit;
      return total + (price * item.quantity);
    }, 0);
  };

  const handleCheckout = async (e) => {
    e.preventDefault();
    if (cart.length === 0) {
      alert('Your cart is empty!');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const orderData = {
        items: cart.map(item => ({
          id: item.id,
          type: item.type,
          quantity: item.quantity
        })),
        delivery_address: checkoutForm.delivery_address,
        payment_method: checkoutForm.payment_method,
        notes: checkoutForm.notes,
        total_amount: getCartTotal()
      };

      await axios.post(`${API_URL}/api/buyer/orders`, orderData, {
        headers: { Authorization: `Bearer ${token}` }
      });

      alert('Order placed successfully!');
      setCart([]);
      setShowCheckout(false);
      setCheckoutForm({ delivery_address: '', payment_method: 'Cash', notes: '' });
      setActiveTab('orders');
    } catch (error) {
      alert('Failed to place order: ' + (error.response?.data?.error || 'Unknown error'));
    }
  };

  return (
    <div>
      <header className="header">
        <div className="header-title">🛒 Buyer Portal</div>
        <div className="header-nav">
          <span className="badge badge-buyer">BUYER</span>
          <span>{user.full_name}</span>
          <button onClick={() => setShowCheckout(!showCheckout)} className="btn btn-primary">
            🛒 Cart ({cart.length})
          </button>
          <Link to="/" className="nav-link">Home</Link>
          <button onClick={onLogout} className="btn btn-secondary">Logout</button>
        </div>
      </header>

      <div className="container">
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
          <button onClick={() => setActiveTab('marketplace')} 
            className={`btn ${activeTab === 'marketplace' ? 'btn-primary' : 'btn-secondary'}`}>
            🌾 Marketplace
          </button>
          <button onClick={() => setActiveTab('orders')} 
            className={`btn ${activeTab === 'orders' ? 'btn-primary' : 'btn-secondary'}`}>
            📦 My Orders
          </button>
          <button onClick={() => setActiveTab('tracking')} 
            className={`btn ${activeTab === 'tracking' ? 'btn-primary' : 'btn-secondary'}`}>
            📍 Order Tracking
          </button>
          <button onClick={() => setActiveTab('history')} 
            className={`btn ${activeTab === 'history' ? 'btn-primary' : 'btn-secondary'}`}>
            📋 Purchase History
          </button>
          <button onClick={() => setActiveTab('profile')} 
            className={`btn ${activeTab === 'profile' ? 'btn-primary' : 'btn-secondary'}`}>
            👤 Profile
          </button>
          <button onClick={() => setShowCheckout(true)} className="btn btn-success" style={{ marginLeft: 'auto' }}>
            🛒 Cart ({cart.length})
          </button>
        </div>

        {/* Cart Sidebar */}
        {showCheckout && (
          <div style={{
            position: 'fixed', top: 0, right: 0, width: '400px', height: '100vh',
            background: 'white', boxShadow: '-2px 0 10px rgba(0,0,0,0.1)',
            overflowY: 'auto', zIndex: 1000, padding: '2rem'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h2>🛒 Shopping Cart</h2>
              <button onClick={() => setShowCheckout(false)} className="btn btn-secondary">✕</button>
            </div>

            {cart.length === 0 ? (
              <p>Your cart is empty</p>
            ) : (
              <>
                <div style={{ marginBottom: '1rem' }}>
                  {cart.map((item, index) => (
                    <div key={index} style={{ 
                      padding: '1rem', marginBottom: '0.5rem', 
                      background: '#f9fafb', borderRadius: '8px' 
                    }}>
                      <h4 style={{ margin: '0 0 0.5rem 0' }}>
                        {item.type === 'crop' ? item.crop_name : item.product_name}
                      </h4>
                      <p style={{ margin: '0.25rem 0' }}>৳{item.price_per_unit}/{item.unit}</p>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
                        <button onClick={() => updateCartQuantity(item.id, item.type, item.quantity - 1)}
                          className="btn btn-secondary" style={{ padding: '0.25rem 0.5rem' }}>-</button>
                        <span>{item.quantity}</span>
                        <button onClick={() => updateCartQuantity(item.id, item.type, item.quantity + 1)}
                          className="btn btn-secondary" style={{ padding: '0.25rem 0.5rem' }}>+</button>
                        <button onClick={() => removeFromCart(item.id, item.type)}
                          className="btn btn-danger" style={{ padding: '0.25rem 0.5rem', marginLeft: 'auto' }}>
                          Remove
                        </button>
                      </div>
                      <p style={{ margin: '0.5rem 0 0 0', fontWeight: 'bold' }}>
                        Subtotal: ৳{(item.price_per_unit * item.quantity).toFixed(2)}
                      </p>
                    </div>
                  ))}
                </div>

                <div style={{ 
                  padding: '1rem', background: '#059669', color: 'white', 
                  borderRadius: '8px', marginBottom: '1rem', fontSize: '1.25rem', fontWeight: 'bold'
                }}>
                  Total: ৳{getCartTotal().toFixed(2)}
                </div>

                <form onSubmit={handleCheckout}>
                  <div className="form-group">
                    <label style={{ color: '#111' }}>Delivery Address *</label>
                    <textarea required className="form-input" rows="2"
                      value={checkoutForm.delivery_address}
                      onChange={(e) => setCheckoutForm({...checkoutForm, delivery_address: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label style={{ color: '#111' }}>Payment Method *</label>
                    <select required className="form-input" value={checkoutForm.payment_method}
                      onChange={(e) => setCheckoutForm({...checkoutForm, payment_method: e.target.value})}>
                      <option value="Cash">Cash on Delivery</option>
                      <option value="Bank Transfer">Bank Transfer</option>
                      <option value="Mobile Banking">Mobile Banking</option>
                      <option value="Card">Credit/Debit Card</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label style={{ color: '#111' }}>Notes (Optional)</label>
                    <textarea className="form-input" rows="2"
                      value={checkoutForm.notes}
                      onChange={(e) => setCheckoutForm({...checkoutForm, notes: e.target.value})} />
                  </div>
                  <button type="submit" className="btn btn-success" style={{ width: '100%' }}>
                    Place Order
                  </button>
                </form>
              </>
            )}
          </div>
        )}

        {activeTab === 'marketplace' && (
          <>
            <div className="card">
              <h2 className="card-title">🌾 Fresh Crops from Farmers</h2>
              {marketplace.crops && marketplace.crops.length === 0 ? (
                <p>No crops available at the moment</p>
              ) : (
                <div className="grid grid-3">
                  {(marketplace.crops || []).map(crop => (
                    <div key={crop.id} className="product-card">
                      <div className="product-info">
                        <h3 className="product-title">{crop.crop_name}</h3>
                        <div style={{ marginBottom: '0.5rem' }}>
                          <p><strong>👨‍🌾 Farm:</strong> {crop.farm_name || 'Unknown Farm'}</p>
                          <p><strong>🧑 Farmer:</strong> {crop.farmer_name || 'Unknown'}</p>
                          <p><strong>📍 Location:</strong> {crop.location || crop.farmer_location || 'Location not specified'}</p>
                        </div>
                        <p className="product-price">৳{crop.price_per_unit}/{crop.unit}</p>
                        <p>Available: {crop.quantity} {crop.unit}</p>
                        <span className="badge badge-success">{crop.category || 'Fresh'}</span>
                        <button onClick={() => addToCart(crop, 'crop')}
                          className="btn btn-success" style={{ width: '100%', marginTop: '1rem' }}>
                          Add to Cart
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="card">
              <h2 className="card-title">🏪 Agricultural Inputs from Vendors</h2>
              {marketplace.products && marketplace.products.length === 0 ? (
                <p>No products available at the moment</p>
              ) : (
                <div className="grid grid-3">
                  {(marketplace.products || []).map(product => (
                    <div key={product.id} className="product-card">
                      <div className="product-info">
                        <h3 className="product-title">{product.product_name}</h3>
                        <span className="badge badge-vendor">{product.category}</span>
                        <p><strong>Vendor:</strong> {product.vendor_name}</p>
                        <p className="product-price">৳{product.price_per_unit}/{product.unit}</p>
                        <p>Stock: {product.quantity_available} {product.unit}</p>
                        <button onClick={() => addToCart(product, 'product')}
                          className="btn btn-success" style={{ width: '100%', marginTop: '1rem' }}>
                          Add to Cart
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}

        {activeTab === 'orders' && (
          <div className="card">
            <h2 className="card-title">📦 My Orders</h2>
            {orders.length === 0 ? (
              <p>No orders yet. Start shopping in the marketplace!</p>
            ) : (
              <div style={{ display: 'grid', gap: '1rem' }}>
                {orders.map(order => (
                  <div key={order.id} style={{
                    padding: '1.5rem',
                    background: '#f9fafb',
                    borderRadius: '12px',
                    border: '2px solid #e5e7eb'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
                      <div>
                        <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.25rem' }}>Order #{order.id}</h3>
                        <p style={{ margin: '0.25rem 0', color: '#64748b' }}>
                          📅 {new Date(order.created_at).toLocaleString()}
                        </p>
                      </div>
                      {(() => {
                        const labelMap = {
                          pending: 'PENDING',
                          confirmed: 'CONFIRMED',
                          in_progress: 'IN PROGRESS',
                          completed: 'DELIVERED',
                          cancelled: 'CANCELLED'
                        };
                        const statusKey = (order.status || '').toLowerCase();
                        const label = labelMap[statusKey] || (order.status || '').toUpperCase();
                        return (
                          <span className={`badge ${
                            statusKey === 'completed' ? 'badge-success' : 
                            statusKey === 'cancelled' ? 'badge-danger' : 
                            'badge-buyer'
                          }`} style={{ fontSize: '0.9rem', padding: '0.5rem 1rem' }}>
                            {label}
                          </span>
                        );
                      })()}
                    </div>
                    
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
                      <div>
                        <p style={{ margin: '0.25rem 0', fontSize: '0.9rem', color: '#64748b' }}>Type</p>
                        <p style={{ margin: '0.25rem 0', fontWeight: '600' }}>{order.order_type === 'crop' ? '🌾 Crop' : '🏪 Product'}</p>
                      </div>
                      <div>
                        <p style={{ margin: '0.25rem 0', fontSize: '0.9rem', color: '#64748b' }}>Quantity</p>
                        <p style={{ margin: '0.25rem 0', fontWeight: '600' }}>{order.quantity}</p>
                      </div>
                      <div>
                        <p style={{ margin: '0.25rem 0', fontSize: '0.9rem', color: '#64748b' }}>Unit Price</p>
                        <p style={{ margin: '0.25rem 0', fontWeight: '600' }}>৳{order.unit_price}</p>
                      </div>
                      <div>
                        <p style={{ margin: '0.25rem 0', fontSize: '0.9rem', color: '#64748b' }}>Total</p>
                        <p style={{ margin: '0.25rem 0', fontWeight: 'bold', fontSize: '1.25rem', color: '#059669' }}>৳{order.total_price}</p>
                      </div>
                    </div>

                    <button 
                      onClick={() => { setSelectedOrder(order); setActiveTab('tracking'); }}
                      className="btn btn-primary"
                      style={{ marginTop: '0.5rem' }}
                    >
                      📍 Track Order
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'tracking' && (
          <div className="card">
            <h2 className="card-title">📍 Order Tracking</h2>
            {selectedOrder ? (
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                  <h3>Order #{selectedOrder.id}</h3>
                  <button onClick={() => { setSelectedOrder(null); setActiveTab('orders'); }} className="btn btn-secondary">
                    ← Back to Orders
                  </button>
                </div>

                <div style={{ marginBottom: '2rem', padding: '1.5rem', background: '#f0f9ff', borderRadius: '12px' }}>
                  <h4 style={{ marginBottom: '1rem' }}>Order Details</h4>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
                    <div>
                      <p style={{ margin: '0.25rem 0', fontSize: '0.9rem', color: '#64748b' }}>Order Type</p>
                      <p style={{ margin: '0.25rem 0', fontWeight: '600' }}>{selectedOrder.order_type === 'crop' ? '🌾 Crop' : '🏪 Vendor Product'}</p>
                    </div>
                    <div>
                      <p style={{ margin: '0.25rem 0', fontSize: '0.9rem', color: '#64748b' }}>Quantity</p>
                      <p style={{ margin: '0.25rem 0', fontWeight: '600' }}>{selectedOrder.quantity} units</p>
                    </div>
                    <div>
                      <p style={{ margin: '0.25rem 0', fontSize: '0.9rem', color: '#64748b' }}>Total Amount</p>
                      <p style={{ margin: '0.25rem 0', fontWeight: 'bold', color: '#059669' }}>৳{selectedOrder.total_price}</p>
                    </div>
                    <div>
                      <p style={{ margin: '0.25rem 0', fontSize: '0.9rem', color: '#64748b' }}>Order Date</p>
                      <p style={{ margin: '0.25rem 0', fontWeight: '600' }}>{new Date(selectedOrder.created_at).toLocaleString()}</p>
                    </div>
                  </div>
                </div>

                {/* Order Status Timeline */}
                <div style={{ marginBottom: '2rem' }}>
                  <h4 style={{ marginBottom: '1.5rem' }}>Order Status Timeline</h4>
                  <div style={{ position: 'relative', paddingLeft: '2rem' }}>
                    {['pending', 'confirmed', 'in_progress', 'completed'].map((status, index) => {
                      const statusOrder = { pending: 0, confirmed: 1, in_progress: 2, completed: 3 };
                      const currentKey = (selectedOrder.status || '').toLowerCase();
                      const currentIndex = statusOrder[currentKey] ?? 0;
                      const isActive = currentIndex >= index;
                      const isCurrent = currentIndex === index;
                      
                      return (
                        <div key={status} style={{ position: 'relative', paddingBottom: '2rem' }}>
                          {/* Vertical line */}
                          {index < 4 && (
                            <div style={{
                              position: 'absolute',
                              left: '-1.25rem',
                              top: '1.5rem',
                              width: '2px',
                              height: '2rem',
                              background: isActive ? '#10b981' : '#e5e7eb'
                            }}></div>
                          )}
                          
                          {/* Status dot */}
                          <div style={{
                            position: 'absolute',
                            left: '-1.6rem',
                            top: '0.25rem',
                            width: '1.5rem',
                            height: '1.5rem',
                            borderRadius: '50%',
                            background: isActive ? '#10b981' : '#e5e7eb',
                            border: isCurrent ? '4px solid #059669' : 'none',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                          }}>
                            {isActive && <span style={{ color: 'white', fontSize: '0.75rem' }}>✓</span>}
                          </div>

                          {/* Status content */}
                          <div style={{
                            padding: '1rem',
                            background: isCurrent ? '#ecfdf5' : '#f9fafb',
                            borderRadius: '8px',
                            border: isCurrent ? '2px solid #10b981' : '1px solid #e5e7eb'
                          }}>
                            <h5 style={{ margin: '0 0 0.5rem 0', textTransform: 'capitalize', color: isActive ? '#059669' : '#64748b' }}>
                              {status === 'pending' && 'pending'}
                              {status === 'confirmed' && 'confirmed'}
                              {status === 'in_progress' && 'in progress'}
                              {status === 'completed' && 'delivered'}
                            </h5>
                            <p style={{ margin: 0, fontSize: '0.9rem', color: '#64748b' }}>
                              {status === 'pending' && 'Order received and awaiting confirmation'}
                              {status === 'confirmed' && 'Order confirmed by seller'}
                              {status === 'in_progress' && 'Order is being prepared or in transit'}
                              {status === 'completed' && 'Order delivered successfully'}
                            </p>
                            {isCurrent && (
                              <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.85rem', color: '#059669', fontWeight: '600' }}>
                                🟢 Current Status
                              </p>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {selectedOrder.delivery_address && (
                  <div style={{ padding: '1rem', background: '#f9fafb', borderRadius: '8px' }}>
                    <h4 style={{ marginBottom: '0.5rem' }}>📍 Delivery Address</h4>
                    <p style={{ margin: 0 }}>{selectedOrder.delivery_address}</p>
                  </div>
                )}
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: '3rem', color: '#64748b' }}>
                <p style={{ fontSize: '3rem', marginBottom: '1rem' }}>📦</p>
                <p style={{ fontSize: '1.1rem', marginBottom: '1rem' }}>Select an order to track</p>
                <button onClick={() => setActiveTab('orders')} className="btn btn-primary">
                  View My Orders
                </button>
              </div>
            )}
          </div>
        )}

        {activeTab === 'history' && (
          <div>
            <div className="card" style={{ marginBottom: '2rem' }}>
              <h2 className="card-title">📊 Purchase Statistics</h2>
              <div className="grid grid-3">
                <div style={{ padding: '1rem', background: '#f9fafb', borderRadius: '8px' }}>
                  <h3>Total Orders</h3>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#3b82f6' }}>
                    {orders.length}
                  </p>
                </div>
                <div style={{ padding: '1rem', background: '#f9fafb', borderRadius: '8px' }}>
                  <h3>Total Spent</h3>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#dc2626' }}>
                    ৳{orders.reduce((sum, o) => sum + (o.total_price || 0), 0).toFixed(2)}
                  </p>
                </div>
                <div style={{ padding: '1rem', background: '#f9fafb', borderRadius: '8px' }}>
                  <h3>Completed Orders</h3>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#059669' }}>
                    {orders.filter(o => o.status === 'completed').length}
                  </p>
                </div>
              </div>
            </div>

            <div className="card">
              <h2 className="card-title">📋 Purchase History</h2>
              {orders.length === 0 ? (
                <p>No purchase history yet</p>
              ) : (
                <table className="table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Order ID</th>
                      <th>Seller</th>
                      <th>Items</th>
                      <th>Amount</th>
                      <th>Payment</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orders.map(order => (
                      <tr key={order.id}>
                        <td>{new Date(order.created_at).toLocaleDateString()}</td>
                        <td>#{order.id}</td>
                        <td>{order.seller_name || 'N/A'}</td>
                        <td>{order.item_count || 'Multiple'} items</td>
                        <td>৳{order.total_price}</td>
                        <td>{order.payment_method || 'Cash'}</td>
                        <td>
                          <span className={`badge ${
                            order.status === 'completed' ? 'badge-success' : 
                            order.status === 'cancelled' ? 'badge-danger' : 'badge-buyer'
                          }`}>
                            {order.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
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

export default BuyerPortal;
