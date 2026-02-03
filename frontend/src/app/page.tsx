"use client";

import { useState } from "react";
import { uploadFile, IngestionResponse } from "../lib/api";

import UploadBox from "../components/UploadBox";
import ExecutiveSummary from "../components/ExecutiveSummary";
import EvidenceOverview from "../components/EvidenceOverview";
import InsightCard from "../components/InsightCard";
import NextSteps from "../components/NextSteps";
import DecisionSummary from "../components/DecisionSummary";




export default function HomePage() {
  const [data, setData] = useState<IngestionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [stage, setStage] = useState<string | null>(null);

  async function handleUpload(file: File) {
    setLoading(true);
    setStage("Analyzing dataset structure and risks…");
    const res = await uploadFile(file);
    setData(res);
    setLoading(false);
    setStage(null);
  }

  /* ===============================
     UPLOAD EXPERIENCE
     =============================== */
  if (!data) {
    return (
      <main className="min-h-screen bg-neutral-100 flex items-center justify-center px-6">
        <div className="w-full max-w-3xl space-y-6">
          <UploadBox onFileSelected={handleUpload} loading={loading} />

          {loading && (
            <div className="rounded-xl bg-white border border-neutral-200 p-6 shadow-sm">
              <p className="text-sm font-semibold text-neutral-900">
                AI Analysis Running
              </p>
              <p className="text-sm text-neutral-600 mt-1">
                {stage}
              </p>

              <div className="mt-4 h-2 rounded bg-neutral-200 overflow-hidden">
                <div className="h-full w-2/3 bg-indigo-600 animate-pulse" />
              </div>
            </div>
          )}
        </div>
      </main>
    );
  }

  /* ===============================
     GROUP INSIGHTS
     =============================== */
  const grouped = data.insights.reduce((acc: any, cur: any) => {
    acc[cur.code] = acc[cur.code] || [];
    acc[cur.code].push(cur);
    return acc;
  }, {});

  const entries = Object.entries(grouped);
  const critical = entries.filter(([, v]: any) => v[0]?.severity === "high");
  const others = entries.filter(([, v]: any) => v[0]?.severity !== "high");

  /* ===============================
     RESULTS DASHBOARD
     =============================== */
  return (
    <main className="bg-neutral-100 text-neutral-900 min-h-screen">
      {/* ================= HERO / EXEC SUMMARY ================= */}
      <section className="bg-gradient-to-r from-slate-900 to-slate-800 text-white px-10 py-20">
        <div className="max-w-6xl mx-auto">
          <ExecutiveSummary insights={data.insights} />
        </div>
      </section>

      <section className="bg-neutral-50 px-10 py-12 border-b border-neutral-200">
  <div className="max-w-6xl mx-auto">
    <DecisionSummary
      totalInsights={data.insights.length}
      highCount={data.insights.filter(
        (i: any) => i.severity === "high"
      ).length}
      confidenceScore={Math.min(
        95,
        70 + data.insights.length * 2
      )}
    />
  </div>
</section>


      {/* ================= VISUAL EVIDENCE ================= */}
      <section className="bg-white px-10 py-16 border-b border-neutral-200">
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <h2 className="text-2xl font-semibold tracking-tight">
              Visual Evidence
            </h2>
            <p className="text-sm text-neutral-600 mt-1">
              Charts supporting the detected signals and anomalies
            </p>
          </div>

          <EvidenceOverview charts={data.charts} />
        </div>
      </section>

      {/* ================= CRITICAL RISKS ================= */}
      {critical.length > 0 && (
        <section className="bg-red-50 px-10 py-20">
          <div className="max-w-6xl mx-auto space-y-8">
            <div>
              <h2 className="text-2xl font-semibold text-red-700">
                Critical Risks Requiring Immediate Attention
              </h2>
              <p className="text-sm text-neutral-700 mt-1">
                These issues pose a high operational or analytical risk
              </p>
            </div>

            {critical.map(([code, items]: any) => (
              <InsightCard
                key={code}
                insightCode={code}
                primary={items[0]}
                supporting={items.slice(1).map((i: any) => i.message)}
                charts={data.charts}
              />
            ))}
          </div>
        </section>
      )}

      {/* ================= OTHER SIGNALS ================= */}
      <section className="bg-white px-10 py-20 border-t border-neutral-200">
        <div className="max-w-6xl mx-auto space-y-8">
          <div>
            <h2 className="text-2xl font-semibold text-amber-700">
              Other Notable Signals
            </h2>
            <p className="text-sm text-neutral-600 mt-1">
              Patterns worth monitoring but not immediately critical
            </p>
          </div>

          {others.map(([code, items]: any) => (
            <InsightCard
              key={code}
              insightCode={code}
              primary={items[0]}
              supporting={items.slice(1).map((i: any) => i.message)}
              charts={data.charts}
            />
          ))}
        </div>
      </section>

      {/* ================= NEXT STEPS ================= */}
      <section className="bg-neutral-50 px-10 py-20 border-t border-neutral-200">
        <div className="max-w-6xl mx-auto">
          <NextSteps
  steps={data.next_steps}
  insights={data.insights}
/>

        </div>
      </section>
    </main>
  );
}
