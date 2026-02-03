"use client";

export default function UploadBox({
  onFileSelected,
  loading,
}: {
  onFileSelected: (file: File) => void;
  loading: boolean;
}) {
  return (
    <div className="rounded-3xl bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 p-[2px] shadow-2xl">
      <div className="rounded-3xl bg-slate-950 px-10 py-14 text-center text-white">
        <p className="text-xs uppercase tracking-widest text-indigo-300">
          Bring Your Own Data
        </p>

        <h1 className="mt-4 text-4xl font-semibold">
          Upload data.<br />Get decisions.
        </h1>

        <p className="mt-4 text-sm text-slate-400 max-w-lg mx-auto">
          Upload any CSV or Excel file. The AI will analyze structure,
          risks, trends, and anomalies automatically.
        </p>

        <label className="mt-8 inline-block cursor-pointer rounded-xl bg-white px-8 py-4 text-sm font-semibold text-slate-900 shadow hover:scale-105 transition">
          {loading ? "Analyzing…" : "Upload dataset"}
          <input
            type="file"
            className="hidden"
            disabled={loading}
            accept=".csv,.xlsx,.xls"
            onChange={(e) =>
              e.target.files?.[0] &&
              onFileSelected(e.target.files[0])
            }
          />
        </label>

        <p className="mt-6 text-xs text-slate-500">
          Secure · No schema · Works with messy data
        </p>
      </div>
    </div>
  );
}
