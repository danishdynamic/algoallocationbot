import React from 'react';
import type { BacktestResult } from '../services/api';
import ExportButton from './ExportButton';

// The 'result' prop must match the interface you defined in api.ts
interface ResultCardProps {
  result: BacktestResult;           /* we used allocation resposne for one symbol*/
}

const ResultCard: React.FC<ResultCardProps> = ({ result }) => {
  // Destructure for cleaner access
  const { transactions ,symbol, sharpe, volatility, final_account_value } = result;

  return (
    <div className="result-card">
      <header className="result-header">
        <h2>Backtest: {symbol}</h2>
        <div className="badge">Success</div>
      </header>

      {/* 1. Summary Metrics Section */}
      <div className="metrics-grid">
        <div className="metric-box">
          <span>Sharpe Ratio</span>
          <strong>{sharpe.toFixed(2)}</strong>
        </div>
        <div className="metric-box">
          <span>Annual Volatility</span>
          <strong>{(volatility * 100).toFixed(1)}%</strong>
        </div>
        <div className="metric-box">
          <span>Final Balance</span>
          <strong>${final_account_value.toLocaleString(undefined, { minimumFractionDigits: 2 })}</strong>
        </div>
      </div>

      <div className="result-header">
        <h2>Results for {result.symbol}</h2>
        <ExportButton transactions={result.transactions} symbol={result.symbol} />
      </div>

      {/* 2. Transaction Table Section */}
      <div className="table-container">
        <h3>Transaction History</h3>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Order</th>
              <th>Price</th>
              <th>Fee</th>
              <th>Label</th>
            </tr>
          </thead>
          <tbody>
            {/* Since your backend returns "Columnar" data, we map by index */}
            {transactions.date.map((dateStr, i) => (
              <tr key={`${dateStr}-${i}`}>
                <td>{dateStr}</td>
                <td className={`order-${transactions.order[i]}`}>
                  {transactions.order[i].toUpperCase()}
                </td>
                <td>${transactions.price[i].toFixed(2)}</td>
                <td>${transactions.fee[i].toFixed(2)}</td>
                <td className="label-text">{transactions.label[i]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ResultCard;