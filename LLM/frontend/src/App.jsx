import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import EnergyDashboard from './components/EnergyDashboard';
import './App.css';

function App() {
  const [analysis, setAnalysis] = useState('');
  const [rawData, setRawData] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchAnalysis = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get('/api/energy-analysis');
      setAnalysis(response.data.analysis);
      const dataMatch = response.data.analysis.match(/Peak generation was.*Temperature was.*°C\nIs it a holiday:.*/s);
      if (dataMatch) {
        setRawData(dataMatch[0]);
      }
    } catch (error) {
      console.error('Error fetching analysis:', error);
      setError('Failed to fetch analysis. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <header className="app-header">
          <h1 className="app-title">GridGenius</h1>
          <p className="tagline">AI-Powered Energy Optimization</p>
        </header>

        <div className="button-container">
          <button onClick={fetchAnalysis} disabled={loading} className="analysis-button">
            {loading ? 'Processing...' : 'Generate Energy Analysis'}
          </button>
          {loading && <div className="loading-spinner"></div>}
          {error && <div className="error-message">{error}</div>}
        </div>

        <div className="results-container">
          {analysis && (
            <div className="analysis-card">
              <h2 className="analysis-title">Energy Analysis Results</h2>
              <ReactMarkdown>{analysis}</ReactMarkdown>
            </div>
          )}
          {rawData && <EnergyDashboard energyData={rawData} />}
        </div>
      </div>
      
      <footer className="app-footer">
        <p>© 2025 GridGenius | Adib Ar Rahman Khan</p>
      </footer>
    </div>
  );
}

export default App;