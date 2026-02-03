"use client";

type NextStep = {
  title: string;
  description: string;
  priority: number;
  derived_from: string;
  category: string;

  // 🔥 Phase 2 — Explainability
  why_now?: string;
  risk_if_ignored?: string;
  confidence?: number;
};

type Insight = {
  code: string;
  severity: "high" | "medium" | "low";
};

export default function NextSteps({
  steps = [],
  insights = [],
}: {
  steps?: NextStep[];
  insights?: Insight[];
}) {
  const hasRisk = insights.some(
    (i) => i.severity === "high" || i.severity === "medium"
  );

  /* ===============================
     EMPTY BUT RISK EXISTS (HONEST)
     =============================== */
  if (steps.length === 0 && hasRisk) {
    return (
      <div className="rounded-3xl bg-white p-8 border border-neutral-200">
        <h2 className="text-lg font-semibold text-neutral-900">
          What should you do next?
        </h2>

        <p className="mt-4 text-sm text-neutral-700">
          ⚠️ Risks were detected in the dataset.  
          Review the insights above and address data quality or integrity
          issues before using this dataset for decisions or modeling.
        </p>
      </div>
    );
  }

  /* ===============================
     TRUE STABLE CASE (RARE)
     =============================== */
  if (steps.length === 0 && !hasRisk) {
    return (
      <div className="rounded-3xl bg-white p-8 border border-neutral-200">
        <h2 className="text-lg font-semibold text-neutral-900">
          What should you do next?
        </h2>

        <p className="mt-4 text-sm text-neutral-700">
          ✅ No immediate risks detected.  
          The dataset appears structurally stable at this time.
        </p>
      </div>
    );
  }

  /* ===============================
     PHASE 2 — ACTIONABLE STEPS
     =============================== */
  const topSteps = steps.slice(0, 3);

  return (
    <div className="rounded-3xl bg-white p-8 border border-neutral-200">
      <h2 className="text-lg font-semibold text-neutral-900">
        What should you do next?
      </h2>

      <ul className="mt-6 space-y-6">
        {topSteps.map((step, idx) => (
          <li
            key={idx}
            className="rounded-xl bg-neutral-50 p-6 border border-neutral-200"
          >
            <div className="flex items-start justify-between gap-4">
              <h3 className="text-sm font-semibold text-neutral-900">
                {step.title}
              </h3>

              <span className="text-xs font-mono text-neutral-500">
                priority {step.priority}
              </span>
            </div>

            <p className="mt-2 text-sm text-neutral-700">
              {step.description}
            </p>

            {step.why_now && (
              <p className="mt-3 text-xs text-neutral-600">
                <strong>Why now:</strong> {step.why_now}
              </p>
            )}

            {step.risk_if_ignored && (
              <p className="mt-1 text-xs text-neutral-600">
                <strong>Risk if ignored:</strong> {step.risk_if_ignored}
              </p>
            )}

            {typeof step.confidence === "number" && (
              <p className="mt-2 text-xs text-neutral-500">
                Confidence:{" "}
                <strong>{Math.round(step.confidence * 100)}%</strong>
              </p>
            )}

            <p className="mt-3 text-xs text-neutral-500">
              Derived from insight:{" "}
              <span className="font-mono">
                {step.derived_from}
              </span>
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}
