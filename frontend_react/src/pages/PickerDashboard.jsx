import React, { useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MapPin,
  Truck,
  CheckCircle,
  Clock,
  AlertCircle,
  Navigation,
  Camera,
  Phone,
  MessageCircle,
  Power,
} from 'lucide-react';
import { PageContainer } from '../components/layout/PageContainer';
import { LoadingState } from '../components/common/LoadingState';
import apiClient from '../services/api';
import { format } from 'date-fns';

const PickerDashboard = () => {
  const [pickerStatus, setPickerStatus] = useState('online'); // online, offline, on_job
  const [assignedJobs, setAssignedJobs] = useState([]);
  const [activeJob, setActiveJob] = useState(null);
  const [jobStage, setJobStage] = useState(null); // accepted, en_route_pickup, arrived_pickup, picked, en_route_delivery, arrived_delivery, completed
  const [loading, setLoading] = useState(true);
  const [gpsLocation, setGpsLocation] = useState(null);
  const [showPhotoCapture, setShowPhotoCapture] = useState(false);
  const [foodPhoto, setFoodPhoto] = useState(null);

  // Mock picker ID (in real app, get from auth)
  const pickerId = 'p_001';
  const pickerName = 'Raj Kumar';

  // Fetch available jobs
  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await apiClient.get('/api/v1/runs');
        // Filter jobs that need picking (dispatch decision but not completed)
        const availableJobs = response.data.runs?.filter(
          (run) => run.decision_action === 'dispatch' && run.status !== 'completed'
        ) || [];
        setAssignedJobs(availableJobs);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch jobs:', error);
        // Mock data for demo
        setAssignedJobs([
          {
            run_id: 'abc123xyz',
            decision_action: 'dispatch',
            recipient_id: 'rec_001',
            start_time: new Date().toISOString(),
            quantity: 10,
            food_type: 'Rice',
            status: 'in_progress',
          },
        ]);
        setLoading(false);
      }
    };

    fetchJobs();
    const interval = setInterval(fetchJobs, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval);
  }, []);

  // Get GPS location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.watchPosition(
        (position) => {
          setGpsLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            accuracy: position.coords.accuracy,
          });
        },
        (error) => console.log('GPS error:', error)
      );
    }
  }, []);

  // Accept job
  const handleAcceptJob = async (job) => {
    try {
      await apiClient.post('/api/v1/picker/accept-job', {
        run_id: job.run_id,
        picker_id: pickerId,
        status: 'accepted',
      });
      setActiveJob(job);
      setJobStage('accepted');
      setPickerStatus('on_job');
    } catch (error) {
      console.error('Failed to accept job:', error);
    }
  };

  // Decline job
  const handleDeclineJob = (job) => {
    setAssignedJobs(assignedJobs.filter((j) => j.run_id !== job.run_id));
  };

  // Start heading to pickup
  const handleStartHeading = async () => {
    if (!activeJob) return;
    try {
      await apiClient.post('/api/v1/picker/update-status', {
        run_id: activeJob.run_id,
        picker_id: pickerId,
        status: 'en_route_to_pickup',
        location: gpsLocation,
      });
      setJobStage('en_route_pickup');
    } catch (error) {
      console.error('Failed to update status:', error);
    }
  };

  // Arrived at pickup
  const handleArrivedPickup = async () => {
    if (!activeJob) return;
    try {
      await apiClient.post('/api/v1/picker/update-status', {
        run_id: activeJob.run_id,
        picker_id: pickerId,
        status: 'arrived_at_pickup',
        location: gpsLocation,
      });
      setJobStage('arrived_pickup');
    } catch (error) {
      console.error('Failed to update status:', error);
    }
  };

  // Food picked up
  const handleFoodPickedUp = async () => {
    if (!activeJob) return;
    try {
      await apiClient.post('/api/v1/picker/pickup-complete', {
        run_id: activeJob.run_id,
        picker_id: pickerId,
        status: 'food_picked',
        photo_url: foodPhoto,
        weight: activeJob.quantity,
        timestamp: new Date().toISOString(),
      });
      setJobStage('picked');
      setShowPhotoCapture(false);
    } catch (error) {
      console.error('Failed to mark as picked:', error);
    }
  };

  // Start delivery
  const handleStartDelivery = async () => {
    if (!activeJob) return;
    try {
      await apiClient.post('/api/v1/picker/update-status', {
        run_id: activeJob.run_id,
        picker_id: pickerId,
        status: 'en_route_to_delivery',
        location: gpsLocation,
      });
      setJobStage('en_route_delivery');
    } catch (error) {
      console.error('Failed to start delivery:', error);
    }
  };

  // Arrived at delivery
  const handleArrivedDelivery = async () => {
    if (!activeJob) return;
    try {
      await apiClient.post('/api/v1/picker/update-status', {
        run_id: activeJob.run_id,
        picker_id: pickerId,
        status: 'arrived_at_delivery',
        location: gpsLocation,
      });
      setJobStage('arrived_delivery');
    } catch (error) {
      console.error('Failed to update status:', error);
    }
  };

  // Complete delivery
  const handleCompleteDelivery = async () => {
    if (!activeJob) return;
    try {
      await apiClient.post('/api/v1/picker/delivery-complete', {
        run_id: activeJob.run_id,
        picker_id: pickerId,
        status: 'delivered',
        location: gpsLocation,
        recipient_signature: 'confirmed',
        timestamp: new Date().toISOString(),
      });
      setJobStage('completed');
      setActiveJob(null);
      setPickerStatus('online');
      setAssignedJobs(assignedJobs.filter((j) => j.run_id !== activeJob.run_id));
    } catch (error) {
      console.error('Failed to complete delivery:', error);
    }
  };

  const handlePhotoCapture = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setFoodPhoto(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  if (loading) {
    return <LoadingState message="Loading picker dashboard..." />;
  }

  // Active Job View
  if (activeJob && jobStage) {
    return (
      <div className="min-h-screen bg-cream p-4">
        {/* Header */}
        <div className="mb-6 pt-4">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-2xl font-bold text-text-primary">Active Delivery</h1>
              <p className="text-sm text-text-muted">
                {pickerName} • {format(new Date(), 'MMM dd, HH:mm')}
              </p>
            </div>
            <button
              onClick={() => {
                setActiveJob(null);
                setPickerStatus('online');
                setJobStage(null);
              }}
              className="p-2 hover:bg-white rounded transition-colors text-text-muted"
            >
              ✕
            </button>
          </div>

          {/* GPS Location */}
          {gpsLocation && (
            <div className="bg-white rounded-lg border border-soft-sage p-3 mb-4 text-xs">
              <p className="text-text-muted">📍 Current Location:</p>
              <p className="font-mono text-primary-600">
                {gpsLocation.lat.toFixed(4)}, {gpsLocation.lng.toFixed(4)}
              </p>
            </div>
          )}
        </div>

        {/* Stage-Specific UI */}
        <div className="space-y-4">
          {/* Stage: ACCEPTED */}
          {jobStage === 'accepted' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-lg border border-soft-sage shadow-sm p-6 space-y-4"
            >
              <h2 className="text-lg font-semibold text-text-primary">✅ Job Accepted</h2>

              <div className="bg-cream rounded-lg p-4 space-y-3">
                <div>
                  <p className="text-xs text-text-muted uppercase font-medium">Food Type</p>
                  <p className="text-lg font-semibold text-text-primary">{activeJob.food_type}</p>
                </div>
                <div>
                  <p className="text-xs text-text-muted uppercase font-medium">Quantity</p>
                  <p className="text-lg font-semibold text-text-primary">{activeJob.quantity} kg</p>
                </div>
                <div>
                  <p className="text-xs text-text-muted uppercase font-medium">Recipient</p>
                  <p className="text-lg font-semibold text-text-primary">
                    Recipient #{activeJob.recipient_id?.slice(0, 4)}
                  </p>
                </div>
              </div>

              <button
                onClick={handleStartHeading}
                className="w-full py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
              >
                <Navigation size={18} />
                Start Navigation to Pickup
              </button>

              <button
                onClick={() => {
                  setActiveJob(null);
                  setJobStage(null);
                  setPickerStatus('online');
                }}
                className="w-full py-2 border border-soft-sage text-text-primary rounded-lg font-semibold hover:bg-soft-sage transition-colors"
              >
                Decline Job
              </button>
            </motion.div>
          )}

          {/* Stage: EN ROUTE TO PICKUP */}
          {jobStage === 'en_route_pickup' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-lg border border-soft-sage shadow-sm p-6 space-y-4"
            >
              <h2 className="text-lg font-semibold text-text-primary">🚗 Heading to Pickup</h2>

              <div className="bg-gradient-to-r from-primary-100 to-primary-50 rounded-lg p-4">
                <p className="text-sm text-primary-700 font-medium">
                  📍 Navigate to pickup location using Google Maps or your preferred navigation app
                </p>
              </div>

              <a
                href="https://maps.google.com/?q=12.9716,77.5946"
                target="_blank"
                rel="noopener noreferrer"
                className="w-full py-3 bg-success text-white rounded-lg font-semibold hover:bg-success-dark transition-colors flex items-center justify-center gap-2"
              >
                <MapPin size={18} />
                Open Google Maps
              </a>

              <button
                onClick={handleArrivedPickup}
                className="w-full py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition-colors"
              >
                ✅ I've Arrived at Pickup
              </button>
            </motion.div>
          )}

          {/* Stage: ARRIVED AT PICKUP */}
          {jobStage === 'arrived_pickup' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-lg border border-soft-sage shadow-sm p-6 space-y-4"
            >
              <h2 className="text-lg font-semibold text-text-primary">📦 Collecting Food</h2>

              <div className="bg-warning-light rounded-lg p-4 border border-warning">
                <p className="text-sm text-warning font-medium">
                  ⚠️ Verify the food quality and condition before accepting
                </p>
              </div>

              {!showPhotoCapture ? (
                <>
                  <button
                    onClick={() => setShowPhotoCapture(true)}
                    className="w-full py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
                  >
                    <Camera size={18} />
                    Take Food Condition Photo
                  </button>

                  {foodPhoto && (
                    <div className="bg-cream rounded-lg p-4">
                      <p className="text-xs text-text-muted mb-2">Photo captured ✅</p>
                      <img src={foodPhoto} alt="Food" className="w-full h-40 object-cover rounded" />
                    </div>
                  )}

                  <button
                    onClick={handleFoodPickedUp}
                    disabled={!foodPhoto}
                    className="w-full py-3 bg-success text-white rounded-lg font-semibold hover:bg-success-dark transition-colors disabled:bg-text-muted disabled:cursor-not-allowed"
                  >
                    ✅ Food Picked Up
                  </button>
                </>
              ) : (
                <div className="space-y-4">
                  <input
                    type="file"
                    accept="image/*"
                    capture="environment"
                    onChange={handlePhotoCapture}
                    className="w-full"
                  />
                  <button
                    onClick={() => setShowPhotoCapture(false)}
                    className="w-full py-2 border border-soft-sage rounded-lg"
                  >
                    Cancel
                  </button>
                </div>
              )}
            </motion.div>
          )}

          {/* Stage: PICKED */}
          {jobStage === 'picked' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-lg border border-soft-sage shadow-sm p-6 space-y-4"
            >
              <h2 className="text-lg font-semibold text-text-primary">✅ Food Picked!</h2>

              <div className="bg-success-light rounded-lg p-4 text-center">
                <p className="text-sm text-success font-semibold">
                  Food successfully collected and verified
                </p>
              </div>

              <button
                onClick={handleStartDelivery}
                className="w-full py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
              >
                <Truck size={18} />
                Start Delivery to Recipient
              </button>
            </motion.div>
          )}

          {/* Stage: EN ROUTE TO DELIVERY */}
          {jobStage === 'en_route_delivery' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-lg border border-soft-sage shadow-sm p-6 space-y-4"
            >
              <h2 className="text-lg font-semibold text-text-primary">🚚 Delivery in Progress</h2>

              <div className="bg-gradient-to-r from-primary-100 to-primary-50 rounded-lg p-4">
                <p className="text-sm text-primary-700 font-medium">
                  📍 Navigate to recipient location for delivery
                </p>
              </div>

              <a
                href="https://maps.google.com/?q=13.0827,80.2707"
                target="_blank"
                rel="noopener noreferrer"
                className="w-full py-3 bg-success text-white rounded-lg font-semibold hover:bg-success-dark transition-colors flex items-center justify-center gap-2"
              >
                <MapPin size={18} />
                Open Google Maps
              </a>

              <button
                onClick={handleArrivedDelivery}
                className="w-full py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition-colors"
              >
                ✅ I've Arrived at Delivery
              </button>
            </motion.div>
          )}

          {/* Stage: ARRIVED AT DELIVERY */}
          {jobStage === 'arrived_delivery' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-lg border border-soft-sage shadow-sm p-6 space-y-4"
            >
              <h2 className="text-lg font-semibold text-text-primary">📍 At Recipient Location</h2>

              <div className="bg-cream rounded-lg p-4 space-y-2 text-sm">
                <p>🍚 <strong>Item:</strong> {activeJob.food_type} ({activeJob.quantity} kg)</p>
                <p>👥 <strong>Recipient:</strong> Recipient #{activeJob.recipient_id?.slice(0, 4)}</p>
                <p>⏱️ <strong>Time:</strong> {format(new Date(), 'HH:mm:ss')}</p>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <a
                  href="tel:+919876543210"
                  className="py-3 bg-info text-white rounded-lg font-semibold hover:bg-info-dark transition-colors flex items-center justify-center gap-2 text-sm"
                >
                  <Phone size={16} />
                  Call Recipient
                </a>

                <a
                  href="sms:+919876543210?body=I have arrived with your food delivery"
                  className="py-3 bg-info text-white rounded-lg font-semibold hover:bg-info-dark transition-colors flex items-center justify-center gap-2 text-sm"
                >
                  <MessageCircle size={16} />
                  Text
                </a>
              </div>

              <button
                onClick={handleCompleteDelivery}
                className="w-full py-3 bg-success text-white rounded-lg font-semibold hover:bg-success-dark transition-colors"
              >
                ✅ Delivery Complete
              </button>
            </motion.div>
          )}

          {/* Stage: COMPLETED */}
          {jobStage === 'completed' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-lg border border-soft-sage shadow-sm p-6 space-y-4 text-center"
            >
              <div className="text-5xl mb-4">🎉</div>
              <h2 className="text-lg font-semibold text-text-primary">Delivery Completed!</h2>
              <p className="text-sm text-text-secondary">
                Thank you for delivering food to those in need
              </p>
              <div className="bg-success-light rounded-lg p-4 mt-4">
                <p className="text-success font-semibold">✅ Job marked as complete</p>
              </div>
              <button
                onClick={() => {
                  setActiveJob(null);
                  setJobStage(null);
                  setPickerStatus('online');
                }}
                className="w-full py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition-colors"
              >
                Back to Job List
              </button>
            </motion.div>
          )}
        </div>
      </div>
    );
  }

  // Job List View
  return (
    <PageContainer>
      {/* Header */}
      <div className="mb-8 flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-text-primary">🚗 Picker Dashboard</h1>
          <p className="text-text-muted mt-1">
            Welcome, {pickerName} • {assignedJobs.length} job(s) available
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div
            className={`w-4 h-4 rounded-full ${
              pickerStatus === 'online' ? 'bg-success' : 'bg-text-muted'
            } animate-pulse`}
          />
          <span className="text-sm font-medium text-text-primary">
            {pickerStatus === 'online' ? '🟢 Online' : '🔴 Offline'}
          </span>
        </div>
      </div>

      {/* GPS Location Widget */}
      {gpsLocation && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 bg-white rounded-lg border border-soft-sage p-4"
        >
          <p className="text-xs text-text-muted mb-1">📍 Your Location</p>
          <p className="text-sm font-mono text-primary-600">
            {gpsLocation.lat.toFixed(4)}, {gpsLocation.lng.toFixed(4)} (±{gpsLocation.accuracy.toFixed(0)}m)
          </p>
        </motion.div>
      )}

      {/* Available Jobs */}
      <div className="grid grid-cols-1 gap-4">
        {assignedJobs.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg border border-soft-sage">
            <p className="text-lg text-text-muted mb-2">📭 No jobs available right now</p>
            <p className="text-sm text-text-muted">Check back in a few moments</p>
          </div>
        ) : (
          assignedJobs.map((job, idx) => (
            <motion.div
              key={job.run_id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="bg-white rounded-lg border border-soft-sage shadow-sm overflow-hidden hover:shadow-md transition-shadow"
            >
              <div className="p-6 space-y-4">
                {/* Job Header */}
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-text-primary text-lg">
                      🍱 {job.food_type}
                    </h3>
                    <p className="text-sm text-text-muted">
                      Quantity: <span className="font-semibold">{job.quantity} kg</span>
                    </p>
                  </div>
                  <span className="px-3 py-1 rounded-full bg-warning-light text-warning text-xs font-semibold">
                    NEW
                  </span>
                </div>

                {/* Job Details */}
                <div className="grid grid-cols-2 gap-3 bg-cream p-3 rounded-lg">
                  <div>
                    <p className="text-xs text-text-muted uppercase font-medium">Pickup</p>
                    <p className="text-sm font-semibold text-text-primary">Main Building</p>
                  </div>
                  <div>
                    <p className="text-xs text-text-muted uppercase font-medium">Delivery</p>
                    <p className="text-sm font-semibold text-text-primary">Community Center</p>
                  </div>
                </div>

                {/* Priority Badge */}
                <div className="flex items-center gap-2">
                  <AlertCircle size={16} className="text-warning" />
                  <span className="text-sm font-medium text-warning">High Priority</span>
                </div>

                {/* Action Buttons */}
                <div className="grid grid-cols-2 gap-3 pt-2">
                  <button
                    onClick={() => handleDeclineJob(job)}
                    className="py-2 border border-soft-sage text-text-primary rounded-lg font-semibold hover:bg-soft-sage transition-colors text-sm"
                  >
                    Decline
                  </button>
                  <button
                    onClick={() => handleAcceptJob(job)}
                    className="py-2 bg-success text-white rounded-lg font-semibold hover:bg-success-dark transition-colors text-sm"
                  >
                    Accept Job
                  </button>
                </div>
              </div>
            </motion.div>
          ))
        )}
      </div>

      {/* Footer Info */}
      <div className="mt-8 text-center text-xs text-text-muted">
        <p>Last updated: {format(new Date(), 'HH:mm:ss')}</p>
      </div>
    </PageContainer>
  );
};

export default PickerDashboard;
