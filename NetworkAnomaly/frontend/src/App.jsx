import React from 'react';
import ThreatReportDashboard from './components/ThreatReportDashboard';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="container mx-auto">
        <h1 className="text-3xl font-bold text-center mb-6">
          Network Anomaly Detection Dashboard
        </h1>
        <ThreatReportDashboard />
      </div>
    </div>
  );
}

export default App;