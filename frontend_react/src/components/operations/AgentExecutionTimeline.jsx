import React from 'react';
import { motion } from 'framer-motion';
import { AGENTS } from '../../utils/constants';

export const AgentExecutionTimeline = ({ trace = {} }) => {
  const agents = trace.agents || [];

  if (!agents || agents.length === 0) {
    return (
      <div className="text-center py-8 text-text-muted">
        No agent execution data available
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Timeline line */}
      <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-primary-600 to-secondary-600" />

      {/* Timeline items */}
      <div className="space-y-6">
        {agents.map((agent, idx) => {
          const agentInfo = AGENTS.find((a) => a.id === agent.id);
          return (
            <motion.div
              key={idx}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="ml-20 pb-6"
            >
              {/* Timeline node */}
              <div className="absolute -left-6 top-0 w-12 h-12 bg-cream border-2 border-primary-600 rounded-full flex items-center justify-center shadow-sm">
                <span className="text-lg">{agentInfo?.icon || '⚙️'}</span>
              </div>

              {/* Content card */}
              <div className="bg-white rounded-lg p-4 border border-soft-sage shadow-sm">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h4 className="font-semibold text-text-primary">{agentInfo?.name || agent.id}</h4>
                    <p className="text-sm text-text-muted">{agentInfo?.role}</p>
                  </div>
                  <span className="text-xs font-mono bg-soft-sage px-2 py-1 rounded">
                    {agent.duration || 'N/A'}ms
                  </span>
                </div>

                {/* Agent output */}
                {agent.output && (
                  <div className="mt-3 p-3 bg-soft-sage rounded border-l-2 border-primary-600">
                    <p className="text-sm text-text-secondary">{agent.output}</p>
                  </div>
                )}

                {/* Status */}
                <div className="mt-3 flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-success" />
                  <span className="text-xs text-text-muted">Completed successfully</span>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};
