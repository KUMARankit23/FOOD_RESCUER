import React from 'react';
import { motion } from 'framer-motion';
import { format } from 'date-fns';
import { Eye } from 'lucide-react';
import { DECISIONS, STATUS_COLORS } from '../../utils/constants';

export const RunHistoryTable = ({ runs = [], onViewRun }) => {
  if (!runs || runs.length === 0) {
    return (
      <div className="text-center py-8 text-text-muted">
        No runs available
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="overflow-x-auto"
    >
      <table className="w-full">
        <thead>
          <tr className="border-b border-soft-sage bg-soft-sage">
            <th className="px-4 py-3 text-left text-sm font-semibold text-text-primary">Run ID</th>
            <th className="px-4 py-3 text-left text-sm font-semibold text-text-primary">Decision</th>
            <th className="px-4 py-3 text-left text-sm font-semibold text-text-primary">Recipient</th>
            <th className="px-4 py-3 text-left text-sm font-semibold text-text-primary">Time</th>
            <th className="px-4 py-3 text-left text-sm font-semibold text-text-primary">Duration</th>
            <th className="px-4 py-3 text-right text-sm font-semibold text-text-primary">Action</th>
          </tr>
        </thead>
        <tbody>
          {runs.map((run, idx) => {
            const decisionInfo = DECISIONS[run.decision_action?.toUpperCase()] || DECISIONS.NO_PICKUP;
            const statusColor = STATUS_COLORS[run.status] || STATUS_COLORS.pending;

            return (
              <motion.tr
                key={run.run_id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: idx * 0.05 }}
                className="border-b border-soft-sage hover:bg-soft-sage transition-colors"
              >
                <td className="px-4 py-3">
                  <code className="text-xs font-mono text-primary-600 bg-soft-sage px-2 py-1 rounded">
                    {run.run_id?.slice(0, 8)}...
                  </code>
                </td>
                <td className="px-4 py-3">
                  <span
                    className="inline-block px-3 py-1 rounded-full text-xs font-semibold"
                    style={{
                      backgroundColor: decisionInfo.bg,
                      color: decisionInfo.color,
                    }}
                  >
                    {decisionInfo.label}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm text-text-secondary">
                  {run.recipient_id ? `Recipient ${run.recipient_id.slice(0, 4)}` : 'N/A'}
                </td>
                <td className="px-4 py-3 text-sm text-text-muted">
                  {run.start_time ? format(new Date(run.start_time), 'MMM dd, HH:mm') : 'N/A'}
                </td>
                <td className="px-4 py-3 text-sm font-mono text-text-secondary">
                  {run.end_time && run.start_time
                    ? `${Math.round((new Date(run.end_time) - new Date(run.start_time)) / 1000)}s`
                    : run.start_time ? 'In Progress' : 'N/A'}
                </td>
                <td className="px-4 py-3 text-right">
                  <button
                    onClick={() => onViewRun(run.run_id)}
                    className="p-2 hover:bg-primary-100 rounded transition-colors text-primary-600"
                  >
                    <Eye size={18} />
                  </button>
                </td>
              </motion.tr>
            );
          })}
        </tbody>
      </table>
    </motion.div>
  );
};
