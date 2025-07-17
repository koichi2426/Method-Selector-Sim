import abc
import uuid  # uuidモジュールをインポート
from typing import List

from .trained_model import TrainedModel

class ModelRegistryDomainService(abc.ABC):
    @abc.abstractmethod
    def findAllModels(self) -> List[TrainedModel]:
        pass

    @abc.abstractmethod
    def deleteModel(self, id: uuid.UUID) -> None: # 引数の型も変更
        pass