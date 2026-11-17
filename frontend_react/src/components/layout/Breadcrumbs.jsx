import React from 'react';
import { Link } from 'react-router-dom';
import { ChevronRight } from 'lucide-react';

export const Breadcrumbs = ({ items }) => {
  return (
    <nav className="flex items-center gap-2 text-sm mb-6">
      {items.map((item, idx) => (
        <div key={idx} className="flex items-center gap-2">
          {item.href ? (
            <Link to={item.href} className="text-primary-600 hover:text-primary-700 transition-colors">
              {item.label}
            </Link>
          ) : (
            <span className="text-text-primary">{item.label}</span>
          )}
          {idx < items.length - 1 && <ChevronRight size={16} className="text-text-muted" />}
        </div>
      ))}
    </nav>
  );
};
