import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  LayoutDashboard,
  Plus,
  Briefcase,
  BarChart3,
  Map,
  Book,
  ChevronLeft,
  ChevronRight,
  Leaf,
} from 'lucide-react';
import { APP_NAME } from '../../utils/constants';

const navItems = [
  { path: '/', label: 'Overview', icon: LayoutDashboard },
  { path: '/submit', label: 'Submit Food', icon: Plus },
  { path: '/operations', label: 'Operations', icon: Briefcase },
  { path: '/analytics', label: 'Analytics', icon: BarChart3 },
  { path: '/map', label: 'Live Map', icon: Map },
  { path: '/knowledge', label: 'Knowledge Base', icon: Book },
];

export const AppSidebar = () => {
  const location = useLocation();
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <motion.aside
      initial={false}
      animate={{ width: isCollapsed ? 80 : 250 }}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
      className="bg-cream border-r border-soft-sage h-screen fixed left-0 top-0 overflow-hidden flex flex-col shadow-sm"
    >
      {/* Brand Area */}
      <div className="p-6 border-b border-soft-sage">
        <div className="flex items-center gap-3">
          <div className="text-3xl">🌱</div>
          {!isCollapsed && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}>
              <h1 className="font-heading font-bold text-primary-600 text-sm whitespace-nowrap">
                {APP_NAME}
              </h1>
              <p className="text-xs text-text-muted">Food Rescue Network</p>
            </motion.div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-6 space-y-2 overflow-y-auto">
        {navItems.map(({ path, label, icon: Icon }) => {
          const isActive = location.pathname === path;
          return (
            <Link key={path} to={path}>
              <motion.button
                whileHover={{ x: 4 }}
                whileTap={{ x: 2 }}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-md transition-colors ${
                  isActive
                    ? 'bg-soft-sage text-primary-600'
                    : 'text-text-secondary hover:bg-soft-sage hover:text-text-primary'
                }`}
              >
                <Icon size={20} className="flex-shrink-0" />
                {!isCollapsed && <span className="text-sm font-medium">{label}</span>}
              </motion.button>
            </Link>
          );
        })}
      </nav>

      {/* Toggle Button */}
      <div className="p-3 border-t border-soft-sage">
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="w-full flex justify-center p-2 rounded-md hover:bg-soft-sage text-text-secondary transition-colors"
        >
          {isCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </button>
      </div>
    </motion.aside>
  );
};
