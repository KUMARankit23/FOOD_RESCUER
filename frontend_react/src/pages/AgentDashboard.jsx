import React, { useState, useMemo, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Activity, AlertCircle, Zap, TrendingUp, MapPin, Truck, Clock, Eye } from 'lucide-react';
import { PageContainer } from '../components/layout/PageContainer';
import { SectionHeader } from '../components/common/SectionHeader';
import { MetricCard } from '../components/common/MetricCard';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { useListRuns, useGetRunTrace } from '../hooks/useReports';
import { format } from 'date-fns';

const AgentDashboard = () => {
  const { data: runs = [], isLoading: runsLoading, error: runsError, refetch } = useListRuns();
  const [selectedRunId, setSelectedRunId] = useState(null);
  const { data: traceData } = useGetRunTrace(selectedRunId);
  const [refreshInterval, setRefreshInterval] = useState(null);

  // Auto-refresh every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      refetch();
    }, 5000);
    return () => clearInterval(interval);
  }, [refetch]);

  // Calculate metrics
  const metrics = useMemo(() => {
    const dispatched = runs.filter((r) => r.decision_action === 'dispatch').length;
    const onHold = runs.filter((r) => r.decision_action === 'hold').length;
    const discarded = runs.filter((r) => r.decision_action === 'discard').length;
    const completed = runs.filter((r) => r.status === 'completed').length;
    const inProgress = runs.filter((r) => r.status === 'in_progress').length;

    return {
      totalRuns: runs.length,
      dispatchedCount: dispatched,
      holdCount: onHold,
      discardCount: discarded,
      completedCount: completed,
      inProgressCount: inProgress,
      successRate: runs.length > 0 ? ((dispatched / runs.length) * 100).toFixed(1) : 0,
      systemHealth: inProgress > 0 ? 100 : 95,
    };
  }, [runs]);

  // Identify alerts
  const alerts = useMemo(() => {
    const alertList = [];

    // Check for delayed runs (created more than 15 minutes ago but still in progress)
    runs.forEach((run) => {
      const createdTime = new Date(run.start_time);
      const now = new Date();
      const diffMinutes = (now - createdTime) / (1000 * 60);

      if (run.status === 'in_progress' && diffMinutes > 15) {
        alertList.push({
          type: 'warning',
          message: `Run ${run.run_id.slice(0, 8)}: Taking longer than expected (${Math.round(diffMinutes)} min)`,
          runId: run.run_id,
        });
      }

      // Check for NO_PICKUP decisions (potential issues)
      if (run.decision_action === 'no_pickup') {
        alertList.push({
          type: 'info',
          message: `Run ${run.run_id.slice(0, 8)}: No suitable recipient found`,
          runId: run.run_id,
        });
      }
    });

    return alertList;
  }, [runs]);

  const selectedRun = runs.find((r) => r.run_id === selectedRunId);

  if (runsLoading) {
    return <LoadingState message="Loading agent dashboard..." />;
  }

  if (runsError) {
    return (
      <ErrorState
        title="Failed to Load Dashboard"
        description={runsError.message}
        onRetry={() => refetch()}
      />
    );
  }

  return (
    <PageContainer>
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <h1 className="text-3xl md:text-4xl font-bold text-text-primary mb-2">
          🤖 Agent Operations Center
        </h1>
        <p className="text-text-muted">
          Real-time monitoring of all food rescue operations and agent decisions
        </p>
      </motion.div>

      {/* KPI Cards */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8"
      >
        <MetricCard
          icon={Activity}
          label="Total Operations"
          value={metrics.totalRuns}
          trend={`${metrics.inProgressCount} active`}
          color="primary"
        />
        <MetricCard
          icon={Truck}
          label="Dispatched"
          value={metrics.dispatchedCount}
          trend={`${metrics.completedCount} completed`}
          color="success"
        />
        <MetricCard
          icon={Clock}
          label="In Progress"
          value={metrics.inProgressCount}
          trend={`${Math.round((metrics.inProgressCount / Math.max(metrics.totalRuns, 1)) * 100)}%`}
          color="warning"
        />
        <MetricCard
          icon={AlertCircle}
          label="On Hold"
          value={metrics.holdCount}
          trend="+2%"
          color="info"
        />
        <MetricCard
          icon={Zap}
          label="System Health"
          value={`${metrics.systemHealth}%`}
          trend="✅ Operational"
          color="success"
        />
      </motion.div>

      {/* Alerts Section */}
      {alerts.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 bg-white rounded-lg border border-soft-sage shadow-sm p-6"
        >
          <h3 className="font-semibold text-text-primary mb-4 flex items-center gap-2">
            <AlertCircle size={20} className="text-warning" />
            System Alerts ({alerts.length})
          </h3>
          <div className="space-y-3">
            {alerts.map((alert, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className={`p-3 rounded-lg border-l-4 ${
                  alert.type === 'warning'
                    ? 'border-warning bg-warning-light text-warning'
                    : 'border-info bg-info-light text-info'
                }`}
              >
                <p className="text-sm font-medium">{alert.message}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Runs */}
        <div className="lg:col-span-2 bg-white rounded-lg border border-soft-sage shadow-sm p-6">
          <h3 className="font-semibold text-text-primary mb-4">Active Operations</h3>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-soft-sage bg-soft-sage">
                  <th className="px-3 py-2 text-left font-semibold">Run ID</th>
                  <th className="px-3 py-2 text-left font-semibold">Decision</th>
                  <th className="px-3 py-2 text-left font-semibold">Recipient</th>
                  <th className="px-3 py-2 text-left font-semibold">Status</th>
                  <th className="px-3 py-2 text-left font-semibold">Time</th>
                  <th className="px-3 py-2 text-center font-semibold">Action</th>
                </tr>
              </thead>
              <tbody>
                {runs.slice(0, 10).map((run) => (
                  <motion.tr
                    key={run.run_id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="border-b border-soft-sage hover:bg-soft-sage transition-colors cursor-pointer"
                    onClick={() => setSelectedRunId(run.run_id)}
                  >
                    <td className="px-3 py-3">
                      <code className="text-xs font-mono bg-cream px-2 py-1 rounded">
                        {run.run_id?.slice(0, 8)}...
                      </code>
                    </td>
                    <td className="px-3 py-3">
                      <span
                        className={`inline-block px-2 py-1 rounded text-xs font-semibold ${
                          run.decision_action === 'dispatch'
                            ? 'bg-success-light text-success'
                            : run.decision_action === 'hold'
                            ? 'bg-warning-light text-warning'
                            : 'bg-info-light text-info'
                        }`}
                      >
                        {run.decision_action?.toUpperCase() || 'PENDING'}
                      </span>
                    </td>
                    <td className="px-3 py-3 text-text-secondary">
                      {run.recipient_id ? `Rec-${run.recipient_id.slice(0, 4)}` : '-'}
                    </td>
                    <td className="px-3 py-3">
                      <span
                        className={`inline-flex items-center gap-1 text-xs font-medium ${
                          run.status === 'completed'
                            ? 'text-success'
                            : run.status === 'in_progress'
                            ? 'text-primary-600'
                            : 'text-text-secondary'
                        }`}
                      >
                        {run.status === 'completed' && '✅'}
                        {run.status === 'in_progress' && '🔄'}
                        {run.status === 'pending' && '⏳'}
                        {run.status?.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-3 py-3 text-text-muted text-xs">
                      {run.start_time ? format(new Date(run.start_time), 'HH:mm') : '-'}
                    </td>
                    <td className="px-3 py-3 text-center">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedRunId(run.run_id);
                        }}
                        className="p-1 hover:bg-primary-100 rounded transition-colors text-primary-600"
                      >
                        <Eye size={16} />
                      </button>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>

          {runs.length === 0 && (
            <p className="text-center text-text-muted py-8">No active operations</p>
          )}
        </div>

        {/* Summary Stats */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-white rounded-lg border border-soft-sage shadow-sm p-6 h-fit"
        >
          <h3 className="font-semibold text-text-primary mb-4">Today's Summary</h3>

          <div className="space-y-4">
            <div className="pb-4 border-b border-soft-sage">
              <p className="text-xs text-text-muted font-medium uppercase mb-2">Success Rate</p>
              <div className="flex items-baseline gap-2">
                <p className="text-2xl font-bold text-success">{metrics.successRate}%</p>
                <p className="text-sm text-text-secondary">of {metrics.totalRuns} runs</p>
              </div>
            </div>

            <div className="pb-4 border-b border-soft-sage">
              <p className="text-xs text-text-muted font-medium uppercase mb-2">Dispatches</p>
              <p className="text-xl font-bold text-primary-600">{metrics.dispatchedCount}</p>
            </div>

            <div className="pb-4 border-b border-soft-sage">
              <p className="text-xs text-text-muted font-medium uppercase mb-2">Completed</p>
              <p className="text-xl font-bold text-success">{metrics.completedCount}</p>
            </div>

            <div>
              <p className="text-xs text-text-muted font-medium uppercase mb-2">System Status</p>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 bg-success rounded-full animate-pulse"></span>
                <span className="text-sm font-medium text-success">Operational</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Detailed Run View */}
      {selectedRunId && selectedRun && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 bg-white rounded-lg border border-soft-sage shadow-sm p-6"
        >
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-semibold text-text-primary text-lg">Run Details & Agent Trace</h3>
            <button
              onClick={() => setSelectedRunId(null)}
              className="text-text-muted hover:text-text-primary transition-colors"
            >
              ✕
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left: Run Details */}
            <div className="space-y-4">
              <div className="pb-4 border-b border-soft-sage">
                <p className="text-xs text-text-muted font-medium uppercase">Run ID</p>
                <p className="text-sm font-mono text-primary-600 mt-1">{selectedRun.run_id}</p>
              </div>

              <div className="pb-4 border-b border-soft-sage">
                <p className="text-xs text-text-muted font-medium uppercase">Decision</p>
                <span
                  className={`inline-block mt-1 px-3 py-1 rounded text-sm font-semibold ${
                    selectedRun.decision_action === 'dispatch'
                      ? 'bg-success-light text-success'
                      : selectedRun.decision_action === 'hold'
                      ? 'bg-warning-light text-warning'
                      : 'bg-info-light text-info'
                  }`}
                >
                  {selectedRun.decision_action?.toUpperCase() || 'PENDING'}
                </span>
              </div>

              <div className="pb-4 border-b border-soft-sage">
                <p className="text-xs text-text-muted font-medium uppercase">Recipient</p>
                <p className="text-sm text-text-primary mt-1">
                  {selectedRun.recipient_id ? `Recipient ${selectedRun.recipient_id}` : 'Not assigned'}
                </p>
              </div>

              <div className="pb-4 border-b border-soft-sage">
                <p className="text-xs text-text-muted font-medium uppercase">Status</p>
                <span
                  className={`inline-block mt-1 px-3 py-1 rounded text-sm font-semibold ${
                    selectedRun.status === 'completed'
                      ? 'bg-success-light text-success'
                      : selectedRun.status === 'in_progress'
                      ? 'bg-warning-light text-warning'
                      : 'bg-info-light text-info'
                  }`}
                >
                  {selectedRun.status?.toUpperCase()}
                </span>
              </div>

              <div>
                <p className="text-xs text-text-muted font-medium uppercase">Timeline</p>
                <div className="space-y-1 mt-2 text-sm">
                  <p>
                    Start: <span className="font-mono">{format(new Date(selectedRun.start_time), 'PPpp')}</span>
                  </p>
                  {selectedRun.end_time && (
                    <p>
                      End: <span className="font-mono">{format(new Date(selectedRun.end_time), 'PPpp')}</span>
                    </p>
                  )}
                </div>
              </div>
            </div>

            {/* Right: Agent Trace */}
            <div>
              <p className="text-xs text-text-muted font-medium uppercase mb-3">Agent Execution Trace</p>
              <div className="space-y-3">
                {traceData?.trace?.steps && Array.isArray(traceData.trace.steps) ? (
                  traceData.trace.steps.map((step, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, x: 10 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="p-3 rounded-lg bg-cream border border-soft-sage"
                    >
                      <div className="flex items-start gap-2">
                        <span className="text-lg">🤖</span>
                        <div className="flex-1 min-w-0">
                          <p className="font-semibold text-sm text-text-primary">
                            {step.agent || 'System'}
                          </p>
                          <p className="text-xs text-text-secondary mt-1 break-words">
                            {step.description || step.output || 'Processing...'}
                          </p>
                          <p className="text-xs text-text-muted mt-1">
                            {step.timestamp
                              ? format(new Date(step.timestamp), 'HH:mm:ss')
                              : format(new Date(), 'HH:mm:ss')}
                          </p>
                        </div>
                      </div>
                    </motion.div>
                  ))
                ) : (
                  <p className="text-center text-text-muted py-4 text-sm">No trace data available yet</p>
                )}
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </PageContainer>
  );
};

export default AgentDashboard;
