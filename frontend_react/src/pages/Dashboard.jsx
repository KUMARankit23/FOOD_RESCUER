import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
import { Activity, Package, Zap, TrendingUp } from 'lucide-react';
import { PageContainer } from '../components/layout/PageContainer';
import { SectionHeader } from '../components/common/SectionHeader';
import { MetricCard } from '../components/common/MetricCard';
import { RescueActivityChart } from '../components/charts/RescueActivityChart';
import { FoodCategoryChart } from '../components/charts/FoodCategoryChart';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import { useListRuns } from '../hooks/useReports';
import { useEvaluationSummary } from '../hooks/useAnalytics';

const Dashboard = () => {
  const { data: runs = [], isLoading: runsLoading, error: runsError } = useListRuns();
  const { data: evalSummary, isLoading: evalLoading } = useEvaluationSummary();

  // Calculate metrics
  const metrics = useMemo(() => {
    const dispatches = runs.filter((r) => r.decision_action === 'dispatch').length;
    const holds = runs.filter((r) => r.decision_action === 'hold').length;
    const discards = runs.filter((r) => r.decision_action === 'discard').length;

    return {
      totalRuns: runs.length,
      dispatchedCount: dispatches,
      holdCount: holds,
      discardCount: discards,
      successRate: runs.length > 0 ? ((dispatches / runs.length) * 100).toFixed(1) : 0,
    };
  }, [runs]);

  // Chart data
  const activityData = useMemo(() => {
    const dailyData = {};
    runs.forEach((run) => {
      const date = new Date(run.start_time).toLocaleDateString();
      dailyData[date] = (dailyData[date] || 0) + 1;
    });
    return Object.entries(dailyData).map(([date, count]) => ({
      name: date,
      quantity: count,
    }));
  }, [runs]);

  const categoryData = useMemo(() => {
    const categories = {
      Dispatch: metrics.dispatchedCount,
      Hold: metrics.holdCount,
      Discard: metrics.discardCount,
    };
    return Object.entries(categories).map(([name, value]) => ({
      name,
      value,
    }));
  }, [metrics]);

  if (runsLoading || evalLoading) {
    return <LoadingState message="Loading dashboard..." />;
  }

  if (runsError) {
    return (
      <ErrorState
        title="Failed to Load Dashboard"
        description={runsError.message}
      />
    );
  }

  return (
    <PageContainer>
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl md:text-4xl font-bold text-text-primary mb-2">
          Welcome to ANNASARTHI AI
        </h1>
        <p className="text-text-muted">
          Good Food. Greater Purpose. Smarter Redistribution.
        </p>
      </motion.div>

      {/* KPI Cards */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8"
      >
        <MetricCard
          icon={Activity}
          label="Total Operations"
          value={metrics.totalRuns}
          trend="+12%"
          color="primary"
        />
        <MetricCard
          icon={Package}
          label="Dispatched"
          value={metrics.dispatchedCount}
          trend="+8%"
          color="success"
        />
        <MetricCard
          icon={Zap}
          label="On Hold"
          value={metrics.holdCount}
          trend="-2%"
          color="warning"
        />
        <MetricCard
          icon={TrendingUp}
          label="Success Rate"
          value={`${metrics.successRate}%`}
          trend="+5%"
          color="primary"
        />
      </motion.div>

      {/* Charts Grid */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8"
      >
        {/* Activity Chart */}
        <div className="lg:col-span-2 bg-white rounded-lg border border-soft-sage shadow-sm p-6">
          <SectionHeader title="Rescue Activity" subtitle="Last 7 days" />
          <RescueActivityChart data={activityData} variant="area" />
        </div>

        {/* Category Distribution */}
        <div className="bg-white rounded-lg border border-soft-sage shadow-sm p-6">
          <SectionHeader title="Decision Distribution" />
          <FoodCategoryChart data={categoryData} />
        </div>
      </motion.div>

      {/* Recent Operations */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="bg-white rounded-lg border border-soft-sage shadow-sm p-6"
      >
        <SectionHeader title="Recent Operations" subtitle={`Latest ${Math.min(5, runs.length)} runs`} />
        
        {runs.slice(0, 5).length > 0 ? (
          <div className="space-y-2">
            {runs.slice(0, 5).map((run, idx) => (
              <motion.div
                key={run.run_id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="flex items-center justify-between p-3 hover:bg-soft-sage rounded transition-colors"
              >
                <div className="flex items-center gap-3 flex-1">
                  <div className="w-2 h-2 rounded-full bg-primary-600" />
                  <div>
                    <p className="text-sm font-medium text-text-primary">
                      {run.decision_action?.toUpperCase() || 'N/A'}
                    </p>
                    <p className="text-xs text-text-muted">
                      {new Date(run.start_time).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
                <span className="text-xs text-text-muted">
                  {run.recipient_id?.slice(0, 8)}
                </span>
              </motion.div>
            ))}
          </div>
        ) : (
          <p className="text-text-muted text-center py-8">No recent operations</p>
        )}
      </motion.div>
    </PageContainer>
  );
};

export default Dashboard;
