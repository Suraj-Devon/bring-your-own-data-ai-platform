"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

type Annotation = {
  x: string;
  label: string;
};

type Props = {
  data: any[];
  xKey: string;
  yKey: string;
  annotations?: Annotation[];
};

export default function LineEvidenceChart({
  data,
  xKey,
  yKey,
  annotations = [],
}: Props) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={data}>
        <XAxis
          dataKey={xKey}
          tick={{ fontSize: 12 }}
          interval="preserveStartEnd"
        />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip />

        <Line
          type="monotone"
          dataKey={yKey}
          stroke="#22c55e"
          strokeWidth={2}
          dot={false}
        />

        {/* 🔎 Evidence markers (X-axis only, no fake Y values) */}
        {annotations.map((a, i) => (
          <ReferenceLine
            key={i}
            x={a.x}
            stroke="#ef4444"
            strokeDasharray="3 3"
            label={{
              value: a.label,
              position: "top",
              fontSize: 10,
              fill: "#ef4444",
            }}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}
