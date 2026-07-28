from sqlalchemy import Column, String, Integer, Float, Text, DateTime
from datetime import datetime
from backend.database.session import Base

class AuditHistoryModel(Base):
    __tablename__ = "audit_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dataset_id = Column(String, unique=True, index=True, nullable=False)
    filename = Column(String, nullable=False)
    analyzed_at = Column(String, nullable=False)
    total_rows = Column(Integer, nullable=False)
    total_columns = Column(Integer, nullable=False)
    readiness_score = Column(Float, nullable=False)
    grade = Column(String, nullable=False)
    issues_found_count = Column(Integer, nullable=False)
    ai_summary = Column(Text, nullable=True)
