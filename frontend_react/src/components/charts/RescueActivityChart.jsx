import React from 'react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { CHART_COLORS } from '../../utils/constants';

export const RescueActivityChart = ({ data = [], variant = 'line' }) => {
  if (!data || data.length === 0) {
    return (
      <div className="h-80 flex items-center justify-center text-text-muted">
        No data available
      </div>
    );
  }

  const chartComponent = variant === 'area' ? (
    <AreaChart data={data}>
      <defs>
        <linearGradient id="colorQuantity" x1="0" y1="0" x2="0" y2="1">
          <stop offset="5%" stopColor={CHART_COLORS.primary} stopOpacity={0.3} />
          <stop offset="95%" stopColor={CHART_COLORS.primary} stopOpacity={0} />
        </linearGradient>
      </defs>
      <CartesianGrid strokeDasharray="3 3" stroke="#E8EFE5" />
      <XAxis dataKey="name" stroke="#A0A69B" style={{ fontSize: '12px' }} />
      <YAxis stroke="#A0A69B" style={{ fontSize: '12px' }} />
      <Tooltip contentStyle={{ backgroundColor: '#F8F5ED', border: '1px solid #E8EFE5', borderRadius: '8px' }} />
      <Area
        type="monotone"
        dataKey="quantity"
        stroke={CHART_COLORS.primary}
        fillOpacity={1}
        fill="url(#colorQuantity)"
        strokeWidth={2}
      />
    </AreaChart>
  ) : (
    <LineChart data={data}>
      <CartesianGrid strokeDasharray="3 3" stroke="#E8EFE5" />
      <XAxis dataKey="name" stroke="#A0A69B" style={{ fontSize: '12px' }} />
      <YAxis stroke="#A0A69B" style={{ fontSize: '12px' }} />
      <Tooltip contentStyle={{ backgroundColor: '#F8F5ED', border: '1px solid #E8EFE5', borderRadius: '8px' }} />
      <Line
        type="monotone"
        dataKey="quantity"
        stroke={CHART_COLORS.primary}
        strokeWidth={2}
        dot={{ fill: CHART_COLORS.primary, r: 4 }}
        activeDot={{ r: 6 }}
      />
    </LineChart>
  );

  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        {chartComponent}
      </ResponsiveContainer>
    </div>
  );
};
