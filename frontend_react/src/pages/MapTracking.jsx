import React, { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { PageContainer } from '../components/layout/PageContainer';
import { SectionHeader } from '../components/common/SectionHeader';
import { MetricCard } from '../components/common/MetricCard';
import { LocationPicker } from '../components/maps/LocationPicker';
import { LoadingState } from '../components/common/LoadingState';
import { useMapTracking, useMapStatistics } from '../hooks/useMapData';
import { MapPin, Package, BarChart3, TrendingUp } from 'lucide-react';

const MapTracking = () => {
  const { data: trackingData, isLoading: trackingLoading } = useMapTracking();
  const { data: statsData, isLoading: statsLoading } = useMapStatistics();
  const [selectedLocation, setSelectedLocation] = useState(null);

  const dispatches = useMemo(() => {
    return trackingData?.dispatches || [];
  }, [trackingData]);

  const donors = useMemo(() => {
    return trackingData?.donors || [];
  }, [trackingData]);

  const recipients = useMemo(() => {
    return trackingData?.recipients || [];
  }, [trackingData]);

  const stats = useMemo(() => {
    return trackingData?.statistics || statsData?.statistics || {};
  }, [trackingData, statsData]);

  const handleLocationSelect = (location) => {
    setSelectedLocation(location);
  };

  if (trackingLoading || statsLoading) {
    return <LoadingState message="Loading map data..." />;
  }

  return (
    <PageContainer>
      <SectionHeader
        title="Live Location Tracker"
        subtitle="Click on map to select your location or search for a place"
      />

      {/* Metrics */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8"
      >
        <MetricCard
          icon={Package}
          label="Active Dispatches"
          value={dispatches.length}
          color="primary"
        />
        <MetricCard
          icon={MapPin}
          label="Donor Locations"
          value={donors.length}
          color="success"
        />
        <MetricCard
          icon={MapPin}
          label="Recipients"
          value={recipients.length}
          color="warning"
        />
        <MetricCard
          icon={TrendingUp}
          label="Total Routes"
          value={stats.total_routes || 0}
          color="secondary"
        />
      </motion.div>

      {/* Main Map Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 lg:grid-cols-3 gap-6"
      >
        {/* Map Picker - Takes 2/3 width */}
        <div className="lg:col-span-2 h-[600px]">
          <LocationPicker
            onLocationSelect={handleLocationSelect}
            selectedLocation={selectedLocation}
          />
        </div>

        {/* Right Sidebar - Stats & Info */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="space-y-6"
        >
          {/* Current Selection */}
          {selectedLocation && (
            <div className="bg-white rounded-lg border-2 border-primary-600 p-6 shadow-lg">
              <h3 className="font-bold text-text-primary mb-3 flex items-center gap-2">
                ✅ Selected Location
              </h3>
              <div className="space-y-2 text-sm">
                <div>
                  <p className="text-text-muted font-medium">Place</p>
                  <p className="text-text-primary font-semibold">{selectedLocation.name}</p>
                </div>
                <div>
                  <p className="text-text-muted font-medium">Latitude</p>
                  <p className="text-text-primary font-mono">
                    {selectedLocation.lat.toFixed(6)}
                  </p>
                </div>
                <div>
                  <p className="text-text-muted font-medium">Longitude</p>
                  <p className="text-text-primary font-mono">
                    {selectedLocation.lng.toFixed(6)}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Route Statistics */}
          <div className="bg-white rounded-lg border border-soft-sage p-6 shadow-sm">
            <h3 className="font-bold text-text-primary mb-4">📊 Route Statistics</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-soft-sage rounded">
                <span className="text-sm text-text-secondary">Avg Distance</span>
                <span className="font-semibold text-text-primary">
                  {(stats.avg_distance || 0).toFixed(1)} km
                </span>
              </div>
              <div className="flex items-center justify-between p-3 bg-soft-sage rounded">
                <span className="text-sm text-text-secondary">Avg Time</span>
                <span className="font-semibold text-text-primary">
                  {(stats.avg_time || 0).toFixed(0)} min
                </span>
              </div>
              <div className="flex items-center justify-between p-3 bg-soft-sage rounded">
                <span className="text-sm text-text-secondary">Total Distance</span>
                <span className="font-semibold text-text-primary">
                  {(stats.total_distance || 0).toFixed(1)} km
                </span>
              </div>
            </div>
          </div>

          {/* Locations List */}
          <div className="bg-white rounded-lg border border-soft-sage p-6 shadow-sm">
            <h3 className="font-bold text-text-primary mb-3 text-sm">
              📦 Donors ({donors.length})
            </h3>
            <div className="space-y-2 max-h-32 overflow-y-auto">
              {donors.length > 0 ? (
                donors.map((donor, idx) => (
                  <div key={idx} className="text-xs text-text-secondary p-2 bg-soft-sage rounded">
                    📍 {donor.name}
                  </div>
                ))
              ) : (
                <p className="text-xs text-text-muted">No donors available</p>
              )}
            </div>
          </div>

          {/* Recipients List */}
          <div className="bg-white rounded-lg border border-soft-sage p-6 shadow-sm">
            <h3 className="font-bold text-text-primary mb-3 text-sm">
              🏢 Recipients ({recipients.length})
            </h3>
            <div className="space-y-2 max-h-32 overflow-y-auto">
              {recipients.length > 0 ? (
                recipients.map((recipient, idx) => (
                  <div key={idx} className="text-xs text-text-secondary p-2 bg-soft-sage rounded">
                    🏢 {recipient.name}
                  </div>
                ))
              ) : (
                <p className="text-xs text-text-muted">No recipients available</p>
              )}
            </div>
          </div>
        </motion.div>
      </motion.div>
    </PageContainer>
  );
};

export default MapTracking;
