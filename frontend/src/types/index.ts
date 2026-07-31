export interface UploadResponse {
  dataset_id: string;
  filename: string;
  file_size_bytes: number;
  uploaded_at: string;
  message: string;
}

export interface ColumnMetadata {
  name: string;
  data_type: string;
  inferred_type: string;
  non_null_count: number;
  null_count: number;
  null_percentage: number;
  unique_count: number;
  sample_values: any[];
}

export interface DatasetMetadata {
  filename: string;
  total_rows: number;
  total_columns: number;
  file_size_bytes: number;
  memory_usage_bytes: number;
  columns: ColumnMetadata[];
}

export interface QualityIssue {
  category: 'missing_values' | 'duplicate_rows' | 'type_inconsistency' | 'outliers';
  severity: 'low' | 'medium' | 'high' | 'critical';
  column?: string | null;
  title: string;
  description: string;
  affected_count: number;
  affected_percentage: number;
}

export interface ReadinessScoreBreakdown {
  completeness_score: number;
  uniqueness_score: number;
  type_validity_score: number;
  outlier_score: number;
}

export interface ReadinessScore {
  overall_score: number;
  grade: string;
  status: string;
  breakdown: ReadinessScoreBreakdown;
}

export interface ColumnSummary {
  column_name: string;
  data_type: string;
  missing_count: number;
  missing_pct: number;
  unique_count: number;
  outlier_count: number;
  min_value?: number | null;
  max_value?: number | null;
  mean_value?: number | null;
  std_value?: number | null;
}

export interface DatasetSummary {
  total_rows: number;
  total_columns: number;
  total_missing_cells: number;
  total_missing_pct: number;
  total_duplicate_rows: number;
  total_duplicate_pct: number;
  total_outliers: number;
  column_summaries: ColumnSummary[];
}

export interface AuditReport {
  dataset_id: string;
  filename: string;
  analyzed_at: string;
  metadata: DatasetMetadata;
  summary: DatasetSummary;
  readiness_score: ReadinessScore;
  issues: QualityIssue[];
}

export interface Decision {
  decision: string;
  target: string;
  confidence: number;
  reason: string;
  expected_impact: string;
  auto_fix: boolean;
}

export interface AIAnalysisResponse {
  dataset_id: string;
  health_summary: string;
  explanation: string;
  decisions: Decision[];
  python_code: string;
}