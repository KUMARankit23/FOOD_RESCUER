import apiClient from './api';

export const reportService = {
  // Submit a food report
  submitReport: async (reportData) => {
    try {
      const response = await apiClient.post('/api/v1/reports', reportData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get a specific report/run
  getReport: async (runId) => {
    try {
      const response = await apiClient.get(`/api/v1/runs/${runId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get execution trace for a run
  getTrace: async (runId) => {
    try {
      const response = await apiClient.get(`/api/v1/runs/${runId}/trace`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Get all runs
  getAllRuns: async () => {
    try {
      const response = await apiClient.get('/api/v1/runs');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};
