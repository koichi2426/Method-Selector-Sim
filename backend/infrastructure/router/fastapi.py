import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import time
import json

# Import controllers
from adapter.controller.find_all_scenario_controller import FindAllScenarioController
from adapter.controller.generate_scenarios_controller import GenerateScenariosController
from adapter.controller.train_new_model_controller import TrainNewModelController
from adapter.controller.evaluate_model_controller import EvaluateModelController
from adapter.controller.find_all_models_controller import FindAllModelsController
from adapter.controller.find_all_triplets_controller import FindAllTripletsController
from adapter.controller.form_triplets_from_controller import FormTripletsFromController
from adapter.controller.process_scenario_controller import ProcessScenarioController
from adapter.controller.delete_scenario_controller import DeleteScenarioController
from adapter.controller.delete_model_controller import DeleteModelController
from adapter.controller.delete_triplets_controller import DeleteTripletsController
from adapter.controller.delete_processed_scenario_controller import DeleteProcessedScenarioController
from adapter.controller.compose_new_dataset_controller import ComposeNewDatasetController
from adapter.controller.delete_dataset_controller import DeleteDatasetController
from adapter.controller.find_all_processed_scenarios_controller import FindAllProcessedScenariosController

# Import usecases
from usecase.find_all_scenario import FindAllScenarioUseCase, FindAllScenarioOutput, FindAllScenarioPresenter, new_find_all_scenario_interactor
from usecase.generate_scenarios import GenerateScenariosUseCase, GenerateScenariosInput, GenerateScenariosOutput, GenerateScenariosPresenter, new_generate_scenarios_interactor
from usecase.train_new_model import TrainNewModelUseCase, TrainNewModelInput, TrainNewModelOutput, TrainNewModelPresenter, new_train_new_model_interactor
from usecase.evaluate_model import EvaluateModelUseCase, EvaluateModelInput, EvaluateModelOutput, EvaluateModelPresenter, new_evaluate_model_interactor
from usecase.find_all_models import FindAllModelsUseCase, FindAllModelsOutput, FindAllModelsPresenter, new_find_all_models_interactor
from usecase.find_all_triplets import FindAllTripletsUseCase, FindAllTripletsOutput, FindAllTripletsPresenter, new_find_all_triplets_interactor
from usecase.form_triplets_from import FormTripletsFromUseCase, FormTripletsFromInput, FormTripletsFromOutput, FormTripletsFromPresenter, new_form_triplets_from_interactor
from usecase.process_scenario import ProcessScenarioUseCase, ProcessScenarioInput, ProcessScenarioOutput, ProcessScenarioPresenter, new_process_scenario_interactor
from usecase.delete_scenario import DeleteScenarioUseCase, DeleteScenarioInput, DeleteScenarioOutput, DeleteScenarioPresenter, new_delete_scenario_interactor
from usecase.delete_model import DeleteModelUseCase, DeleteModelInput, DeleteModelOutput, DeleteModelPresenter, new_delete_model_interactor
from usecase.delete_triplets import DeleteTripletsUseCase, DeleteTripletsInput, DeleteTripletsOutput, DeleteTripletsPresenter, new_delete_triplets_interactor
from usecase.delete_processed_scenario import DeleteProcessedScenarioUseCase, DeleteProcessedScenarioInput, DeleteProcessedScenarioOutput, DeleteProcessedScenarioPresenter, new_delete_processed_scenario_interactor
from usecase.compose_new_dataset import ComposeNewDatasetUseCase, ComposeNewDatasetInput, ComposeNewDatasetOutput, ComposeNewDatasetPresenter, new_compose_new_dataset_interactor
from usecase.delete_dataset import DeleteDatasetUseCase, DeleteDatasetInput, DeleteDatasetOutput, DeleteDatasetPresenter, new_delete_dataset_interactor
from usecase.find_all_processed_scenarios import FindAllProcessedScenariosUseCase, FindAllProcessedScenariosOutput, FindAllProcessedScenariosPresenter, new_find_all_processed_scenarios_interactor

