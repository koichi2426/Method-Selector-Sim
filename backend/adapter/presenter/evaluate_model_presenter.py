from usecase.evaluate_model import EvaluateModelPresenter, EvaluateModelOutput, EvaluationSummaryOutput
from domain import ModelEvaluationSession, UUID

class EvaluateModelPresenterImpl(EvaluateModelPresenter):
    def output(self, session: ModelEvaluationSession) -> EvaluateModelOutput:
        summary = EvaluationSummaryOutput(
            average_score=session.average_score,
            average_inference_time_ms=session.average_inference_time_ms,
            average_power_consumption_mw=session.average_power_consumption_mw,
            total_test_cases=session.total_test_cases
        )
        return EvaluateModelOutput(
            ID=session.ID,
            TrainedModel_ID=session.TrainedModel_ID,
            Dataset_ID=session.Dataset_ID,
            summary_metrics=summary,
            created_at=session.created_at.isoformat()
        )

def new_evaluate_model_presenter() -> EvaluateModelPresenter:
    return EvaluateModelPresenterImpl() 