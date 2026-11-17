import React from 'react';

export const SectionHeader = ({ icon, title, subtitle = '' }) => {
  return (
    <div className="mb-6">
      <div className="flex items-center gap-3 mb-2">
        <span className="text-2xl">{icon}</span>
        <h2 className="text-h3 font-heading font-bold text-text-primary">{title}</h2>
      </div>
      {subtitle && (
        <p className="text-text-secondary text-sm ml-10">{subtitle}</p>
      )}
    </div>
  );
};
