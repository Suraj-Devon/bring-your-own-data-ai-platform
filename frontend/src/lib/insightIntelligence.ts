export type InsightExplanation = {
  title: string;
  risk: string;
  impact: string;
  action: string;
  chartHint?: string;
};

export const INSIGHT_INTELLIGENCE: Record<string, InsightExplanation> = {
  CATEGORY_DOMINANCE: {
    title: "Category Dominance Detected",
    risk:
      "One category overwhelmingly dominates the dataset, reducing signal diversity.",
    impact:
      "Predictions, trends, and alerts may be biased or misleading due to lack of variation.",
    action:
      "Segment analysis by category or rebalance the dataset before using insights.",
    chartHint:
      "The chart highlights how one category disproportionately outweighs others.",
  },

  SUDDEN_DROP: {
    title: "Sudden Drop in Values",
    risk:
      "A sharp and unexpected decline was detected in the time series.",
    impact:
      "This may indicate data loss, system failure, reporting gaps, or real-world disruption.",
    action:
      "Investigate the affected period and validate upstream data sources.",
    chartHint:
      "Notice the abrupt downward movement compared to surrounding periods.",
  },

  HIGH_MISSINGNESS: {
    title: "High Missing Data",
    risk:
      "A large percentage of values are missing in one or more columns.",
    impact:
      "Model confidence and statistical reliability are significantly reduced.",
    action:
      "Impute missing values, drop the column, or fix data collection pipelines.",
  },

  DATA_QUALITY_ISSUES: {
    title: "Multiple Data Quality Warnings",
    risk:
      "Several structural and consistency issues were detected in the dataset.",
    impact:
      "Downstream analytics and decisions may be unreliable.",
    action:
      "Review schema consistency, null handling, and value ranges.",
  },
};
