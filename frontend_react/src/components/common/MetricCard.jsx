import React from 'react';
import { motion } from 'framer-motion';

export const MetricCard = ({ 
  icon: Icon, 
  label, 
  value, 
  unit = '', 
  subtitle = '', 
  trend = null,
  color = 'primary'
}) => {
  const accentColor = {
    primary: '#3F654A',
    success: '#43865B',
    warning: '#D69B43',
    danger: '#C65C50',
    info: '#6689A4',
  }[color];

  return (
    <motion.div
      className="bg-white rounded-lg border border-soft-sage p-6 shadow-sm hover:shadow-md transition-shadow"
      whileHover={{ y: -4 }}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="text-4xl text-primary-600">
          {Icon && <Icon size={40} />}
        </div>
        {trend && (
          <div className={`text-sm font-semibold ${trend.positive ? 'text-success' : 'text-danger'}`}>
            {trend.positive ? '↑' : '↓'} {trend.value}
          </div>
        )}
      </div>
      
      <div className="mb-3">
        <div className="text-sm text-text-secondary font-medium mb-1">{label}</div>
        <div className="flex items-baseline gap-2">
          <span className="text-3xl font-bold" style={{ color: accentColor }}>
            {value}
          </span>
          {unit && <span className="text-text-secondary">{unit}</span>}
        </div>
      </div>

      {subtitle && (
        <div className="text-xs text-text-muted">{subtitle}</div>
      )}
    </motion.div>
  );
};
