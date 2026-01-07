import React, { useState } from 'react';
import { runAllocation } from '../services/api';
import type { AllocationResponse, BacktestResult } from '../services/api';
import ResultCard from '../components/ResultCard';
import TransactionsTable from '../components/TransactionsTable';
import AllocationForm from '../components/AllocationForm';
import { StockChart } from '../components/StockChart';

const Home: React.FC = () => {
  const [resultData, setResultData] = useState<AllocationResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleStartBacktest = async (tickers: string[], capital: number) => {
    setLoading(true);
    setResultData(null);
    try {
      const data = await runAllocation(tickers, capital);
      setResultData(data);
    } catch (err) {
      alert("Error: " + err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-page max-w-5xl mx-auto p-6 space-y-10">
      <AllocationForm onSubmit={handleStartBacktest} loading={loading} />

      {resultData?.results && Object.entries(resultData.results).map(([ticker, asset]: [string, BacktestResult]) => (
        <div key={ticker} className="border-t pt-10 first:border-t-0">
          
          {/* Title Area */}
          <div className="mb-6">
            <h2 className="text-3xl font-bold">{asset.symbol}</h2>
            <p className="text-gray-500">Backtest Results Overview</p>
          </div>

          {/* Chart Section - High importance, full width */}
          <div className="mb-8 block">
            <StockChart data={asset.history} />
          </div>

          {/* Performance Data Section */}
          <div className="space-y-8">
            <ResultCard result={asset} />
            <TransactionsTable transactions={asset.transactions} />
          </div>

        </div>
      ))}
    </div>
  );
};

export default Home;