// 1. Define the shape of the transaction data
interface TransactionsData {
  date: string[];
  order: string[];
  price: number[];
  value: number[];
  fee: number[];
  label: string[];
}

// 2. Define the Props for the component
interface TransactionsTableProps {
  transactions?: TransactionsData | null;
}

export default function TransactionsTable({ transactions }: TransactionsTableProps) {
  // Use optional chaining and check for the date array's length
  if (!transactions || !transactions.date?.length) return null;

  return (
    <table >
      <thead>
        <tr>
          {["Date", "Order", "Price", "Value", "Fee", "Label"].map((head) => (
            <th key={head} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
              {head}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {/* Mapping over the 'date' array index to build the rows */}
        {transactions.date.map((_, i) => (
          <tr key={i}>
            <td>{transactions.date[i]}</td>
            <td>{transactions.order[i].toUpperCase()}</td>
            <td>{transactions.price[i].toFixed(2)}</td>
            <td>{transactions.value[i].toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
            <td>{transactions.fee[i].toFixed(2)}</td>
            <td>{transactions.label[i]}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}