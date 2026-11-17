import React from 'react';
import { motion } from 'framer-motion';

export const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  className = '',
  type = 'button',
  ...props
}) => {
  const baseStyles = 'font-medium rounded-md transition-all inline-flex items-center justify-center gap-2 whitespace-nowrap';

  const variants = {
    primary: 'bg-primary-400 text-white hover:bg-primary-600 disabled:bg-text-muted',
    secondary: 'bg-soft-sage text-primary-600 hover:bg-sage-300 disabled:bg-text-muted',
    outline: 'border border-primary-400 text-primary-400 hover:bg-soft-sage disabled:border-text-muted disabled:text-text-muted',
    danger: 'bg-danger text-white hover:opacity-90 disabled:bg-text-muted',
    ghost: 'text-primary-400 hover:bg-soft-sage disabled:text-text-muted',
  };

  const sizes = {
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2.5 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <motion.button
      type={type}
      disabled={disabled || loading}
      onClick={onClick}
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      whileHover={!disabled && !loading ? { y: -2 } : {}}
      whileTap={!disabled && !loading ? { y: 0 } : {}}
      {...props}
    >
      {loading && (
        <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      )}
      {children}
    </motion.button>
  );
};
