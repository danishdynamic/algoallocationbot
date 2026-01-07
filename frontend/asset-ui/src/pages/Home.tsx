import React, { useState } from 'react';
import { runAllocation} from '../services/api';
import type { AllocationResponse, BacktestResult } from '../services/api';
import ResultCard from '../components/ResultCard';
import TransactionsTable from '../components/TransactionsTable';
import AllocationForm from '../components/AllocationForm';

const Home: React.FC = () => {
  const [resultData, setResultData] = useState<AllocationResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleStartBacktest = async (tickers: string[], capital: number) => {
    setLoading(true);
    setResultData(null);

    try {
      // Ensure these match your API expectations
      const data = await runAllocation(tickers, capital); 
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
      <AllocationForm onSubmit={handleStartBacktest} loading={loading} />

      {/* This conditional (resultData && ...) is crucial. 
          It ensures ResultCard only renders when resultData is NOT null,
          satisfying the TypeScript requirement for the 'result' prop.
          {resultData && <ResultCard result={resultData} />} for one stock 
      */}
      {resultData?.results && Object.entries(resultData.results).map(([ticker, asset] : [string, BacktestResult]) => (
        <div key={ticker} className="mb-6">
          {/* Display a Heading for each stock */}
          <h2 className="text-2xl font-bold mb-2 text-blue-600">{asset.symbol} {resultData.ticker ? `(Portfolio: ${resultData.ticker})` : ''}</h2>
          
          {/* Pass the specific stock data to the ResultCard */}
          <ResultCard result={asset} />
          
          {/* Pass the specific stock transactions to your Table */}
          <div className="mt-4">
            <TransactionsTable transactions={asset.transactions} />
          </div>
        </div>
      ))}
    </div>
  );
};

export default Home;