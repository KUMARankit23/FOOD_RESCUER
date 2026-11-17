import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Button } from '../components/common/Button';
import { AlertCircle } from 'lucide-react';

const NotFound = () => {
  return (
    <div className="flex items-center justify-center h-screen bg-cream">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center px-6"
      >
        <div className="mb-6 p-6 bg-soft-sage rounded-full w-fit mx-auto">
          <AlertCircle size={48} className="text-primary-600" />
        </div>
        
        <h1 className="text-5xl font-bold text-text-primary mb-2">404</h1>
        <h2 className="text-2xl font-semibold text-text-secondary mb-4">
          Page Not Found
        </h2>
        <p className="text-text-muted mb-8 max-w-sm">
          The page you're looking for doesn't exist. Let's get you back on track.
        </p>

        <Link to="/">
          <Button>
            Return to Dashboard
          </Button>
        </Link>
      </motion.div>
    </div>
  );
};

export default NotFound;
