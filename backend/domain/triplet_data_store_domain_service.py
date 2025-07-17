import abc
import uuid  # uuidモジュールをインポート
from typing import List

from .triplet import Triplet

class TripletDataStoreDomainService(abc.ABC):
    @abc.abstractmethod
    def find_all_triplets(self) -> List[Triplet]:
        pass

    @abc.abstractmethod
    def delete_triplet(self, id: uuid.UUID) -> None: # 引数の型も変更
        pass