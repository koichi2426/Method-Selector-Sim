import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Dict, List
from dataclasses import is_dataclass
from fastapi.responses import Response 

# --- Controller, Presenter, Repository, Usecase imports ---
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
from adapter.controller.find_all_dataset_controller import FindAllDatasetController # 追加

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
from adapter.presenter.find_all_dataset_presenter import new_find_all_dataset_presenter # 追加

from adapter.repository.scenario_mysql import ScenarioMySQL
from adapter.repository.trained_model_mysql import TrainedModelMySQL
from adapter.repository.dataset_mysql import DatasetMySQL
from adapter.repository.triplet_mysql import TripletMySQL
from adapter.repository.training_ready_scenario_mysql import TrainingReadyScenarioMySQL
from adapter.repository.model_evaluation_session_mysql import ModelEvaluationSessionMySQL
from adapter.repository.sql import SQL

from usecase.find_all_scenario import new_find_all_scenario_interactor
from usecase.generate_scenarios import GenerateScenariosInput, new_generate_scenarios_interactor
from usecase.train_new_model import TrainNewModelInput, new_train_new_model_interactor
from usecase.evaluate_model import EvaluateModelInput, new_evaluate_model_interactor
from usecase.find_all_models import new_find_all_models_interactor
from usecase.find_all_triplets import new_find_all_triplets_interactor
from usecase.form_triplets_from import FormTripletsFromInput, new_form_triplets_from_interactor
from usecase.process_scenario import ProcessScenarioInput, new_process_scenario_interactor
from usecase.delete_scenario import DeleteScenarioInput, new_delete_scenario_interactor
from usecase.delete_model import DeleteModelInput, new_delete_model_interactor
from usecase.delete_triplets import DeleteTripletsInput, new_delete_triplets_interactor
from usecase.delete_processed_scenario import DeleteProcessedScenarioInput, new_delete_processed_scenario_interactor
from usecase.compose_new_dataset import ComposeNewDatasetInput, new_compose_new_dataset_interactor
from usecase.delete_dataset import DeleteDatasetInput, new_delete_dataset_interactor
from usecase.find_all_processed_scenarios import new_find_all_processed_scenarios_interactor
from usecase.find_all_dataset import new_find_all_dataset_interactor # 追加

# --- Domain services ---
from domain import UUID

# --- Domain service implementations ---
from infrastructure.domain.scenario_generator_domain_service_impl import ScenarioGeneratorDomainServiceImpl
from infrastructure.domain.model_trainer_domain_service_impl import ModelTrainerDomainServiceImpl
from infrastructure.domain.performance_evaluator_domain_service_impl import PerformanceEvaluatorDomainServiceImpl
from infrastructure.domain.triplet_former_domain_service_impl import TripletFormerDomainServiceImpl
from infrastructure.domain.preprocessor_domain_service_impl import PreprocessorDomainServiceImpl


from infrastructure.database.mysql_handler import MySQLHandler
from infrastructure.database.config import NewMySQLConfigFromEnv

router = APIRouter()
db_handler = MySQLHandler(NewMySQLConfigFromEnv())
ctx_timeout = 10.0

# --- Pydantic models for request validation ---
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

# --- Helper function for response handling (修正箇所) ---
def handle_response(response_dict: Dict, success_code: int = 200):
    status_code = response_dict.get("status", 500)
    data = response_dict.get("data")

    if status_code >= 400:
        return JSONResponse(content=data, status_code=status_code)

    # --- ここから修正 ---
    # 成功コードが204の場合、中身が空のレスポンスを返す
    if success_code == 204:
        return Response(status_code=204)
    # --- ここまで修正 ---

    try:
        # json.dumpsにdefault=strを渡すことで、dataclassやUUID、datetimeなどを
        # 自動的に文字列に変換してJSON文字列を生成する。
        # その後、json.loadsでJSONシリアライズ可能な辞書/リストに戻す。
        content_str = json.dumps(data, default=str)
        content_data = json.loads(content_str)
    except TypeError:
        # 万が一、それでもシリアライズできないオブジェクトがあった場合のエラーハンドリング
        content_data = {"error": "Failed to serialize response data"}
        status_code = 500

    return JSONResponse(content=content_data, status_code=success_code if status_code < 400 else status_code)


