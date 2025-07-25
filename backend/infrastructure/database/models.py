# backend/infrastructure/database/models.py
from sqlalchemy import Column, String, Text, DateTime, JSON, Float, ForeignKey, func
from sqlalchemy.orm import declarative_base
import datetime

# 全モデル共通の親クラス
Base = declarative_base()

# `datasets`テーブルの定義
class Dataset(Base):
    __tablename__ = 'datasets'
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    type = Column(String(50))
    triplet_ids = Column(JSON)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now, server_default=func.now())

# `scenarios`テーブルの定義
class Scenario(Base):
    __tablename__ = 'scenarios'
    id = Column(String(36), primary_key=True)
    state = Column(Text, nullable=False)
    method_group = Column(Text, nullable=False)
    target_method = Column(Text, nullable=False)
    negative_method_group = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now, server_default=func.now())

# `training_ready_scenarios`テーブルの定義
class TrainingReadyScenario(Base):
    __tablename__ = 'training_ready_scenarios'
    id = Column(String(36), primary_key=True)
    scenario_id = Column(String(36), ForeignKey('scenarios.id'), nullable=False)
    state = Column(Text, nullable=False)
    method_group = Column(Text, nullable=False)
    negative_method_group = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now, server_default=func.now())

# `triplets`テーブルの定義
class Triplet(Base):
    __tablename__ = 'triplets'
    id = Column(String(36), primary_key=True)
    training_ready_scenario_id = Column(String(36), ForeignKey('training_ready_scenarios.id'), nullable=False)
    anchor = Column(Text, nullable=False)
    positive = Column(Text, nullable=False)
    negative = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now, server_default=func.now())

# `trained_models`テーブルの定義
class TrainedModel(Base):
    __tablename__ = 'trained_models'
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    dataset_id = Column(String(36), ForeignKey('datasets.id'), nullable=False)
    description = Column(Text)
    file_path = Column(String(255))
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now, server_default=func.now())

# `model_evaluation_sessions`テーブルの定義
class ModelEvaluationSession(Base):
    __tablename__ = 'model_evaluation_sessions'
    id = Column(String(36), primary_key=True)
    trained_model_id = Column(String(36), ForeignKey('trained_models.id'), nullable=False)
    dataset_id = Column(String(36), ForeignKey('datasets.id'), nullable=False)
    summary_metrics = Column(JSON)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now, server_default=func.now())

# `individual_evaluation_results`テーブルの定義
class IndividualEvaluationResult(Base):
    __tablename__ = 'individual_evaluation_results'
    id = Column(String(36), primary_key=True)
    model_evaluation_session_id = Column(String(36), ForeignKey('model_evaluation_sessions.id'), nullable=False)
    test_data_id = Column(String(36), nullable=False)
    inference_time_ms = Column(Float)
    power_consumption_mw = Column(Float)
    llm_judge_score = Column(Float)
    llm_judge_reasoning = Column(Text)