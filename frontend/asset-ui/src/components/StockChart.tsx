import {LineChart,Line,XAxis,YAxis,CartesianGrid,Tooltip,ResponsiveContainer,} from 'recharts';

export const StockChart = ({data,}: {data: { date: string; price: number }[];}) => {
  if (!data || data.length === 0) {
    return (
      <div className="h-[400px] flex items-center justify-center text-slate-400">
        No data available
      </div>
    );
  }

  return (
    <div className="w-full">
      <ResponsiveContainer width="100%" aspect={3}>
        <LineChart data={data} margin={{ top: 10, right: 16, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />

          <XAxis dataKey="date" hide />

          <YAxis
            orientation="right"
            width={60}
            tick={{ fontSize: 12, fill: '#94a3b8' }}
            tickFormatter={(val) => `$${Number(val).toLocaleString()}`}
            axisLine={false}
            tickLine={false}
            domain={[
              (min: number) => min * 0.97,
              (max: number) => max * 1.03,
            ]}
          />

          <Tooltip
            contentStyle={{
              borderRadius: '8px',
              border: 'none',
              boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
            }}
            formatter={(value: number | string | undefined) => [
              `$${Number(value ?? 0).toLocaleString()}`,
              'Price',
            ]}
          />

          <Line
            type="linear"
            dataKey="price"
            stroke="#3b82f6"
            strokeWidth={2.5}
            dot={false}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
