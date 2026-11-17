import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { PageContainer } from '../components/layout/PageContainer';
import { SectionHeader } from '../components/common/SectionHeader';
import { RunHistoryTable } from '../components/operations/RunHistoryTable';
import { AgentExecutionTimeline } from '../components/operations/AgentExecutionTimeline';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { useListRuns, useGetRunTrace } from '../hooks/useReports';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/common/Tabs';
import { AgentChat } from '../components/operations/AgentChat';
import { LiveTracking } from '../components/operations/LiveTracking';
import { RecipientStatusUpdate } from '../components/operations/RecipientStatusUpdate';

const Operations = () => {
  const { data: runs = [], isLoading: runsLoading, error: runsError, refetch } = useListRuns();
  const [selectedRunId, setSelectedRunId] = useState(null);
  const { data: traceData, isLoading: traceLoading } = useGetRunTrace(selectedRunId);

  const selectedRun = useMemo(() => {
    return runs.find((r) => r.run_id === selectedRunId);
  }, [runs, selectedRunId]);

  if (runsLoading) {
    return <LoadingState message="Loading operations..." />;
  }

  if (runsError) {
    return (
      <ErrorState
        title="Failed to Load Operations"
        description={runsError.message}
        onRetry={() => refetch()}
      />
    );
  }

  return (
    <PageContainer>
      <SectionHeader
        title="Operations"
        subtitle="View all food rescue operations, live tracking, and agent communication"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Run History */}
        <div className="lg:col-span-2 bg-white rounded-lg border border-soft-sage shadow-sm p-6">
          <h3 className="font-semibold text-text-primary mb-4">Run History</h3>
          <RunHistoryTable
            runs={runs}
            onViewRun={(runId) => setSelectedRunId(runId)}
          />
        </div>

        {/* Run Details */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-white rounded-lg border border-soft-sage shadow-sm p-6 h-fit"
        >
          <h3 className="font-semibold text-text-primary mb-4">📋 Run Details</h3>
          {selectedRun ? (
            <div className="space-y-5">
              {/* Run ID */}
              <div className="pb-4 border-b border-soft-sage">
                <p className="text-xs text-text-muted font-medium uppercase tracking-wide">Run ID</p>
                <p className="text-sm font-mono text-primary-600 break-all mt-1">
                  {selectedRun.run_id}
                </p>
              </div>

              {/* Decision */}
              <div className="pb-4 border-b border-soft-sage">
                <p className="text-xs text-text-muted font-medium uppercase tracking-wide mb-2">🎯 Decision</p>
                <div>
                  <span className={`inline-block px-3 py-2 rounded-lg text-sm font-semibold ${
                    selectedRun.decision_action === 'MATCHED' ? 'bg-success-light text-success' :
                    selectedRun.decision_action === 'ACCEPTED' ? 'bg-primary-100 text-primary-600' :
                    'bg-warning-light text-warning'
                  }`}>
                    {selectedRun.decision_action?.toUpperCase() || 'PENDING'}
                  </span>
                </div>
              </div>

              {/* Recipient */}
              <div className="pb-4 border-b border-soft-sage">
                <p className="text-xs text-text-muted font-medium uppercase tracking-wide">👥 Recipient</p>
                <p className="text-sm text-text-primary mt-1 font-medium">
                  {selectedRun.recipient_id ? `Recipient: ${selectedRun.recipient_id}` : '⏳ Waiting for assignment'}
                </p>
                <p className="text-xs text-text-secondary mt-1">Food facility / Organization</p>
              </div>

              {/* Time & Duration */}
              <div className="pb-4 border-b border-soft-sage">
                <p className="text-xs text-text-muted font-medium uppercase tracking-wide mb-2">⏱️ Timeline</p>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-text-secondary">Start Time:</span>
                    <span className="text-sm font-mono text-primary-600">
                      {selectedRun.start_time ? new Date(selectedRun.start_time).toLocaleString() : 'N/A'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-text-secondary">End Time:</span>
                    <span className="text-sm font-mono text-primary-600">
                      {selectedRun.end_time ? new Date(selectedRun.end_time).toLocaleString() : 'In Progress'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center pt-2 border-t border-soft-sage">
                    <span className="text-sm font-medium text-text-primary">Duration:</span>
                    <span className="text-sm font-bold text-success">
                      {selectedRun.end_time && selectedRun.start_time
                        ? `${Math.round((new Date(selectedRun.end_time) - new Date(selectedRun.start_time)) / 1000)} seconds`
                        : selectedRun.start_time ? '⏳ In Progress' : 'N/A'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Status */}
              <div>
                <p className="text-xs text-text-muted font-medium uppercase tracking-wide mb-2">Status</p>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-success rounded-full"></span>
                  <span className="inline-block px-3 py-1 rounded-full text-xs bg-success-light text-success font-semibold">
                    {selectedRun.status === 'completed' ? '✅ Completed' : '🔄 In Progress'}
                  </span>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-center text-text-muted py-8">
              👈 Select a run from the history to view details
            </p>
          )}
        </motion.div>
      </div>

      {/* Live Tracking & Agent Chat */}
      {selectedRunId && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6"
        >
          <LiveTracking runId={selectedRunId} />
          <AgentChat runId={selectedRunId} />
        </motion.div>
      )}

      {/* Recipient Status Update */}
      {selectedRunId && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8"
        >
          <RecipientStatusUpdate
            runId={selectedRunId}
            currentStatus={selectedRun?.status || 'In Progress'}
            onStatusUpdate={(data) => {
              console.log('Recipient status updated:', data);
              // Here you can call API to save the update
            }}
          />
        </motion.div>
      )}

      {/* Agent Execution Timeline */}
      {selectedRunId && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 bg-white rounded-lg border border-soft-sage shadow-sm p-6"
        >
          <h3 className="font-semibold text-text-primary mb-6">Agent Execution Timeline</h3>
          {traceLoading ? (
            <LoadingState message="Loading trace..." />
          ) : (
            <AgentExecutionTimeline trace={traceData?.trace || {}} />
          )}
        </motion.div>
      )}
    </PageContainer>
  );
};

export default Operations;
