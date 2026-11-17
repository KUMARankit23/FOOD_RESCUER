import React, { useEffect, useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { MapPin, Search, Navigation, X } from 'lucide-react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet default icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.3.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.3.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.3.1/images/marker-shadow.png',
});

export const LocationPicker = ({ onLocationSelect, selectedLocation }) => {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const marker = useRef(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCoords, setSelectedCoords] = useState(selectedLocation || null);
  const [locationName, setLocationName] = useState('');
  const [loading, setLoading] = useState(false);

  // Initialize map
  useEffect(() => {
    if (!map.current && mapContainer.current) {
      map.current = L.map(mapContainer.current).setView([28.6139, 77.2090], 13);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19,
      }).addTo(map.current);

      // Click to select location
      map.current.on('click', (e) => {
        const { lat, lng } = e.latlng;
        handleLocationSelect(lat, lng);
      });

      // Get user's live location
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const { latitude, longitude } = position.coords;
            map.current.setView([latitude, longitude], 15);
          },
          (error) => console.log('Location error:', error)
        );
      }
    }

    return () => {
      // Cleanup
    };
  }, []);

  // Update marker when location changes
  useEffect(() => {
    if (selectedCoords && map.current) {
      if (marker.current) {
        map.current.removeLayer(marker.current);
      }

      // Custom marker with animation
      const customIcon = L.divIcon({
        className: 'location-marker',
        html: `
          <div style="
            position: relative;
            width: 50px;
            height: 50px;
          ">
            <div style="
              position: absolute;
              width: 100%;
              height: 100%;
              background: linear-gradient(135deg, #3F654A, #829B78);
              border: 3px solid white;
              border-radius: 50%;
              display: flex;
              align-items: center;
              justify-content: center;
              box-shadow: 0 4px 12px rgba(63, 101, 74, 0.3);
              animation: dropPin 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
            ">
              <div style="
                width: 10px;
                height: 10px;
                background: white;
                border-radius: 50%;
              "></div>
            </div>
          </div>
          <style>
            @keyframes dropPin {
              0% {
                transform: translateY(-200px);
                opacity: 0;
              }
              100% {
                transform: translateY(0);
                opacity: 1;
              }
            }
          </style>
        `,
        iconSize: [50, 50],
        iconAnchor: [25, 50],
        popupAnchor: [0, -50],
      });

      marker.current = L.marker([selectedCoords.lat, selectedCoords.lng], {
        icon: customIcon,
      })
        .addTo(map.current)
        .bindPopup(
          `<div style="font-size: 12px; font-weight: bold;">
            📍 ${locationName || 'Selected Location'}
            <br/>
            Lat: ${selectedCoords.lat.toFixed(6)}
            <br/>
            Lon: ${selectedCoords.lng.toFixed(6)}
          </div>`
        )
        .openPopup();

      map.current.setView([selectedCoords.lat, selectedCoords.lng], 16);
    }
  }, [selectedCoords, locationName]);

  const handleLocationSelect = async (lat, lng) => {
    setSelectedCoords({ lat, lng });

    // Reverse geocoding to get location name
    try {
      setLoading(true);
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`
      );
      const data = await response.json();
      const name = data.address?.city || data.address?.town || data.address?.village || 'Custom Location';
      setLocationName(name);
      onLocationSelect({ lat, lng, name });
    } catch (error) {
      console.log('Geocoding error:', error);
      setLocationName('Custom Location');
      onLocationSelect({ lat, lng, name: 'Custom Location' });
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(searchQuery)}&format=json&limit=1`
      );
      const data = await response.json();

      if (data.length > 0) {
        const { lat, lon, display_name } = data[0];
        handleLocationSelect(parseFloat(lat), parseFloat(lon));
        setLocationName(display_name);
      } else {
        alert('Location not found. Try clicking on the map instead.');
      }
    } catch (error) {
      console.error('Search error:', error);
      alert('Search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          handleLocationSelect(latitude, longitude);
          setLocationName('Your Current Location');
        },
        (error) => {
          alert('Could not get your location: ' + error.message);
        }
      );
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col h-full bg-cream rounded-lg overflow-hidden border-2 border-soft-sage"
    >
      {/* Search Header */}
      <div className="p-4 bg-white border-b-2 border-soft-sage space-y-3">
        <h3 className="font-bold text-text-primary flex items-center gap-2">
          <MapPin size={20} className="text-primary-600" />
          Pick Location on Map
        </h3>

        {/* Search Input */}
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Search location..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            className="flex-1 px-4 py-2 rounded-lg border border-soft-sage bg-cream text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary-600"
          />
          <button
            onClick={handleSearch}
            disabled={loading}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-text-muted transition-colors flex items-center gap-2"
          >
            <Search size={18} />
          </button>
        </div>

        {/* Current Location Button */}
        <button
          onClick={getCurrentLocation}
          className="w-full px-4 py-2 bg-soft-sage text-primary-600 rounded-lg hover:bg-sage-300 transition-colors flex items-center justify-center gap-2 font-medium"
        >
          <Navigation size={18} />
          Use My Current Location
        </button>

        {/* Selected Location Display */}
        {selectedCoords && (
          <motion.div
            initial={{ y: -10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="p-3 bg-soft-sage rounded-lg border-l-4 border-primary-600"
          >
            <p className="text-sm font-bold text-text-primary flex items-center gap-2">
              ✅ Selected Location
            </p>
            <p className="text-xs text-text-secondary mt-1">{locationName}</p>
            <p className="text-xs text-text-muted font-mono mt-1">
              {selectedCoords.lat.toFixed(6)}, {selectedCoords.lng.toFixed(6)}
            </p>
          </motion.div>
        )}
      </div>

      {/* Map Container */}
      <div
        ref={mapContainer}
        className="flex-1 relative"
        style={{ minHeight: '400px' }}
      />

      {/* Instructions */}
      <div className="p-3 bg-primary-50 border-t-2 border-soft-sage text-xs text-text-secondary">
        💡 Click on the map to select a location, or search for a place
      </div>

      {/* Loading Indicator */}
      {loading && (
        <div className="absolute inset-0 bg-black/20 flex items-center justify-center rounded-lg">
          <div className="bg-white rounded-lg p-4 shadow-lg flex items-center gap-2">
            <div className="animate-spin w-4 h-4 border-2 border-primary-600 border-t-transparent rounded-full"></div>
            <span className="text-sm text-text-primary font-medium">Loading...</span>
          </div>
        </div>
      )}
    </motion.div>
  );
};