# Import repositories
from adapter.repository.scenario_mysql import ScenarioMySQL
from adapter.repository.trained_model_mysql import TrainedModelMySQL
from adapter.repository.dataset_mysql import DatasetMySQL
from adapter.repository.triplet_mysql import TripletMySQL
from adapter.repository.training_ready_scenario_mysql import TrainingReadyScenarioMySQL
from adapter.repository.model_evaluation_session_mysql import ModelEvaluationSessionMySQL

# Import presenters
from adapter.presenter.find_all_scenario_presenter import new_find_all_scenario_presenter
from adapter.presenter.generate_scenarios_presenter import new_generate_scenarios_presenter
from adapter.presenter.train_new_model_presenter import new_train_new_model_presenter
from adapter.presenter.evaluate_model_presenter import new_evaluate_model_presenter
from adapter.presenter.find_all_models_presenter import new_find_all_models_presenter
from adapter.presenter.find_all_triplets_presenter import new_find_all_triplets_presenter
from adapter.presenter.form_triplets_from_presenter import new_form_triplets_from_presenter
from adapter.presenter.process_scenario_presenter import new_process_scenario_presenter
from adapter.presenter.delete_scenario_presenter import new_delete_scenario_presenter
from adapter.presenter.delete_model_presenter import new_delete_model_presenter
from adapter.presenter.delete_triplets_presenter import new_delete_triplets_presenter
from adapter.presenter.delete_processed_scenario_presenter import new_delete_processed_scenario_presenter
from adapter.presenter.compose_new_dataset_presenter import new_compose_new_dataset_presenter
from adapter.presenter.delete_dataset_presenter import new_delete_dataset_presenter
from adapter.presenter.find_all_processed_scenarios_presenter import new_find_all_processed_scenarios_presenter

# Import domain services
from backend.domain import (
    ScenarioGeneratorDomainService,
    ModelTrainerDomainService,
    PerformanceEvaluatorDomainService,
    TripletFormerDomainService,
    PreprocessorDomainService,
    TripletDataStoreDomainService,
    ProcessedDataStoreDomainService,
    ModelRegistryDomainService
)

# Import SQL handler
from adapter.repository.sql import SQL

# Pydantic models for request validation
class GenerateScenariosRequest(BaseModel):
    output_count: int
    method_pool: List[Dict[str, Any]]
    situations: List[Dict[str, Any]]

class TrainNewModelRequest(BaseModel):
    dataset_id: str
    epochs: int
    batch_size: int
    learning_rate: float

class EvaluateModelRequest(BaseModel):
    model_id: str
    test_dataset_id: str

class FormTripletsFromRequest(BaseModel):
    training_ready_scenario_id: str

class ProcessScenarioRequest(BaseModel):
    scenario_ids: List[str]

class ComposeNewDatasetRequest(BaseModel):
    name: str
    description: str
    triplet_ids: List[str]

class DeleteRequest(BaseModel):
    id: str

