import React from 'react';

const EnergyDashboard = ({ energyData }) => {
  // Extract data from the energyData string
  const extractDataPoint = (text, pattern) => {
    const match = text.match(pattern);
    return match ? parseFloat(match[1]) : null;
  };

  const dayPeakGen = extractDataPoint(energyData, /Peak generation was (\d+(\.\d+)?)MW during the day/);
  const eveningPeakGen = extractDataPoint(energyData, /and (\d+(\.\d+)?)MW in the evening/);
  const maxDemand = extractDataPoint(energyData, /Maximum demand reached (\d+(\.\d+)?)MW/);
  const temperature = extractDataPoint(energyData, /Temperature was (\d+(\.\d+)?)°C/);
  const isHoliday = energyData.includes('Is it a holiday: Yes');

  const calculateEfficiency = () => {
    if (maxDemand && (dayPeakGen || eveningPeakGen)) {
      const peakGen = Math.max(dayPeakGen || 0, eveningPeakGen || 0);
      return Math.min(100, (peakGen / maxDemand) * 100).toFixed(1);
    }
    return null;
  };

  const efficiency = calculateEfficiency();

  // If we couldn't extract any data, don't render the component
  if (!dayPeakGen && !eveningPeakGen && !maxDemand && !temperature) {
    return null;
  }

  return (
    <div className="dashboard-container">
      <h3>Energy Dashboard</h3>
      
      <div className="metrics-grid">
        {dayPeakGen && (
          <div className="metric-card">
            <div className="metric-value">{dayPeakGen}</div>
            <div className="metric-label">Day Peak (MW)</div>
          </div>
        )}
        
        {eveningPeakGen && (
          <div className="metric-card">
            <div className="metric-value">{eveningPeakGen}</div>
            <div className="metric-label">Evening Peak (MW)</div>
          </div>
        )}
        
        {maxDemand && (
          <div className="metric-card">
            <div className="metric-value">{maxDemand}</div>
            <div className="metric-label">Max Demand (MW)</div>
          </div>
        )}
        
        {temperature && (
          <div className="metric-card">
            <div className="metric-value">{temperature}°C</div>
            <div className="metric-label">Temperature</div>
          </div>
        )}
      </div>

      {efficiency && (
        <div className="efficiency-meter">
          <div className="efficiency-label">System Efficiency</div>
          <div className="progress-container">
            <div 
              className="progress-bar" 
              style={{ 
                width: `${efficiency}%`,
                backgroundColor: efficiency > 80 ? '#22c55e' : efficiency > 60 ? '#f59e0b' : '#ef4444'
              }}
            ></div>
          </div>
          <div className="efficiency-value">{efficiency}%</div>
        </div>
      )}

      {isHoliday !== undefined && (
        <div className={`holiday-indicator ${isHoliday ? 'is-holiday' : 'not-holiday'}`}>
          {isHoliday ? 'Holiday' : 'Working Day'}
        </div>
      )}
    </div>
  );
};

export default EnergyDashboard;