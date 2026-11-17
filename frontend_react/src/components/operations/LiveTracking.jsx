import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  MapPin,
  Truck,
  CheckCircle,
  Clock,
  AlertCircle,
} from 'lucide-react';

const TrackingStep = ({ icon: Icon, status, title, description, time, isLast }) => {
  const statusColors = {
    completed: 'bg-success text-white',
    inProgress: 'bg-primary-600 text-white animate-pulse',
    pending: 'bg-soft-sage text-text-secondary',
  };

  return (
    <div className="flex gap-4 mb-6 last:mb-0">
      {/* Timeline connector */}
      <div className="flex flex-col items-center">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className={`w-10 h-10 rounded-full flex items-center justify-center ${statusColors[status]} flex-shrink-0`}
        >
          <Icon size={20} />
        </motion.div>
        {!isLast && (
          <div
            className={`w-1 h-12 mt-2 ${
              status === 'completed' ? 'bg-success' : 'bg-soft-sage'
            }`}
          />
        )}
      </div>

      {/* Content */}
      <div className="flex-1 pt-1">
        <div className="flex justify-between items-start mb-1">
          <h4 className="font-semibold text-text-primary">{title}</h4>
          {time && (
            <span className="text-xs text-text-muted font-mono">{time}</span>
          )}
        </div>
        <p className="text-sm text-text-secondary">{description}</p>
      </div>
    </div>
  );
};

export const LiveTracking = ({ runId }) => {
  const [trackingData, setTrackingData] = useState([
    {
      icon: MapPin,
      status: 'completed',
      title: '📍 Location Verified',
      description: 'Food pickup point confirmed and validated',
      time: '2:15 PM',
    },
    {
      icon: AlertCircle,
      status: 'completed',
      title: '✅ Safety Checks Passed',
      description: 'Temperature and prep time meet standards',
      time: '2:16 PM',
    },
    {
      icon: Truck,
      status: 'inProgress',
      title: '🚗 Agent Dispatched',
      description: 'Driver is on the way - ETA 12 minutes',
      time: 'In Progress',
    },
    {
      icon: CheckCircle,
      status: 'pending',
      title: '📦 Pickup',
      description: 'Waiting for food collection',
      time: 'Pending',
    },
    {
      icon: Truck,
      status: 'pending',
      title: '🚚 Delivery in Progress',
      description: 'En route to recipient facility',
      time: 'Pending',
    },
    {
      icon: CheckCircle,
      status: 'pending',
      title: '🏁 Delivered',
      description: 'Food safely transferred to recipient',
      time: 'Pending',
    },
  ]);

  // Simulate progress updates
  useEffect(() => {
    if (!runId) return;

    const progressInterval = setInterval(() => {
      setTrackingData((prev) => {
        const updated = [...prev];
        const inProgressIdx = updated.findIndex((s) => s.status === 'inProgress');

        if (inProgressIdx < updated.length - 1) {
          updated[inProgressIdx].status = 'completed';
          updated[inProgressIdx + 1].status = 'inProgress';
          updated[inProgressIdx + 1].time = new Date().toLocaleTimeString();
        }

        return updated;
      });
    }, 6000);

    return () => clearInterval(progressInterval);
  }, [runId]);

  const inProgressStep = trackingData.find((s) => s.status === 'inProgress');

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="bg-white rounded-lg border border-soft-sage shadow-sm p-6"
    >
      <div className="mb-6">
        <h3 className="font-semibold text-text-primary mb-2">Live Tracking</h3>
        {inProgressStep && (
          <p className="text-sm text-primary-600 font-medium flex items-center gap-2">
            <span className="w-2 h-2 bg-primary-600 rounded-full animate-pulse" />
            {inProgressStep.title}
          </p>
        )}
      </div>

      <div>
        {trackingData.map((step, idx) => (
          <TrackingStep
            key={idx}
            icon={step.icon}
            status={step.status}
            title={step.title}
            description={step.description}
            time={step.time}
            isLast={idx === trackingData.length - 1}
          />
        ))}
      </div>

      {/* Progress Bar */}
      <div className="mt-8 pt-6 border-t border-soft-sage">
        <div className="flex justify-between mb-2">
          <p className="text-xs font-medium text-text-secondary">Overall Progress</p>
          <p className="text-xs font-bold text-primary-600">
            {Math.round(
              (trackingData.filter((s) => s.status === 'completed').length /
                trackingData.length) *
                100
            )}
            %
          </p>
        </div>
        <div className="w-full bg-soft-sage rounded-full h-2 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{
              width: `${
                (trackingData.filter((s) => s.status === 'completed').length /
                  trackingData.length) *
                100
              }%`,
            }}
            transition={{ duration: 0.5 }}
            className="h-full bg-gradient-to-r from-primary-600 to-success"
          />
        </div>
      </div>
    </motion.div>
  );
};
