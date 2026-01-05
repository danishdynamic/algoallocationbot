import React, { useState } from "react";

// 1. Define what props this component accepts
interface AllocationFormProps {
  onSubmit: (ticker: string, capital: number) => void;
  loading: boolean;
}

export default function AllocationForm({ onSubmit, loading }: AllocationFormProps) {
  const [ticker, setTicker] = useState<string>("");
  const [capital, setCapital] = useState<string>("");

  // 2. Type the event as React.FormEvent
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Logic: Convert ticker to uppercase and capital to a number before sending
    if (ticker && capital) {
      onSubmit(ticker.toUpperCase(), Number(capital));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="allocation-form">
      <div>
        <label htmlFor="ticker">Ticker Symbol:</label>
        <input
          type="text"
          id="ticker"
          value={ticker}
          // TypeScript knows 'e' is a ChangeEvent here automatically
          onChange={(e) => setTicker(e.target.value)}
          placeholder="e.g. AAPL"
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
        {loading ? "Processing..." : "Allocate"}
      </button>
    </form>
  );
}