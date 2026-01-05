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
          <th>Date</th>
          <th>Order</th>
          <th>Price</th>
          <th>Value</th>
          <th>Fee</th>
          <th>Label</th>
        </tr>
      </thead>
      <tbody>
        {/* Mapping over the 'date' array index to build the rows */}
        {transactions.date.map((_, i) => (
          <tr key={i}>
            <td>{transactions.date[i]}</td>
            <td>{transactions.order[i]}</td>
            <td>{transactions.price[i]}</td>
            <td>{transactions.value[i]}</td>
            <td>{transactions.fee[i]}</td>
            <td>{transactions.label[i]}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}