from pydantic import BaseModel
from typing import Optional, Any, Dict, List, Generic, TypeVar, Type
from datetime import datetime

# Generic Type Variable for Pydantic models
ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True

class Message(BaseModel):
    detail: str
