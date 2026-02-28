from pydantic import BaseModel
from typing import List, Optional, Dict

class IntentOutput(BaseModel):
    dataset_summary: Optional[str] = None
    domain: Optional[str] = None
    user_goal_interpreted: Optional[str] = None
    problem_type: Optional[str] = None
    target_column: Optional[str] = None
    priority_features: Optional[List[str]] = None

class EDAOutput(BaseModel):
    missing_values: Optional[Dict[str, int]] = None
    strong_correlations: Optional[List[str]] = None
    anomalies: Optional[List[str]] = None
    data_quality_warnings: Optional[List[str]] = None
    duplicates: Optional[int] = None
    class_imbalance: Optional[Dict[str, Dict[str, float]]] = None

class InsightOutput(BaseModel):
    executive_summary: Optional[str] = None
    key_findings: Optional[List[str]] = None
    risk_flags: Optional[List[str]] = None
    feature_ideas: Optional[List[str]] = None

class MLStrategyOutput(BaseModel):
    final_problem_type: Optional[str] = None
    recommended_target: Optional[str] = None
    suggested_models: Optional[List[str]] = None
    preprocessing_steps: Optional[List[str]] = None
    feature_engineering: Optional[List[str]] = None
    training_risks: Optional[List[str]] = None
    readiness_score: Optional[float] = None

class SummaryOutput(BaseModel):
    summary_text: str
    key_findings: Optional[List[str]] = None
