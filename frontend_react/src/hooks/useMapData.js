import { useQuery } from '@tanstack/react-query';
import apiClient from '../services/api';

export const useMapTracking = () => {
  return useQuery({
    queryKey: ['mapTracking'],
    queryFn: async () => {
      const response = await apiClient.get('/api/v1/map/tracking');
      return response.data;
    },
    refetchInterval: 10000, // Refetch every 10 seconds
  });
};

export const useMapStatistics = () => {
  return useQuery({
    queryKey: ['mapStatistics'],
    queryFn: async () => {
      const response = await apiClient.get('/api/v1/map/statistics');
      return response.data;
    },
    refetchInterval: 15000, // Refetch every 15 seconds
  });
};

export const useDispatchHistory = () => {
  return useQuery({
    queryKey: ['dispatchHistory'],
    queryFn: async () => {
      const response = await apiClient.get('/api/v1/map/history');
      return response.data;
    },
  });
};

export const useDonorLocations = () => {
  return useQuery({
    queryKey: ['donorLocations'],
    queryFn: async () => {
      const response = await apiClient.get('/api/v1/map/donors');
      return response.data.donors || [];
    },
  });
};

export const useRecipientLocations = () => {
  return useQuery({
    queryKey: ['recipientLocations'],
    queryFn: async () => {
      const response = await apiClient.get('/api/v1/map/recipients');
      return response.data.recipients || [];
    },
  });
};
