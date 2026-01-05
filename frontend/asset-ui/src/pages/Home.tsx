import React, { useState } from 'react';
import { runAllocation} from '../services/api';
import type { AllocationResponse } from '../services/api';
import ResultCard from '../components/ResultCard';

const Home: React.FC = () => {
  const [resultData, setResultData] = useState<AllocationResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleStartBacktest = async () => {
    setLoading(true);
    try {
      // Ensure these match your API expectations
      const data = await runAllocation("AAPL", 100000); 
      setResultData(data);
    } catch (err) {
      // check if error is especially from rate limit exceeded
      if (err instanceof Error && err.message.includes("429")) {
        alert("Rate limit exceeded. Please try again later.");
      } else {
        alert("Failed to fetch backtest: " + err);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-page">
      <button onClick={handleStartBacktest} disabled={loading}>
        {loading ? "Calculating..." : "Run Momentum Backtest"}
      </button>

      {/* This conditional (resultData && ...) is crucial. 
          It ensures ResultCard only renders when resultData is NOT null,
          satisfying the TypeScript requirement for the 'result' prop.
      */}
      {resultData && <ResultCard result={resultData} />}
    </div>
  );
};

export default Home;