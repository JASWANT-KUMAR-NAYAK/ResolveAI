export interface DeviationData {
  site: string;
  dateOfOccurrence: string;
  title: string;
  description: string;

  relatedProduct: string | null;
  relatedMaterial: string | null;
  batchNumber: string | null;
  processParameter: string | null;
}

export type DocumentStatus =
  | "idle"
  | "uploading"
  | "uploaded"
  | "error";

export type ExtractionStatus =
  | "idle"
  | "processing"
  | "complete"
  | "error";

export type AnalysisStatus =
  | "idle"
  | "processing"
  | "complete"
  | "error";

export type ImpactLevel =
  | "Critical"
  | "High"
  | "Medium"
  | "Low";

export type SeverityLevel =
  | "Critical"
  | "High"
  | "Medium"
  | "Low";

export interface DocumentState {
  file: File | null;
  text: string;
  status: DocumentStatus;
  preview: string;
}

export interface ExtractionState {
  status: ExtractionStatus;
  progress: number;
  data: DeviationData;
  confidence: number;
  error: string | null;
}

export interface AnalysisState {
  status: AnalysisStatus;

  impact: {
    level: ImpactLevel | null;
    reasoning: string;
  };

  severity: {
    level: SeverityLevel | null;
    reasoning: string;
  };
}

export interface FormState {
  values: DeviationData;
  isDirty: boolean;
  userEdits: Partial<DeviationData>;
}

export interface DeviationIntakeState {
  document: DocumentState;
  extraction: ExtractionState;
  analysis: AnalysisState;
  form: FormState;
}