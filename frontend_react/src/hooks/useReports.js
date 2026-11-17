import { useMutation, useQuery } from '@tanstack/react-query';
import apiClient from '../services/api';

export const useSubmitReport = () => {
  return useMutation({
    mutationFn: async (reportData) => {
      const response = await apiClient.post('/api/v1/reports', reportData);
      return response.data;
    },
  });
};

export const useListRuns = () => {
  return useQuery({
    queryKey: ['runs'],
    queryFn: async () => {
      const response = await apiClient.get('/api/v1/runs');
      return response.data.runs || [];
    },
    refetchInterval: 5000, // Refetch every 5 seconds
  });
};

export const useGetRun = (runId) => {
  return useQuery({
    queryKey: ['run', runId],
    queryFn: async () => {
      const response = await apiClient.get(`/api/v1/runs/${runId}`);
      return response.data;
    },
    enabled: !!runId,
  });
};

export const useGetRunTrace = (runId) => {
  return useQuery({
    queryKey: ['runTrace', runId],
    queryFn: async () => {
      const response = await apiClient.get(`/api/v1/runs/${runId}/trace`);
      return response.data;
    },
    enabled: !!runId,
  });
};