# --- Scenario endpoints ---
@router.get("/v1/scenarios")
def get_all_scenarios():
    repo = ScenarioMySQL(db_handler)
    presenter = new_find_all_scenario_presenter()
    usecase = new_find_all_scenario_interactor(presenter, repo, ctx_timeout)
    controller = FindAllScenarioController(usecase)
    response_dict = controller.execute()
    return handle_response(response_dict)

@router.post("/v1/scenarios/generate")
def generate_scenarios(request: GenerateScenariosRequest):
    repo = ScenarioMySQL(db_handler)
    presenter = new_generate_scenarios_presenter()
    domain_service = ScenarioGeneratorDomainServiceImpl() # 修正
    usecase = new_generate_scenarios_interactor(repo, presenter, domain_service, ctx_timeout)
    controller = GenerateScenariosController(usecase)
    input_data = GenerateScenariosInput(
        output_count=request.output_count,
        method_pool=request.method_pool,
        situations=request.situations,
    )
    response_dict = controller.execute(input_data)
    return handle_response(response_dict, success_code=201)

@router.delete("/v1/scenarios/{scenario_id}")
def delete_scenario(scenario_id: str):
    repo = ScenarioMySQL(db_handler)
    presenter = new_delete_scenario_presenter()
    usecase = new_delete_scenario_interactor(presenter, repo, ctx_timeout)
    controller = DeleteScenarioController(usecase)
    input_data = DeleteScenarioInput(scenario_id=UUID(value=scenario_id))
    response_dict = controller.execute(input_data)
    return handle_response(response_dict, success_code=204)

@router.post("/v1/scenarios/process")
def process_scenario(request: ProcessScenarioRequest):
    scenario_repo = ScenarioMySQL(db_handler)
    trs_repo = TrainingReadyScenarioMySQL(db_handler)
    presenter = new_process_scenario_presenter()
    domain_service = PreprocessorDomainServiceImpl() # 修正
    usecase = new_process_scenario_interactor(scenario_repo, trs_repo, presenter, domain_service, ctx_timeout)
    controller = ProcessScenarioController(usecase)
    input_data = ProcessScenarioInput(
        scenario_ids=[UUID(value=sid) for sid in request.scenario_ids],
    )
    response_dict = controller.execute(input_data)
    return handle_response(response_dict, success_code=201)

# --- Processed scenarios endpoints ---
@router.get("/v1/processed-scenarios")
def get_all_processed_scenarios():
    repo = TrainingReadyScenarioMySQL(db_handler)
    presenter = new_find_all_processed_scenarios_presenter()
    usecase = new_find_all_processed_scenarios_interactor(presenter, repo, ctx_timeout)
    controller = FindAllProcessedScenariosController(usecase)
    response_dict = controller.execute()
    return handle_response(response_dict)

@router.delete("/v1/processed-scenarios/{scenario_id}")
def delete_processed_scenario(scenario_id: str):
    repo = TrainingReadyScenarioMySQL(db_handler)
    presenter = new_delete_processed_scenario_presenter()
    usecase = new_delete_processed_scenario_interactor(presenter, repo, ctx_timeout)
    controller = DeleteProcessedScenarioController(usecase)
    input_data = DeleteProcessedScenarioInput(processed_scenario_id=UUID(value=scenario_id))
    response_dict = controller.execute(input_data)
    return handle_response(response_dict, success_code=204)

# --- Model endpoints ---
@router.get("/v1/models")
def get_all_models():
    repo = TrainedModelMySQL(db_handler)
    presenter = new_find_all_models_presenter()
    usecase = new_find_all_models_interactor(presenter, repo, ctx_timeout)
    controller = FindAllModelsController(usecase)
    response_dict = controller.execute()
    return handle_response(response_dict)

@router.post("/v1/models/train")
def train_new_model(request: TrainNewModelRequest):
    dataset_repo = DatasetMySQL(db_handler)
    trained_model_repo = TrainedModelMySQL(db_handler)
    presenter = new_train_new_model_presenter()
    domain_service = ModelTrainerDomainServiceImpl() # 修正
    usecase = new_train_new_model_interactor(dataset_repo, trained_model_repo, presenter, domain_service, ctx_timeout)
    controller = TrainNewModelController(usecase)
    input_data = TrainNewModelInput(
        dataset_id=UUID(value=request.dataset_id),
        epochs=request.epochs,
        batch_size=request.batch_size,
        learning_rate=request.learning_rate,
    )
    response_dict = controller.execute(input_data)
    return handle_response(response_dict, success_code=201)

