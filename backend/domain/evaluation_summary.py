from dataclasses import dataclass

@dataclass
class EvaluationSummary:
    average_score: float
    average_inference_time_ms: float
    average_power_consumption_mw: float
    total_test_cases: int

def NewEvaluationSummary(
    average_score: float,
    average_inference_time_ms: float,
    average_power_consumption_mw: float,
    total_test_cases: int,
) -> EvaluationSummary:
    """
    EvaluationSummaryインスタンスを生成するファクトリ関数。
    """
    return EvaluationSummary(
        average_score=average_score,
        average_inference_time_ms=average_inference_time_ms,
        average_power_consumption_mw=average_power_consumption_mw,
        total_test_cases=total_test_cases,
    )
