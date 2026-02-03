"use client";

import { useState } from "react";
import ChartRenderer from "./charts/ChartRenderer";
import { INSIGHT_INTELLIGENCE } from "../lib/insightIntelligence";

type Props = {
  insightCode: string;
  primary?: {
    severity?: "high" | "medium" | "low";
    message?: string;
  };
  supporting?: string[];
  charts?: any[];
};

export default function InsightCard({
  insightCode,
  primary,
  supporting = [],
  charts = [],
}: Props) {
  const [open, setOpen] = useState(false);

  const severity = primary?.severity ?? "low";
  const intelligence = INSIGHT_INTELLIGENCE[insightCode] ?? null;

  /* =========================
     SEVERITY DESIGN SYSTEM
     ========================= */
  const theme = {
    high: {
      border: "border-red-500",
      badge: "bg-red-600 text-white",
      title: "text-red-900",
      text: "text-red-800",
    },
    medium: {
      border: "border-amber-400",
      badge: "bg-amber-500 text-white",
      title: "text-amber-900",
      text: "text-amber-800",
    },
    low: {
      border: "border-emerald-400",
      badge: "bg-emerald-600 text-white",
      title: "text-emerald-900",
      text: "text-emerald-800",
    },
  }[severity];

  return (
    <div
      className={`rounded-2xl border-l-8 ${theme.border} bg-white p-6 shadow-md`}
    >
      {/* HEADER */}
      <div className="flex items-start justify-between gap-6">
        <div>
          <span
            className={`inline-block rounded-full px-3 py-1 text-xs font-bold tracking-wide ${theme.badge}`}
          >
            {severity.toUpperCase()} RISK
          </span>

          <h3
            className={`mt-3 text-lg font-semibold tracking-tight ${theme.title}`}
          >
            {intelligence?.title ??
              insightCode.replaceAll("_", " ")}
          </h3>
        </div>

        {charts.length > 0 && (
          <button
            onClick={() => setOpen(!open)}
            className="text-sm font-semibold text-indigo-600 hover:underline"
          >
            {open ? "Hide evidence" : "View evidence"}
          </button>
        )}
      </div>

      {/* DESCRIPTION */}
      <p className={`mt-3 text-sm leading-relaxed ${theme.text}`}>
        {intelligence?.risk ??
          primary?.message ??
          "A notable pattern was detected in the dataset."}
      </p>

      {/* SUPPORTING BULLETS */}
      {supporting.length > 0 && (
        <ul className="mt-4 list-disc pl-5 space-y-1 text-sm text-neutral-700">
          {supporting.slice(0, 4).map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      )}

      {/* EXPANDED SECTION */}
      {open && (
        <div className="mt-6 space-y-4">
          {intelligence?.impact && (
            <div className="rounded-xl border border-neutral-200 bg-neutral-50 p-4">
              <p className="text-xs font-semibold uppercase text-neutral-600">
                Business Impact
              </p>
              <p className="mt-1 text-sm text-neutral-800">
                {intelligence.impact}
              </p>
            </div>
          )}

          {intelligence?.action && (
            <div className="rounded-xl border border-neutral-200 bg-neutral-50 p-4">
              <p className="text-xs font-semibold uppercase text-neutral-600">
                Recommended Action
              </p>
              <p className="mt-1 text-sm text-neutral-800">
                {intelligence.action}
              </p>
            </div>
          )}

          {intelligence?.chartHint && (
            <p className="text-xs italic text-neutral-500">
              {intelligence.chartHint}
            </p>
          )}

          {Array.isArray(charts) && charts.length > 0 && (
            <div className="rounded-xl border border-neutral-200 bg-white p-4">
              <ChartRenderer
                charts={charts}
                insightCode={insightCode}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
