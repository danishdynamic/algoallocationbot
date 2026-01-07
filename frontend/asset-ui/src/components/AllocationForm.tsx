import React, { useState } from "react";

// 1. Define what props this component accepts
interface AllocationFormProps {
  onSubmit: (ticker: string[], capital: number) => void;
  loading: boolean;
}

export default function AllocationForm({ onSubmit, loading }: AllocationFormProps) {
  const [tickerInput, setTickerInput] = useState<string>("");
  const [capital, setCapital] = useState<string>("");

  // 2. Type the event as React.FormEvent
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
      
    if (tickerInput && capital) {
        // Logic: Split by comma, trim whitespace, and filter out empty strings
        const tickerArray = tickerInput
          .split(",")
          .map((t) => t.trim().toUpperCase())
          .filter((t) => t !== "");

        onSubmit(tickerArray, Number(capital));
      }
    };

  return (
    <form onSubmit={handleSubmit} className="allocation-form">
      <div>
        <label htmlFor="ticker">Ticker Symbol:</label>
        <input
          type="text"
          id="ticker"
          value={tickerInput}
          // TypeScript knows 'e' is a ChangeEvent here automatically
          onChange={(e) => setTickerInput(e.target.value)}
          placeholder="e.g. AAPL,MSFT,NVDA"
          required
        />
      </div>
      <div>
        <label htmlFor="capital">Capital:</label>
        <input
          type="number"
          id="capital"
          value={capital}
          onChange={(e) => setCapital(e.target.value)}
          required
        />
      </div>
      <button type="submit" disabled={loading}>
        {loading ? "Processing..." : "Run Multi Asset Backtest"}
      </button>
    </form>
  );
}