import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import ProfileEditor from '../shared/ProfileEditor';
import axios from 'axios';
import '../../styles/portals/vendor.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function VendorPortal({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [stats, setStats] = useState({ totalProducts: 0, totalOrders: 0, totalRevenue: 0, lowStock: 0 });
  const [showProductForm, setShowProductForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [productForm, setProductForm] = useState({
    product_name: '', category: 'Seeds', price_per_unit: '', quantity_available: '', 
    unit: 'kg', description: '', image_url: ''
  });

  useEffect(() => {
    if (activeTab === 'dashboard') fetchDashboardData();
    if (activeTab === 'products') fetchProducts();
    if (activeTab === 'orders') fetchOrders();
  }, [activeTab]);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      const [productsRes, ordersRes] = await Promise.all([
        axios.get(`${API_URL}/api/vendor/products`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API_URL}/api/vendor/orders`, { headers: { Authorization: `Bearer ${token}` } })
      ]);
      
      const productsData = productsRes.data.products || [];
      const ordersData = ordersRes.data.orders || [];
      
      const totalRevenue = ordersData
        .filter(o => o.status === 'completed')
        .reduce((sum, o) => sum + (o.total_price || 0), 0);
      
      const lowStock = productsData.filter(p => p.quantity_available < 10).length;
      
      setProducts(productsData);
      setOrders(ordersData);
      setStats({
        totalProducts: productsData.length,
        totalOrders: ordersData.length,
        totalRevenue,
        lowStock
      });
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const fetchProducts = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/vendor/products`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProducts(response.data.products);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const fetchOrders = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/vendor/orders`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOrders(response.data.orders);
    } catch (error) {
      console.error('Error fetching orders:', error);
    }
  };

  const handleProductSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const url = editingProduct 
        ? `${API_URL}/api/vendor/products/${editingProduct.id}`
        : `${API_URL}/api/vendor/products`;
      const method = editingProduct ? 'put' : 'post';
      
      await axios[method](url, productForm, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      alert(editingProduct ? 'Product updated successfully!' : 'Product added successfully!');
      setShowProductForm(false);
      setEditingProduct(null);
      setProductForm({ product_name: '', category: 'Seeds', price_per_unit: '', 
        quantity_available: '', unit: 'kg', description: '', image_url: '' });
      fetchProducts();
      if (activeTab === 'dashboard') fetchDashboardData();
    } catch (error) {
      alert('Failed to save product: ' + (error.response?.data?.error || 'Unknown error'));
    }
  };

  const handleEditProduct = (product) => {
    setEditingProduct(product);
    setProductForm({
      product_name: product.product_name,
      category: product.category,
      price_per_unit: product.price_per_unit,
      quantity_available: product.quantity_available,
      unit: product.unit,
      description: product.description || '',
      image_url: product.image_url || ''
    });
    setShowProductForm(true);
  };

  const handleDeleteProduct = async (productId) => {
    if (!window.confirm('Are you sure you want to delete this product?')) return;
    
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API_URL}/api/vendor/products/${productId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Product deleted successfully!');
      fetchProducts();
      if (activeTab === 'dashboard') fetchDashboardData();
    } catch (error) {
      alert('Failed to delete product: ' + (error.response?.data?.error || 'Unknown error'));
    }
  };

  const handleUpdateOrderStatus = async (orderId, newStatus) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(`${API_URL}/api/vendor/orders/${orderId}`, 
        { status: newStatus },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('Order status updated!');
      fetchOrders();
      if (activeTab === 'dashboard') fetchDashboardData();
    } catch (error) {
      alert('Failed to update order: ' + (error.response?.data?.error || 'Unknown error'));
    }
  };

  return (
    <div>
      <header className="header">
        <div className="header-title">🏪 Vendor Portal</div>
        <div className="header-nav">
          <span className="badge badge-vendor">VENDOR</span>
          <span>{user.full_name}</span>
          <Link to="/" className="nav-link">Home</Link>
          <button onClick={onLogout} className="btn btn-secondary">Logout</button>
        </div>
      </header>

      <div className="container">
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
          <button onClick={() => setActiveTab('dashboard')} 
            className={`btn ${activeTab === 'dashboard' ? 'btn-primary' : 'btn-secondary'}`}>
            📊 Dashboard
          </button>
          <button onClick={() => setActiveTab('products')} 
            className={`btn ${activeTab === 'products' ? 'btn-primary' : 'btn-secondary'}`}>
            📦 My Products
          </button>
          <button onClick={() => setActiveTab('orders')} 
            className={`btn ${activeTab === 'orders' ? 'btn-primary' : 'btn-secondary'}`}>
            🛒 Orders ({orders.length})
          </button>
          <button onClick={() => setActiveTab('sales')} 
            className={`btn ${activeTab === 'sales' ? 'btn-primary' : 'btn-secondary'}`}>
            💰 Sales History
          </button>
          <button onClick={() => setActiveTab('profile')} 
            className={`btn ${activeTab === 'profile' ? 'btn-primary' : 'btn-secondary'}`}>
            👤 Profile
          </button>
        </div>

        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && (
          <div>
            <h2 style={{ marginBottom: '1.5rem' }}>📊 Vendor Dashboard</h2>
            
            {/* Statistics Cards */}
            <div className="grid grid-4" style={{ marginBottom: '2rem' }}>
              <div className="card" style={{ textAlign: 'center', background: '#4f46e5', color: 'white' }}>
                <h3 style={{ fontSize: '2rem', margin: '0.5rem 0' }}>{stats.totalProducts}</h3>
                <p style={{ margin: 0 }}>Total Products</p>
              </div>
              <div className="card" style={{ textAlign: 'center', background: '#059669', color: 'white' }}>
                <h3 style={{ fontSize: '2rem', margin: '0.5rem 0' }}>{stats.totalOrders}</h3>
                <p style={{ margin: 0 }}>Total Orders</p>
              </div>
              <div className="card" style={{ textAlign: 'center', background: '#dc2626', color: 'white' }}>
                <h3 style={{ fontSize: '2rem', margin: '0.5rem 0' }}>৳{stats.totalRevenue.toFixed(2)}</h3>
                <p style={{ margin: 0 }}>Total Revenue</p>
              </div>
              <div className="card" style={{ textAlign: 'center', background: '#ea580c', color: 'white' }}>
                <h3 style={{ fontSize: '2rem', margin: '0.5rem 0' }}>{stats.lowStock}</h3>
                <p style={{ margin: 0 }}>Low Stock Alerts</p>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="card" style={{ marginBottom: '2rem' }}>
              <h3 className="card-title">Quick Actions</h3>
              <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                <button onClick={() => { setActiveTab('products'); setShowProductForm(true); }} 
                  className="btn btn-primary">
                  + Add New Product
                </button>
                <button onClick={() => setActiveTab('orders')} className="btn btn-success">
                  View Pending Orders
                </button>
                <button onClick={() => setActiveTab('sales')} className="btn btn-secondary">
                  View Sales Report
                </button>
              </div>
            </div>

            {/* Recent Products */}
            <div className="card">
              <h3 className="card-title">Recent Products</h3>
              {products.length === 0 ? (
                <p>No products yet. Add your first product!</p>
              ) : (
                <div className="grid grid-3">
                  {products.slice(0, 6).map(product => (
                    <div key={product.id} className="product-card">
                      <div className="product-info">
                        <h3 className="product-title">{product.product_name}</h3>
                        <span className="badge badge-vendor">{product.category}</span>
                        <p className="product-price">৳{product.price_per_unit}/{product.unit}</p>
                        <p>Stock: {product.quantity_available} {product.unit}</p>
                        {product.quantity_available < 10 && (
                          <span className="badge" style={{ background: '#ef4444', color: 'white' }}>
                            Low Stock!
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Products Tab */}
        {activeTab === 'products' && (
          <div>
            <div className="card" style={{ marginBottom: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h2 className="card-title">My Products</h2>
                <button onClick={() => { 
                  setShowProductForm(!showProductForm); 
                  setEditingProduct(null);
                  setProductForm({ product_name: '', category: 'Seeds', price_per_unit: '', 
                    quantity_available: '', unit: 'kg', description: '', image_url: '' });
                }} className="btn btn-primary">
                  {showProductForm ? 'Cancel' : '+ Add New Product'}
                </button>
              </div>

              {showProductForm && (
                <form onSubmit={handleProductSubmit} style={{ marginTop: '1rem', padding: '1rem', background: '#f9fafb', borderRadius: '8px' }}>
                  <h3>{editingProduct ? 'Edit Product' : 'Add New Product'}</h3>
                  <div className="grid grid-2">
                    <div className="form-group">
                      <label>Product Name *</label>
                      <input type="text" required className="form-input" 
                        value={productForm.product_name}
                        onChange={(e) => setProductForm({...productForm, product_name: e.target.value})} />
                    </div>
                    <div className="form-group">
                      <label>Category *</label>
                      <select required className="form-input" value={productForm.category}
                        onChange={(e) => setProductForm({...productForm, category: e.target.value})}>
                        <option value="Seeds">Seeds</option>
                        <option value="Fertilizers">Fertilizers</option>
                        <option value="Pesticides">Pesticides</option>
                        <option value="Tools">Tools</option>
                        <option value="Equipment">Equipment</option>
                        <option value="Other">Other</option>
                      </select>
                    </div>
                    <div className="form-group">
                      <label>Price per Unit (৳) *</label>
                      <input type="number" step="0.01" required className="form-input" 
                        value={productForm.price_per_unit}
                        onChange={(e) => setProductForm({...productForm, price_per_unit: e.target.value})} />
                    </div>
                    <div className="form-group">
                      <label>Quantity Available *</label>
                      <input type="number" step="0.01" required className="form-input" 
                        value={productForm.quantity_available}
                        onChange={(e) => setProductForm({...productForm, quantity_available: e.target.value})} />
                    </div>
                    <div className="form-group">
                      <label>Unit *</label>
                      <select required className="form-input" value={productForm.unit}
                        onChange={(e) => setProductForm({...productForm, unit: e.target.value})}>
                        <option value="kg">Kilogram (kg)</option>
                        <option value="g">Gram (g)</option>
                        <option value="L">Liter (L)</option>
                        <option value="piece">Piece</option>
                        <option value="bag">Bag</option>
                        <option value="box">Box</option>
                      </select>
                    </div>
                    <div className="form-group">
                      <label>Image URL (Optional)</label>
                      <input type="url" className="form-input" 
                        value={productForm.image_url}
                        onChange={(e) => setProductForm({...productForm, image_url: e.target.value})} />
                    </div>
                  </div>
                  <div className="form-group">
                    <label>Description</label>
                    <textarea className="form-input" rows="3" value={productForm.description}
                      onChange={(e) => setProductForm({...productForm, description: e.target.value})} />
                  </div>
                  <button type="submit" className="btn btn-primary">
                    {editingProduct ? 'Update Product' : 'Add Product'}
                  </button>
                </form>
              )}
            </div>

            <div className="card">
              {products.length === 0 ? (
                <p>No products yet. Add your first product to start selling!</p>
              ) : (
                <table className="table">
                  <thead>
                    <tr>
                      <th>Product Name</th>
                      <th>Category</th>
                      <th>Price</th>
                      <th>Stock</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {products.map(product => (
                      <tr key={product.id}>
                        <td>{product.product_name}</td>
                        <td><span className="badge badge-vendor">{product.category}</span></td>
                        <td>৳{product.price_per_unit}/{product.unit}</td>
                        <td>{product.quantity_available} {product.unit}</td>
                        <td>
                          {product.quantity_available > 0 ? (
                            product.quantity_available < 10 ? (
                              <span className="badge" style={{ background: '#f59e0b' }}>Low Stock</span>
                            ) : (
                              <span className="badge badge-success">In Stock</span>
                            )
                          ) : (
                            <span className="badge" style={{ background: '#ef4444' }}>Out of Stock</span>
                          )}
                        </td>
                        <td>
                          <button onClick={() => handleEditProduct(product)} 
                            className="btn btn-primary" style={{ marginRight: '0.5rem' }}>Edit</button>
                          <button onClick={() => handleDeleteProduct(product.id)} 
                            className="btn btn-danger">Delete</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}

        {/* Orders Tab */}
        {activeTab === 'orders' && (
          <div className="card">
            <h2 className="card-title">Orders Received</h2>
            <p>Manage incoming orders from buyers</p>
            {orders.length === 0 ? (
              <p>No orders yet</p>
            ) : (
              <table className="table">
                <thead>
                  <tr>
                    <th>Order ID</th>
                    <th>Buyer</th>
                    <th>Product</th>
                    <th>Quantity</th>
                    <th>Total</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.map(order => (
                    <tr key={order.id}>
                      <td>#{order.id}</td>
                      <td>{order.buyer_name}</td>
                      <td>{order.product_name}</td>
                      <td>{order.quantity}</td>
                      <td>৳{order.total_price}</td>
                      <td><span className="badge badge-vendor">{order.status}</span></td>
                      <td>{new Date(order.created_at).toLocaleDateString()}</td>
                      <td>
                        <select value={order.status} 
                          onChange={(e) => handleUpdateOrderStatus(order.id, e.target.value)}
                          className="form-input" style={{ padding: '0.25rem' }}>
                          <option value="pending">Pending</option>
                          <option value="confirmed">Confirmed</option>
                          <option value="processing">Processing</option>
                          <option value="shipped">Shipped</option>
                          <option value="completed">Completed</option>
                          <option value="cancelled">Cancelled</option>
                        </select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}

        {/* Sales History Tab */}
        {activeTab === 'sales' && (
          <div>
            <div className="card" style={{ marginBottom: '2rem' }}>
              <h2 className="card-title">💰 Sales Analytics</h2>
              <div className="grid grid-3">
                <div style={{ padding: '1rem', background: '#f9fafb', borderRadius: '8px' }}>
                  <h3>Total Sales</h3>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#059669' }}>
                    ৳{orders.filter(o => o.status === 'completed').reduce((sum, o) => sum + (o.total_price || 0), 0).toFixed(2)}
                  </p>
                </div>
                <div style={{ padding: '1rem', background: '#f9fafb', borderRadius: '8px' }}>
                  <h3>Completed Orders</h3>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#3b82f6' }}>
                    {orders.filter(o => o.status === 'completed').length}
                  </p>
                </div>
                <div style={{ padding: '1rem', background: '#f9fafb', borderRadius: '8px' }}>
                  <h3>Pending Orders</h3>
                  <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#f59e0b' }}>
                    {orders.filter(o => o.status === 'pending' || o.status === 'confirmed').length}
                  </p>
                </div>
              </div>
            </div>

            <div className="card">
              <h2 className="card-title">Sales History</h2>
              {orders.length === 0 ? (
                <p>No sales history yet</p>
              ) : (
                <table className="table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Order ID</th>
                      <th>Buyer</th>
                      <th>Product</th>
                      <th>Quantity</th>
                      <th>Amount</th>
                      <th>Status</th>
                      <th>Profit</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orders.map(order => {
                      const profit = order.status === 'completed' ? (order.total_price * 0.2).toFixed(2) : '0.00';
                      return (
                        <tr key={order.id}>
                          <td>{new Date(order.created_at).toLocaleDateString()}</td>
                          <td>#{order.id}</td>
                          <td>{order.buyer_name}</td>
                          <td>{order.product_name}</td>
                          <td>{order.quantity}</td>
                          <td>৳{order.total_price}</td>
                          <td>
                            <span className={`badge ${order.status === 'completed' ? 'badge-success' : 'badge-vendor'}`}>
                              {order.status}
                            </span>
                          </td>
                          <td style={{ color: order.status === 'completed' ? '#059669' : '#6b7280' }}>
                            ৳{profit}
                          </td>
                        </tr>
                      );
                    })}
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

export default VendorPortal;
