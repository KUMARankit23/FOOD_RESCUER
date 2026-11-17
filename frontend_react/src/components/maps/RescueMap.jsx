import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { MapPin, Navigation, Loader, AlertCircle } from 'lucide-react';

export const RescueMap = ({ dispatches = [], donors = [], recipients = [] }) => {
  const [position, setPosition] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [accuracy, setAccuracy] = useState(null);
  const [heading, setHeading] = useState(null);
  const [mapUrl, setMapUrl] = useState('');

  useEffect(() => {
    // Get user's live location
    const getLocation = () => {
      if (navigator.geolocation) {
        const watchId = navigator.geolocation.watchPosition(
          (position) => {
            const { latitude, longitude, accuracy, heading } = position.coords;
            setPosition({ lat: latitude, lon: longitude });
            setAccuracy(accuracy);
            setHeading(heading);
            setError(null);
            setLoading(false);
            
            // Create map URL with your live location
            const mapUrlString = `https://www.openstreetmap.org/export/embed.html?bbox=${longitude - 0.01},${latitude - 0.01},${longitude + 0.01},${latitude + 0.01}&layer=mapnik&marker=${latitude},${longitude}`;
            setMapUrl(mapUrlString);
          },
          (error) => {
            console.error('Location error:', error);
            setError(error.message);
            setLoading(false);
            
            // Fallback to Delhi
            const fallbackLat = 28.6139;
            const fallbackLon = 77.2090;
            setPosition({ lat: fallbackLat, lon: fallbackLon });
            const mapUrlString = `https://www.openstreetmap.org/export/embed.html?bbox=${fallbackLon - 0.01},${fallbackLat - 0.01},${fallbackLon + 0.01},${fallbackLat + 0.01}&layer=mapnik&marker=${fallbackLat},${fallbackLon}`;
            setMapUrl(mapUrlString);
          },
          {
            enableHighAccuracy: true,
            maximumAge: 0,
            timeout: 5000,
          }
        );

        return () => navigator.geolocation.clearWatch(watchId);
      } else {
        setError('Geolocation not supported');
        setLoading(false);
        
        // Fallback
        const fallbackLat = 28.6139;
        const fallbackLon = 77.2090;
        setPosition({ lat: fallbackLat, lon: fallbackLon });
        const mapUrlString = `https://www.openstreetmap.org/export/embed.html?bbox=${fallbackLon - 0.01},${fallbackLat - 0.01},${fallbackLon + 0.01},${fallbackLat + 0.01}&layer=mapnik&marker=${fallbackLat},${fallbackLon}`;
        setMapUrl(mapUrlString);
      }
    };

    getLocation();
  }, []);

  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="w-full h-full flex items-center justify-center bg-cream"
      >
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          >
            <Navigation className="mx-auto mb-4" size={48} color="#3F654A" />
          </motion.div>
          <p className="text-text-secondary font-medium">Getting your live location...</p>
          <p className="text-text-muted text-sm mt-2">Please allow location access</p>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="w-full h-full flex flex-col bg-cream relative"
    >
      {/* Error Banner */}
      {error && error !== 'Geolocation not supported' && (
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="bg-warning-light border-l-4 border-warning p-4 flex gap-3"
        >
          <AlertCircle className="text-warning flex-shrink-0" size={20} />
          <div>
            <p className="text-sm font-semibold text-warning">Location Warning</p>
            <p className="text-xs text-text-secondary">{error}</p>
          </div>
        </motion.div>
      )}

      {/* Live Status Card - Floating */}
      {position && (
        <motion.div
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="absolute top-6 right-6 z-50 bg-white rounded-xl shadow-lg p-5 border-2 border-primary-600 max-w-xs"
        >
          <div className="flex items-center gap-2 mb-4">
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1.5, repeat: Infinity }}
              className="w-3 h-3 bg-success rounded-full"
            />
            <span className="font-bold text-text-primary">📍 Live Tracking Active</span>
          </div>
          
          <div className="space-y-2 text-sm">
            <div className="flex justify-between items-center bg-soft-sage p-2 rounded">
              <span className="text-text-secondary">Latitude:</span>
              <span className="font-mono font-semibold text-primary-600">
                {position.lat.toFixed(6)}
              </span>
            </div>
            
            <div className="flex justify-between items-center bg-soft-sage p-2 rounded">
              <span className="text-text-secondary">Longitude:</span>
              <span className="font-mono font-semibold text-primary-600">
                {position.lon.toFixed(6)}
              </span>
            </div>
            
            {accuracy && (
              <div className="flex justify-between items-center bg-soft-sage p-2 rounded">
                <span className="text-text-secondary">📏 Accuracy:</span>
                <span className="font-semibold text-secondary-600">
                  {accuracy.toFixed(0)}m
                </span>
              </div>
            )}
            
            {heading !== null && (
              <div className="flex justify-between items-center bg-soft-sage p-2 rounded">
                <span className="text-text-secondary">🧭 Heading:</span>
                <span className="font-semibold text-secondary-600">
                  {heading.toFixed(0)}°
                </span>
              </div>
            )}
          </div>

          {/* Stats */}
          <div className="mt-4 pt-4 border-t border-soft-sage space-y-2 text-xs">
            <div className="flex justify-between text-text-secondary">
              <span>📦 Dispatches:</span>
              <span className="font-bold text-primary-600">{dispatches.length}</span>
            </div>
            <div className="flex justify-between text-text-secondary">
              <span>📦 Donors:</span>
              <span className="font-bold text-primary-600">{donors.length}</span>
            </div>
            <div className="flex justify-between text-text-secondary">
              <span>🏢 Recipients:</span>
              <span className="font-bold text-primary-600">{recipients.length}</span>
            </div>
          </div>
        </motion.div>
      )}

      {/* Map Container */}
      <div className="flex-1 relative overflow-hidden">
        {mapUrl && (
          <motion.iframe
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            width="100%"
            height="100%"
            frameBorder="0"
            src={mapUrl}
            style={{
              border: 0,
              borderRadius: '0'
            }}
            allowFullScreen={true}
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
          />
        )}
        
        {/* Legend Overlay - Bottom Left */}
        <motion.div
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="absolute bottom-6 left-6 bg-white rounded-lg shadow-lg p-4 border border-soft-sage"
        >
          <p className="font-bold text-text-primary mb-3 text-sm">Map Legend</p>
          <div className="space-y-2 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-success animate-pulse"></div>
              <span className="text-text-secondary">Your Location</span>
            </div>
            <div className="flex items-center gap-2">
              <MapPin size={16} className="text-primary-600" />
              <span className="text-text-secondary">Food Sources</span>
            </div>
            <div className="flex items-center gap-2">
              <MapPin size={16} className="text-warning" />
              <span className="text-text-secondary">Recipients</span>
            </div>
          </div>
        </motion.div>

        {/* Zoom Info - Top Left */}
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.35 }}
          className="absolute top-6 left-6 bg-white rounded-lg shadow-lg p-3 border border-soft-sage text-xs text-text-secondary"
        >
          <p className="font-semibold text-text-primary">🗺️ Neighborhood View</p>
          <p className="text-xs mt-1">Zoom: 18 | Full Coverage</p>
        </motion.div>
      </div>
    </motion.div>
  );
};
