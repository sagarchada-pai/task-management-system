from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from ..models.task import TaskStatus

class ProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None

class ProjectInDBBase(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Project(ProjectInDBBase):
    pass

class ProjectWithTasks(ProjectInDBBase):
    tasks: List['Task'] = []

class ProjectInDB(ProjectInDBBase):
    pass
