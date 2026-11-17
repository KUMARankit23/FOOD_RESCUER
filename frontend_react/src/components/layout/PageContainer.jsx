import React from 'react';
import { motion } from 'framer-motion';

export const PageContainer = ({ children, className = '' }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
      className={`p-6 md:p-8 max-w-7xl ${className}`}
    >
      {children}
    </motion.div>
  );
};
