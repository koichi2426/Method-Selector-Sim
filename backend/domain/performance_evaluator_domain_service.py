import abc

from .trained_model import TrainedModel
from .dataset import Dataset
from .model_evaluation_session import ModelEvaluationSession

class PerformanceEvaluatorDomainService(abc.ABC):
    @abc.abstractmethod
    def evaluate_model(self, model: TrainedModel, dataset: Dataset) -> ModelEvaluationSession:
        pass