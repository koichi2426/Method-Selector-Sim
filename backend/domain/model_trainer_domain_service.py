import abc
from typing import List

from .dataset import Dataset
from .training_parameters import TrainingParameters
from .trained_model import TrainedModel

class ModelTrainerDomainService(abc.ABC):
    @abc.abstractmethod
    def compose_new_dataset(self, name: str, description: str, triplet_ids: List[str]) -> Dataset:
        pass

    @abc.abstractmethod
    def delete_dataset(self, id: str) -> None:
        pass

    @abc.abstractmethod
    def train_new_model(self, dataset: Dataset, params: TrainingParameters) -> TrainedModel:
        pass