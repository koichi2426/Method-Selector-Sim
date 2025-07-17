from dataclasses import dataclass

@dataclass
class IndividualEvaluationResult:
    ID: str
    ModelEvaluationSession_ID: str
    test_data_id: str
    inference_time_ms: float
    power_consumption_mw: float
    llm_judge_score: float
    llm_judge_reasoning: str