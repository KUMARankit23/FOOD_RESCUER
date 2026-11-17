import React from 'react';
import { motion } from 'framer-motion';

export const LoadingState = ({ message = 'Loading...' }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col items-center justify-center py-16 px-6"
    >
      <div className="relative w-12 h-12 mb-4">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          className="w-full h-full border-4 border-soft-sage border-t-primary-600 rounded-full"
        />
      </div>
      <p className="text-text-muted text-center">{message}</p>
    </motion.div>
  );
};
