import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertCircle, Trash2, Minus } from 'lucide-react';
import { DECISIONS } from '../../utils/constants';

const decisionIcons = {
  DISPATCH: CheckCircle,
  HOLD: AlertCircle,
  DISCARD: Trash2,
  NO_PICKUP: Minus,
};

export const DecisionCard = ({ decision = {} }) => {
  const decisionKey = decision.action?.toUpperCase() || 'NO_PICKUP';
  const decisionInfo = DECISIONS[decisionKey] || DECISIONS.NO_PICKUP;
  const DecisionIcon = decisionIcons[decisionKey] || AlertCircle;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="border-2 rounded-lg p-6"
      style={{ borderColor: decisionInfo.color, backgroundColor: decisionInfo.bg }}
    >
      <div className="flex items-center gap-4">
        <div
          className="p-3 rounded-full"
          style={{ backgroundColor: decisionInfo.color + '20' }}
        >
          <DecisionIcon size={32} style={{ color: decisionInfo.color }} />
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-bold" style={{ color: decisionInfo.color }}>
            {decisionInfo.label}
          </h3>
          {decision.recipient_name && (
            <p className="text-sm text-text-secondary mt-1">
              Recipient: {decision.recipient_name}
            </p>
          )}
          {decision.reason && (
            <p className="text-sm text-text-secondary mt-1">
              Reason: {decision.reason}
            </p>
          )}
        </div>
      </div>
    </motion.div>
  );
};
