import React from 'react';
import { useLocation } from 'react-router-dom';
import { Wifi, WifiOff, RefreshCw } from 'lucide-react';

export const TopNavbar = ({ isConnected = true }) => {
  const location = useLocation();

  const getPageTitle = () => {
    const titles = {
      '/': 'Overview',
      '/submit': 'Submit Food',
      '/operations': 'Operations',
      '/analytics': 'Analytics',
      '/map': 'Live Map',
      '/knowledge': 'Knowledge Base',
    };
    return titles[location.pathname] || 'ANNASARTHI AI';
  };

  return (
    <nav className="bg-white border-b border-soft-sage h-16 fixed top-0 left-0 right-0 z-40">
      <div className="ml-80 h-full flex items-center justify-between px-6">
        <div>
          <h2 className="font-heading text-lg font-semibold text-text-primary">
            {getPageTitle()}
          </h2>
        </div>

        <div className="flex items-center gap-4">
          {/* Connection Status */}
          <div className="flex items-center gap-2">
            {isConnected ? (
              <>
                <Wifi size={18} className="text-success" />
                <span className="text-xs text-success font-medium">Connected</span>
              </>
            ) : (
              <>
                <WifiOff size={18} className="text-danger" />
                <span className="text-xs text-danger font-medium">Offline</span>
              </>
            )}
          </div>

          {/* Refresh Button */}
          <button className="p-2 rounded-md hover:bg-soft-sage text-text-secondary transition-colors">
            <RefreshCw size={18} />
          </button>

          {/* Timestamp */}
          <div className="text-xs text-text-muted px-3 py-2 bg-soft-sage rounded-md">
            {new Date().toLocaleTimeString()}
          </div>
        </div>
      </div>
    </nav>
  );
};
