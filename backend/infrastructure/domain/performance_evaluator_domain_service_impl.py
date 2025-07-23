import random
from datetime import datetime

from domain.trained_model import TrainedModel
from domain.dataset import Dataset
from domain.model_evaluation_session import ModelEvaluationSession, NewModelEvaluationSession
from domain.evaluation_summary import EvaluationSummary
from domain.custom_uuid import NewUUID
from domain.performance_evaluator_domain_service import PerformanceEvaluatorDomainService

class PerformanceEvaluatorDomainServiceImpl(PerformanceEvaluatorDomainService):
    """
    PerformanceEvaluatorDomainServiceの具体的な実装クラス。
    """
    def evaluate_model(self, model: TrainedModel, dataset: Dataset) -> ModelEvaluationSession:
        """
        モデルの性能を評価し、評価セッションオブジェクトを生成する。
        この実装では、ダミーの評価指標を生成する。
        """
        
        # 1. ダミーの評価サマリーを生成
        dummy_summary = EvaluationSummary(
            accuracy=round(random.uniform(0.85, 0.99), 4),
            precision=round(random.uniform(0.85, 0.99), 4),
            recall=round(random.uniform(0.85, 0.99), 4),
            f1_score=round(random.uniform(0.85, 0.99), 4)
        )

        # 2. 評価セッションオブジェクトを生成
        evaluation_session = NewModelEvaluationSession(
            ID=NewUUID(),
            TrainedModel_ID=model.ID,
            Dataset_ID=dataset.ID,
            summary_metrics=dummy_summary,
            created_at=datetime.now()
        )

        return evaluation_session
