'use client';

import { useState } from 'react';
import { trackOrder } from '../lib/api';

export default function OrderTracker() {
  const [orderNumber, setOrderNumber] = useState('');
  const [order, setOrder] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!orderNumber.trim()) {
      setError('Please enter an order number');
      return;
    }

    setLoading(true);
    setError('');
    setOrder(null);

    const { data, error: apiError } = await trackOrder(orderNumber.trim());

    setLoading(false);

    if (apiError) {
      setError(apiError);
    } else {
      setOrder(data);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not available';
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Order Tracking</h1>
        <p>Track your order in real-time</p>
      </div>

      <div className="search-card">
        <form onSubmit={handleSubmit} className="search-form">
          <input
            type="text"
            className="search-input"
            placeholder="Enter your order number..."
            value={orderNumber}
            onChange={(e) => setOrderNumber(e.target.value)}
            disabled={loading}
          />
          <button 
            type="submit" 
            className="search-button"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="loading"></span>
                {' SEARCHING...'}
              </>
            ) : (
              'SEARCH'
            )}
          </button>
        </form>

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {!order && !error && !loading && (
          <div className="alert alert-info">
            Enter your order number to track its status
          </div>
        )}
      </div>

      {order && (
        <div className="order-card">
          <div className="order-header">
            <div className="order-number">
              Order #{order.order_number}
            </div>
            <span className={`status-badge status-${order.status}`}>
              {order.status_display}
            </span>
          </div>

          {order.is_delayed && (
            <div className="delay-alert">
              <svg className="delay-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="delay-content">
                <div className="delay-title">Your order is on its way</div>
                <div className="delay-message">We apologize for the delay. We're working to deliver your order as soon as possible.</div>
              </div>
            </div>
          )}

          {order.current_location && (
            <div className="current-location" style={{ marginBottom: '30px' }}>
              <svg className="location-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <div>
                <div style={{ fontSize: '0.85rem', color: '#666' }}>Current Location</div>
                <div className="current-location-text">{order.current_location}</div>
              </div>
            </div>
          )}

          <div className="delivery-info">
            <div className="info-row">
              <svg className="info-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span className="info-label">Estimated Delivery:</span>
              <span className="info-value">{formatDate(order.estimated_delivery)}</span>
            </div>
            
            {order.delivered_at && (
              <div className="info-row">
                <svg className="info-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="info-label">Delivered On:</span>
                <span className="info-value">{formatDate(order.delivered_at)}</span>
              </div>
            )}
          </div>

          {order.history && order.history.length > 0 && (
            <div className="timeline-section">
              <h3>Tracking History</h3>
              <div className="timeline">
                {order.history.map((item) => (
                  <div key={item.id} className="timeline-item">
                    <div className="timeline-status">{item.status_display}</div>
                    {item.location && (
                      <div className="timeline-location">{item.location}</div>
                    )}
                    {item.description && (
                      <div className="timeline-description">{item.description}</div>
                    )}
                    <div className="timeline-date">{formatDate(item.timestamp)}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
