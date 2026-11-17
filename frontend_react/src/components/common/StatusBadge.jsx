import React from 'react';

export const StatusBadge = ({ status, size = 'md' }) => {
  const statusConfig = {
    dispatch: { label: 'Dispatch', color: '#43865B', bg: '#E8F5E9' },
    hold: { label: 'Hold', color: '#D69B43', bg: '#FFF8E1' },
    discard: { label: 'Discard', color: '#C65C50', bg: '#FFEBEE' },
    no_pickup: { label: 'No Pickup', color: '#A0A69B', bg: '#F5F5F5' },
    success: { label: 'Success', color: '#43865B', bg: '#E8F5E9' },
    failed: { label: 'Failed', color: '#C65C50', bg: '#FFEBEE' },
    pending: { label: 'Pending', color: '#D69B43', bg: '#FFF8E1' },
  };

  const config = statusConfig[status?.toLowerCase()] || statusConfig.pending;
  const sizeClass = size === 'sm' ? 'text-xs px-2 py-1' : 'text-sm px-3 py-1.5';

  return (
    <span
      className={`inline-block rounded-full font-medium ${sizeClass}`}
      style={{ color: config.color, backgroundColor: config.bg }}
    >
      {config.label}
    </span>
  );
};
