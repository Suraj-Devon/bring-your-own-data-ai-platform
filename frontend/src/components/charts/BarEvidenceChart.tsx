"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  LabelList,
} from "recharts";

type Props = {
  data: any[];
  xKey: string;
  yKey: string;
};

export default function BarEvidenceChart({
  data,
  xKey,
  yKey,
}: Props) {
  if (!Array.isArray(data) || data.length === 0) return null;

  // --------------------------------------------------
  // Detect dominant value
  // --------------------------------------------------
  const values = data.map((d) => Number(d[yKey] ?? 0));
  const maxValue = Math.max(...values);
  const total = values.reduce((a, b) => a + b, 0);

  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data}>
        <XAxis
          dataKey={xKey}
          tick={{ fontSize: 12 }}
          interval="preserveStartEnd"
        />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip />

        <Bar dataKey={yKey} radius={[6, 6, 0, 0]}>
          {data.map((entry, index) => {
            const value = Number(entry[yKey] ?? 0);
            const isDominant = value === maxValue;

            return (
              <Cell
                key={`cell-${index}`}
                fill={isDominant ? "#ef4444" : "#94a3b8"}
                opacity={isDominant ? 1 : 0.5}
              />
            );
          })}

          {/* Label only on dominant bar */}
          <LabelList
            position="top"
            formatter={(label) => {
              const value = Number(label);
              if (!Number.isFinite(value)) return "";
              if (value !== maxValue) return "";
              if (!total) return "";

              const pct = Math.round((value / total) * 100);
              return `${pct}%`;
            }}
            style={{
              fontSize: 12,
              fontWeight: 600,
              fill: "#ef4444",
            }}
          />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
