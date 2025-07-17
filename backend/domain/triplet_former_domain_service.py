import abc

from .training_ready_scenario import TrainingReadyScenario
from .triplet import Triplet

class TripletFormerDomainService(abc.ABC):
    @abc.abstractmethod
    def form_triplets_from(self, scenario: TrainingReadyScenario) -> Triplet:
        pass