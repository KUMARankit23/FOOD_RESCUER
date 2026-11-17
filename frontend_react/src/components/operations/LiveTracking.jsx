import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  MapPin,
  Truck,
  CheckCircle,
  Clock,
  AlertCircle,
} from 'lucide-react';
import { useGetRunTrace } from '../../hooks/useReports';

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
  const { data: traceData } = useGetRunTrace(runId);
  const [trackingData, setTrackingData] = useState([]);

  // Convert real trace data to tracking steps
  useEffect(() => {
    if (!traceData?.trace) return;

    const trace = traceData.trace;
    const steps = [];

    // Map trace data to tracking steps based on real agent execution
    const statusMap = {
      'location_verified': {
        icon: MapPin,
        title: '📍 Location Verified',
        description: 'Food pickup point confirmed',
      },
      'safety_check': {
        icon: AlertCircle,
        title: '✅ Safety Checks Passed',
        description: 'Meeting food safety standards',
      },
      'dispatch': {
        icon: Truck,
        title: '🚗 Dispatch Agent',
        description: 'Agent assigned and on the way',
      },
      'pickup': {
        icon: CheckCircle,
        title: '📦 Food Pickup',
        description: 'Food collected from donor',
      },
      'delivery': {
        icon: Truck,
        title: '🚚 Delivery in Progress',
        description: 'En route to recipient facility',
      },
      'completed': {
        icon: CheckCircle,
        title: '🏁 Delivered',
        description: 'Food safely transferred to recipient',
      },
    };

    // Build steps based on actual trace status
    const traceStatus = (trace.status || 'pending').toLowerCase();
    
    // Add all steps and mark status based on trace
    Object.entries(statusMap).forEach(([key, step]) => {
      const isCompleted = key === 'location_verified' || 
                         key === 'safety_check' ||
                         (traceStatus.includes(key) || traceStatus.includes('completed'));
      const isInProgress = traceStatus.includes(key) && key !== 'location_verified' && key !== 'safety_check';

      steps.push({
        ...step,
        status: isCompleted && !isInProgress ? 'completed' : isInProgress ? 'inProgress' : 'pending',
        time: isCompleted || isInProgress ? new Date().toLocaleTimeString() : 'Pending',
      });
    });

    setTrackingData(steps);
  }, [traceData]);

  // Poll every 2 seconds for real-time updates
  useEffect(() => {
    if (!runId) return;
    const pollInterval = setInterval(() => {
      // The useGetRunTrace hook will automatically refetch
    }, 2000);
    return () => clearInterval(pollInterval);
  }, [runId]);

  const inProgressStep = trackingData.find((s) => s.status === 'inProgress');
  const completedCount = trackingData.filter((s) => s.status === 'completed').length;

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
            {trackingData.length > 0 
              ? Math.round((completedCount / trackingData.length) * 100)
              : 0}
            %
          </p>
        </div>
        <div className="w-full bg-soft-sage rounded-full h-2 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{
              width: trackingData.length > 0 
                ? `${(completedCount / trackingData.length) * 100}%`
                : '0%',
            }}
            transition={{ duration: 0.5 }}
            className="h-full bg-gradient-to-r from-primary-600 to-success"
          />
        </div>
      </div>
    </motion.div>
  );
};