class FastAPIEngine:
    """
    GoのginEngine構造体に相当する、サーバー全体を管理するクラス。
    """
    def __init__(
        self,
        db: SQL,
        port: int,
        timeout_sec: float,
    ):
        self.router = FastAPI(title="Clean Architecture API")
        self.db = db
        self.port = port
        self.ctx_timeout = timeout_sec
        self._set_app_handlers()

    def listen(self):
        """
        サーバーを起動する。GoのListenメソッドに相当。
        UvicornがGraceful Shutdownを処理する。
        """
        print(f"INFO: Starting HTTP Server port={self.port}")
        uvicorn.run(self.router, host="0.0.0.0", port=self.port)

    def _set_app_handlers(self):
        """
        APIエンドポイントをルーターに登録する。
        GoのsetAppHandlersメソッドに相当。
        """
        # Scenario endpoints
        self.router.get("/v1/scenarios")(self._build_find_all_scenario_handler())
        self.router.post("/v1/scenarios/generate")(self._build_generate_scenarios_handler())
        self.router.delete("/v1/scenarios/{scenario_id}")(self._build_delete_scenario_handler())
        self.router.post("/v1/scenarios/process")(self._build_process_scenario_handler())
        
        # Processed scenarios endpoints
        self.router.get("/v1/processed-scenarios")(self._build_find_all_processed_scenarios_handler())
        self.router.delete("/v1/processed-scenarios/{scenario_id}")(self._build_delete_processed_scenario_handler())

        # Model endpoints
        self.router.get("/v1/models")(self._build_find_all_models_handler())
        self.router.post("/v1/models/train")(self._build_train_new_model_handler())
        self.router.post("/v1/models/evaluate")(self._build_evaluate_model_handler())
        self.router.delete("/v1/models/{model_id}")(self._build_delete_model_handler())

        # Dataset endpoints
        self.router.post("/v1/datasets")(self._build_compose_new_dataset_handler())
        self.router.delete("/v1/datasets/{dataset_id}")(self._build_delete_dataset_handler())

        # Triplet endpoints
        self.router.get("/v1/triplets")(self._build_find_all_triplets_handler())
        self.router.post("/v1/triplets/form")(self._build_form_triplets_from_handler())
        self.router.delete("/v1/triplets/{triplet_id}")(self._build_delete_triplets_handler())

        # Health check
        self.router.get("/v1/health")(self._healthcheck())

    def _build_find_all_scenario_handler(self):
        """FindAllScenarioのハンドラ関数を構築する"""
        async def handler():
            repo = ScenarioMySQL(self.db)
            presenter = new_find_all_scenario_presenter()
            usecase = new_find_all_scenario_interactor(presenter, repo, self.ctx_timeout)
            controller = FindAllScenarioController(usecase)
            
            response_dict = controller.execute()
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_generate_scenarios_handler(self):
        """GenerateScenariosのハンドラ関数を構築する"""
        async def handler(request: GenerateScenariosRequest):
            repo = ScenarioMySQL(self.db)
            presenter = new_generate_scenarios_presenter()
            domain_service = ScenarioGeneratorDomainService()  # This would need proper initialization
            usecase = new_generate_scenarios_interactor(repo, presenter, domain_service, self.ctx_timeout)
            controller = GenerateScenariosController(usecase)
            
            # Convert Pydantic model to usecase input
            input_data = GenerateScenariosInput(
                output_count=request.output_count,
                method_pool=request.method_pool,  # This would need conversion to MethodProfile objects
                situations=request.situations,    # This would need conversion to Situation objects
            )
            
            response_dict = controller.execute(input_data)
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_train_new_model_handler(self):
        """TrainNewModelのハンドラ関数を構築する"""
        async def handler(request: TrainNewModelRequest):
            dataset_repo = DatasetMySQL(self.db)
            trained_model_repo = TrainedModelMySQL(self.db)
            presenter = new_train_new_model_presenter()
            domain_service = ModelTrainerDomainService()  # This would need proper initialization
            usecase = new_train_new_model_interactor(dataset_repo, trained_model_repo, presenter, domain_service, self.ctx_timeout)
            controller = TrainNewModelController(usecase)
            
            # Convert string UUID to domain UUID
            from backend.domain import UUID
            input_data = TrainNewModelInput(
                dataset_id=UUID(value=request.dataset_id),
                epochs=request.epochs,
                batch_size=request.batch_size,
                learning_rate=request.learning_rate,
            )
            
            response_dict = controller.execute(input_data)
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_evaluate_model_handler(self):
        """EvaluateModelのハンドラ関数を構築する"""
        async def handler(request: EvaluateModelRequest):
            model_repo = TrainedModelMySQL(self.db)
            dataset_repo = DatasetMySQL(self.db)
            session_repo = ModelEvaluationSessionMySQL(self.db)
            presenter = new_evaluate_model_presenter()
            domain_service = PerformanceEvaluatorDomainService()  # This would need proper initialization
            usecase = new_evaluate_model_interactor(model_repo, dataset_repo, session_repo, presenter, domain_service, self.ctx_timeout)
            controller = EvaluateModelController(usecase)
            
            # Convert string UUID to domain UUID
            from backend.domain import UUID
            input_data = EvaluateModelInput(
                model_id=UUID(value=request.model_id),
                dataset_id=UUID(value=request.test_dataset_id),
            )
            
            response_dict = controller.execute(input_data)
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_find_all_models_handler(self):
        """FindAllModelsのハンドラ関数を構築する"""
        async def handler():
            repo = TrainedModelMySQL(self.db)
            presenter = new_find_all_models_presenter()
            usecase = new_find_all_models_interactor(presenter, repo, self.ctx_timeout)
            controller = FindAllModelsController(usecase)
            
            response_dict = controller.execute()
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_find_all_triplets_handler(self):
        """FindAllTripletsのハンドラ関数を構築する"""
        async def handler():
            repo = TripletMySQL(self.db)
            presenter = new_find_all_triplets_presenter()
            usecase = new_find_all_triplets_interactor(presenter, repo, self.ctx_timeout)
            controller = FindAllTripletsController(usecase)
            
            response_dict = controller.execute()
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_form_triplets_from_handler(self):
        """FormTripletsFromのハンドラ関数を構築する"""
        async def handler(request: FormTripletsFromRequest):
            trs_repo = TrainingReadyScenarioMySQL(self.db)
            triplet_repo = TripletMySQL(self.db)
            presenter = new_form_triplets_from_presenter()
            domain_service = TripletFormerDomainService()  # This would need proper initialization
            usecase = new_form_triplets_from_interactor(trs_repo, triplet_repo, presenter, domain_service, self.ctx_timeout)
            controller = FormTripletsFromController(usecase)
            
            # Convert string UUID to domain UUID
            from backend.domain import UUID
            input_data = FormTripletsFromInput(
                training_ready_scenario_id=UUID(value=request.training_ready_scenario_id),
            )
            
            response_dict = controller.execute(input_data)
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_process_scenario_handler(self):
        """ProcessScenarioのハンドラ関数を構築する"""
        async def handler(request: ProcessScenarioRequest):
            scenario_repo = ScenarioMySQL(self.db)
            trs_repo = TrainingReadyScenarioMySQL(self.db)
            presenter = new_process_scenario_presenter()
            domain_service = PreprocessorDomainService()  # This would need proper initialization
            usecase = new_process_scenario_interactor(scenario_repo, trs_repo, presenter, domain_service, self.ctx_timeout)
            controller = ProcessScenarioController(usecase)
            
            # Convert string UUIDs to domain UUIDs
            from backend.domain import UUID
            input_data = ProcessScenarioInput(
                scenario_ids=[UUID(value=scenario_id) for scenario_id in request.scenario_ids],
            )
            
            response_dict = controller.execute(input_data)
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_find_all_processed_scenarios_handler(self):
        """FindAllProcessedScenariosのハンドラ関数を構築する"""
        async def handler():
            repo = TrainingReadyScenarioMySQL(self.db)
            presenter = new_find_all_processed_scenarios_presenter()
            usecase = new_find_all_processed_scenarios_interactor(presenter, repo, self.ctx_timeout)
            controller = FindAllProcessedScenariosController(usecase)
            
            response_dict = controller.execute()
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_delete_scenario_handler(self):
        """DeleteScenarioのハンドラ関数を構築する"""
        async def handler(scenario_id: str):
            repo = ScenarioMySQL(self.db)
            presenter = new_delete_scenario_presenter()
            usecase = new_delete_scenario_interactor(repo, presenter, self.ctx_timeout)
            controller = DeleteScenarioController(usecase)
            
            from backend.domain import UUID
            input_data = DeleteScenarioInput(id=UUID(value=scenario_id))
            
            response_dict = controller.execute(input_data)
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_delete_model_handler(self):
        """DeleteModelのハンドラ関数を構築する"""
        async def handler(model_id: str):
            repo = TrainedModelMySQL(self.db)
            presenter = new_delete_model_presenter()
            usecase = new_delete_model_interactor(repo, presenter, self.ctx_timeout)
            controller = DeleteModelController(usecase)
            
            from backend.domain import UUID
            input_data = DeleteModelInput(id=UUID(value=model_id))
            response_dict = controller.execute(input_data)
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_delete_triplets_handler(self):
        """DeleteTripletsのハンドラ関数を構築する"""
        async def handler(triplet_id: str):
            repo = TripletMySQL(self.db)
            presenter = new_delete_triplets_presenter()
            usecase = new_delete_triplets_interactor(repo, presenter, self.ctx_timeout)
            controller = DeleteTripletsController(usecase)
            
            from backend.domain import UUID
            input_data = DeleteTripletsInput(id=UUID(value=triplet_id))
            
            response_dict = controller.execute(input_data)
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_delete_processed_scenario_handler(self):
        """DeleteProcessedScenarioのハンドラ関数を構築する"""
        async def handler(scenario_id: str):
            repo = TrainingReadyScenarioMySQL(self.db)
            presenter = new_delete_processed_scenario_presenter()
            usecase = new_delete_processed_scenario_interactor(repo, presenter, self.ctx_timeout)
            controller = DeleteProcessedScenarioController(usecase)
            
            from backend.domain import UUID
            input_data = DeleteProcessedScenarioInput(id=UUID(value=scenario_id))
            
            response_dict = controller.execute(input_data)
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_compose_new_dataset_handler(self):
        """ComposeNewDatasetのハンドラ関数を構築する"""
        async def handler(request: ComposeNewDatasetRequest):
            repo = DatasetMySQL(self.db)
            presenter = new_compose_new_dataset_presenter()
            usecase = new_compose_new_dataset_interactor(repo, presenter, self.ctx_timeout)
            controller = ComposeNewDatasetController(usecase)
            
            # Convert string UUIDs to domain UUIDs
            from backend.domain import UUID
            input_data = ComposeNewDatasetInput(
                name=request.name,
                description=request.description,
                triplet_ids=[UUID(value=triplet_id) for triplet_id in request.triplet_ids],
            )
            
            response_dict = controller.execute(input_data)
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _build_delete_dataset_handler(self):
        """DeleteDatasetのハンドラ関数を構築する"""
        async def handler(dataset_id: str):
            repo = DatasetMySQL(self.db)
            presenter = new_delete_dataset_presenter()
            usecase = new_delete_dataset_interactor(repo, presenter, self.ctx_timeout)
            controller = DeleteDatasetController(usecase)
            
            from backend.domain import UUID
            input_data = DeleteDatasetInput(id=UUID(value=dataset_id))
            
            response_dict = controller.execute(input_data)
            return JSONResponse(
                content=response_dict.get("data"),
                status_code=response_dict.get("status", 500)
            )
        return handler

    def _healthcheck(self):
        """ヘルスチェック用のハンドラ関数を返す"""
        def handler():
            return {"status": "ok"}
        return handler


def new_fastapi_server(
    db: SQL,
    port: int,
    timeout_sec: float,
) -> FastAPIEngine:
    """
    FastAPIEngineのインスタンスを生成するファクトリ関数。
    GoのnewGinServerに相当。
    """
    return FastAPIEngine(
        db=db,
        port=port,
        timeout_sec=timeout_sec,
    )


# --- アプリケーションのエントリーポイント ---

if __name__ == "__main__":
    # 実際のアプリケーションでは、ここで環境変数などから設定を読み込む
    db_handler = SQL() # ここで実際のDBハンドラを初期化
    port = 8000
    timeout = 10.0

    # サーバーエンジンを生成し、起動
    server = new_fastapi_server(
        db=db_handler,
        port=port,
        timeout_sec=timeout,
    )
    server.listen()