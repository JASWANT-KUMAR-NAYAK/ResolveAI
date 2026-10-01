export interface RiskAssessment {
  severity: "low" | "medium" | "high" | "critical" | null;

  impact: string;

  rationale: string;

  recommendedAction: string;

  confidence: number | null;
}
