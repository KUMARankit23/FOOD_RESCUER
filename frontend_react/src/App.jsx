import React, { Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClientProvider, QueryClient } from '@tanstack/react-query';
import { AppSidebar } from './components/layout/AppSidebar';
import { TopNavbar } from './components/layout/TopNavbar';
import { LoadingState } from './components/common/LoadingState';

// Pages - Lazy load
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const AgentDashboard = React.lazy(() => import('./pages/AgentDashboard'));
const PickerDashboard = React.lazy(() => import('./pages/PickerDashboard'));
const SubmitReport = React.lazy(() => import('./pages/SubmitReport'));
const Operations = React.lazy(() => import('./pages/Operations'));
const Analytics = React.lazy(() => import('./pages/Analytics'));
const MapTracking = React.lazy(() => import('./pages/MapTracking'));
const KnowledgeBase = React.lazy(() => import('./pages/KnowledgeBase'));
const NotFound = React.lazy(() => import('./pages/NotFound'));

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="flex h-screen bg-cream">
          <AppSidebar />
          <div className="flex-1 flex flex-col overflow-hidden ml-[250px] transition-all duration-300">
            <TopNavbar />
            <main className="flex-1 overflow-auto">
              <Suspense fallback={<LoadingState message="Loading page..." />}>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/agent" element={<AgentDashboard />} />
                  <Route path="/picker" element={<PickerDashboard />} />
                  <Route path="/submit" element={<SubmitReport />} />
                  <Route path="/operations" element={<Operations />} />
                  <Route path="/analytics" element={<Analytics />} />
                  <Route path="/map" element={<MapTracking />} />
                  <Route path="/knowledge" element={<KnowledgeBase />} />
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </Suspense>
            </main>
          </div>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
