# backend/infrastructure/database/models.py
from sqlalchemy import Column, String, Text, DateTime, JSON
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
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)

# --- 同様に、scenarios, trained_models など他のテーブルもここに定義 ---