"use client";

type Props = {
  dataset: {
    rows_analyzed: number;
    columns: number;
    missing_cells_percentage: number;
    duplicate_rows: number;
  };
  time_series?: {
    date_column?: string | null;
    frequency?: string | null;
  };
};

export default function DatasetContext({ dataset, time_series }: Props) {
  return (
    <div className="rounded-xl bg-white border border-neutral-200 px-6 py-4 text-sm text-neutral-700">
      <div className="flex flex-wrap gap-6">
        <span>
          Rows: <strong>{dataset.rows_analyzed}</strong>
        </span>
        <span>
          Columns: <strong>{dataset.columns}</strong>
        </span>
        <span>
          Missing:{" "}
          <strong>
            {dataset.missing_cells_percentage.toFixed(1)}%
          </strong>
        </span>
        <span>
          Duplicates: <strong>{dataset.duplicate_rows}</strong>
        </span>
        <span>
          Time-series:{" "}
          <strong>
            {time_series?.date_column
              ? `Yes (${time_series.frequency})`
              : "No"}
          </strong>
        </span>
      </div>
    </div>
  );
}
