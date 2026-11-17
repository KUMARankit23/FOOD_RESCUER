import React from 'react';
import { motion } from 'framer-motion';

export const EmptyState = ({ icon: Icon, title, description, action }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex flex-col items-center justify-center py-16 px-6"
    >
      <div className="mb-4 p-4 bg-soft-sage rounded-full">
        <Icon size={32} className="text-primary-600" />
      </div>
      <h3 className="text-lg font-semibold text-text-primary mb-2">{title}</h3>
      <p className="text-text-muted text-center max-w-sm mb-6">{description}</p>
      {action && <div className="mt-2">{action}</div>}
    </motion.div>
  );
};
