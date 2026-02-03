"use client";

import BarEvidenceChart from "./BarEvidenceChart";
import LineEvidenceChart from "./LineEvidenceChart";

export default function ChartRenderer({
  charts,
  insightCode,
}: {
  charts: any[];
  insightCode: string;
}) {
  const matched = charts.filter(
    (c) => c.insight_code === insightCode
  );

  if (matched.length === 0) return null;

  return (
    <div className="mt-4 space-y-6">
      {matched.map((chart, idx) => {
        // 🔒 STRICT GUARDS (NO GUESSING)
        if (!Array.isArray(chart.data)) return null;
        if (!chart.xKey || !chart.yKey) return null;
        if (chart.data.length === 0) return null;

        return (
          <div
            key={`${chart.insight_code}-${idx}`}
            className="rounded-xl bg-slate-900/60 p-4 border border-slate-700"
          >
            {/* FIXED HEIGHT CONTAINER */}
            <div className="w-full h-[280px]">
              {chart.type === "bar" && (
                <BarEvidenceChart
                  data={chart.data}
                  xKey={chart.xKey}
                  yKey={chart.yKey}
                />
              )}

              {chart.type === "line" && (
                <LineEvidenceChart
                  data={chart.data}
                  xKey={chart.xKey}
                  yKey={chart.yKey}
                  annotations={chart.annotations ?? []}
                />
              )}
            </div>

            {chart.caption && (
              <p className="mt-2 text-xs text-slate-400">
                {chart.caption}
              </p>
            )}
          </div>
        );
      })}
    </div>
  );
}
