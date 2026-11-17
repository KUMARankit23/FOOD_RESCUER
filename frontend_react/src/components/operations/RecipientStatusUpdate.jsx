import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, AlertCircle, MessageSquare, Send, X } from 'lucide-react';

export const RecipientStatusUpdate = ({ runId, currentStatus, onStatusUpdate }) => {
  const [showUpdateForm, setShowUpdateForm] = useState(false);
  const [selectedStatus, setSelectedStatus] = useState('');
  const [feedback, setFeedback] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const statusOptions = [
    {
      id: 'received',
      label: '✅ Food Received',
      description: 'I have received the food',
      color: 'bg-success-light text-success',
    },
    {
      id: 'partial',
      label: '⚠️ Partially Received',
      description: 'I received only part of the food',
      color: 'bg-warning-light text-warning',
    },
    {
      id: 'issue',
      label: '❌ Issue with Delivery',
      description: 'There was an issue with the food/delivery',
      color: 'bg-danger-light text-danger',
    },
    {
      id: 'feedback',
      label: '💬 Provide Feedback',
      description: 'Share feedback about the food or service',
      color: 'bg-blue-100 text-blue-600',
    },
  ];

  const handleSubmitUpdate = async () => {
    if (!selectedStatus) return;

    setIsSubmitting(true);

    try {
      // Simulate API call to update status
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const updateData = {
        run_id: runId,
        recipient_status: selectedStatus,
        feedback: feedback || null,
        timestamp: new Date().toISOString(),
      };

      // Call parent callback
      if (onStatusUpdate) {
        onStatusUpdate(updateData);
      }

      setSuccessMessage(`✅ Status updated: ${statusOptions.find((s) => s.id === selectedStatus)?.label}`);

      // Reset form
      setTimeout(() => {
        setShowUpdateForm(false);
        setSelectedStatus('');
        setFeedback('');
        setSuccessMessage('');
      }, 2000);
    } catch (error) {
      console.error('Error updating status:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="bg-white rounded-lg border border-soft-sage shadow-sm p-6"
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-text-primary flex items-center gap-2">
          <MessageSquare size={20} className="text-primary-600" />
          Recipient Status Update
        </h3>
        {!showUpdateForm && (
          <button
            onClick={() => setShowUpdateForm(true)}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium"
          >
            Update Status
          </button>
        )}
      </div>

      <AnimatePresence>
        {successMessage && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mb-4 p-3 bg-success-light text-success rounded-lg text-sm font-medium"
          >
            {successMessage}
          </motion.div>
        )}
      </AnimatePresence>

      {!showUpdateForm ? (
        <div className="space-y-2 text-sm text-text-secondary">
          <p>
            📍 <strong>Current Status:</strong> {currentStatus || 'Pending'}
          </p>
          <p>
            💬 Use the button above to confirm receipt and provide feedback about the food or
            delivery service.
          </p>
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="space-y-4"
        >
          {/* Status Options */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {statusOptions.map((option) => (
              <motion.button
                key={option.id}
                onClick={() => setSelectedStatus(option.id)}
                whileHover={{ scale: 1.02 }}
                className={`p-4 rounded-lg border-2 transition-all text-left ${
                  selectedStatus === option.id
                    ? `border-primary-600 ${option.color} bg-opacity-20`
                    : 'border-soft-sage hover:border-primary-300'
                }`}
              >
                <p className="font-semibold text-sm">{option.label}</p>
                <p className="text-xs text-text-secondary mt-1">{option.description}</p>
              </motion.button>
            ))}
          </div>

          {/* Feedback Text Area */}
          {selectedStatus && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="space-y-2"
            >
              <label className="block text-sm font-medium text-text-primary">
                Additional Comments (Optional)
              </label>
              <textarea
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                placeholder="Share any feedback or details about the delivery..."
                className="w-full px-4 py-3 rounded-lg border border-soft-sage bg-cream focus:outline-none focus:ring-2 focus:ring-primary-600 resize-none"
                rows={4}
              />
            </motion.div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-3 pt-2">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleSubmitUpdate}
              disabled={!selectedStatus || isSubmitting}
              className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-text-muted transition-colors flex items-center justify-center gap-2 font-medium"
            >
              <Send size={18} />
              {isSubmitting ? 'Updating...' : 'Submit Update'}
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => {
                setShowUpdateForm(false);
                setSelectedStatus('');
                setFeedback('');
              }}
              className="px-4 py-2 bg-soft-sage text-text-primary rounded-lg hover:bg-sage-300 transition-colors flex items-center gap-2 font-medium"
            >
              <X size={18} />
              Cancel
            </motion.button>
          </div>
        </motion.div>
      )}

      {/* Info Box */}
      <div className="mt-6 p-4 bg-primary-50 rounded-lg border border-primary-200">
        <p className="text-xs text-text-secondary">
          <strong>ℹ️ How it works:</strong> When you receive the food, please update your status
          here. This helps the donor and system track the delivery and improves future operations.
          Your feedback is valuable!
        </p>
      </div>
    </motion.div>
  );
};
