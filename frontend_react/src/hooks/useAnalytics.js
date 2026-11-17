import { useQuery } from '@tanstack/react-query';
import apiClient from '../services/api';

export const useEvaluationSummary = () => {
  return useQuery({
    queryKey: ['evaluationSummary'],
    queryFn: async () => {
      const response = await apiClient.get('/api/v1/evaluate/summary');
      return response.data;
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  });
};

export const useRecipients = () => {
  return useQuery({
    queryKey: ['recipients'],
    queryFn: async () => {
      const response = await apiClient.get('/api/v1/recipients');
      return response.data.recipients || [];
    },
  });
};
