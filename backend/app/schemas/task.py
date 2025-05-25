from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from ..models.task import TaskStatus
from .user import User

class TaskBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: Optional[int] = Field(None, ge=1, le=5)
    due_date: Optional[datetime] = None
    project_id: int
    assignee_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None

class TaskInDBBase(TaskBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Task(TaskInDBBase):
    assignee: Optional[User] = None

# Temporarily removed TaskWithComments to resolve circular import
# Will be re-implemented after fixing the schema dependencies
