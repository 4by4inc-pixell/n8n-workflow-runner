from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
    ARRAY,
    ForeignKey,
    DateTime,
    Boolean,
)
from pydantic import BaseModel, Field
from models.base import Base
from datetime import datetime


class N8NTask(Base):
    __tablename__ = "scheduled_tasks"

    id = Column(Integer, primary_key=True, index=True)
    labels = Column(ARRAY(String), nullable=False)
    task_type = Column(String, nullable=False)
    params = Column(JSON, nullable=False)


class N8NTaskResult(Base):
    __tablename__ = "completed_tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, nullable=False)
    task_labels = Column(ARRAY(String), nullable=False)
    task_type = Column(String, nullable=False)
    task_params = Column(JSON, nullable=False)
    status = Column(Boolean, nullable=False)  # 성공/실패
    result = Column(String, nullable=True)  # 결과 데이터
    executed_at = Column(DateTime, default=datetime.utcnow)


class N8NTaskCreate(BaseModel):
    labels: list[str] = Field(..., description="Labels", example=["test", "do nothing"])
    task_type: str = Field(..., description="Task type", example="test")
    params: dict = Field(
        ...,
        description="Task's parameters",
        example={"test-param-1": "1", "test-param-2": "2"},
    )


class N8NTaskRead(N8NTaskCreate):
    id: int

    class Config:
        from_attributes = True  # from_orm() 활성화
