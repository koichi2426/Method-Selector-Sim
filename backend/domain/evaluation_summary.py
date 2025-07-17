from dataclasses import dataclass

@dataclass
class EvaluationSummary:
    average_score: float
    average_inference_time_ms: float
    average_power_consumption_mw: float
    total_test_cases: int