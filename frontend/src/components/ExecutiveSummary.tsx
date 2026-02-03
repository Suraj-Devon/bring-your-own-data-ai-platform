"use client";

export default function ExecutiveSummary({
  insights,
}: {
  insights: any[];
}) {
  const high = insights.filter((i) => i.severity === "high").length;
  const medium = insights.filter((i) => i.severity === "medium").length;

  return (
    <div className="space-y-4">
      <p className="uppercase tracking-widest text-xs opacity-90">
        AI Decision Report
      </p>

      <h1 className="text-3xl font-semibold">
        {high > 0
          ? "High Operational Risk Detected"
          : "No Critical Risks Detected"}
      </h1>

      <p className="max-w-3xl text-sm opacity-95">
        The AI analyzed your dataset for structure, quality, imbalance,
        and temporal instability. The findings below highlight
        decision-relevant risks.
      </p>

      <div className="flex gap-6 text-sm">
        <span>
          <strong>{high}</strong> critical risks
        </span>
        <span>
          <strong>{medium}</strong> moderate risks
        </span>
        <span>
          <strong>{insights.length}</strong> total signals
        </span>
      </div>
    </div>
  );
}
