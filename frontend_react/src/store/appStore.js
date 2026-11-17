import { create } from 'zustand';

export const useAppStore = create((set) => ({
  // UI State
  sidebarOpen: true,
  setSidebarOpen: (open) => set({ sidebarOpen: open }),

  // Filter State
  selectedDecision: null,
  setSelectedDecision: (decision) => set({ selectedDecision: decision }),

  selectedAgent: null,
  setSelectedAgent: (agent) => set({ selectedAgent: agent }),

  dateRange: { from: null, to: null },
  setDateRange: (range) => set({ dateRange: range }),

  // View State
  selectedRun: null,
  setSelectedRun: (runId) => set({ selectedRun: runId }),

  detailsPanel: false,
  setDetailsPanel: (open) => set({ detailsPanel: open }),

  // Real-time Connection Status
  isConnected: true,
  setIsConnected: (connected) => set({ isConnected: connected }),

  lastUpdate: new Date(),
  setLastUpdate: () => set({ lastUpdate: new Date() }),

  // Reset filters
  resetFilters: () =>
    set({
      selectedDecision: null,
      selectedAgent: null,
      dateRange: { from: null, to: null },
    }),
}));
