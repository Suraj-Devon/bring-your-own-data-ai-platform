"use client";

type Props = {
  totalInsights: number;
  highCount: number;
  confidenceScore?: number;
};

export default function DecisionSummary({
  totalInsights,
  highCount,
  confidenceScore = 82,
}: Props) {
  const riskLevel =
    highCount > 0
      ? "High"
      : totalInsights > 0
      ? "Moderate"
      : "Low";

  const config = {
    High: {
      border: "border-red-500",
      bg: "bg-red-50",
      badge: "bg-red-600 text-white",
      title: "High Risk Dataset",
      message:
        "Critical risks were detected that may invalidate downstream analysis or decisions.",
      action: "Immediate investigation and mitigation is recommended.",
    },
    Moderate: {
      border: "border-amber-400",
      bg: "bg-amber-50",
      badge: "bg-amber-500 text-white",
      title: "Moderate Risk Dataset",
      message:
        "Some structural or statistical issues were detected that require monitoring.",
      action: "Validate affected areas before relying on this dataset.",
    },
    Low: {
      border: "border-emerald-400",
      bg: "bg-emerald-50",
      badge: "bg-emerald-600 text-white",
      title: "Low Risk Dataset",
      message:
        "No critical risks were detected in the dataset structure or trends.",
      action: "The dataset appears safe for exploratory analysis.",
    },
  }[riskLevel];

  return (
    <section
      className={`rounded-3xl border-l-8 ${config.border} ${config.bg} p-8 shadow-sm`}
    >
      <div className="flex items-start justify-between gap-6">
        <div>
          <span
            className={`inline-block rounded-full px-3 py-1 text-xs font-semibold tracking-wide ${config.badge}`}
          >
            AI DECISION SUMMARY
          </span>

          <h2 className="mt-3 text-xl font-semibold text-neutral-900">
            {config.title}
          </h2>

          <p className="mt-2 text-sm text-neutral-700">
            {config.message}
          </p>

          <p className="mt-1 text-sm font-medium text-neutral-800">
            {config.action}
          </p>
        </div>

        <div className="text-right">
          <p className="text-xs uppercase tracking-wide text-neutral-500">
            Confidence
          </p>
          <p className="text-2xl font-bold text-neutral-900">
            {confidenceScore}%
          </p>
        </div>
      </div>

      <div className="mt-6 flex flex-wrap gap-6 text-sm text-neutral-700">
        <span>
          <strong>{totalInsights}</strong> insights detected
        </span>
        <span>
          <strong>{highCount}</strong> high severity
        </span>
        <span>
          Risk Level: <strong>{riskLevel}</strong>
        </span>
      </div>
    </section>
  );
}
