"use client";

import BarEvidenceChart from "./charts/BarEvidenceChart";
import LineEvidenceChart from "./charts/LineEvidenceChart";

export default function EvidenceOverview({
  charts = [],
}: {
  charts: any[];
}) {
  if (!Array.isArray(charts) || charts.length === 0) return null;

  /* =========================================
     OVERVIEW EVIDENCE FILTER (CRITICAL)
     =========================================
     Only show charts that explain OVERALL risk.
     Per-insight evidence belongs in InsightCard.
  */
  const overviewCharts = charts.filter((c) =>
    ["SUDDEN_DROP", "SUDDEN_SPIKE", "MISSING_PERIODS"].includes(
      c.insight_code
    )
  );

  if (overviewCharts.length === 0) return null;

  return (
    <div className="rounded-2xl bg-white p-8 shadow space-y-6">
      {/* HEADER */}
      <div>
        <h2 className="text-lg font-semibold text-neutral-900">
          Key Evidence
        </h2>
        <p className="text-sm text-neutral-600">
          Visual proof supporting the overall risk assessment
        </p>
      </div>

      {/* EVIDENCE GRID */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {overviewCharts.slice(0, 4).map((chart, i) => {
          // 🔒 HARD GUARDS — NO GUESSING
          if (!Array.isArray(chart.data)) return null;
          if (!chart.xKey || !chart.yKey) return null;
          if (chart.data.length === 0) return null;

          return (
            <div
              key={`${chart.insight_code}-${i}`}
              className="rounded-xl border bg-slate-50 p-4"
            >
              {/* FIXED HEIGHT PREVENTS RECHARTS COLLAPSE */}
              <div className="h-80 min-h-[320px] w-full">
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
                <p className="mt-2 text-xs text-neutral-600">
                  {chart.caption}
                </p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
