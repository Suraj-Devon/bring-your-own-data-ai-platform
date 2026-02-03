import ChartRenderer from "./charts/ChartRenderer";

export default function NarrativeInsight({
  insight,
  charts,
}: {
  insight: any;
  charts: any[];
}) {
  const tone =
    insight.severity === "high"
      ? "border-red-500/40 bg-red-500/10"
      : insight.severity === "medium"
      ? "border-amber-500/40 bg-amber-500/10"
      : "border-emerald-500/40 bg-emerald-500/10";

  return (
    <article className={`rounded-3xl border ${tone} p-8`}>
      <p className="text-xs uppercase tracking-widest opacity-70">
        {insight.severity} severity signal
      </p>

      <h2 className="mt-3 text-2xl font-semibold">
        {insight.code.replaceAll("_", " ")}
      </h2>

      <p className="mt-4 text-slate-300">
        {insight.message}
      </p>

      {insight.recommendation && (
        <div className="mt-6 rounded-xl bg-black/30 p-4">
          <p className="text-sm font-semibold">
            Recommended Action
          </p>
          <p className="mt-1 text-sm text-slate-300">
            {insight.recommendation}
          </p>
        </div>
      )}

      <div className="mt-8 h-72">
        <ChartRenderer
          insightCode={insight.code}
          charts={charts}
        />
      </div>
    </article>
  );
}
