import React, { useState, useEffect } from 'react';
import {
  AlertTriangle,
  BarChart2,
  Info,
  Clock,
  PieChart,
  Layers,
} from 'lucide-react';

const ThreatReportDashboard = () => {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadReportData = async () => {
      try {
        const mockReport = {
          timestamp: new Date().toISOString(),
          total_samples: 1000,
          anomaly_count: 120,
          anomaly_percentage: 12,
          top_anomalous_features: ['src_bytes', 'dst_bytes', 'duration', 'num_compromised', 'hot'],
        };
        setReportData(mockReport);
        setLoading(false);
      } catch (error) {
        console.error('Error loading report:', error);
        setLoading(false);
      }
    };
    loadReportData();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen p-6">
        <p className="text-gray-600 font-semibold">Loading threat report...</p>
      </div>
    );
  }

  if (!reportData) {
    return (
      <div className="flex justify-center items-center h-screen p-6">
        <p className="text-red-600 font-semibold">No threat report available</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-100 min-h-screen p-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Timestamp Card */}
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-700">Report Timestamp</h3>
            <Clock className="h-5 w-5 text-gray-500" />
          </div>
          <div className="text-xl font-bold text-gray-800">
            {new Date(reportData.timestamp).toLocaleString()}
          </div>
        </div>

        {/* Anomaly Overview Card */}
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-700">Anomaly Overview</h3>
            <AlertTriangle className="h-5 w-5 text-red-500" />
          </div>
          <div className="flex items-center">
            <div className="text-2xl font-bold text-red-600">
              {reportData.anomaly_count}
            </div>
            <div className="ml-2 text-sm text-gray-600">
              ({reportData.anomaly_percentage}%)
            </div>
          </div>
          <p className="text-sm text-gray-600 mt-2">
            Out of {reportData.total_samples} total samples
          </p>
        </div>

        {/* Top Anomalous Features Card */}
        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-700">Top Anomalous Features</h3>
            <Layers className="h-5 w-5 text-gray-500" />
          </div>
          <ul className="space-y-2">
            {reportData.top_anomalous_features.map((feature, index) => (
              <li key={feature} className="flex items-center text-gray-700">
                <span className="mr-2">{index + 1}.</span>
                <span className="font-medium">{feature}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ThreatReportDashboard;