@router.post("/v1/models/evaluate")
def evaluate_model(request: EvaluateModelRequest):
    model_repo = TrainedModelMySQL(db_handler)
    dataset_repo = DatasetMySQL(db_handler)
    session_repo = ModelEvaluationSessionMySQL(db_handler)
    presenter = new_evaluate_model_presenter()
    domain_service = PerformanceEvaluatorDomainServiceImpl() # 修正
    usecase = new_evaluate_model_interactor(model_repo, dataset_repo, session_repo, presenter, domain_service, ctx_timeout)
    controller = EvaluateModelController(usecase)
    input_data = EvaluateModelInput(
        model_id=UUID(value=request.model_id),
        dataset_id=UUID(value=request.test_dataset_id),
    )
    response_dict = controller.execute(input_data)
    return handle_response(response_dict, success_code=201)

@router.delete("/v1/models/{model_id}")
def delete_model(model_id: str):
    repo = TrainedModelMySQL(db_handler)
    presenter = new_delete_model_presenter()
    usecase = new_delete_model_interactor(presenter, repo, ctx_timeout)
    controller = DeleteModelController(usecase)
    input_data = DeleteModelInput(model_id=UUID(value=model_id))
    response_dict = controller.execute(input_data)
    return handle_response(response_dict, success_code=204)

# --- Dataset endpoints ---
@router.get("/v1/datasets") # 追加
def get_all_datasets():
    repo = DatasetMySQL(db_handler)
    presenter = new_find_all_dataset_presenter()
    usecase = new_find_all_dataset_interactor(presenter, repo, ctx_timeout)
    controller = FindAllDatasetController(usecase)
    response_dict = controller.execute()
    return handle_response(response_dict)

@router.post("/v1/datasets")
def compose_new_dataset(request: ComposeNewDatasetRequest):
    repo = DatasetMySQL(db_handler)
    presenter = new_compose_new_dataset_presenter()
    usecase = new_compose_new_dataset_interactor(repo, presenter, ctx_timeout)
    controller = ComposeNewDatasetController(usecase)
    input_data = ComposeNewDatasetInput(
        name=request.name,
        description=request.description,
        triplet_ids=[UUID(value=tid) for tid in request.triplet_ids],
    )
    response_dict = controller.execute(input_data)
    return handle_response(response_dict, success_code=201)

@router.delete("/v1/datasets/{dataset_id}")
def delete_dataset(dataset_id: str):
    repo = DatasetMySQL(db_handler)
    presenter = new_delete_dataset_presenter()
    usecase = new_delete_dataset_interactor(presenter, repo, ctx_timeout)
    controller = DeleteDatasetController(usecase)
    input_data = DeleteDatasetInput(dataset_id=UUID(value=dataset_id))
    response_dict = controller.execute(input_data)
    return handle_response(response_dict, success_code=204)

# --- Triplet endpoints ---
@router.get("/v1/triplets")
def get_all_triplets():
    repo = TripletMySQL(db_handler)
    presenter = new_find_all_triplets_presenter()
    usecase = new_find_all_triplets_interactor(presenter, repo, ctx_timeout)
    controller = FindAllTripletsController(usecase)
    response_dict = controller.execute()
    return handle_response(response_dict)

@router.post("/v1/triplets/form")
def form_triplets_from(request: FormTripletsFromRequest):
    trs_repo = TrainingReadyScenarioMySQL(db_handler)
    triplet_repo = TripletMySQL(db_handler)
    presenter = new_form_triplets_from_presenter()
    domain_service = TripletFormerDomainServiceImpl() # 修正
    usecase = new_form_triplets_from_interactor(trs_repo, triplet_repo, presenter, domain_service, ctx_timeout)
    controller = FormTripletsFromController(usecase)
    input_data = FormTripletsFromInput(
        training_ready_scenario_id=UUID(value=request.training_ready_scenario_id),
    )
    response_dict = controller.execute(input_data)
    return handle_response(response_dict, success_code=201)

@router.delete("/v1/triplets/{triplet_id}")
def delete_triplets(triplet_id: str):
    repo = TripletMySQL(db_handler)
    presenter = new_delete_triplets_presenter()
    usecase = new_delete_triplets_interactor(presenter, repo, ctx_timeout)
    controller = DeleteTripletsController(usecase)
    input_data = DeleteTripletsInput(triplet_id=UUID(value=triplet_id))
    response_dict = controller.execute(input_data)
    return handle_response(response_dict, success_code=204)

# --- Health check ---
@router.get("/v1/health")
def healthcheck():
    return {"status": "ok"}