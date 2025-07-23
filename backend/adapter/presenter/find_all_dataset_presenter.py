from typing import List
from usecase.find_all_dataset import (
    FindAllDatasetPresenter,
    FindAllDatasetOutput,
    DatasetOutputDTO,
)
from domain import Dataset


class FindAllDatasetPresenterImpl(FindAllDatasetPresenter):
    def output(self, datasets: List[Dataset]) -> FindAllDatasetOutput:
        """
        Datasetドメインオブジェクトのリストを、
        FindAllDatasetOutput DTOに変換する。
        """
        dtos = []
        for dataset in datasets:
            # 各DatasetオブジェクトをDatasetOutputDTOに変換
            dto = DatasetOutputDTO(
                ID=dataset.ID,
                name=dataset.name,
                description=dataset.description,
                type=dataset.type,
                Triplet_ids=dataset.Triplet_ids,
                created_at=dataset.created_at.isoformat(),
            )
            dtos.append(dto)
        
        # DTOのリストを最終的なOutputオブジェクトでラップして返す
        return FindAllDatasetOutput(datasets=dtos)


def new_find_all_dataset_presenter() -> FindAllDatasetPresenter:
    """
    FindAllDatasetPresenterImplのインスタンスを生成するファクトリ関数。
    """
    return FindAllDatasetPresenterImpl()
