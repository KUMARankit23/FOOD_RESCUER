import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { PageContainer } from '../components/layout/PageContainer';
import { SectionHeader } from '../components/common/SectionHeader';
import { Button } from '../components/common/Button';
import { LocationPicker } from '../components/maps/LocationPicker';
import { useSubmitReport } from '../hooks/useReports';
import { FOOD_TYPES } from '../utils/constants';

const reportSchema = z.object({
  food_type: z.string().min(1, 'Please select a food type'),
  quantity: z.coerce.number().min(1, 'Quantity must be at least 1'),
  prep_time: z.string().min(1, 'Please enter preparation time'),
  temperature_c: z.coerce.number().min(-50).max(100),
  location: z.string().min(1, 'Please select a location on the map'),
  pickup_deadline: z.string().min(1, 'Please select a pickup deadline'),
});

const SubmitReport = () => {
  const navigate = useNavigate();
  const { mutate: submitReport, isPending } = useSubmitReport();
  const [submitError, setSubmitError] = useState(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState(null);

  const { control, handleSubmit, reset, formState: { errors }, setValue } = useForm({
    resolver: zodResolver(reportSchema),
    defaultValues: {
      food_type: '',
      quantity: 10,
      prep_time: 'Fresh',
      temperature_c: 25,
      location: '',
      pickup_deadline: '',
    },
  });

  const handleLocationSelect = (location) => {
    setSelectedLocation(location);
    // Set location value with coordinates and name
    setValue('location', `${location.name} (${location.lat.toFixed(4)}, ${location.lng.toFixed(4)})`);
  };

  const onSubmit = (data) => {
    if (!selectedLocation) {
      setSubmitError('Please select a location on the map');
      return;
    }

    setSubmitError(null);
    submitReport(data, {
      onSuccess: (response) => {
        setSubmitSuccess(true);
        reset();
        setSelectedLocation(null);
        setTimeout(() => {
          navigate('/operations', { state: { runId: response.run_id } });
        }, 2000);
      },
      onError: (error) => {
        setSubmitError(error.response?.data?.detail || 'Failed to submit report');
      },
    });
  };

  return (
    <PageContainer>
      <SectionHeader
        title="Submit Food Report"
        subtitle="Report surplus food for redistribution"
      />

      {submitSuccess && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 p-4 bg-success-light rounded-lg border border-success text-success"
        >
          ✓ Report submitted successfully! Redirecting to operations...
        </motion.div>
      )}

      {submitError && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 p-4 bg-danger-light rounded-lg border border-danger text-danger"
        >
          ✗ {submitError}
        </motion.div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Food Details Section */}
        <div className="bg-white rounded-lg border border-soft-sage shadow-sm p-6">
          <h3 className="font-semibold text-text-primary mb-4">Food Details</h3>

          <div className="space-y-4">
            {/* Food Type */}
            <div>
              <label className="block text-sm font-medium text-text-primary mb-2">
                Food Type
              </label>
              <Controller
                name="food_type"
                control={control}
                render={({ field }) => (
                  <select
                    {...field}
                    className="w-full px-4 py-2 rounded-md border border-soft-sage bg-white text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-600 focus:border-transparent"
                  >
                    <option value="">Select food type...</option>
                    {FOOD_TYPES.map((type) => (
                      <option key={type} value={type}>
                        {type}
                      </option>
                    ))}
                  </select>
                )}
              />
              {errors.food_type && (
                <p className="text-xs text-danger mt-1">{errors.food_type.message}</p>
              )}
            </div>

            {/* Quantity */}
            <div>
              <label className="block text-sm font-medium text-text-primary mb-2">
                Quantity (units)
              </label>
              <Controller
                name="quantity"
                control={control}
                render={({ field }) => (
                  <input
                    type="number"
                    {...field}
                    min="1"
                    className="w-full px-4 py-2 rounded-md border border-soft-sage bg-white text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-600 focus:border-transparent"
                  />
                )}
              />
              {errors.quantity && (
                <p className="text-xs text-danger mt-1">{errors.quantity.message}</p>
              )}
            </div>

            {/* Prep Time */}
            <div>
              <label className="block text-sm font-medium text-text-primary mb-2">
                Preparation Time
              </label>
              <Controller
                name="prep_time"
                control={control}
                render={({ field }) => (
                  <input
                    type="text"
                    {...field}
                    placeholder="e.g., Fresh, 2 hours ago"
                    className="w-full px-4 py-2 rounded-md border border-soft-sage bg-white text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-600 focus:border-transparent"
                  />
                )}
              />
              {errors.prep_time && (
                <p className="text-xs text-danger mt-1">{errors.prep_time.message}</p>
              )}
            </div>
          </div>
        </div>

        {/* Safety & Temperature Section */}
        <div className="bg-white rounded-lg border border-soft-sage shadow-sm p-6">
          <h3 className="font-semibold text-text-primary mb-4">Safety & Temperature</h3>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              Temperature (°C)
            </label>
            <Controller
              name="temperature_c"
              control={control}
              render={({ field }) => (
                <input
                  type="number"
                  {...field}
                  step="0.1"
                  min="-50"
                  max="100"
                  className="w-full px-4 py-2 rounded-md border border-soft-sage bg-white text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-600 focus:border-transparent"
                />
              )}
            />
            {errors.temperature_c && (
              <p className="text-xs text-danger mt-1">{errors.temperature_c.message}</p>
            )}
          </div>
        </div>

        {/* Location Section - Live Map Picker */}
        <div className="bg-white rounded-lg border border-soft-sage shadow-sm p-6">
          <h3 className="font-semibold text-text-primary mb-4">📍 Pickup Location</h3>
          <div className="mb-4 h-[400px]">
            <LocationPicker
              onLocationSelect={handleLocationSelect}
              selectedLocation={selectedLocation}
            />
          </div>
          {errors.location && (
            <p className="text-xs text-danger mt-1">{errors.location.message}</p>
          )}
          {selectedLocation && (
            <motion.div
              initial={{ y: -10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              className="mt-4 p-3 bg-soft-sage rounded border-l-4 border-primary-600"
            >
              <p className="text-sm font-bold text-text-primary">✅ Location Selected</p>
              <p className="text-xs text-text-secondary mt-1">{selectedLocation.name}</p>
              <p className="text-xs text-text-muted font-mono">
                {selectedLocation.lat.toFixed(6)}, {selectedLocation.lng.toFixed(6)}
              </p>
            </motion.div>
          )}
        </div>

        {/* Timing Section */}
        <div className="bg-white rounded-lg border border-soft-sage shadow-sm p-6">
          <h3 className="font-semibold text-text-primary mb-4">Pickup Deadline</h3>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              Pickup Deadline
            </label>
            <Controller
              name="pickup_deadline"
              control={control}
              render={({ field }) => (
                <input
                  type="datetime-local"
                  {...field}
                  className="w-full px-4 py-2 rounded-md border border-soft-sage bg-white text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-600 focus:border-transparent"
                />
              )}
            />
            {errors.pickup_deadline && (
              <p className="text-xs text-danger mt-1">{errors.pickup_deadline.message}</p>
            )}
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex gap-3 pt-4">
          <Button
            type="submit"
            loading={isPending}
            className="flex-1"
          >
            Submit Report
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => {
              reset();
              setSelectedLocation(null);
            }}
            disabled={isPending}
            className="flex-1"
          >
            Clear
          </Button>
        </div>
      </form>
    </PageContainer>
  );
};

export default SubmitReport;
