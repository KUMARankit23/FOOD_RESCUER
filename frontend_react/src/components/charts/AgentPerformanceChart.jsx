import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { CHART_COLORS } from '../../utils/constants';

export const AgentPerformanceChart = ({ data = [] }) => {
  if (!data || data.length === 0) {
    return (
      <div className="h-80 flex items-center justify-center text-text-muted">
        No data available
      </div>
    );
  }

  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E8EFE5" />
          <XAxis dataKey="name" stroke="#A0A69B" style={{ fontSize: '12px' }} />
          <YAxis stroke="#A0A69B" style={{ fontSize: '12px' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#F8F5ED',
              border: '1px solid #E8EFE5',
              borderRadius: '8px',
            }}
          />
          <Legend />
          <Bar dataKey="accuracy" fill={CHART_COLORS.primary} />
          <Bar dataKey="latency" fill={CHART_COLORS.secondary} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
