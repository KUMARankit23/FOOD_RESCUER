import React from 'react';
import { motion } from 'framer-motion';
import { format } from 'date-fns';
import { MapPin, Package } from 'lucide-react';
import { STATUS_COLORS } from '../../utils/constants';

export const DispatchTable = ({ dispatches = [] }) => {
  if (!dispatches || dispatches.length === 0) {
    return (
      <div className="text-center py-8 text-text-muted">
        No dispatches available
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="grid grid-cols-1 gap-4"
    >
      {dispatches.map((dispatch, idx) => (
        <motion.div
          key={dispatch.run_id}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: idx * 0.05 }}
          className="border border-soft-sage rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1">
              <h4 className="font-semibold text-text-primary flex items-center gap-2">
                <Package size={18} className="text-primary-600" />
                Dispatch: {dispatch.recipient_name || 'Recipient'}
              </h4>
              <p className="text-xs text-text-muted mt-1">
                {format(new Date(dispatch.created_at), 'MMM dd, yyyy HH:mm:ss')}
              </p>
            </div>
            <span
              className="px-3 py-1 rounded-full text-xs font-semibold"
              style={{
                backgroundColor: STATUS_COLORS.success.bg,
                color: STATUS_COLORS.success.color,
              }}
            >
              {dispatch.status}
            </span>
          </div>

          <div className="grid grid-cols-3 gap-4 pt-3 border-t border-soft-sage">
            <div>
              <p className="text-xs text-text-muted font-medium">From</p>
              <p className="text-sm text-text-primary flex items-center gap-1 mt-1">
                <MapPin size={14} className="text-primary-600" />
                {dispatch.donor_location}
              </p>
            </div>
            <div>
              <p className="text-xs text-text-muted font-medium">To</p>
              <p className="text-sm text-text-primary flex items-center gap-1 mt-1">
                <MapPin size={14} className="text-accent" />
                {dispatch.recipient_name}
              </p>
            </div>
            <div>
              <p className="text-xs text-text-muted font-medium">Quantity</p>
              <p className="text-sm font-semibold text-text-primary mt-1">
                {dispatch.quantity} units
              </p>
            </div>
          </div>
        </motion.div>
      ))}
    </motion.div>
  );
};
