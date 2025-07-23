import abc
from dataclasses import dataclass
from typing import Protocol, List
from domain import Dataset, DatasetRepository, UUID

# Usecaseのインターフェース定義
class FindAllDatasetUseCase(Protocol):
    def execute(self) -> tuple["FindAllDatasetOutput", Exception | None]:
        ...

# UsecaseのInput (今回は不要)
@dataclass
class FindAllDatasetInput:
    pass

# Presenterが最終的に生成するOutputのデータ形式
@dataclass
class DatasetOutputDTO:
    ID: UUID
    name: str
    description: str
    type: str
    Triplet_ids: List[UUID]
    created_at: str

@dataclass
class FindAllDatasetOutput:
    datasets: List[DatasetOutputDTO]

# Presenterのインターフェース定義
class FindAllDatasetPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, datasets: List[Dataset]) -> "FindAllDatasetOutput":
        pass

# Usecaseの具体的な実装
class FindAllDatasetInteractor:
    def __init__(
        self,
        presenter: "FindAllDatasetPresenter",
        repo: DatasetRepository,
        timeout_sec: int = 10,
    ):
        self.presenter = presenter
        self.repo = repo
        self.timeout_sec = timeout_sec

    def execute(self) -> tuple["FindAllDatasetOutput", Exception | None]:
        try:
            # リポジトリから全てのデータセットを取得
            datasets = self.repo.find_all()
            # 取得したデータをPresenterに渡して整形
            output = self.presenter.output(datasets)
            return output, None
        except Exception as e:
            # エラー時は空のOutputを返す
            empty_output = FindAllDatasetOutput(datasets=[])
            return empty_output, e

# Usecaseインスタンスを生成するファクトリ関数
def new_find_all_dataset_interactor(
    presenter: "FindAllDatasetPresenter",
    repo: DatasetRepository,
    timeout_sec: int,
) -> "FindAllDatasetUseCase":
    return FindAllDatasetInteractor(
        presenter=presenter,
        repo=repo,
        timeout_sec=timeout_sec,
    )
