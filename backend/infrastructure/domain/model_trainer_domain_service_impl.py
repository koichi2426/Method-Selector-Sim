from datetime import datetime
from typing import List

from domain.dataset import Dataset, NewDataset
from domain.training_parameters import TrainingParameters
from domain.trained_model import TrainedModel, NewTrainedModel
from domain.custom_uuid import UUID, NewUUID
from domain.model_trainer_domain_service import ModelTrainerDomainService

class ModelTrainerDomainServiceImpl(ModelTrainerDomainService):
    """
    ModelTrainerDomainServiceの具体的な実装クラス。
    """
    def compose_new_dataset(self, name: str, description: str, triplet_ids: List[UUID]) -> Dataset:
        """
        新しいデータセットオブジェクトを生成する。
        （永続化はUsecase層がリポジトリを介して行う）
        """
        new_dataset = NewDataset(
            ID=NewUUID(),
            name=name,
            description=description,
            type="training", # デフォルトのタイプを設定
            Triplet_ids=triplet_ids,
            created_at=datetime.now()
        )
        return new_dataset

    def delete_dataset(self, id: UUID) -> None:
        """
        データセット削除に関するドメインロジック。
        この実装では特別なロジックはないため、何もしない。
        （実際の削除はUsecase層がリポジトリを介して行う）
        """
        pass

    def train_new_model(self, dataset: Dataset, params: TrainingParameters) -> TrainedModel:
        """
        データセットと訓練パラメータに基づいて、新しい訓練済みモデルオブジェクトを生成する。
        この実装では、実際の訓練は行わず、ダミーのモデル情報を生成する。
        """
        new_model_id = NewUUID()
        
        # ダミーのモデル名とファイルパスを生成
        model_name = f"model_on_{dataset.name.replace(' ', '_')}_{new_model_id.value[:8]}"
        file_path = f"/models/{model_name}.pt"

        new_model = NewTrainedModel(
            ID=new_model_id,
            name=model_name,
            Dataset_ID=dataset.ID,
            description=f"Trained with {params.epochs} epochs and a learning rate of {params.learning_rate}",
            file_path=file_path,
            created_at=datetime.now()
        )
        return new_model