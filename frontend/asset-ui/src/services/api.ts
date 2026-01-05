const API_URL = "http://localhost:8000";

// 1. Define the internal table structure
export interface TransactionData {
  date: string[];
  order: string[];
  price: number[];
  value: number[];
  fee: number[];
  label: string[];
}

// 2. Define the main API response
export interface AllocationResponse {
  symbol : string;
  ticker: string;
  shares: number;
  remaining_capital: number;
  status: string;
  sharpe: number;
  volatility: number;
  final_account_value: number;
  transactions: TransactionData; 
}

export async function runAllocation(
  ticker: string, 
  capital: number
): Promise<AllocationResponse> {
  const response = await fetch(`${API_URL}/allocate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ 
      tickers: [ticker], // Wrap in an array to match List[str]
      capital: capital    // Ensure key name matches 'capital'
    }),
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "API error");
  }

  return response.json() as Promise<AllocationResponse>;
}