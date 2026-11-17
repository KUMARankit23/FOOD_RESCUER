import React from 'react';
import { motion } from 'framer-motion';
import { AlertCircle } from 'lucide-react';

export const ErrorState = ({ title, description, onRetry }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex flex-col items-center justify-center py-16 px-6 bg-danger-bg rounded-lg"
    >
      <div className="mb-4 p-4 bg-danger-light rounded-full">
        <AlertCircle size={32} className="text-danger" />
      </div>
      <h3 className="text-lg font-semibold text-danger mb-2">{title}</h3>
      <p className="text-text-secondary text-center max-w-sm mb-6">{description}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-danger text-white rounded-md hover:opacity-90 transition-opacity"
        >
          Try Again
        </button>
      )}
    </motion.div>
  );
};
