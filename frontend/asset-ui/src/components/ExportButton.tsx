import React from 'react';

// Define exactly what 'transactions' looks like
interface Transactions {
  date: string[];
  order: string[];
  price: number[];
  value: number[];
  fee: number[];
  label: string[];
}

interface ExportButtonProps {
  transactions: Transactions; // This must match the prop name you use in ResultCard
  symbol: string;
}

const ExportButton: React.FC<ExportButtonProps> = ({ transactions, symbol }) => {
  const handleDownload = () => {
    // Basic check to ensure data exists before trying to map it
    if (!transactions || !transactions.date) {
      console.error("No transaction data available for export");
      return;
    }

    const headers = ["Date", "Order", "Price", "Value", "Fee", "Label"];
    
    const rows = transactions.date.map((_, i) => [
      transactions.date[i],
      transactions.order[i],
      transactions.price[i]?.toFixed(2) || "0.00", // Optional chaining prevents crashes
      transactions.value[i]?.toFixed(2) || "0.00",
      transactions.fee[i]?.toFixed(2) || "0.00",
      transactions.label[i]
    ]);

    const csvContent = [
      headers.join(","),
      ...rows.map(row => row.join(","))
    ].join("\n");

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `${symbol}_backtest.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <button className="btn-secondary" onClick={handleDownload}>
      📥 Export to CSV
    </button>
  );
};

export default ExportButton;