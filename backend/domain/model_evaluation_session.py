from dataclasses import dataclass
from datetime import datetime

from .evaluation_summary import EvaluationSummary

@dataclass
class ModelEvaluationSession:
    ID: str
    TrainedModel_ID: str
    Dataset_ID: str
    summary_metrics: EvaluationSummary
    created_at: datetime