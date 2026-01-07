const API_URL = "http://localhost:8000";

// 1. Define the internal table structure
export interface TransactionData {
  date: string[];
  order: string[];
  price: number[];
  symbol: string[];
  value: number[];
  fee: number[];
  label: string[];
}

export interface BacktestResult {
  symbol: string;
  initial_money: number;
  sharpe: number;
  volatility: number;
  final_account_value: number;
  transactions: TransactionData;
}

export interface AllocationResponse {
  // Global metadata (if your backend sends it)
  ticker: string; 
  status?: string;
  
  // The actual data for AAPL, MSFT, etc.
  results: { 
    [key: string]: BacktestResult 
  };
  
  error: string | null;
}


export async function runAllocation(
  tickers: string[], //Changed from ticker string to string []
  capital: number
): Promise<AllocationResponse> {
  const response = await fetch(`${API_URL}/allocate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ 
      tickers: tickers,   // Wrap in an array to match List[str] for one such as ticker[]
      capital: capital    // Ensure key name matches 'capital'
    }),
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "API error");
  }

  return response.json() as Promise<AllocationResponse>;
}

